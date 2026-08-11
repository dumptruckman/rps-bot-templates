# Consume the materialized Runner catalog

Status: ready-for-agent

Priority: 2

Blocked by: 01; rps-tournament catalog-authority 02

## Parent

[Consume the Runner-owned catalog](../PRD.md)

## What to build

Make local and GitHub Advisory Validation use the exact catalog inside the
materialized, content-verified Runner checkout. The unchanged Team Template
should pass without consulting this repository's duplicate catalog tree.

## Acceptance criteria

- [ ] Materialization verifies the offline bundle checksum, exact Runner commit,
  package version, catalog path, and catalog identity before validation begins.
- [ ] Team Source validation, wrapper smoke tests, Advisory Validation, and
  cross-platform proof all consume the materialized Runner catalog.
- [ ] Local and GitHub workflows use only full immutable action, runtime, core,
  and catalog references.
- [ ] A missing, corrupt, stale, or identity-mismatched materialized catalog
  fails with an organizer-actionable diagnostic.
- [ ] A clean clone can materialize and validate the starter Team Source without
  network access after the pinned bundle and runtime are present.
- [ ] Compatibility tests prove the Team Template satisfies the catalog's public
  Team Source contract without asserting equality to a catalog-owned template.

## Comments

Keep the old catalog copy temporarily during this expand step, but prove no
active validation path reads it.
