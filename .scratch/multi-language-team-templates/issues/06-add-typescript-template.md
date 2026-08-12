# Add the TypeScript Team Template

Status: ready-for-agent

Blocked by: 04; rps-tournament multi-language-environments 05

## Parent

[Multi-language Team Templates](../PRD.md)

## What to build

Deliver an independently releasable TypeScript Team Template with equivalent
strategy, build, test, native-development, Docker-development, and Runner
compatibility behavior.

## Acceptance criteria

- [ ] The toolchain uses the latest upstream-supported Node.js LTS release and an
  exactly pinned compatible stable TypeScript compiler at preparation time, with
  immutable Catalog and Template Release identities.
- [ ] The TypeScript starter implements the common strategy contract and includes
  deterministic unit tests for legal moves and seeded behavior.
- [ ] One TypeScript-owned script builds and tests the starter with compatible
  local Node.js and TypeScript tools.
- [ ] Docker invokes that identical TypeScript-owned script and passes the
  complete build and unit-test suite without Node.js or TypeScript installed on
  the host.
- [ ] Dependency installation is deterministic and complies with the matching
  Language Environment's networkless build policy.
- [ ] Advisory Validation consumes the matching TypeScript Language Environment
  from the exact pinned Catalog Release and passes its complete conformance
  contract.
- [ ] TypeScript guidance documents Team Source boundaries, native prerequisites,
  Docker usage, and the distinction between Advisory and Final Validation.
- [ ] TypeScript can be selected, checked, and released without changing another
  Team Template's descriptor or release identity.
