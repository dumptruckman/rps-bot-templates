# Remove the singular Team Template shape

Status: ready-for-agent

Blocked by: 02

## Parent

[Multi-language Team Templates](../PRD.md)

## What to build

Complete the reorganization after Python is green by removing the legacy
single-template interface and making the collection the sole participant-facing
and maintainer-facing path.

## Acceptance criteria

- [ ] No active command, workflow, test, release path, or participant guide
  assumes the former root-level Python source or singular descriptor.
- [ ] The root command requires an explicit or unambiguous Team Template
  selection and reports available language IDs when selection fails.
- [ ] A clean clone can check, Advisory Validate, and prepare an independent
  Python Template Release through the collection interface.
- [ ] Repository documentation describes the stable layout and the checklist for
  adding another Team Template.
- [ ] Guard tests reject reintroduction of Python-specific path and language
  constants in shared collection tooling.
- [ ] All legacy compatibility material removed by this contraction has an
  intentional migration note or replacement.

## Comments

This is the contract step. It should not begin until the migrated Python path is
the fully verified replacement.
