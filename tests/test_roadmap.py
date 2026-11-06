# SPDX-License-Identifier: LGPL-3.0-or-later
# Copyright (C) 2026 Cavanshirpro
# Licensed under LGPL-3.0-or-later; see NOTICE, LICENSE and COPYING.
"""Guard real roadmap traceability and parser/drift failure paths without network."""
import copy
import json
from pathlib import Path
import sys
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
import audit_roadmap as audit


class RoadmapTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        folder = audit.ROOT / 'docs/roadmap'
        cls.snapshot = json.loads((folder / 'upstream.json').read_text(encoding='utf-8'))
        cls.coverage = json.loads((folder / 'coverage.json').read_text(encoding='utf-8'))
        cls.markdown = (audit.ROOT / 'docs/ROADMAP.md').read_text(encoding='utf-8')
        cls.diagram = (audit.ROOT / 'docs/ROADMAP.mmd').read_text(encoding='utf-8')

    def validate(self, snapshot=None, coverage=None, markdown=None, diagram=None):
        return audit.validate(snapshot if snapshot is not None else self.snapshot,
                              coverage if coverage is not None else self.coverage,
                              markdown if markdown is not None else self.markdown,
                              diagram if diagram is not None else self.diagram)

    def test_real_inventory_is_mapped_without_network(self):
        with patch('urllib.request.build_opener', side_effect=AssertionError('Offline audit must not fetch')):
            result = self.validate()
        self.assertGreater(result['python_symbols'], 4000)
        self.assertGreater(result['discord_index_pages'], 150)
        self.assertGreaterEqual(result['component_types'], 20)

    def test_unmapped_index_page_is_rejected(self):
        data = copy.deepcopy(self.coverage)
        source = next(s for s in self.snapshot['sources'] if s['kind'] == 'discord-index')
        del data['page_workstreams'][source['facts']['pages'][0]['url']]
        with self.assertRaisesRegex(ValueError, 'Unmapped'):
            self.validate(coverage=data)

    def test_unknown_public_root_is_rejected(self):
        data = copy.deepcopy(self.snapshot)
        source = next(s for s in data['sources'] if s['kind'] == 'python-api')
        source['facts']['symbols'].append('discord.FutureResource.create')
        with self.assertRaisesRegex(ValueError, 'root mapping differs'):
            self.validate(snapshot=data)

    def test_new_component_and_stale_component_mapping_are_rejected(self):
        snapshot = copy.deepcopy(self.snapshot)
        source = next(s for s in snapshot['sources'] if s['facts'].get('components'))
        source['facts']['components'].append({'type': 999, 'name': 'FutureControl', 'usage': 'Modal'})
        with self.assertRaisesRegex(ValueError, 'Unmapped component'):
            self.validate(snapshot=snapshot)
        coverage = copy.deepcopy(self.coverage)
        coverage['component_workstreams']['999'] = ['W14']
        with self.assertRaisesRegex(ValueError, 'Component mapping differs'):
            self.validate(coverage=coverage)

    def test_dependency_cycles_are_rejected(self):
        data = copy.deepcopy(self.coverage)
        # W02 already depends on W01.
        data['workstreams'][0]['depends_on'] = ['W02']
        with self.assertRaisesRegex(ValueError, 'cycle'):
            self.validate(coverage=data)

    def test_missing_anchor_and_changed_diagram_are_rejected(self):
        with self.assertRaisesRegex(ValueError, 'anchor'):
            self.validate(markdown=self.markdown.replace('<a id="w01"></a>', ''))
        with self.assertRaisesRegex(ValueError, 'diagrams differ'):
            self.validate(diagram=self.diagram + '\nB --> N\n')

    def test_dependency_metadata_and_baseline_text_cannot_go_stale(self):
        data = copy.deepcopy(self.coverage)
        data['workstreams'][0]['depends_on'] = ['W04']
        with self.assertRaisesRegex(ValueError, 'metadata differs'):
            self.validate(coverage=data)
        with self.assertRaisesRegex(ValueError, 'baseline/review text'):
            self.validate(markdown=self.markdown.replace('Shipped library baseline: **v0.4.1**', 'Shipped library baseline: **v0.0.0**'))

    def test_task_and_acceptance_cannot_disappear_from_markdown(self):
        row = self.coverage['workstreams'][0]
        with self.assertRaisesRegex(ValueError, 'task text'):
            self.validate(markdown=self.markdown.replace(row['scope'][0], 'REMOVED'))
        with self.assertRaisesRegex(ValueError, 'Acceptance criterion'):
            self.validate(markdown=self.markdown.replace(row['acceptance'][0], 'REMOVED'))

    def test_partial_and_complete_claims_require_evidence(self):
        data = copy.deepcopy(self.coverage)
        data['workstreams'][0]['evidence'] = []
        with self.assertRaisesRegex(ValueError, 'needs evidence'):
            self.validate(coverage=data)
        data = copy.deepcopy(self.coverage)
        data['workstreams'][0]['status'] = 'complete'
        with self.assertRaisesRegex(ValueError, 'needs review and evidence'):
            self.validate(coverage=data)

    def test_evidence_outside_the_repository_is_rejected(self):
        data = copy.deepcopy(self.coverage)
        data['workstreams'][0]['evidence'] = ['../outside-evidence.md']
        with self.assertRaisesRegex(ValueError, 'evidence path'):
            self.validate(coverage=data)

    def test_version_bump_requires_new_baseline_review(self):
        data = copy.deepcopy(self.snapshot)
        data['library_version'] = '0.0.0'
        with self.assertRaisesRegex(ValueError, 'version changed'):
            self.validate(snapshot=data)

    def test_documented_symbol_extraction_and_known_sphinx_alias(self):
        body = b'<dt id="discord.Client.close"></dt><div id="discord.NotDefinition"></div><dt id="discord.Client.close"></dt>'
        self.assertEqual(audit.facts('python-api', body)['symbols'], ['discord.Client.close'])
        self.assertEqual(audit.symbol_root('discord.discord.ext.commands.Author'), 'discord.ext.commands.Author')

    def test_routes_and_component_tables_are_not_confused_with_opcodes(self):
        body = b'''# Reference
## Get Thing
GET
/things/[{thing.id}](https://docs.discord.com/developers/resources/example)
| 99 | [Not a component](https://example.test) | note | layout | Message |
###### Component Types
| Type | Name | Description | Style | Usage |
| 23 | [Checkbox](https://docs.discord.com/developers/components/reference#checkbox) | input | Interactive | Modal |
## Another table
| 98 | [Also not a component](https://example.test) | note | layout | Message |
'''
        data = audit.facts('discord-reference', body)
        self.assertEqual(data['routes'], [{'method': 'GET', 'path': '/things/{thing.id}', 'section': 'Get Thing'}])
        self.assertEqual(data['components'], [{'type': 23, 'name': 'Checkbox', 'usage': 'Modal'}])

    def test_structural_and_prose_only_upstream_drift_require_review(self):
        source = {'id': 'example', 'url': 'https://docs.discord.com/llms.txt',
                  'sha256': 'a' * 64, 'facts': {'pages': []}}
        self.assertIsNone(audit.compare_source(source, source['facts'], source['sha256']))
        changed = audit.compare_source(source, {'pages': [{'title': 'New', 'url': 'https://docs.discord.com/new'}]}, 'b' * 64)
        self.assertEqual(changed['reason'], 'structure_changed')
        self.assertTrue(changed['changes']['pages']['added'])
        changed = audit.compare_source(source, source['facts'], 'c' * 64)
        self.assertEqual(changed['reason'], 'source_content_changed')

    def test_online_fetch_rejects_nonofficial_or_insecure_hosts_before_request(self):
        with patch('urllib.request.build_opener', side_effect=AssertionError('Must not fetch')):
            for url in ('https://localhost/private', 'http://docs.discord.com/llms.txt'):
                with self.assertRaisesRegex(ValueError, 'official documentation'):
                    audit.fetch_source({'url': url, 'kind': 'discord-index'})

    def test_policy_article_digest_ignores_page_nonces_but_detects_content_and_links(self):
        a = b'<script>nonce=1</script><div class="article-body"><p>Current policy</p><a href="/one">details</a></div>'
        b = a.replace(b'nonce=1', b'nonce=2')
        self.assertEqual(audit.document_digest('policy-html', a), audit.document_digest('policy-html', b))
        self.assertNotEqual(audit.document_digest('policy-html', a), audit.document_digest('policy-html', a.replace(b'Current', b'Changed')))
        self.assertNotEqual(audit.document_digest('policy-html', a), audit.document_digest('policy-html', a.replace(b'/one', b'/two')))
        with self.assertRaisesRegex(ValueError, 'article body'):
            audit.document_digest('policy-html', b'<html>Unexpected response</html>')


if __name__ == '__main__':
    unittest.main()
