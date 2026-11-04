# Roadmap

Maintained in [YoungLionOrganization/yl-discord.cpp](https://github.com/YoungLionOrganization/yl-discord.cpp).
Last reviewed: 2026-11-04. This is an ordered plan, not a release-date promise.
Unchecked items are not available features; version targets may change after
compatibility and implementation review.

The goal is a coroutine-based, class-friendly C++20 library that is approachable
for small bots and exposes clear ownership, resource limits and extension points
for advanced applications. Correctness and measured resource use take priority
over broad performance claims or quickly matching every discord.py feature.

## Current foundation — v0.1.0 through v0.4.1

- [x] C++20 tasks, one event loop, Client/Bot subclasses and Cog-owned callbacks.
- [x] Live TLS REST/Gateway, heartbeats, reconnect/resume and server-driven limits.
- [x] Prefix commands, aliases, converters, checks, cooldowns and generated help.
- [x] Message operations, reactions, embeds and explicit mention policy.
- [x] Buffered multipart uploads and explicit attachment retention.
- [x] Removable listeners and predicate waits with deadlines/cancellation.
- [x] Offline transports, network fixtures and static/shared package consumers.
- [x] Automated version tag, tested packages and published GitHub Releases.
- [x] Optional offline performance harness with raw samples and limitations.

Slash commands, UI, voice, broad guild state and sharding are not implemented.
Authenticated Discord smoke testing is owner-initiated; automated tests use
synthetic credentials and local fixtures.

## First priority — maintenance and performance (v0.4.x)

- [x] Update repository URLs, package sources, badges and HTTP identification for
  YoungLionOrganization; retain original copyright attribution.
- [x] Verify generated package downloads, transferred-repository Actions and
  release publication under the organization.
- [x] Preserve canonical command/alias identity on argument syntax errors.
- [x] Resolve command names before parsing unknown-command arguments; avoid
  allocating and shifting a combined command/argument vector.
- [x] Track VERSION changes in incremental CMake builds so generated versions
  and shared-library names cannot remain stale.
- [x] Add regression coverage and run all local native/network suites.
- [x] Verify package consumers and the cross-platform release CI matrix.
- [x] Record before/after measurements with the same compiler, configuration and
  workload; retain raw data without generalizing synthetic results to live bots.

Exit criteria: regression coverage and native/package CI pass; source archives
contain the intended files; an immutable patch release publishes with valid
checksums. Public layout/interface changes require a minor version.

The first maintenance batch is complete in
[v0.4.1](https://github.com/YoungLionOrganization/yl-discord.cpp/releases/tag/v0.4.1).
The [release run](https://github.com/YoungLionOrganization/yl-discord.cpp/actions/runs/41886169544)
passed; all eight downloaded release assets and seven SHA-256 entries were checked,
and both source archives were validated. The initial MSYS2 mirror timeout was
resolved by rerunning the failed job; the release checks were retained.

## Runtime reliability and resource controls (proposed v0.5)

- [ ] Bound REST, dispatch and upload admission, with explicit rejection and
  cancellation behavior rather than silent dropping.
- [ ] Add opt-in REST latency, rate-limit waiting, heartbeat health and queue-depth
  diagnostics with credential-safe defaults.
- [ ] Define Cog lifecycle hooks and managed background-task shutdown.
- [ ] Add sustained-load fixtures covering full queues, cancellation and memory.
- [ ] Profile JSON/model copies, scheduling and cooldown cleanup before optimizing.

Exit criteria: documented bounds hold under load, cancellation releases pending
work and failures reach error hooks without exposing credentials.

## Application commands and interactions (proposed v0.6)

- [ ] Typed interaction models and raw ingress independent of a full guild cache.
- [ ] Slash-command registration/sync with explicit scope and deletion policy.
- [ ] Initial response, defer, edit and followup helpers with clear state errors.
- [ ] Reuse converters, checks and command errors where semantics match.
- [ ] Fixture tests for acknowledgement state, duplicate responses, expiration,
  reconnect and HTTP failures; a minimal slash-command example.

Exit criteria: small slash bots use owning Context-like values and coroutine
callbacks; invalid response sequences fail predictably.

## Interactive UI (proposed v0.7)

- [ ] Buttons, selects, modals and response helpers.
- [ ] Class-based Views with explicit ownership, timeout and cancellation.
- [ ] Routing, authorization and opt-in persistent component handling.
- [ ] Stale/concurrent interaction and callback-removal fixtures plus examples.

Exit criteria: Views have bounded lifetime and cleanup; supported controls do not
require ordinary users to construct raw JSON.

## Guild APIs and optional state (proposed v0.8)

- [ ] Guild, channel, member, role and permission REST models/helpers.
- [ ] Explicit partial-model and fetch semantics.
- [ ] Opt-in caches with entry/byte budgets, TTL, eviction and cache-free use.
- [ ] Permission and partial/unavailable-object fixtures.
- [ ] Filesystem/stream upload sources and progress with bounded memory.

Exit criteria: applications choose state/memory policy; cached objects do not
silently imply complete or current guild state.

## Larger deployments (proposed v0.9)

- [ ] Shard lifecycle and identify coordination with explicit restart policy.
- [ ] Backpressure across shard/event boundaries and predictable shutdown.
- [ ] Document executor integration and thread-safe operation boundaries.
- [ ] Controlled sustained-load/recovery measurements; optional replay fixtures
  with explicit message-content and credential retention policy.

Exit criteria: shard recovery respects resource/identify limits without unbounded
queues, leaked tasks or duplicate ownership.

## Stable API (v1.0 readiness)

- [ ] Review naming, ownership, cancellation and errors across APIs.
- [ ] Publish compatibility/ABI policy and migration guidance; verify supported
  compiler/dependency combinations.
- [ ] Complete installation, cookbook, class-based examples and extension docs.
- [ ] Measure equivalent live workloads on controlled hardware, separating network
  limits from framework CPU costs.
- [ ] Complete an owner-run authenticated smoke test before claiming live-platform
  validation; keep real credentials out of PR workflows.

Voice/audio needs a separate design and dependency review; it is outside these
milestones rather than an implied v1.0 commitment.

## Selecting and verifying work

1. Reproduce a bug or identify a measured bottleneck before changing behavior.
2. Add targeted regression coverage while preserving ownership/cancellation,
   custom transport and class callback semantics.
3. Run the relevant suites and [CI matrix](TESTING.md). Retain the
   [configuration and raw samples](BENCHMARKS.md) for performance changes.
4. Update documentation/changelog and follow the [release process](RELEASING.md).

The transfer does not change LGPL-3.0-or-later licensing. Existing tags/assets
remain immutable; new package recipes use the organization URL.
