# Reframe the Template repository as a catalog consumer

Status: ready-for-agent

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

- [ ] Repository language says Team Templates and Team guidance are authoritative
  here, while the Language Environment Catalog and organizer-owned execution
  assets are authoritative in `rps-tournament`.
- [ ] The domain language distinguishes Language Environment, Team Template,
  Template Release, catalog release, Advisory Validation, and Final Validation.
- [ ] The core lock records a full Runner commit, package version, catalog path
  and identity, and offline bundle identity without mutable references.
- [ ] The lock identifies one published Runner catalog release and rejects a
  mismatched materialized checkout.
- [ ] Team-editable and organizer-owned paths remain unmistakably separate.

## Comments

This ticket changes the declared interface before the duplicate catalog is
removed.
