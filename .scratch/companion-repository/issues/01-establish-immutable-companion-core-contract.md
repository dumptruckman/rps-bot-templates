# Establish the immutable companion-to-core contract

Status: resolved

Blocked by: None

## What to build

Make this repository the event-facing source of truth for the Python Language
Environment while consuming the Tournament repository's generic validation and
build tooling through an immutable pin. A maintainer can change a catalog asset
or core pin intentionally and immediately see whether the two repositories still
satisfy their shared consumer contract.

## Acceptance criteria

- [x] The repository declares an immutable core-tool version or commit and an explicit Language Environment Catalog version; no workflow resolves a mutable branch or `latest` value.
- [x] The Python Language Environment includes its Team Source schema, template, platform-specific runtime digests, networkless build recipe, wrapper, Seed Adapter, readiness contract, fixed entrypoint, dependency policy, and conformance fixtures.
- [x] The pinned core tool loads and content-verifies the repository-owned catalog without repository-specific changes to Tournament scheduling, scoring, state, storage, or projection behavior.
- [x] Automated contract coverage fails on stale asset digests, missing versions, changed participant contracts, or drift between a core fixture and this repository's authoritative catalog.
- [x] The ownership boundary clearly identifies this repository as catalog authority and `rps-tournament` as authority for generic validation, building, certification, execution, and official Tournament operation.

## Answer

Added the versioned Python Language Environment Catalog and complete organizer-
owned package, locked the generic Tournament core at commit
`ba9242ed46023a237f76e82d1296e8af706fd48c`, and added an immutable GitHub
contract workflow. The contract suite exercises the pinned core's public catalog
and Team Source boundary, verifies every asset digest and required version,
protects the participant contract, and compares the repository-owned generic
fixture with the pinned core fixture. The README records the ownership boundary
and maintainer verification procedure.
