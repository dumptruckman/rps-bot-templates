# Freeze and release the first event catalog

Status: ready-for-agent

Blocked by: 05, 06

## What to build

Publish a clean, immutable repository release that Teams can branch from and the
organizer can cite for one event, with every template, workflow, catalog asset,
core-tool pin, and validation identity frozen together.

## Acceptance criteria

- [ ] A clean clone can create a Team branch, validate the starter strategy locally or through GitHub, and reproduce the documented advisory evidence without unpublished files or maintainer state.
- [ ] The release records the exact repository commit, catalog identity, core-tool pin, conformance-suite identity, execution-profile identity, wrapper and recipe versions, and both platform-specific runtime digests.
- [ ] The release process verifies catalog content digests and rejects mutable core, runtime, action, or dependency references.
- [ ] The released Python environment uses only the standard library and organizer-pinned contents; neither participant nor GitHub validation requires build-time package downloads.
- [ ] The release notes preserve the distinction between a Submission Candidate, a disposable advisory image, and the canonical organizer-built Bot Artifact.
- [ ] A maintainer checklist freezes the catalog before coding begins and prohibits routine catalog, wrapper, recipe, base-image, or conformance changes until the event completes.
