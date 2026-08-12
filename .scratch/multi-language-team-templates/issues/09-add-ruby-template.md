# Add the Ruby Team Template

Status: ready-for-agent

Blocked by: 04; rps-tournament multi-language-environments 08

## Parent

[Multi-language Team Templates](../PRD.md)

## What to build

Deliver an independently releasable Ruby Team Template with equivalent
strategy, build, test, native-development, Docker-development, and Runner
compatibility behavior.

## Acceptance criteria

- [ ] Ruby uses the latest upstream-supported stable release at preparation time
  and is pinned immutably in the matching Catalog and Template Releases.
- [ ] The Ruby starter implements the common strategy contract and includes
  deterministic unit tests for legal moves and seeded behavior.
- [ ] One Ruby-owned script builds and tests the starter with a compatible local
  Ruby toolchain.
- [ ] Docker invokes that identical Ruby-owned script and passes the complete
  build and unit-test suite without Ruby installed on the host.
- [ ] Dependency resolution is deterministic and complies with the matching
  Language Environment's networkless build policy.
- [ ] Advisory Validation consumes the matching Ruby Language Environment from
  the exact pinned Catalog Release and passes its complete conformance contract.
- [ ] Ruby guidance documents Team Source boundaries, native prerequisites,
  Docker usage, and the distinction between Advisory and Final Validation.
- [ ] Ruby can be selected, checked, and released without changing another Team
  Template's descriptor or release identity.
