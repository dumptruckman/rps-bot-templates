# Add the JavaScript Team Template

Status: ready-for-agent

Blocked by: 04; rps-tournament multi-language-environments 10

## Parent

[Multi-language Team Templates](../PRD.md)

## What to build

Deliver an independently releasable JavaScript Team Template with equivalent
strategy, build, test, native-development, Docker-development, and Runner
compatibility behavior.

## Acceptance criteria

- [ ] JavaScript uses the latest upstream-supported Node.js LTS at preparation
  time and is pinned immutably in the matching Catalog and Template Releases.
- [ ] The JavaScript starter implements the common strategy contract and
  includes deterministic unit tests for legal moves and seeded behavior.
- [ ] One JavaScript-owned script builds and tests the starter with a compatible
  local Node.js toolchain.
- [ ] Docker invokes that identical JavaScript-owned script and passes the
  complete build and unit-test suite without Node.js installed on the host.
- [ ] Dependency resolution is deterministic and complies with the matching
  Language Environment's networkless build policy.
- [ ] Advisory Validation consumes the matching JavaScript Language Environment
  from the exact pinned Catalog Release and passes its complete conformance
  contract.
- [ ] JavaScript guidance documents Team Source boundaries, native
  prerequisites, Docker usage, and the distinction between Advisory and Final
  Validation.
- [ ] JavaScript can be selected, checked, and released without changing another
  Team Template's descriptor or release identity.
