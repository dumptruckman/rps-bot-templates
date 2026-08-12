# Remove the singular Team Template shape

Status: resolved

Blocked by: 02

## Parent

[Multi-language Team Templates](../PRD.md)

## What to build

Complete the reorganization after Python is green by removing the legacy
single-template interface and making the collection the sole participant-facing
and maintainer-facing path.

## Acceptance criteria

- [x] No active command, workflow, test, release path, or participant guide
  assumes the former root-level Python source or singular descriptor.
- [x] The root command requires an explicit or unambiguous Team Template
  selection and reports available language IDs when selection fails.
- [x] A clean clone can check, Advisory Validate, and prepare an independent
  Python Template Release through the collection interface.
- [x] Repository documentation describes the stable layout and the checklist for
  adding another Team Template.
- [x] Guard tests reject reintroduction of Python-specific path and language
  constants in shared collection tooling.
- [x] All legacy compatibility material removed by this contraction has an
  intentional migration note or replacement.

## Comments

This is the contract step. It should not begin until the migrated Python path is
the fully verified replacement.

## Answer

Removed the root `team-template.json`, `team_source/`, participant guide, and
the legacy validation and Template Release fallbacks. Shared commands and both
active workflows now resolve Team Source, Language Environment, entrypoint,
Template Release identity, and paths through `team-templates.json`; failed
selection lists the available language IDs.

Documented the stable per-language layout, new-template checklist, clean-clone
Python check/Advisory Validation/Template Release commands, and the intentional
`template-v1` migration boundary. Added contraction guards that reject legacy
root files and Python-specific paths or language constants in shared tooling.

All 72 repository tests, the native check, the digest-pinned Docker check, a
collection-derived Python Template Release manifest, and complete participant-local
Advisory Validation with practice Match pass. The starter Source Digest remains
`sha256:e2890c1587c6c98acb62121e5524d8f75a53925ed738f333f63beee81e60fd1a`.
