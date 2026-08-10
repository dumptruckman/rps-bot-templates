# Validate every Team commit on native AMD64

Status: resolved

Blocked by: 03

## What to build

Give every pushed Team commit an automatic GitHub check that runs the same
pinned conformance suite on native Linux/AMD64 and leaves durable,
commit-specific eligibility evidence without publishing a Bot Artifact.

## Acceptance criteria

- [x] The workflow runs on Team branch commits, checks out the exact commit, installs the immutable core-tool pin, and validates against the frozen repository-owned catalog.
- [x] It builds only `linux/amd64`, invokes `github-advisory` authority, and never uses QEMU, creates a multi-platform image, or pushes an image to a registry.
- [x] Workflow permissions are read-only and minimal, no repository or deployment secret is exposed to Team Source, and untrusted Team code receives no privileged Docker or repository authority beyond the conformance contract.
- [x] Superseded work on the same Team branch is cancelled without erasing the latest completed green candidate.
- [x] The durable result identifies the exact source commit, Source Digest, catalog, core tool, suite, recipe, wrapper, runtime digest, platform, disposable image identity, execution profile, and pass or fail result.
- [x] A practice Match's score or winner cannot fail an otherwise conforming Submission Candidate.

## Answer

Added the `Team Advisory Validation` workflow for every `team/**` push. It
checks out the pushed commit and immutable core pin without persisted
credentials, asserts a native Linux/AMD64 Docker server, and delegates source
freezing, one-platform building, and `github-advisory` conformance to the pinned
core. Branch-scoped concurrency cancels superseded work.

Every completed run retains a 90-day, commit-named evidence artifact containing
the pass/fail result and all available frozen identities; identities whose
producing stage could not run are marked explicitly. Only the eligibility record
and conformance report are uploaded—the disposable image is removed and no Bot
Artifact is published. The job gates on that evidence result, while the pinned
suite keeps practice Match score and winner non-gating. Contract tests cover the
workflow, its authority boundaries, evidence, cancellation, and Team guide.
