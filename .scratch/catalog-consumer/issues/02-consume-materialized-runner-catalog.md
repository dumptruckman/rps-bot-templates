# Consume the materialized Runner catalog

Status: resolved

Priority: 2

Blocked by: 01; rps-tournament catalog-authority 02

## Parent

[Consume the Runner-owned catalog](../PRD.md)

## What to build

Make local and GitHub Advisory Validation use the exact catalog inside the
materialized, content-verified Runner checkout. The unchanged Team Template
should pass without consulting this repository's duplicate catalog tree.

## Acceptance criteria

- [x] Materialization verifies the offline bundle checksum, exact Runner commit,
  package version, catalog path, and catalog identity before validation begins.
- [x] Team Source validation, wrapper smoke tests, Advisory Validation, and
  cross-platform proof all consume the materialized Runner catalog.
- [x] Local and GitHub workflows use only full immutable action, runtime, core,
  and catalog references.
- [x] A missing, corrupt, stale, or identity-mismatched materialized catalog
  fails with an organizer-actionable diagnostic.
- [x] A clean clone can materialize and validate the starter Team Source without
  network access after the pinned bundle and runtime are present.
- [x] Compatibility tests prove the Team Template satisfies the catalog's public
  Team Source contract without asserting equality to a catalog-owned template.

## Comments

Keep the old catalog copy temporarily during this expand step, but prove no
active validation path reads it.

## Answer

`catalog_compatibility.py` now verifies the complete immutable Catalog Release
claim: offline bundle bytes, clean Runner commit, package version, safe catalog
path, canonical catalog identity, and the exact content identity of every
catalog asset. `materialize-core-tool` applies that verification before exposing
the checkout and reports coordinate-specific organizer repair guidance for
missing, corrupt, stale, or mismatched inputs.

Local Advisory Validation, GitHub Advisory Validation, wrapper and Team Source
compatibility tests, and the native cross-platform proof now derive their
catalog exclusively from the materialized Runner. A guard test proves none of
those active paths names the transitional local catalog. The Team Template is
tested through the public callable, wrapper, and source-schema contracts without
asserting equality to a Runner-owned starter file.

The full 45-test suite and Python 3.9 compilation pass. Two-axis review found no
remaining repository-standards or ticket-spec findings.
