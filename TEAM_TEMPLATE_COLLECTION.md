# Maintaining the Team Template collection

The collection is the repository-owned inventory of participant-facing Team
Templates. [`team-templates.json`](team-templates.json) is the discovery index;
its stable language IDs point to descriptors such as
[`templates/python/team-template.json`](templates/python/team-template.json).
The Python descriptor binds the migrated source, tests, guidance, and
build-and-test script below `templates/python/`. The former root-level Python
paths remain temporarily as legacy compatibility material until the separate
contraction work is complete.

Each descriptor binds one language ID to:

- its controlled Team Source directory and participant guidance;
- its repository-owned build-and-test entrypoint;
- its independently addressable Template Release version, tag, and expected
  Source Digest;
- its Advisory Validation workflow; and
- the matching Runner-owned Language Environment.

Paths are repository-relative POSIX paths. Collection loading rejects duplicate
language IDs, missing descriptors or bound files, paths that escape the
repository, symbolic-link targets, and selection without a language ID once the
index contains more than one template.

## Validate and prepare one release

The collection-aware forms select a descriptor by stable language ID:

```sh
./check-team-template --template python --mode docker
./check-team-template --template python --mode native
./validate-team --template python
./release-team-template --template python manifest python-template-v2
```

Docker and native modes both execute `templates/python/build-and-test`; Docker
selects the immutable development toolchain for its native platform from the
matching Language Environment in the exact pinned Catalog Release. Release
creation and verification accept the same `--template python` option. Omitting
the option temporarily preserves the older singular Python validation and
release interfaces.

Both selected commands first verify `core-tool.lock.json` and the materialized
Runner checkout. They then derive Team Source, release metadata, and the
Language Environment from the selected descriptor. Loading fails if that
Language Environment is absent or is contract-only in the exact pinned Catalog
Release, so an indexed starter cannot be presented as supported without its
Runner execution contract.

## Ownership boundary

This shape preserves [ADR 0001](docs/adr/0001-consume-runner-owned-catalog.md).
This repository owns Team Templates, Team guidance, collection metadata,
participant build-and-test entrypoints, Advisory Validation entrypoints, and
Template Releases. It does not copy or redefine Runner-owned Language
Environments, wrappers, Seed Adapters, runtimes, build recipes, readiness
contracts, entrypoints, or conformance fixtures. The descriptor is a one-way
compatibility binding to the exact pinned Catalog Release, not a second catalog
authority.
