# Add the Java Team Template

Status: ready-for-agent

Blocked by: 04; rps-tournament multi-language-environments 04

## Parent

[Multi-language Team Templates](../PRD.md)

## What to build

Deliver an independently releasable Java Team Template with equivalent strategy,
build, test, native-development, Docker-development, and Runner compatibility
behavior.

## Acceptance criteria

- [ ] The Java toolchain is the latest upstream-supported LTS release at
  preparation time and is pinned immutably in the matching Catalog and Template
  Releases.
- [ ] The Java starter implements the common strategy contract and includes
  deterministic unit tests for legal moves and seeded behavior.
- [ ] One Java-owned script builds and tests the starter with a compatible local
  Java toolchain.
- [ ] Docker invokes that identical Java-owned script and passes the complete
  build and unit-test suite without Java installed on the host.
- [ ] Advisory Validation consumes the matching Java Language Environment from
  the exact pinned Catalog Release and passes its complete conformance contract.
- [ ] Java guidance documents Team Source boundaries, native prerequisites,
  Docker usage, and the distinction between Advisory and Final Validation.
- [ ] Java can be selected, checked, and released without changing another Team
  Template's descriptor or release identity.
