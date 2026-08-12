# Expand to a collection of Team Templates

Status: ready-for-agent

Blocked by: None

## Parent

[Multi-language Team Templates](../PRD.md)

## What to build

Add a collection-aware interface beside the existing singular Python interface
so maintainers can describe, select, validate, and release one Team Template by
language without breaking the current Python workflow.

## Acceptance criteria

- [ ] A repository-owned index discovers Team Templates by stable language ID
  and rejects duplicates, missing descriptors, unsafe paths, and ambiguous
  selection.
- [ ] Each template descriptor can bind its Team Source, participant guidance,
  build-and-test entrypoint, Template Release identity, and matching Runner-owned
  Language Environment.
- [ ] Validation and release commands accept a selected template and derive its
  paths and Language Environment from metadata rather than Python constants.
- [ ] A template cannot be presented as supported when its Language Environment
  is absent from the exact pinned Catalog Release.
- [ ] Existing Python validation, workflow, release, and clean-clone behavior
  remain green through the legacy interface during this expand step.
- [ ] Contract tests cover the collection boundary without requiring any new
  language toolchain.
- [ ] Maintainer documentation explains how the collection preserves the ADR
  boundary between Team Templates and Runner-owned Language Environments.

## Comments

This is the expand step of an expand-and-contract reorganization. Do not move or
remove the existing Python paths yet.
