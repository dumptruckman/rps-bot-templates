# Freeze and release the first Tournament Language Environment Catalog

Status: resolved

Blocked by: 05, 06

## What to build

Publish a clean, immutable repository release that Teams can branch from and the
organizer can cite for one Tournament, with every template, workflow, catalog asset,
core-tool pin, and validation identity frozen together.

## Acceptance criteria

- [x] A clean clone can create a Team branch, validate the starter strategy locally or through GitHub, and reproduce the documented advisory evidence without unpublished files or maintainer state.
- [x] The release records the exact repository commit, catalog identity, core-tool pin, conformance-suite identity, execution-profile identity, wrapper and recipe versions, and both platform-specific runtime digests.
- [x] The release process verifies catalog content digests and rejects mutable core, runtime, action, or dependency references.
- [x] The released Python environment uses only the standard library and organizer-pinned contents; neither Team-local nor GitHub Advisory Validation requires build-time package downloads.
- [x] The release notes preserve the distinction between a Submission Candidate, a disposable advisory image, and the canonical organizer-built Bot Artifact.
- [x] A maintainer checklist freezes the catalog before coding begins and prohibits routine catalog, wrapper, recipe, base-image, or conformance changes until the Tournament completes.

## Answer

Added an organizer-owned Language Environment Catalog release command that
content-verifies every catalog asset through the pinned core, rejects mutable
core, runtime, action, and dependency inputs, and records the complete frozen
identity set in the JSON annotation of an exact-commit Git tag. The tag-based record avoids the
self-reference that would result from trying to store a commit's own SHA inside
a file in that commit.

The release runbook supplies the pre-coding maintainer checklist, clean-clone
Team branch and Advisory Validation reproduction path, standard-library-only
and no-download guarantees, until-completion change freeze, infrastructure-
correction policy, and explicit authority distinction among a Submission
Candidate, disposable advisory image, and canonical organizer-built Bot
Artifact. The Catalog contract workflow re-verifies published release tags, and
contract tests cover the required identities and every mutable-input rejection.

The release also carries a content-addressed Git bundle containing the complete
history needed to materialize the exact private core-tool commit without a
cross-repository credential, package download, or maintainer checkout. Team-
local and active GitHub workflows use the same bundled pin; the release process
records and verifies its SHA-256 digest with the core commit and package version.
