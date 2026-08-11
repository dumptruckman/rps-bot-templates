# Remove the duplicate catalog and release the Team Template

Status: ready-for-agent

Priority: 2

Blocked by: 02

## Parent

[Consume the Runner-owned catalog](../PRD.md)

## What to build

Delete the locally maintained Language Environment Catalog and replace catalog
release ownership with an immutable Template Release that pins the Runner-owned
catalog and identifies the participant-facing starter contents.

## Acceptance criteria

- [ ] No wrapper, runtime definition, recipe, readiness contract, entrypoint,
  conformance suite, or catalog manifest is maintained as an authoritative copy
  in this repository.
- [ ] Catalog-freezing tooling, workflow language, and tests are removed or
  replaced with Template Release equivalents.
- [ ] A Template Release manifest records the Template repository commit,
  Team Template digest, pinned Runner commit and package version, catalog
  identity, Advisory Validation workflow identity, and supported template
  version.
- [ ] Release creation and verification reject a dirty tree, mutable references,
  mismatched catalog lock, changed Team Template, or incorrect annotated tag.
- [ ] Team branch creation, Team guidance, submission cutoff, and Advisory
  Validation point at the Template Release rather than a catalog tag owned here.
- [ ] Repository tests prove there is no second catalog source tree.

## Comments

The materialized Runner checkout is a verified dependency cache, not a second
source of catalog authority.
