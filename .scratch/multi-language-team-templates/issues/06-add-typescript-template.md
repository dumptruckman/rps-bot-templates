# Add the TypeScript Team Template

Status: resolved

Blocked by: 04; rps-tournament multi-language-environments 05

## Parent

[Multi-language Team Templates](../PRD.md)

## What to build

Deliver an independently releasable TypeScript Team Template with equivalent
strategy, build, test, native-development, Docker-development, and Runner
compatibility behavior.

## Acceptance criteria

- [x] The toolchain uses the latest upstream-supported Node.js LTS release and an
  exactly pinned compatible stable TypeScript compiler at preparation time, with
  immutable Catalog and Template Release identities.
- [x] The TypeScript starter implements the common strategy contract and includes
  deterministic unit tests for legal moves and seeded behavior.
- [x] One TypeScript-owned script builds and tests the starter with compatible
  local Node.js and TypeScript tools.
- [x] Docker invokes that identical TypeScript-owned script and passes the
  complete build and unit-test suite without Node.js or TypeScript installed on
  the host.
- [x] Dependency installation is deterministic and complies with the matching
  Language Environment's networkless build policy.
- [x] Advisory Validation consumes the matching TypeScript Language Environment
  from the exact pinned Catalog Release and passes its complete conformance
  contract.
- [x] TypeScript guidance documents Team Source boundaries, native prerequisites,
  Docker usage, and the distinction between Advisory and Final Validation.
- [x] TypeScript can be selected, checked, and released without changing another
  Team Template's descriptor or release identity.

## Answer

Added an independently selectable TypeScript Team Template pinned to the exact
`catalog-v5` Runner release. The starter implements the common `chooseMove`
contract, deterministic legal-move and same-seed unit tests, and one
TypeScript-owned `build-and-test` script. Native mode requires compatible
Node.js plus exactly TypeScript 6.0.3; Docker invokes the identical script with
networking disabled, the immutable Node.js 24.19.0 toolchain image, and the
catalog-owned checksummed compiler archive.

The pinned Docker suite passed without TypeScript installed on the host, and
complete participant-local Advisory Validation passed source freezing,
networkless artifact build, readiness, protocol, determinism, diagnostics,
resource/isolation checks, and a Practice Match. Guidance documents Team Source
ownership, both development modes, and the Advisory/Final Validation authority
boundary. The template has its own descriptor, source identity, version, and
`typescript-template-v1` release tag without changing another template's
release identity.
