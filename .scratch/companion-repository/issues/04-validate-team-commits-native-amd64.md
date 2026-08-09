# Validate every Team commit on native AMD64

Status: ready-for-agent

Blocked by: 03

## What to build

Give every pushed Team commit an automatic GitHub check that runs the same
pinned conformance suite on native Linux/AMD64 and leaves durable,
commit-specific eligibility evidence without publishing a Bot Artifact.

## Acceptance criteria

- [ ] The workflow runs on Team branch commits, checks out the exact commit, installs the immutable core-tool pin, and validates against the frozen repository-owned catalog.
- [ ] It builds only `linux/amd64`, invokes `github-advisory` authority, and never uses QEMU, creates a multi-platform image, or pushes an image to a registry.
- [ ] Workflow permissions are read-only and minimal, no repository or deployment secret is exposed to Team Source, and untrusted Team code receives no privileged Docker or repository authority beyond the conformance contract.
- [ ] Superseded work on the same Team branch is cancelled without erasing the latest completed green candidate.
- [ ] The durable result identifies the exact source commit, Source Digest, catalog, core tool, suite, recipe, wrapper, runtime digest, platform, disposable image identity, execution profile, and pass or fail result.
- [ ] A practice Match's score or winner cannot fail an otherwise conforming Submission Candidate.
