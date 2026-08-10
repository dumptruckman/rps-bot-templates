# Prove the AMD64 signal against canonical ARM64 validation

Status: resolved

Blocked by: 04

## What to build

Demonstrate that one selected Python Submission Candidate can pass advisory
validation on native AMD64 and Final Validation on native ARM64 through the same
catalog and suite, while preserving architecture-specific runtime, image, and
validation identities.

## Acceptance criteria

- [x] The same frozen Team Source and Language Environment assets exercise build, wrapper readiness, protocol version 1, Seed Adapter determinism, isolation, resource limits, lifecycle, and practice-Match conformance on both native platforms.
- [x] The GitHub lane produces a disposable single-platform AMD64 confidence image, and the organizer lane produces the canonical single-platform ARM64 Bot Artifact.
- [x] Cross-platform evidence compares source compatibility and contract behavior without requiring equal runtime digests, image digests, or language-native random streams.
- [x] The acceptance path uses no QEMU, multi-platform build, combined OCI index, remote registry for Bot Artifact images, or GitHub-built image in the official roster.
- [x] The retained evidence is sufficient to diagnose a rare architecture-specific failure and drive the documented compatibility-only repair policy.

## Answer

Added an organizer-owned `prove-amd64-against-arm64` command that consumes the
selected commit's retained GitHub Advisory Validation evidence and exact
exported Team Source, verifies the pinned core and a native ARM64 Docker server,
then freezes, builds, and Final Validates one new single-platform ARM64 Bot
Artifact. The command never imports the disposable GitHub image or invokes a
registry, emulation, or multi-platform build path.

The resulting proof compares the Source Digest, frozen Language Environment
identities, and every conformance check while retaining AMD64 and ARM64 runtime,
image, and validation identities separately. Per-stage logs, partial outputs,
the source bundle, build diagnostics, both validation records, and the canonical
Bot Artifact Manifest remain available for architecture-specific diagnosis and
the documented compatibility-only repair process. The acceptance runbook and
contract tests document and enforce those boundaries.

GitHub run `31354054919` passed Advisory Validation for selected commit
`5b754ee8bf3ea3166eeade9b6a53b80751739078` on native Linux/AMD64. Its
catalog-pinned base runtime was fetched by digest, its disposable confidence
image was removed, and no Bot Artifact image entered a registry. The same Team
Source Digest then passed organizer Final Validation on native Linux/ARM64.

The retained proof records shared Source Digest, catalog, suite, wrapper,
recipe, entrypoint, execution profile, core tool, and every contract check. It
keeps the AMD64 and ARM64 runtime, image, and validation identities distinct.
The complete audit evidence is under
`.scratch/companion-repository/evidence/native-platform-proof-5b754ee8/`.
