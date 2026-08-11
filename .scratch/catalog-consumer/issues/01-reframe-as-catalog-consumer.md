# Reframe the Template repository as a catalog consumer

Status: resolved

Priority: 2

Blocked by: rps-tournament catalog-authority 01

## Parent

[Consume the Runner-owned catalog](../PRD.md)

## What to build

Define the Template repository's participant-facing authority and the immutable
lock through which it consumes a Runner-owned Language Environment Catalog.
Maintainers and Teams should be able to tell which facts belong to a Template
Release and which belong to the catalog release it pins.

## Acceptance criteria

- [x] Repository language says Team Templates and Team guidance are authoritative
  here, while the Language Environment Catalog and organizer-owned execution
  assets are authoritative in `rps-tournament`.
- [x] The domain language distinguishes Language Environment, Team Template,
  Template Release, catalog release, Advisory Validation, and Final Validation.
- [x] The core lock records a full Runner commit, package version, catalog path
  and identity, and offline bundle identity without mutable references.
- [x] The lock identifies one published Runner catalog release and rejects a
  mismatched materialized checkout.
- [x] Team-editable and organizer-owned paths remain unmistakably separate.

## Comments

This ticket changes the declared interface before the duplicate catalog is
removed.

## Answer

`core-tool.lock.json` now carries the complete immutable catalog compatibility
claim: exact Runner commit, package version, catalog path and
identity, catalog asset identities, and versioned offline-bundle identity. The
materializer consumes the new lock shape and rejects an existing destination
that is not the locked clean Runner checkout.

The glossary, accepted ADR, repository overview, compatibility contract, Team
guide, and legacy catalog-release notice establish the one-way authority:
participant-facing Team Templates and guidance belong here; the Catalog Release
and all organizer-controlled execution assets belong to `rps-tournament`.
`team_source/` remains the only Team-editable path. The duplicate catalog is
explicitly transitional and non-authoritative pending the later cutover ticket.

Contract tests cover the lock coordinates against the materialized Runner,
offline bundle identity, mismatched-checkout rejection, domain terms, and
repository boundaries. The full 42-test suite passes on Python 3.9.6.
