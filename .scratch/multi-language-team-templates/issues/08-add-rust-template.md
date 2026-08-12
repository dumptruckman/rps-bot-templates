# Add the optional Rust Team Template

Status: ready-for-agent

Blocked by: 04; rps-tournament multi-language-environments 07

## Parent

[Multi-language Team Templates](../PRD.md)

## What to build

Deliver Rust as an optional independently releasable Team Template, without
lowering the build, test, native-development, Docker-development, or Runner
compatibility bar used by required languages.

## Acceptance criteria

- [ ] The Rust toolchain is the latest upstream-supported stable release at
  preparation time and is pinned immutably in the matching Catalog and Template
  Releases.
- [ ] The Rust starter implements the common strategy contract and includes
  deterministic unit tests for legal moves and seeded behavior.
- [ ] One Rust-owned script builds and tests the starter with a compatible local
  Rust toolchain.
- [ ] Docker invokes that identical Rust-owned script and passes the complete
  build and unit-test suite without Rust installed on the host.
- [ ] Dependency resolution is deterministic and complies with the matching
  Language Environment's networkless build policy.
- [ ] Advisory Validation consumes the matching Rust Language Environment from
  the exact pinned Catalog Release and passes its complete conformance contract.
- [ ] Rust guidance documents Team Source boundaries, native prerequisites,
  Docker usage, and the distinction between Advisory and Final Validation.
- [ ] Rust is advertised as supported only after meeting every required-language
  conformance and release criterion.
