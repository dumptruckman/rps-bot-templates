# Prove the AMD64 signal against canonical ARM64 validation

Status: ready-for-agent

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
