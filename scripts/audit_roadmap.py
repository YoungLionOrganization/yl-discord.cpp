# SPDX-License-Identifier: LGPL-3.0-or-later
# Copyright (C) 2026 Cavanshirpro
# Licensed under LGPL-3.0-or-later; see NOTICE, LICENSE and COPYING.
"""Check roadmap traceability offline; optionally detect changes in official docs."""
import argparse
from concurrent.futures import ThreadPoolExecutor
import hashlib
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import sys
import urllib.parse
import urllib.request

ROOT = Path(__file__).resolve().parents[1]
POLICY_REDIRECTS = {
    'https://docs.discord.com/developers/policies/developer-policy.md':
        'https://support-dev.discord.com/hc/en-us/articles/8563934450327-Discord-Developer-Policy',
    'https://docs.discord.com/developers/policies/developer-terms-of-service.md':
        'https://support-dev.discord.com/hc/en-us/articles/8562894815383-Discord-Developer-Terms-of-Service',
}


class ArticleParser(HTMLParser):
    """Ignore Zendesk navigation/request nonces while hashing the policy article."""
    def __init__(self):
        super().__init__()
        self.depth = 0
        self.text = []
        self.links = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == 'div' and 'article-body' in attrs.get('class', '').split():
            self.depth = 1
        elif self.depth and tag == 'div':
            self.depth += 1
        if self.depth and tag == 'a' and 'href' in attrs:
            self.links.append(attrs['href'])

    def handle_endtag(self, tag):
        if self.depth and tag == 'div':
            self.depth -= 1

    def handle_data(self, data):
        if self.depth:
            self.text.append(data)


def document_digest(kind, body):
    if kind == 'policy-html':
        parser = ArticleParser()
        parser.feed(body.decode('utf-8-sig'))
        require(parser.text, 'Official policy article body was not found')
        content = {'text': ' '.join(' '.join(parser.text).split()), 'links': parser.links}
        body = json.dumps(content, sort_keys=True, ensure_ascii=False).encode('utf-8')
    return hashlib.sha256(body).hexdigest()


class DocumentParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.symbols = set()
        self.headings = []
        self.heading = None
        self.fragments = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == 'dt' and attrs.get('id', '').startswith('discord.'):
            self.symbols.add(attrs['id'])
        if tag in ('h1', 'h2', 'h3'):
            self.heading, self.fragments = tag, []

    def handle_data(self, data):
        if self.heading:
            self.fragments.append(data)

    def handle_endtag(self, tag):
        if tag == self.heading:
            self.headings.append(' '.join(''.join(self.fragments).replace('¶', '').split()))
            self.heading = None


def plain(text):
    text = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', text)
    return text.replace('\\', '').replace('`', '').strip()


def facts(kind, body):
    """Keep identifiers/schema keys and references, never upstream prose or HTML."""
    text = body.decode('utf-8-sig')
    if kind in ('python-api', 'python-changelog', 'python-guide', 'policy-html'):
        parser = DocumentParser()
        parser.feed(text)
        return {'symbols': sorted(parser.symbols)} if kind == 'python-api' else {'headings': parser.headings}
    if kind == 'discord-index':
        pages = {}
        for title, url in re.findall(r'^- \[([^]]+)\]\(([^)]+)\)', text, re.M):
            pages[url] = title
        return {'pages': [{'title': title, 'url': url} for url, title in sorted(pages.items())]}
    if kind != 'discord-reference':
        raise ValueError('Unknown source kind: ' + kind)
    headings = list(re.finditer(r'^(#{1,6})\s+(.+)', text, re.M))
    routes = []
    for match in re.finditer(r'^(GET|POST|PUT|PATCH|DELETE)\s+([^\r\n]+)', text, re.M):
        section = next((plain(h[2]) for h in reversed(headings) if h.start() < match.start()), '')
        routes.append({'method': match[1], 'path': plain(match[2]), 'section': section})
    components = []
    section = re.search(r'^#{1,6}\s+Component Types\s*\n(.*?)(?=\n#{1,6}\s|\Z)', text, re.M | re.S)
    component_table = section[1] if section else ''
    for match in re.finditer(r'^\|\s*(\d+)\s*\|\s*\[([^]]+)\]\([^)]+\)\s*\|[^|]*\|[^|]*\|\s*([^|]+)\|', component_table, re.M):
        components.append({'type': int(match[1]), 'name': match[2], 'usage': plain(match[3])})
    return {'headings': [plain(h[2]) for h in headings], 'routes': routes,
            'table_keys': sorted({plain(m) for m in re.findall(r'^\|\s*([^|]+?)\s*\|', text, re.M)}),
            'components': components}


def symbol_root(symbol):
    # Stable docs currently expose six commands anchors with a doubled prefix.
    # Preserve the original inventory ID, but group these under the actual API.
    if symbol.startswith('discord.discord.ext.commands.'):
        symbol = symbol.removeprefix('discord.')
    for namespace in ('discord.ext.commands.', 'discord.ext.tasks.', 'discord.app_commands.',
                      'discord.ui.', 'discord.abc.', 'discord.utils.', 'discord.opus.'):
        if symbol.startswith(namespace):
            return namespace + symbol[len(namespace):].split('.')[0]
    return '.'.join(symbol.split('.')[:2])


def require(condition, message):
    if not condition:
        raise ValueError(message)


def validate(snapshot, coverage, markdown, diagram, root=ROOT):
    require(snapshot['schema'] == coverage['schema'] == 1, 'Unsupported roadmap schema')
    require(snapshot['reviewed_on'] == coverage['reviewed_on'], 'Review dates differ')
    require(re.fullmatch(r'\d{4}-\d{2}-\d{2}', snapshot['reviewed_on']), 'Invalid review date')
    streams = {row['id']: row for row in coverage['workstreams']}
    require(len(streams) == len(coverage['workstreams']), 'Duplicate workstream ID')
    for key, row in streams.items():
        require(re.fullmatch(r'W\d{2}', key), 'Invalid workstream ID: ' + key)
        require(markdown.count(f'<a id="{key.lower()}"></a>') == 1, 'Missing/duplicate roadmap anchor: ' + key)
        require(row['status'] in ('partial', 'planned', 'research', 'complete'), 'Invalid status: ' + key)
        require(row['scope'] and row['acceptance'] and row['milestone'], 'Incomplete plan: ' + key)
        require(row['status'] != 'partial' or row['evidence'], 'Partial status needs evidence: ' + key)
        for path in row['evidence']:
            target = (root / path).resolve()
            require(target.is_relative_to(root.resolve()) and target.is_file(), 'Missing/unsafe evidence path: ' + path)
        require(set(row['depends_on']) <= streams.keys() and key not in row['depends_on'], 'Invalid dependency: ' + key)
        done = row.get('done_tasks', {})
        task_ids = {f'{key}.{index}' for index in range(1, len(row['scope']) + 1)}
        require(done.keys() <= task_ids, 'Unknown completed task: ' + key)
        if row['status'] == 'complete':
            require(row.get('completion_review') and done.keys() == task_ids,
                    'Completed workstream needs review and evidence for every task: ' + key)
        for index, task in enumerate(row['scope'], 1):
            task_id = f'{key}.{index}'
            marker = 'x' if task_id in done else ' '
            require(markdown.count(f'- [{marker}] **{task_id}** — {task}') == 1,
                    'Roadmap task text/state differs from registry: ' + task_id)
            if task_id in done:
                require(done[task_id], 'Completed task needs evidence: ' + task_id)
                for path in done[task_id]:
                    target = (root / path).resolve()
                    require(target.is_relative_to(root.resolve()) and target.is_file(), 'Missing task evidence: ' + task_id)
        for criterion in row['acceptance']:
            require('- ' + criterion in markdown, 'Acceptance criterion missing from roadmap: ' + key)
    visiting, visited = set(), set()

    def visit(key):
        require(key not in visiting, 'Roadmap dependency cycle at ' + key)
        if key in visited:
            return
        visiting.add(key)
        for dependency in streams[key]['depends_on']:
            visit(dependency)
        visiting.remove(key)
        visited.add(key)

    for key in streams:
        visit(key)
    for key, row in streams.items():
        dependencies = ', '.join(f'[{value}](#{value.lower()})' for value in row['depends_on']) or 'none'
        metadata = (f'**Status:** {row["status"]}. **Proposed slice:** {row["milestone"]}. '
                    f'**Prerequisites:** {dependencies}.')
        require(markdown.count(f'## {key} — {row["title"]}') == 1 and metadata in markdown,
                'Workstream metadata differs from roadmap: ' + key)
    blocks = re.findall(r'```mermaid\s*\n(.*?)```', markdown, re.S)
    require(len(blocks) == 1 and blocks[0].strip() == diagram.strip(), 'Markdown/Mermaid roadmap diagrams differ')
    require('v1.0' not in markdown, 'Roadmap must not introduce a major-release target')
    require('0.10.x' in markdown and '0.11.x' in markdown, 'Open-ended 0.x policy missing')
    require(coverage['cpp_api_review_commit'] == snapshot['cpp_api_review_commit'], 'C++ baseline differs')
    require(re.fullmatch(r'[a-f0-9]{40}', snapshot['cpp_api_review_commit']), 'C++ review needs a full commit SHA')
    require(snapshot['library_version'] == (root / 'VERSION').read_text(encoding='utf-8').strip(),
            'Library version changed; review and update roadmap baseline before release')
    require(f'Shipped library baseline: **v{snapshot["library_version"]}**' in markdown
            and snapshot['cpp_api_review_commit'] in markdown
            and f'Reviewed: **{snapshot["reviewed_on"]}**' in markdown,
            'Roadmap baseline/review text differs from snapshot')
    sources = {source['id']: source for source in snapshot['sources']}
    require(len(sources) == len(snapshot['sources']), 'Duplicate source IDs')
    require(all(source['kind'] in ('python-api', 'python-guide', 'python-changelog',
                                   'discord-index', 'discord-reference', 'policy-html')
                for source in sources.values()), 'Unknown upstream source kind')
    require(all(source['url'].startswith('https://') and re.fullmatch(r'[a-f0-9]{64}', source['sha256'])
                for source in sources.values()), 'Invalid source reference/digest')
    page_urls, python_roots, symbols = set(), set(), set()
    route_count = 0
    components = {}
    for source in sources.values():
        for item in source['facts'].get('pages', []):
            page_urls.add(item['url'])
        for symbol in source['facts'].get('symbols', []):
            symbols.add(symbol)
            python_roots.add(symbol_root(symbol))
        route_count += len(source['facts'].get('routes', []))
        for component in source['facts'].get('components', []):
            key = str(component['type'])
            require(key not in components or components[key] == component, 'Conflicting upstream component definitions: ' + key)
            components[key] = component
            require(key in coverage['component_workstreams'], 'Unmapped component type: ' + key)
        require(source['url'] in coverage['page_workstreams'], 'Unmapped fetched source: ' + source['url'])
    require(page_urls <= coverage['page_workstreams'].keys(),
            'Unmapped Discord index pages: ' + ', '.join(sorted(page_urls - coverage['page_workstreams'].keys())))
    require(python_roots == coverage['python_roots'].keys(),
            'Python root mapping differs: ' + ', '.join(sorted(python_roots ^ coverage['python_roots'].keys())))
    require(components.keys() == coverage['component_workstreams'].keys(), 'Component mapping differs from snapshot')
    require(components and route_count > 0 and len(symbols) > 0, 'Empty upstream inventory')
    used = set()
    for mapping in ('page_workstreams', 'python_roots', 'component_workstreams'):
        for key, value in coverage[mapping].items():
            require(value and set(value) <= streams.keys(), 'Unknown/empty mapping: ' + key)
            used.update(value)
    require(used == streams.keys(), 'Workstream has no upstream mapping: ' + ', '.join(sorted(streams.keys() - used)))
    return {'workstreams': len(streams), 'discord_index_pages': len(page_urls),
            'python_symbols': len(symbols), 'python_roots': len(python_roots),
            'source_pages': len(sources), 'route_entries': route_count, 'component_types': len(components)}


def fetch_source(source):
    url = source['url']
    require(urllib.parse.urlsplit(url).scheme == 'https' and urllib.parse.urlsplit(url).hostname in ('docs.discord.com', 'discordpy.readthedocs.io'),
            'Only official documentation hosts may be fetched')
    request = urllib.request.Request(url, headers={'User-Agent': 'yl-discord.cpp-roadmap-audit'})
    class OfficialRedirects(urllib.request.HTTPRedirectHandler):
        def redirect_request(self, req, fp, code, msg, headers, newurl):
            target = urllib.parse.urlsplit(newurl)
            allowed = (target.scheme == 'https' and
                       (target.hostname == urllib.parse.urlsplit(url).hostname or POLICY_REDIRECTS.get(url) == newurl))
            require(allowed, 'Unexpected documentation redirect from ' + url)
            return super().redirect_request(req, fp, code, msg, headers, newurl)

    opener = urllib.request.build_opener(OfficialRedirects())
    with opener.open(request, timeout=45) as response:
        body = response.read(8 * 1024 * 1024 + 1)
    require(len(body) <= 8 * 1024 * 1024, 'Documentation response too large')
    return facts(source['kind'], body), document_digest(source['kind'], body)


def compare_source(source, fresh_facts, fresh_hash):
    # Structural changes are named; prose-only revisions also require review.
    if fresh_hash == source['sha256']:
        return None
    before, after = source['facts'], fresh_facts
    changes = {}
    for field in sorted(before.keys() | after.keys()):
        old = {json.dumps(value, sort_keys=True) for value in before.get(field, [])}
        new = {json.dumps(value, sort_keys=True) for value in after.get(field, [])}
        if old != new:
            changes[field] = {'added': [json.loads(value) for value in sorted(new - old)],
                              'removed': [json.loads(value) for value in sorted(old - new)]}
    return {'source': source['id'], 'url': source['url'],
            'reason': 'structure_changed' if changes else 'source_content_changed', 'changes': changes}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check-upstream', action='store_true', help='Read official docs and fail on unreviewed drift')
    parser.add_argument('--report', type=Path, help='Optional JSON drift report; no source files are updated')
    args = parser.parse_args()
    folder = ROOT / 'docs' / 'roadmap'
    snapshot = json.loads((folder / 'upstream.json').read_text(encoding='utf-8'))
    coverage = json.loads((folder / 'coverage.json').read_text(encoding='utf-8'))
    result = validate(snapshot, coverage, (ROOT / 'docs/ROADMAP.md').read_text(encoding='utf-8'),
                      (ROOT / 'docs/ROADMAP.mmd').read_text(encoding='utf-8'))
    print('Roadmap inventory:', json.dumps(result, sort_keys=True))
    if args.check_upstream:
        with ThreadPoolExecutor(max_workers=4) as pool:
            fresh = list(pool.map(fetch_source, snapshot['sources']))
        drift = [change for source, (data, digest) in zip(snapshot['sources'], fresh)
                 if (change := compare_source(source, data, digest))]
        if args.report:
            args.report.parent.mkdir(parents=True, exist_ok=True)
            args.report.write_text(json.dumps({'changes': drift}, indent=2) + '\n', encoding='utf-8')
        for change in drift:
            print('Upstream review required:', change['source'], change['reason'])
        require(not drift, 'Unreviewed upstream changes; inspect the report and update the roadmap deliberately')
        print('Official documentation snapshot unchanged')


if __name__ == '__main__':
    try:
        main()
    except (ValueError, KeyError, OSError) as error:
        print('Roadmap audit failed:', error, file=sys.stderr)
        sys.exit(1)
