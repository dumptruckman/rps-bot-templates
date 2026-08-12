# Add the Go Team Template tracer bullet

Status: resolved

Blocked by: 03; rps-tournament multi-language-environments 03

## Parent

[Multi-language Team Templates](../PRD.md)

## What to build

Deliver Go as the first genuinely new Team Template, proving that the collection,
independent release, shared native/Docker script, and Runner compatibility seams
work beyond migrated Python.

## Acceptance criteria

- [x] The selected Go toolchain is the latest upstream-supported stable release
  at preparation time and is pinned immutably in the matching Catalog and
  Template Releases.
- [x] The Go starter implements the common strategy contract and includes
  deterministic unit tests for legal moves and seeded behavior.
- [x] One Go-owned script builds and tests the starter with a compatible local Go
  toolchain.
- [x] Docker invokes that identical Go-owned script and passes the complete build
  and unit-test suite without Go installed on the host.
- [x] Advisory Validation consumes the matching Go Language Environment from the
  exact pinned Catalog Release and passes its complete conformance contract.
- [x] Go guidance documents Team Source boundaries, native prerequisites, Docker
  usage, and the distinction between Advisory and Final Validation.
- [x] Go can be selected, checked, and released without changing Python's
  descriptor or release identity.
- [x] Discoveries that affect every language are incorporated into the shared
  collection contract and tests before later language tickets start.

## Answer

Added `go-team-template-v1` as an independently selectable Team Template with
the immutable `go-template-v1` release identity. Its Team Source implements the
common `ChooseMove` contract, and its Go-owned `build-and-test` entrypoint
compiles the complete Team Source tree and runs deterministic legal-move and
seeded-behavior tests. The Runner-owned conformance suite verifies the published
Seed Adapter golden vectors.

The compatibility lock now consumes Runner commit
`1380c98118153172331b141c3539dfb37da601db` and Catalog identity
`rps-language-environment-catalog-v1@sha256:9e78f85567c3ae4152bae4dec378643e3bf5572a0602ab7599b8bb486ce93ee8`,
which pins Go 1.26.5 independently for Linux/AMD64 and Linux/ARM64. The exact
Linux/ARM64 toolchain ran the identical Go entrypoint in Docker, and complete
participant-local Advisory Validation passed source freezing, build,
conformance, determinism, isolation, lifecycle, and Practice Match checks.

The first compiled-language template exposed two shared Docker-workspace
assumptions: 64 MiB was insufficient for Go compilation, and a `noexec` tmpfs
could not run the compiled test binary. The collection checker now provides an
ephemeral, networkless, executable 512 MiB tmpfs while retaining a read-only
repository mount; regression coverage records that cross-language contract.
