# Establish the immutable companion-to-core contract

Status: ready-for-agent

Blocked by: None

## What to build

Make this repository the event-facing source of truth for the Python Language
Environment while consuming the Tournament repository's generic validation and
build tooling through an immutable pin. A maintainer can change a catalog asset
or core pin intentionally and immediately see whether the two repositories still
satisfy their shared consumer contract.

## Acceptance criteria

- [ ] The repository declares an immutable core-tool version or commit and an explicit Language Environment Catalog version; no workflow resolves a mutable branch or `latest` value.
- [ ] The Python Language Environment includes its Team Source schema, template, platform-specific runtime digests, networkless build recipe, wrapper, Seed Adapter, readiness contract, fixed entrypoint, dependency policy, and conformance fixtures.
- [ ] The pinned core tool loads and content-verifies the repository-owned catalog without repository-specific changes to Tournament scheduling, scoring, state, storage, or projection behavior.
- [ ] Automated contract coverage fails on stale asset digests, missing versions, changed participant contracts, or drift between a core fixture and this repository's authoritative catalog.
- [ ] The ownership boundary clearly identifies this repository as catalog authority and `rps-tournament` as authority for generic validation, building, certification, execution, and official Tournament operation.
