# Versioning

Package versions use **MAJOR.MINOR.PATCH** with decimal components and no leading
zeros. The first release is **0.1.0**, Git tag **v0.1.0**. `v0.1` is a shorthand
in discussion, not a release tag accepted by the tooling.

- **PATCH:** backward-compatible fixes, documentation and packaging corrections.
- **MINOR:** new functionality; before 1.0 this may also include documented API breaks.
- **MAJOR:** reserved for a separately decided major-version policy change; there
  is no scheduled major-version milestone in the current roadmap.

Development continues in the 0.x series for as many minor releases as needed:
`0.9.x` -> `0.10.x` -> `0.11.x` is valid. Version components are compared as
integers; `0.10.0` is newer than `0.9.99` and is not another spelling of `0.1.0`.

Before 1.0 there is no cross-minor API/ABI compatibility promise. The installed
CMake package uses SameMinorVersion compatibility; patch updates within a minor
line are intended to remain source-compatible. CMake version selection does not
promise binary compatibility: pre-1.0 object layouts remain experimental. Shared
libraries use the full MAJOR.MINOR.PATCH in their soname/DLL runtime name before
1.0 to prevent accidental loading into an old binary. Rebuild v0.1.0 consumers
for v0.1.1 and rebuild again for the v0.2.0 minor release. No cross-compiler/standard-library ABI compatibility is promised.

`VERSION` is the canonical package version, read by CMake and Conan. CMake generates
public version constants. `release.json` adds the exact tag and a GitHub
`prerelease` boolean; the vcpkg manifest and release notes must agree.
The boolean is GitHub release metadata, not an extra semantic-version component.
v0.1.0 is marked as a prerelease because it was an offline foundation. v0.1.1 completes the initial live-message milestone
and is published as a normal GitHub release.
v0.2.0 adds the command toolkit and message operations as a normal minor release.
v0.3.0 extends event control, rich messages and mention policy; rebuild its consumers.
v0.4.0 adds buffered multipart uploads and attachment models; rebuild its consumers.

For a later release, prepare completed Markdown notes mentioning the new tag:

```sh
python scripts/bump_version.py 0.1.2 --notes /path/to/completed-notes.md
```

Use `--stable` to set GitHub's prerelease flag to false. The helper refuses an
older/equal version, writes VERSION/release metadata/vcpkg version, and copies
the notes into both `release.md` and `docs/releases/<version>.md`. It does not
commit, tag, push or invent changelog entries. Update README/CHANGELOG, validate
and follow [the release procedure](RELEASING.md). Never move a published tag.
