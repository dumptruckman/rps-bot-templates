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

The native ARM64 organizer lane passed locally for the starter Team Source. The
temporary `team/native-platform-proof` branch was published at commit
`00e34711cf59c2396ccdfac13bec54449a8e697b`, but GitHub run `31351896384`
stopped before validation because the pinned `dumptruckman/rps-bot-tournament`
repository is intentionally private. A repository-scoped `GITHUB_TOKEN` cannot
read that separate private repository, and a Team-controlled workflow must not
receive a broader PAT or deploy credential.

The maintainer will publish the core repository shortly before the work
Tournament. At that point, rerun the temporary branch's `Team Advisory
Validation`, download its genuine native AMD64 evidence, and pass the same
selected Team Source through this command on native ARM64. Until then, the
ticket remains open rather than claiming synthetic cross-platform proof.
