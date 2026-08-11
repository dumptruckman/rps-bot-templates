# Remove the duplicate catalog and release the Team Template

Status: resolved

Priority: 2

Blocked by: 02

## Parent

[Consume the Runner-owned catalog](../PRD.md)

## What to build

Delete the locally maintained Language Environment Catalog and replace catalog
release ownership with an immutable Template Release that pins the Runner-owned
catalog and identifies the participant-facing starter contents.

## Acceptance criteria

- [x] No wrapper, runtime definition, recipe, readiness contract, entrypoint,
  conformance suite, or catalog manifest is maintained as an authoritative copy
  in this repository.
- [x] Catalog-freezing tooling, workflow language, and tests are removed or
  replaced with Template Release equivalents.
- [x] A Template Release manifest records the Template repository commit,
  Team Template digest, pinned Runner commit and package version, catalog
  identity, Advisory Validation workflow identity, and supported template
  version.
- [x] Release creation and verification reject a dirty tree, mutable references,
  mismatched catalog lock, changed Team Template, or incorrect annotated tag.
- [x] Team branch creation, Team guidance, submission cutoff, and Advisory
  Validation point at the Template Release rather than a catalog tag owned here.
- [x] Repository tests prove there is no second catalog source tree.

## Comments

The materialized Runner checkout is a verified dependency cache, not a second
source of catalog authority.

## Answer

The duplicate `language_environments/` tree, catalog-freezing command, Catalog
Release workflow and runbook, and catalog-authority tests are removed. The
repository now contains only the participant-facing Team Template and consumes
the exact catalog materialized from its content-verified Runner bundle. A guard
test proves that neither the catalog tree nor the retired authority files exist.

`release-team-template` creates and verifies an annotated Template Release tag.
Its manifest binds the exact Template repository commit, deterministic Team
Template tree digest, complete `core-tool.lock.json` compatibility claim,
supported template version, and Advisory Validation workflow identity. Tests
prove that dirty trees, mutable actions, lock/catalog mismatches, changed starter
contents, wrong tag targets, and lightweight tags fail closed.

The release runbook and Team guide create branches from the dereferenced
Template Release tag. GitHub Advisory Validation verifies that release and the
Team-only editing boundary, then retains the release manifest and identities in
commit-specific evidence. The submission cutoff and cross-platform proof now
reconcile the selected source with the same Template Release. The full 43-test
suite and Python 3.9 compilation pass; two-axis review found no spec gaps, and
its one domain-vocabulary finding was corrected.
