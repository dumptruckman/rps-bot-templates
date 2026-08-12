# Add the Go Team Template tracer bullet

Status: ready-for-agent

Blocked by: 03; rps-tournament multi-language-environments 03

## Parent

[Multi-language Team Templates](../PRD.md)

## What to build

Deliver Go as the first genuinely new Team Template, proving that the collection,
independent release, shared native/Docker script, and Runner compatibility seams
work beyond migrated Python.

## Acceptance criteria

- [ ] The selected Go toolchain is the latest upstream-supported stable release
  at preparation time and is pinned immutably in the matching Catalog and
  Template Releases.
- [ ] The Go starter implements the common strategy contract and includes
  deterministic unit tests for legal moves and seeded behavior.
- [ ] One Go-owned script builds and tests the starter with a compatible local Go
  toolchain.
- [ ] Docker invokes that identical Go-owned script and passes the complete build
  and unit-test suite without Go installed on the host.
- [ ] Advisory Validation consumes the matching Go Language Environment from the
  exact pinned Catalog Release and passes its complete conformance contract.
- [ ] Go guidance documents Team Source boundaries, native prerequisites, Docker
  usage, and the distinction between Advisory and Final Validation.
- [ ] Go can be selected, checked, and released without changing Python's
  descriptor or release identity.
- [ ] Discoveries that affect every language are incorporated into the shared
  collection contract and tests before later language tickets start.
