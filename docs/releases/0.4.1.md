# yl-discord.cpp v0.4.1

Maintenance release for the transfer to YoungLionOrganization and command parsing.
The C++20 coroutine API and LGPL-3.0-or-later license remain unchanged.

## Repository and packaging

- Canonical repository: [YoungLionOrganization/yl-discord.cpp](https://github.com/YoungLionOrganization/yl-discord.cpp).
- Updated CMake/Conan metadata, vcpkg/MSYS2 source generators and package templates.
- Updated badges, download/setup links, issue/security links and HTTP User-Agent.
- Preserved original author/copyright notices and immutable published tags/assets.
- Added a regression check for consistent package/runtime repository identity.

## Command correctness and performance

- Resolve a command name before interpreting its argument tail. Unknown names
  are ignored even if their unused arguments contain malformed quotes/escapes.
- Preserve canonical command name, invoked alias and original Message when a
  known command's argument syntax is invalid. The incomplete argument list is
  not exposed as a successful parse.
- Share token-scanning logic between command lookup and the public parser,
  preserving quoted/escaped names, empty arguments and normal argument behavior.
- Avoid allocating a combined command/argument vector and shifting all arguments
  to remove its first element. This is a targeted synthetic-path optimization;
  it does not establish a general live-bot speed advantage.

## Documentation and validation

- Ordered roadmap with priorities, proposed milestones and completion criteria.
- Offline benchmark tooling, raw samples and reproduction/interpretation guidance.
- Regression coverage for unknown malformed tails, syntax-error Context identity,
  quoted/escaped aliases and empty arguments.
- Local validation: six CTest suites, including 13 core, 11 command, 15 event,
  6 embed, 6 file and 16 network scenarios, plus 12 release-tool tests.
- Publication requires Linux/Windows static/shared builds, sanitizer checks and
  Conan, vcpkg and MINGW64/UCRT64 package consumers through the release workflow.

No authenticated Discord smoke test was run. Existing dependency licenses and
the documented experimental API/ABI policy still apply. Rebuild shared consumers
for the versioned v0.4.1 runtime library.

## Downloads and guides

- [Source ZIP](https://github.com/YoungLionOrganization/yl-discord.cpp/releases/download/v0.4.1/yl-discord.cpp-v0.4.1.zip)
- [Source TAR.GZ](https://github.com/YoungLionOrganization/yl-discord.cpp/releases/download/v0.4.1/yl-discord.cpp-v0.4.1.tar.gz)
- [Roadmap](https://github.com/YoungLionOrganization/yl-discord.cpp/blob/v0.4.1/docs/ROADMAP.md)
- [Commands](https://github.com/YoungLionOrganization/yl-discord.cpp/blob/v0.4.1/docs/COMMANDS.md)
- [Benchmarks](https://github.com/YoungLionOrganization/yl-discord.cpp/blob/v0.4.1/docs/BENCHMARKS.md)
