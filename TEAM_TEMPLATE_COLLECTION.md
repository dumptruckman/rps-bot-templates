# Maintaining the Team Template collection

The collection is the repository-owned inventory of participant-facing Team
Templates. [`team-templates.json`](team-templates.json) is the discovery index;
its stable language IDs point to descriptors such as
[`templates/python/team-template.json`](templates/python/team-template.json).
The Python descriptor currently binds the existing root-level Team Source and
guidance during the expand phase. Those legacy paths remain in place until the
separate migration and contraction work is complete.

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
./validate-team --template python
./release-team-template --template python manifest template-v1
```

Release creation and verification accept the same `--template python` option.
During this expand step, omitting the option preserves the existing singular
Python validation and release interfaces for Team branches, workflows, and
clean-clone checks.

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
