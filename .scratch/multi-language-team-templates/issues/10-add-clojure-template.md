# Add the Clojure Team Template

Status: ready-for-agent

Blocked by: 04; rps-tournament multi-language-environments 09

## Parent

[Multi-language Team Templates](../PRD.md)

## What to build

Deliver an independently releasable Clojure Team Template with equivalent
strategy, build, test, native-development, Docker-development, and Runner
compatibility behavior.

## Acceptance criteria

- [ ] Clojure uses the latest upstream-supported stable release and a compatible
  upstream-supported Java LTS at preparation time, pinned immutably in the
  matching Catalog and Template Releases.
- [ ] The Clojure starter implements the common strategy contract and includes
  deterministic unit tests for legal moves and seeded behavior.
- [ ] One Clojure-owned script builds and tests the starter with a compatible
  local Clojure and Java toolchain.
- [ ] Docker invokes that identical Clojure-owned script and passes the complete
  build and unit-test suite without Clojure or Java installed on the host.
- [ ] Dependency resolution is deterministic and complies with the matching
  Language Environment's networkless build policy.
- [ ] Advisory Validation consumes the matching Clojure Language Environment
  from the exact pinned Catalog Release and passes its complete conformance
  contract.
- [ ] Clojure guidance documents Team Source boundaries, native prerequisites,
  Docker usage, and the distinction between Advisory and Final Validation.
- [ ] Clojure can be selected, checked, and released without changing another
  Team Template's descriptor or release identity.
