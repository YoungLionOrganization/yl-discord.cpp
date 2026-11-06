# Roadmap research and traceability register

Review date: **2026-11-06**. Library audit baseline: **v0.4.1**,
commit `f224337e01bb201718aa72d15576e7de44253f0d`.
This register supports the [canonical roadmap](../ROADMAP.md), not a claim that
mapped upstream features are already implemented.

## Method and boundaries

1. Read Discord's official documentation index, core protocol/resource/component
   references and current discord.py core/interactions/commands/tasks API docs.
2. Capture all documented Python definition IDs from the four API pages, resource
   HTTP route/section/schema keys, component IDs and every unique index URL.
3. Review the stable changelog, compatibility/intents guides, command/converter/
   Cog/extension guides and access-gated neighboring platform categories.
4. Compare those families with public C++ headers, implementations, fixtures and
   package/CI evidence. Mark broad families partial even when a small subset works.
5. Record scope, prerequisites, acceptance criteria and source mappings, then run
   offline and explicit online drift checks.

Only identifiers, schema keys, section titles, URLs and SHA-256 source digests are
checked in. Upstream prose/HTML is not redistributed. Original responses were read
for this review; source hashes allow subsequent changes to be detected. Most
digests cover the response bytes. The two developer-policy URLs redirect to
Discord's official support site: their `policy-html` digests cover normalized
article text and link targets, excluding changing page navigation/request nonces.
Only those two exact support redirects are allowed by the online checker.

The Python snapshot is a documented public-definition inventory, not every Python
object, inherited alias, private implementation detail or generated overload.
Six current Sphinx anchors have a doubled `discord.discord.ext.commands` prefix;
the original IDs are retained and grouped under their actual command API roots.
Methods inside large roots such as Client/Guild still require per-member review
when the workstream is implemented; mapping a root never certifies full coverage.

HTTP counts are documentation route entries, including deprecated/overlapping
entries, not a count of unique implemented endpoints. Schema keys identify review
areas, not a complete executable OpenAPI schema or exhaustive parameter typing.
Counts must never be used as an implemented-parity percentage.

## Source kinds

- **Fetched reference:** source body read and structure/hash captured. These are
  the only pages the online drift command fetches.
- **Index-scoped page:** URL/category reviewed for applicability, not a claim of
  deep review of every Social SDK, game tutorial or browser SDK document.
- **Library evidence:** existing C++ source/test paths; these justify only the
  partial baseline described in the workstream.

## Scope decisions

| Surface | Decision and rationale |
| --- | --- |
| Documented discord.py core, commands, tasks, interactions and UI | Target C++ equivalents across W01-W30; retain typed/behavioral parity gaps explicitly |
| Discord bot REST/Gateway and current components/modals | Core target, including current fields, access restrictions, deprecations and error behavior |
| Social SDK friends/provisional accounts/lobbies/game identity | W31 explicit optional/access-gated integration review; not silently treated as bot-token functionality |
| Embedded Activities / browser SDK / desktop RPC / certified devices | W31 scope/authorization decision; activity callbacks belong in W10/W11 where applicable |
| Website component-embed previews | W31 optional website output, distinct from bot embeds and LayoutView |
| Group DM/OAuth-only and approval-restricted operations | W26/W31 credential/access gate; public documentation is not a promise of bot access |
| Voice receive/recording/video/screen sharing | Separate W28 scope decision; do not imply playback parity includes these features |
| Python decorators/GC/module reload and synchronous adapters | Explicit C++ ergonomic/ABI/executor design decisions, not copied syntax or hidden blocking calls |
| Private endpoints, user-account self-bots, approval bypasses | Outside supported bot-library scope; never counted as completed public API coverage |

## Inventory summary

- 66 unique fetched official sources; 173 unique Discord index URLs.
- 4419 distinct documented Python identifiers in 610 reviewed API roots.
- 251 captured HTTP route entries; 20 current component types; 35 workstreams and 215 tracked scope tasks.

## Source-to-workstream register

<a id="w01"></a>

### W01 — Coroutine runtime, lifecycle and errors

Plan and acceptance: [W01](../ROADMAP.md#w01).

Reviewed Python roots assigned here: 16. Exact members and original anchors remain in [upstream.json](upstream.json); assignments are in [coverage.json](coverage.json).


<a id="w02"></a>

### W02 — HTTP engine, authentication and rate limits

Plan and acceptance: [W02](../ROADMAP.md#w02).

Reviewed Python roots assigned here: 1. Exact members and original anchors remain in [upstream.json](upstream.json); assignments are in [coverage.json](coverage.json).

- [API Reference](https://docs.discord.com/developers/reference.md) — fetched `discord-reference`.
- [Rate Limits](https://docs.discord.com/developers/topics/rate-limits.md) — fetched `discord-topics--rate-limits`.

<a id="w03"></a>

### W03 — Gateway, intents, presence and protocol control

Plan and acceptance: [W03](../ROADMAP.md#w03).

Reviewed Python roots assigned here: 16. Exact members and original anchors remain in [upstream.json](upstream.json); assignments are in [coverage.json](coverage.json).

- [Intents and member caches](https://discordpy.readthedocs.io/en/stable/intents.html) — fetched `discordpy-intents`.
- [Gateway Events](https://docs.discord.com/developers/events/gateway-events.md) — fetched `discord-events--gateway-events`.
- [Gateway](https://docs.discord.com/developers/events/gateway.md) — fetched `discord-events--gateway`.
- [Opcodes and Status Codes](https://docs.discord.com/developers/topics/opcodes-and-status-codes.md) — fetched `discord-topics--opcodes-and-status-codes`.

<a id="w04"></a>

### W04 — Models, serialization, flags, assets and utilities

Plan and acceptance: [W04](../ROADMAP.md#w04).

Reviewed Python roots assigned here: 43. Exact members and original anchors remain in [upstream.json](upstream.json); assignments are in [coverage.json](coverage.json).

- [discordpy-core](https://discordpy.readthedocs.io/en/stable/api.html) — fetched `discordpy-core`.
- [API Reference](https://docs.discord.com/developers/reference.md) — fetched `discord-reference`.

<a id="w05"></a>

### W05 — Typed events, state and cache policy

Plan and acceptance: [W05](../ROADMAP.md#w05).

Reviewed Python roots assigned here: 117. Exact members and original anchors remain in [upstream.json](upstream.json); assignments are in [coverage.json](coverage.json).

- [discordpy-core](https://discordpy.readthedocs.io/en/stable/api.html) — fetched `discordpy-core`.
- [Intents and member caches](https://discordpy.readthedocs.io/en/stable/intents.html) — fetched `discordpy-intents`.
- [Gateway Events](https://docs.discord.com/developers/events/gateway-events.md) — fetched `discord-events--gateway-events`.
- [Overview of Events](https://docs.discord.com/developers/events/overview.md) — fetched `discord-events--overview`.

<a id="w06"></a>

### W06 — Complete prefix-command framework

Plan and acceptance: [W06](../ROADMAP.md#w06).

Reviewed Python roots assigned here: 128. Exact members and original anchors remain in [upstream.json](upstream.json); assignments are in [coverage.json](coverage.json).

- [discordpy-commands](https://discordpy.readthedocs.io/en/stable/ext/commands/api.html) — fetched `discordpy-commands`.
- [Converters, flags and hybrid commands](https://discordpy.readthedocs.io/en/stable/ext/commands/commands.html) — fetched `discordpy-command-guide`.

<a id="w07"></a>

### W07 — Automatic and fully replaceable help

Plan and acceptance: [W07](../ROADMAP.md#w07).

Reviewed Python roots assigned here: 4. Exact members and original anchors remain in [upstream.json](upstream.json); assignments are in [coverage.json](coverage.json).

- [discordpy-commands](https://discordpy.readthedocs.io/en/stable/ext/commands/api.html) — fetched `discordpy-commands`.

<a id="w08"></a>

### W08 — Cogs, extensions and reload lifecycle

Plan and acceptance: [W08](../ROADMAP.md#w08).

Reviewed Python roots assigned here: 9. Exact members and original anchors remain in [upstream.json](upstream.json); assignments are in [coverage.json](coverage.json).

- [discordpy-commands](https://discordpy.readthedocs.io/en/stable/ext/commands/api.html) — fetched `discordpy-commands`.
- [Cog lifecycle](https://discordpy.readthedocs.io/en/stable/ext/commands/cogs.html) — fetched `discordpy-cogs`.
- [Extension reload and cleanup](https://discordpy.readthedocs.io/en/stable/ext/commands/extensions.html) — fetched `discordpy-extensions`.

<a id="w09"></a>

### W09 — Managed background loops and scheduling

Plan and acceptance: [W09](../ROADMAP.md#w09).

Reviewed Python roots assigned here: 3. Exact members and original anchors remain in [upstream.json](upstream.json); assignments are in [coverage.json](coverage.json).

- [discordpy-tasks](https://discordpy.readthedocs.io/en/stable/ext/tasks/index.html) — fetched `discordpy-tasks`.

<a id="w10"></a>

### W10 — Interaction ingress and response lifecycle

Plan and acceptance: [W10](../ROADMAP.md#w10).

Reviewed Python roots assigned here: 10. Exact members and original anchors remain in [upstream.json](upstream.json); assignments are in [coverage.json](coverage.json).

- [discordpy-interactions](https://discordpy.readthedocs.io/en/stable/interactions/api.html) — fetched `discordpy-interactions`.
- [Interactions Overview](https://docs.discord.com/developers/interactions/overview.md) — fetched `discord-interactions--overview`.
- [Receiving and Responding to Interactions](https://docs.discord.com/developers/interactions/receiving-and-responding.md) — fetched `discord-interactions--receiving-and-responding`.

<a id="w11"></a>

### W11 — CommandTree, slash, context menus and hybrid commands

Plan and acceptance: [W11](../ROADMAP.md#w11).

Reviewed Python roots assigned here: 67. Exact members and original anchors remain in [upstream.json](upstream.json); assignments are in [coverage.json](coverage.json).

- [Converters, flags and hybrid commands](https://discordpy.readthedocs.io/en/stable/ext/commands/commands.html) — fetched `discordpy-command-guide`.
- [discordpy-interactions](https://discordpy.readthedocs.io/en/stable/interactions/api.html) — fetched `discordpy-interactions`.
- [Application Commands](https://docs.discord.com/developers/interactions/application-commands.md) — fetched `discord-interactions--application-commands`.

<a id="w12"></a>

### W12 — Legacy components, buttons, selects and View

Plan and acceptance: [W12](../ROADMAP.md#w12).

Reviewed Python roots assigned here: 20. Exact members and original anchors remain in [upstream.json](upstream.json); assignments are in [coverage.json](coverage.json).

- [discordpy-interactions](https://discordpy.readthedocs.io/en/stable/interactions/api.html) — fetched `discordpy-interactions`.
- [Components Overview](https://docs.discord.com/developers/components/overview.md) — fetched `discord-components--overview`.
- [Component Reference](https://docs.discord.com/developers/components/reference.md) — fetched `discord-components--reference`.
- [Using Message Components](https://docs.discord.com/developers/components/using-message-components.md) — fetched `discord-components--using-message-components`.

<a id="w13"></a>

### W13 — Components V2 and LayoutView

Plan and acceptance: [W13](../ROADMAP.md#w13).

Reviewed Python roots assigned here: 18. Exact members and original anchors remain in [upstream.json](upstream.json); assignments are in [coverage.json](coverage.json).

- [discordpy-interactions](https://discordpy.readthedocs.io/en/stable/interactions/api.html) — fetched `discordpy-interactions`.
- [Components Overview](https://docs.discord.com/developers/components/overview.md) — fetched `discord-components--overview`.
- [Component Reference](https://docs.discord.com/developers/components/reference.md) — fetched `discord-components--reference`.
- [Using Message Components](https://docs.discord.com/developers/components/using-message-components.md) — fetched `discord-components--using-message-components`.

<a id="w14"></a>

### W14 — Modern modals and every current modal control

Plan and acceptance: [W14](../ROADMAP.md#w14).

Reviewed Python roots assigned here: 16. Exact members and original anchors remain in [upstream.json](upstream.json); assignments are in [coverage.json](coverage.json).

- [discordpy-interactions](https://discordpy.readthedocs.io/en/stable/interactions/api.html) — fetched `discordpy-interactions`.
- [Components Overview](https://docs.discord.com/developers/components/overview.md) — fetched `discord-components--overview`.
- [Component Reference](https://docs.discord.com/developers/components/reference.md) — fetched `discord-components--reference`.
- [Using Modal Components](https://docs.discord.com/developers/components/using-modal-components.md) — fetched `discord-components--using-modal-components`.

<a id="w15"></a>

### W15 — Roles, permissions and effective access

Plan and acceptance: [W15](../ROADMAP.md#w15).

Reviewed Python roots assigned here: 22. Exact members and original anchors remain in [upstream.json](upstream.json); assignments are in [coverage.json](coverage.json).

- [Channels Resource](https://docs.discord.com/developers/resources/channel.md) — fetched `discord-resources--channel`.
- [Guild Resource](https://docs.discord.com/developers/resources/guild.md) — fetched `discord-resources--guild`.
- [Permissions](https://docs.discord.com/developers/topics/permissions.md) — fetched `discord-topics--permissions`.

<a id="w16"></a>

### W16 — Users, members, DMs and moderation

Plan and acceptance: [W16](../ROADMAP.md#w16).

Reviewed Python roots assigned here: 11. Exact members and original anchors remain in [upstream.json](upstream.json); assignments are in [coverage.json](coverage.json).

- [Guild Resource](https://docs.discord.com/developers/resources/guild.md) — fetched `discord-resources--guild`.
- [User Resource](https://docs.discord.com/developers/resources/user.md) — fetched `discord-resources--user`.

<a id="w17"></a>

### W17 — Guilds, onboarding, integrations, invites and templates

Plan and acceptance: [W17](../ROADMAP.md#w17).

Reviewed Python roots assigned here: 36. Exact members and original anchors remain in [upstream.json](upstream.json); assignments are in [coverage.json](coverage.json).

- [Guild Template Resource](https://docs.discord.com/developers/resources/guild-template.md) — fetched `discord-resources--guild-template`.
- [Guild Resource](https://docs.discord.com/developers/resources/guild.md) — fetched `discord-resources--guild`.
- [Invite Resource](https://docs.discord.com/developers/resources/invite.md) — fetched `discord-resources--invite`.

<a id="w18"></a>

### W18 — All channel types, forums, media and threads

Plan and acceptance: [W18](../ROADMAP.md#w18).

Reviewed Python roots assigned here: 18. Exact members and original anchors remain in [upstream.json](upstream.json); assignments are in [coverage.json](coverage.json).

- [Channels Resource](https://docs.discord.com/developers/resources/channel.md) — fetched `discord-resources--channel`.
- [Voice Resource](https://docs.discord.com/developers/resources/voice.md) — fetched `discord-resources--voice`.
- [Threads](https://docs.discord.com/developers/topics/threads.md) — fetched `discord-topics--threads`.

<a id="w19"></a>

### W19 — Complete messages, embeds, attachments and history

Plan and acceptance: [W19](../ROADMAP.md#w19).

Reviewed Python roots assigned here: 17. Exact members and original anchors remain in [upstream.json](upstream.json); assignments are in [coverage.json](coverage.json).

- [discordpy-core](https://discordpy.readthedocs.io/en/stable/api.html) — fetched `discordpy-core`.
- [Message Resource](https://docs.discord.com/developers/resources/message.md) — fetched `discord-resources--message`.

<a id="w20"></a>

### W20 — Reactions, emoji, stickers and expressive metadata

Plan and acceptance: [W20](../ROADMAP.md#w20).

Reviewed Python roots assigned here: 11. Exact members and original anchors remain in [upstream.json](upstream.json); assignments are in [coverage.json](coverage.json).

- [Emoji Resource](https://docs.discord.com/developers/resources/emoji.md) — fetched `discord-resources--emoji`.
- [Message Resource](https://docs.discord.com/developers/resources/message.md) — fetched `discord-resources--message`.
- [Sticker Resource](https://docs.discord.com/developers/resources/sticker.md) — fetched `discord-resources--sticker`.

<a id="w21"></a>

### W21 — Polls and vote lifecycle

Plan and acceptance: [W21](../ROADMAP.md#w21).

Reviewed Python roots assigned here: 4. Exact members and original anchors remain in [upstream.json](upstream.json); assignments are in [coverage.json](coverage.json).

- [Poll Resource](https://docs.discord.com/developers/resources/poll.md) — fetched `discord-resources--poll`.

<a id="w22"></a>

### W22 — Webhooks, webhook messages and HTTP event delivery

Plan and acceptance: [W22](../ROADMAP.md#w22).

Reviewed Python roots assigned here: 7. Exact members and original anchors remain in [upstream.json](upstream.json); assignments are in [coverage.json](coverage.json).

- [Webhook Events](https://docs.discord.com/developers/events/webhook-events.md) — fetched `discord-events--webhook-events`.
- [Webhook Resource](https://docs.discord.com/developers/resources/webhook.md) — fetched `discord-resources--webhook`.

<a id="w23"></a>

### W23 — Audit logs and Auto Moderation

Plan and acceptance: [W23](../ROADMAP.md#w23).

Reviewed Python roots assigned here: 13. Exact members and original anchors remain in [upstream.json](upstream.json); assignments are in [coverage.json](coverage.json).

- [Audit Logs Resource](https://docs.discord.com/developers/resources/audit-log.md) — fetched `discord-resources--audit-log`.
- [Auto Moderation](https://docs.discord.com/developers/resources/auto-moderation.md) — fetched `discord-resources--auto-moderation`.

<a id="w24"></a>

### W24 — Scheduled events and stage instances

Plan and acceptance: [W24](../ROADMAP.md#w24).

Reviewed Python roots assigned here: 4. Exact members and original anchors remain in [upstream.json](upstream.json); assignments are in [coverage.json](coverage.json).

- [Guild Scheduled Event](https://docs.discord.com/developers/resources/guild-scheduled-event.md) — fetched `discord-resources--guild-scheduled-event`.
- [Stage Instance Resource](https://docs.discord.com/developers/resources/stage-instance.md) — fetched `discord-resources--stage-instance`.

<a id="w25"></a>

### W25 — Soundboard and voice effects

Plan and acceptance: [W25](../ROADMAP.md#w25).

Reviewed Python roots assigned here: 7. Exact members and original anchors remain in [upstream.json](upstream.json); assignments are in [coverage.json](coverage.json).

- [Soundboard Resource](https://docs.discord.com/developers/resources/soundboard.md) — fetched `discord-resources--soundboard`.

<a id="w26"></a>

### W26 — Applications, teams, OAuth2 and linked roles

Plan and acceptance: [W26](../ROADMAP.md#w26).

Reviewed Python roots assigned here: 11. Exact members and original anchors remain in [upstream.json](upstream.json); assignments are in [coverage.json](coverage.json).

- [Application Identity Profile Resource](https://docs.discord.com/developers/resources/application-identity-profile.md) — fetched `discord-resources--application-identity-profile`.
- [Application Role Connection Metadata](https://docs.discord.com/developers/resources/application-role-connection-metadata.md) — fetched `discord-resources--application-role-connection-metadata`.
- [Application Resource](https://docs.discord.com/developers/resources/application.md) — fetched `discord-resources--application`.
- [User Resource](https://docs.discord.com/developers/resources/user.md) — fetched `discord-resources--user`.
- [OAuth2](https://docs.discord.com/developers/topics/oauth2.md) — fetched `discord-topics--oauth2`.
- [Managing Your Developer Team](https://docs.discord.com/developers/topics/teams.md) — fetched `discord-topics--teams`.

<a id="w27"></a>

### W27 — SKUs, entitlements, subscriptions and purchases

Plan and acceptance: [W27](../ROADMAP.md#w27).

Reviewed Python roots assigned here: 12. Exact members and original anchors remain in [upstream.json](upstream.json); assignments are in [coverage.json](coverage.json).

- [Webhook Events](https://docs.discord.com/developers/events/webhook-events.md) — fetched `discord-events--webhook-events`.
- [Enabling Monetization](https://docs.discord.com/developers/monetization/enabling-monetization.md) — fetched `discord-monetization--enabling-monetization`.
- [Implementing App Subscriptions](https://docs.discord.com/developers/monetization/implementing-app-subscriptions.md) — fetched `discord-monetization--implementing-app-subscriptions`.
- [Implementing In-App Purchases for Activities](https://docs.discord.com/developers/monetization/implementing-iap-for-activities.md) — fetched `discord-monetization--implementing-iap-for-activities`.
- [Implementing One-Time Purchases](https://docs.discord.com/developers/monetization/implementing-one-time-purchases.md) — fetched `discord-monetization--implementing-one-time-purchases`.
- [Managing SKUs](https://docs.discord.com/developers/monetization/managing-skus.md) — fetched `discord-monetization--managing-skus`.
- [Monetizing Your Discord App](https://docs.discord.com/developers/monetization/overview.md) — fetched `discord-monetization--overview`.
- [Entitlement Resource](https://docs.discord.com/developers/resources/entitlement.md) — fetched `discord-resources--entitlement`.
- [SKU Resource](https://docs.discord.com/developers/resources/sku.md) — fetched `discord-resources--sku`.
- [Subscription Resource](https://docs.discord.com/developers/resources/subscription.md) — fetched `discord-resources--subscription`.

<a id="w28"></a>

### W28 — Voice transport, DAVE and audio sources

Plan and acceptance: [W28](../ROADMAP.md#w28).

Reviewed Python roots assigned here: 15. Exact members and original anchors remain in [upstream.json](upstream.json); assignments are in [coverage.json](coverage.json).

- [discordpy-core](https://discordpy.readthedocs.io/en/stable/api.html) — fetched `discordpy-core`.
- [Voice Resource](https://docs.discord.com/developers/resources/voice.md) — fetched `discord-resources--voice`.
- [Opcodes and Status Codes](https://docs.discord.com/developers/topics/opcodes-and-status-codes.md) — fetched `discord-topics--opcodes-and-status-codes`.
- [Voice](https://docs.discord.com/developers/topics/voice-connections.md) — fetched `discord-topics--voice-connections`.

<a id="w29"></a>

### W29 — Sharding, multi-client operation and scale

Plan and acceptance: [W29](../ROADMAP.md#w29).

Reviewed Python roots assigned here: 4. Exact members and original anchors remain in [upstream.json](upstream.json); assignments are in [coverage.json](coverage.json).


<a id="w30"></a>

### W30 — Advanced extension points, observability and performance

Plan and acceptance: [W30](../ROADMAP.md#w30).

Reviewed Python roots assigned here: 1. Exact members and original anchors remain in [upstream.json](upstream.json); assignments are in [coverage.json](coverage.json).


<a id="w31"></a>

### W31 — Access-gated and adjacent platform surfaces

Plan and acceptance: [W31](../ROADMAP.md#w31).

Reviewed Python roots assigned here: 0. Exact members and original anchors remain in [upstream.json](upstream.json); assignments are in [coverage.json](coverage.json).

- [Webhook Events](https://docs.discord.com/developers/events/webhook-events.md) — fetched `discord-events--webhook-events`.
- [Website component embeds](https://docs.discord.com/developers/link-previews/component-embeds.md) — fetched `discord-component-embeds`.
- [Link preview scope](https://docs.discord.com/developers/link-previews/overview.md) — fetched `discord-link-previews`.
- [Application Identity Profile Resource](https://docs.discord.com/developers/resources/application-identity-profile.md) — fetched `discord-resources--application-identity-profile`.
- [Lobby Resource](https://docs.discord.com/developers/resources/lobby.md) — fetched `discord-resources--lobby`.
- [Certified Devices](https://docs.discord.com/developers/topics/certified-devices.md) — fetched `discord-topics--certified-devices`.
- [RPC](https://docs.discord.com/developers/topics/rpc.md) — fetched `discord-topics--rpc`.

<a id="w32"></a>

### W32 — Builds, packaging, releases and supply chain

Plan and acceptance: [W32](../ROADMAP.md#w32).

Reviewed Python roots assigned here: 2. Exact members and original anchors remain in [upstream.json](upstream.json); assignments are in [coverage.json](coverage.json).

- [Compatibility and public API policy](https://discordpy.readthedocs.io/en/stable/version_guarantees.html) — fetched `discordpy-version-policy`.

<a id="w33"></a>

### W33 — Compatibility, security and adversarial verification

Plan and acceptance: [W33](../ROADMAP.md#w33).

Reviewed Python roots assigned here: 0. Exact members and original anchors remain in [upstream.json](upstream.json); assignments are in [coverage.json](coverage.json).

- [Compatibility and public API policy](https://discordpy.readthedocs.io/en/stable/version_guarantees.html) — fetched `discordpy-version-policy`.
- [Developer Policy](https://docs.discord.com/developers/policies/developer-policy.md) — fetched `discord-policies--developer-policy`.
- [Developer Terms of Service](https://docs.discord.com/developers/policies/developer-terms-of-service.md) — fetched `discord-policies--developer-terms-of-service`.

<a id="w34"></a>

### W34 — Developer ergonomics, reference and examples

Plan and acceptance: [W34](../ROADMAP.md#w34).

Reviewed Python roots assigned here: 0. Exact members and original anchors remain in [upstream.json](upstream.json); assignments are in [coverage.json](coverage.json).


<a id="w35"></a>

### W35 — Coverage registry and upstream-change review

Plan and acceptance: [W35](../ROADMAP.md#w35).

Reviewed Python roots assigned here: 0. Exact members and original anchors remain in [upstream.json](upstream.json); assignments are in [coverage.json](coverage.json).

- [discordpy-changelog](https://discordpy.readthedocs.io/en/stable/whats_new.html) — fetched `discordpy-changelog`.
- [Change Log](https://docs.discord.com/developers/change-log.md) — fetched `discord-change-log`.
- [discord-index](https://docs.discord.com/llms.txt) — fetched `discord-index`.

## Current component inventory

Every listed type is **planned**, not shipped in v0.4.1. Placement/limits/interaction behavior require implementation as well as serialization.

| Type | Name | Documented placement | Plan |
| ---: | --- | --- | --- |
| 1 | Action Row | Message | W12 |
| 2 | Button | Message | W12 |
| 3 | String Select | Message, Modal | W12, W14 |
| 4 | Text Input | Modal | W14 |
| 5 | User Select | Message, Modal | W12, W14 |
| 6 | Role Select | Message, Modal | W12, W14 |
| 7 | Mentionable Select | Message, Modal | W12, W14 |
| 8 | Channel Select | Message, Modal | W12, W14 |
| 9 | Section | Message | W13 |
| 10 | Text Display | Message, Modal | W13, W14 |
| 11 | Thumbnail | Message | W13 |
| 12 | Media Gallery | Message | W13 |
| 13 | File | Message | W13 |
| 14 | Separator | Message | W13 |
| 17 | Container | Message | W13 |
| 18 | Label | Modal | W14 |
| 19 | File Upload | Modal | W14 |
| 21 | Radio Group | Modal | W14 |
| 22 | Checkbox Group | Modal | W14 |
| 23 | Checkbox | Modal | W14 |

## Resource endpoint coverage

These are fetched documentation entries, not implemented endpoints. Current bot/access restrictions and deprecated paths are part of each work package.

| Resource | Route entries | Plan |
| --- | ---: | --- |
| [Application Resource](https://docs.discord.com/developers/resources/application.md) | 3 | W26 |
| [Application Identity Profile Resource](https://docs.discord.com/developers/resources/application-identity-profile.md) | 5 | W31, W26 |
| [Application Role Connection Metadata](https://docs.discord.com/developers/resources/application-role-connection-metadata.md) | 2 | W26 |
| [Audit Logs Resource](https://docs.discord.com/developers/resources/audit-log.md) | 1 | W23 |
| [Auto Moderation](https://docs.discord.com/developers/resources/auto-moderation.md) | 5 | W23 |
| [Channels Resource](https://docs.discord.com/developers/resources/channel.md) | 26 | W18, W15 |
| [Emoji Resource](https://docs.discord.com/developers/resources/emoji.md) | 10 | W20 |
| [Entitlement Resource](https://docs.discord.com/developers/resources/entitlement.md) | 5 | W27 |
| [Guild Resource](https://docs.discord.com/developers/resources/guild.md) | 47 | W17, W15, W16 |
| [Guild Scheduled Event](https://docs.discord.com/developers/resources/guild-scheduled-event.md) | 6 | W24 |
| [Guild Template Resource](https://docs.discord.com/developers/resources/guild-template.md) | 6 | W17 |
| [Invite Resource](https://docs.discord.com/developers/resources/invite.md) | 9 | W17 |
| [Lobby Resource](https://docs.discord.com/developers/resources/lobby.md) | 16 | W31 |
| [Message Resource](https://docs.discord.com/developers/resources/message.md) | 20 | W19, W20 |
| [Poll Resource](https://docs.discord.com/developers/resources/poll.md) | 2 | W21 |
| [SKU Resource](https://docs.discord.com/developers/resources/sku.md) | 1 | W27 |
| [Soundboard Resource](https://docs.discord.com/developers/resources/soundboard.md) | 7 | W25 |
| [Stage Instance Resource](https://docs.discord.com/developers/resources/stage-instance.md) | 4 | W24 |
| [Sticker Resource](https://docs.discord.com/developers/resources/sticker.md) | 8 | W20 |
| [Subscription Resource](https://docs.discord.com/developers/resources/subscription.md) | 2 | W27 |
| [User Resource](https://docs.discord.com/developers/resources/user.md) | 12 | W16, W26 |
| [Voice Resource](https://docs.discord.com/developers/resources/voice.md) | 5 | W28, W18 |
| [Webhook Resource](https://docs.discord.com/developers/resources/webhook.md) | 15 | W22 |

## Refresh procedure

Run `python scripts/audit_roadmap.py --check-upstream --report build/roadmap-drift.json`.
If it reports changes, read the affected official sources and changelogs first.
Review new definitions, changed parameters/placement, removed/deprecated APIs,
credential scope and dependency effects. Update the task/acceptance/mapping before
capturing new source facts and digests. Do not change hashes just to suppress drift.

The parser `facts(kind, body)` in [audit_roadmap.py](../../scripts/audit_roadmap.py)
reproduces the structural extraction; source URL/kind entries in
[upstream.json](upstream.json) specify the inputs. `fetch_source()` reads current
official sources without secrets. Refreshes are deliberately reviewed changes,
not an automatic overwrite command. Add a new source URL when the official index
introduces a relevant family; a new index page is a review event even if it is not
yet a fetched reference.

Run the offline audit, focused tests and release/link scanner after editing.
Normal source CI makes no external documentation requests, so upstream outages
cannot silently rewrite scope or block unrelated offline development.

A library VERSION change also requires a deliberate roadmap baseline review.
The online audit does not update sources, mappings, completion checkboxes or
baseline metadata. Root mappings and digests are planning evidence, not proof that
all methods/parameters already have a C++ implementation.
