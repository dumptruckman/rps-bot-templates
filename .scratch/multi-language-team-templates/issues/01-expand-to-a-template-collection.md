# Expand to a collection of Team Templates

Status: resolved

Blocked by: None

## Parent

[Multi-language Team Templates](../PRD.md)

## What to build

Add a collection-aware interface beside the existing singular Python interface
so maintainers can describe, select, validate, and release one Team Template by
language without breaking the current Python workflow.

## Acceptance criteria

- [x] A repository-owned index discovers Team Templates by stable language ID
  and rejects duplicates, missing descriptors, unsafe paths, and ambiguous
  selection.
- [x] Each template descriptor can bind its Team Source, participant guidance,
  build-and-test entrypoint, Template Release identity, and matching Runner-owned
  Language Environment.
- [x] Validation and release commands accept a selected template and derive its
  paths and Language Environment from metadata rather than Python constants.
- [x] A template cannot be presented as supported when its Language Environment
  is absent from the exact pinned Catalog Release.
- [x] Existing Python validation, workflow, release, and clean-clone behavior
  remain green through the legacy interface during this expand step.
- [x] Contract tests cover the collection boundary without requiring any new
  language toolchain.
- [x] Maintainer documentation explains how the collection preserves the ADR
  boundary between Team Templates and Runner-owned Language Environments.

## Comments

This is the expand step of an expand-and-contract reorganization. Do not move or
remove the existing Python paths yet.

## Answer

Added `team-templates.json` and a Python collection descriptor that bind the
existing Team Source, participant guidance, validation entrypoint, Template
Release identity, Advisory Validation workflow, and Runner-owned Python
Language Environment without moving the singular Python paths.

`validate-team` and `release-team-template` now accept `--template python`, load
paths and the Language Environment from verified collection metadata, and fail
closed for duplicate IDs, missing descriptors, unsafe or symlinked paths,
ambiguous selection, and environments absent or unsupported in the exact pinned
Catalog Release. Legacy and selected release verification interoperate so the
existing workflow can verify releases created through either interface.

Contract tests require no additional language toolchain. The collection guide
documents the expand-phase commands and preserves ADR 0001's one-way ownership
boundary: this repository describes Team Templates but does not copy or redefine
Runner-owned Language Environments. Python 3.9 compilation and the complete
repository test suite pass.
