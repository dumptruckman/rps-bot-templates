# Prove the AMD64 signal against canonical ARM64 validation

Status: ready-for-human

Blocked by: 04

## What to build

Demonstrate that one selected Python Submission Candidate can pass advisory
validation on native AMD64 and Final Validation on native ARM64 through the same
catalog and suite, while preserving architecture-specific runtime, image, and
validation identities.

## Acceptance criteria

- [ ] The same frozen Team Source and Language Environment assets exercise build, wrapper readiness, protocol version 1, Seed Adapter determinism, isolation, resource limits, lifecycle, and practice-Match conformance on both native platforms.
- [ ] The GitHub lane produces a disposable single-platform AMD64 confidence image, and the organizer lane produces the canonical single-platform ARM64 Bot Artifact.
- [ ] Cross-platform evidence compares source compatibility and contract behavior without requiring equal runtime digests, image digests, or language-native random streams.
- [ ] The acceptance path uses no QEMU, multi-platform build, combined OCI index, remote registry, or GitHub-built image in the official roster.
- [ ] The retained evidence is sufficient to diagnose a rare architecture-specific failure and drive the documented compatibility-only repair policy.

## Implementation status

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

The native ARM64 organizer lane passed locally for the starter Team Source. A
genuine cross-platform proof cannot be retained until the eight predecessor
commits and this workflow are published to GitHub, one `team/**` commit produces
native AMD64 evidence, and that exact selected Team Source is run through this
command. Publishing branches and starting that external run require maintainer
authorization, so the ticket remains open rather than claiming synthetic proof.
