# Contributing

Check the [current feature status](docs/COMPARISON.md) and
[workstream roadmap](docs/ROADMAP.md) before adding features. Name the relevant
workstream/task in the change and update its scope, acceptance criteria and evidence
when behavior changes. A generic REST method does not establish typed feature parity.

Use C++20 and the existing namespace/style. Keep simple bot code concise while
documenting ownership and advanced access. Take owned event/Context values in
coroutines; do not retain references to temporary callback arguments. Never
block the event-loop thread for network I/O. Keep command and Cog lifetimes safe
across suspension and registry changes.

Build/test with the [build guide](docs/BUILDING.md), then run:

```sh
python scripts/check_release.py
python scripts/audit_roadmap.py
python -m unittest discover -s tests -p 'test_*.py' -v
```

For package-facing changes also install and run `tests/consumer`, and use
`conan create` where appropriate. Change docs/examples with API changes. Tests
should cover behavior or meaningful failure cases rather than duplicate code.
Do not add token-dependent CI tests, generated build files or credentials.

Before implementing a new API family or preparing a release, run the explicit
official-source [drift review](docs/roadmap/RESEARCH.md#refresh-procedure).
Normal source CI uses the committed snapshot offline. Review new fields, methods,
access restrictions and deprecations before updating its digest/mappings; never
delete unmapped items just to make the audit pass. Update the reviewed baseline
when VERSION changes. Completed task checkboxes need implementation/test evidence.

Use the issue/PR templates to describe the concrete problem, final behavior and
validation. Keep release versions unchanged in ordinary feature PRs; the
maintainer updates versions using [the release process](docs/RELEASING.md).
Project-owned contributions use LGPL-3.0-or-later, with the existing copyright
and SPDX notices. Third-party files retain their original licenses.
