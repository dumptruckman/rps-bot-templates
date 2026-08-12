# Add the Java Team Template

Status: resolved

Blocked by: 04; rps-tournament multi-language-environments 04

## Parent

[Multi-language Team Templates](../PRD.md)

## What to build

Deliver an independently releasable Java Team Template with equivalent strategy,
build, test, native-development, Docker-development, and Runner compatibility
behavior.

## Acceptance criteria

- [x] The Java toolchain is the latest upstream-supported LTS release at
  preparation time and is pinned immutably in the matching Catalog and Template
  Releases.
- [x] The Java starter implements the common strategy contract and includes
  deterministic unit tests for legal moves and seeded behavior.
- [x] One Java-owned script builds and tests the starter with a compatible local
  Java toolchain.
- [x] Docker invokes that identical Java-owned script and passes the complete
  build and unit-test suite without Java installed on the host.
- [x] Advisory Validation consumes the matching Java Language Environment from
  the exact pinned Catalog Release and passes its complete conformance contract.
- [x] Java guidance documents Team Source boundaries, native prerequisites,
  Docker usage, and the distinction between Advisory and Final Validation.
- [x] Java can be selected, checked, and released without changing another Team
  Template's descriptor or release identity.

## Answer

Added `java-team-template-v1` as an independently selectable Team Template with
the immutable `java-template-v1` Template Release identity. Its controlled Team
Source implements the common `Strategy.chooseMove` contract using the
wrapper-provided `RandomGenerator`, and its standard-library-only test harness
proves legal moves and deterministic behavior for the same bot-visible seed.
The Java-owned `build-and-test` entrypoint compiles every Team Source `.java`
file and runs the complete tests both natively and in the exact pinned Docker
JDK.

The compatibility lock now consumes Runner commit
`098a5cfc8bbf562ff5a6c1781d0b3c1e147185d8`, Catalog Release `catalog-v4`,
and Catalog identity
`rps-language-environment-catalog-v1@sha256:e90ce9d6e5eaad43451a7647ac25fa4623f2daf266f09c29eb3ce180be606801`.
Complete participant-local Advisory Validation passed source freezing, build,
the Java conformance suite, determinism, isolation, lifecycle, and a Practice
Match on native Linux/ARM64. The independently addressable Template Release
was created and verified without changing the Python or Go descriptors or
release identities; all 83 repository tests passed with 2 expected opt-in
integration skips.
