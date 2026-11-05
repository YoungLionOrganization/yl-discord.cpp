# Current scope compared with discord.py

Reviewed against the current public C++ API on 2026-11-06. The implemented library
is v0.4.1. This inventory describes usable high-level features, not what could be
built manually from raw REST/JSON. It does not imply complete discord.py coverage.

| Area | yl-discord.cpp v0.4.1 status |
| --- | --- |
| Async functions/classes | Implemented: task/co_await, Client/Bot overrides, owning callbacks |
| Prefix commands | Implemented: configured prefix, aliases, quoted arguments, typed parameters, checks and cooldowns |
| Slash commands / Bot command tree | Not implemented; a typed CommandTree and Bot integration are planned |
| Hybrid commands / application-command groups / autocomplete | Not implemented |
| User/message context menus | Not implemented |
| View / LayoutView / Components V2 | Not implemented |
| Buttons / all select-menu types | Not implemented |
| Modals / modern modal controls | Not implemented |
| Generated prefix help | Implemented, explicitly enabled with add_help_command(); constructor does not add it |
| Custom help | Name and command metadata are configurable; replace the command for custom text/embeds; no HelpCommand/provider class yet |
| Cogs | Basic command ownership, registration/removal and in-flight safety; no Cog lifecycle hooks, GroupCog or extension loader |
| Embeds | Implemented typed rich subset: title, description, fields, author/footer, color, timestamp, image/thumbnail |
| Message operations/uploads | Send/reply/fetch/edit/delete, own reactions, buffered multipart files and attachment retention |
| Gateway / REST | Bot sessions, heartbeat/resume, async HTTP and bucket/global limits |
| Event helpers | Message/Ready/RawEvent waits with predicates, deadlines/cancellation; removable listeners |
| Broad guild/member/role/cache APIs | Not implemented; current typed models cover an initial message-oriented subset |
| Voice / sharding | Not implemented |
| Webhooks, polls, moderation, scheduled events, broad thread/presence APIs | No dedicated high-level feature sets yet |
| Advanced access/testing | Raw Gateway dispatch, low-level REST, Asio executor and MemoryTransport |
| Distribution | Source/CMake, Conan recipe, vcpkg overlay and native MSYS2 assets |

## Components V2 and modern modals

Discord's [component reference](https://docs.discord.com/developers/components/reference)
and discord.py's [LayoutView/UI reference](https://discordpy.readthedocs.io/en/stable/interactions/api.html#discord.ui.LayoutView)
are the implementation references. Planned UI work explicitly covers Components V2
layout/content types, buttons, every current select-menu category and modern modal
layout/controls, including Label, modal file picking and the radio/checkbox controls
listed by the platform. Placement and validation rules need implementation too.

None of that UI layer is shipped in this C++ library yet. In particular,
FileUpload currently means outgoing attachment bytes, not a modal file-picker.
Typed embeds are also distinct from Components V2 layout messages.

## Help customization and ergonomics

The [command guide](COMMANDS.md) shows opt-in generated help and a replacement
command for custom output. Built-in help is a fixed text formatter; it is not an
equivalent of discord.py's extensible HelpCommand class.

The current API provides a short coroutine/class-based path for small prefix and
message bots. That does not establish mature developer ergonomics or feature
parity for interaction-heavy bots: slash commands, context menus, UI, broader state
and extension/lifecycle tools are still missing. Usability examples and review
remain part of the [roadmap](ROADMAP.md).

The API aims for familiar concepts, not Python syntax emulation. Limited synthetic
[benchmark measurements](BENCHMARKS.md) exist; a general live-bot performance
advantage has not been established. See the
[discord.py documentation](https://discordpy.readthedocs.io/en/stable/) for the
comparison target's complete public surface.
