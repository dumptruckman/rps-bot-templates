# Tickets: Team-facing Bot template repository

Build the shared Team repository described by the Containerized Bot Build and
Execution PRD and its post-container follow-up tickets in `rps-tournament`,
using core contract evidence from commit `ba9242e`.

Work the **frontier**: any ticket whose blockers are all done.

## Establish the immutable companion-to-core contract

**What to build:** Make this repository the event-facing source of truth for the
Python Language Environment while consuming the Tournament repository's generic
validation and build tooling through an immutable pin. A maintainer can change a
catalog asset or core pin intentionally and immediately see whether the two
repositories still satisfy their shared consumer contract.

**Blocked by:** None — can start immediately.

- [ ] The repository declares an immutable core-tool version or commit and an explicit Language Environment Catalog version; no workflow resolves a mutable branch or `latest` value.
- [ ] The Python Language Environment includes its Team Source schema, template, platform-specific runtime digests, networkless build recipe, wrapper, Seed Adapter, readiness contract, fixed entrypoint, dependency policy, and conformance fixtures.
- [ ] The pinned core tool loads and content-verifies the repository-owned catalog without repository-specific changes to Tournament scheduling, scoring, state, storage, or projection behavior.
- [ ] Automated contract coverage fails on stale asset digests, missing versions, changed participant contracts, or drift between a core fixture and this repository's authoritative catalog.
- [ ] The ownership boundary clearly identifies this repository as catalog authority and `rps-tournament` as authority for generic validation, building, certification, execution, and official Tournament operation.

## Give each Team a branch-ready Python template

**What to build:** Let a Team start from an organizer-owned Python example on its
own shared-repository branch, edit only controlled Team Source, and receive fast
static feedback without learning container or Tournament internals.

**Blocked by:** Establish the immutable companion-to-core contract.

- [ ] A fresh Team branch contains a working Python strategy that demonstrates the four-argument `choose_move` contract and uses the wrapper-provided deterministic random generator.
- [ ] Teams can add approved Python modules and controlled CSV, JSON, or text resources within the catalog's size, count, and path limits.
- [ ] The editable Team Source boundary is unmistakable; wrappers, recipes, entrypoints, dependency definitions, workflows, and catalog metadata remain organizer-owned.
- [ ] The template explains that only `R`, `P`, or `S` is a valid move and that the wrapper owns protocol I/O, readiness, seeding, and process lifecycle.
- [ ] The shared-branch honor policy and branch naming convention allow one branch per Team without claiming submission secrecy.

## Add one-command participant validation

**What to build:** Give a Team with Docker one documented command that validates
its current Team Source, builds one native-platform confidence image, runs the
participant-local conformance suite, and completes a practice Match through the
pinned core tool.

**Blocked by:** Establish the immutable companion-to-core contract; Give each Team a branch-ready Python template.

- [ ] The command is a thin adapter over the pinned public core commands and contains no independent source-validation, build, protocol, isolation, resource, or scoring logic.
- [ ] The command uses the repository-owned frozen catalog and builds exactly one native platform without a multi-platform image or OCI index.
- [ ] Successful output identifies the Team Source digest, catalog, core tool, suite, recipe, wrapper, runtime, platform, disposable image, and advisory validation result.
- [ ] Diagnostics distinguish source, build, readiness, protocol, determinism, isolation, resource, lifecycle, and Docker-host failures in Team-facing language.
- [ ] A missing local Docker engine points the Team to GitHub advisory validation, and every local result is clearly insufficient for official Tournament entry.

## Validate every Team commit on native AMD64

**What to build:** Give every pushed Team commit an automatic GitHub check that
runs the same pinned conformance suite on native Linux/AMD64 and leaves durable,
commit-specific eligibility evidence without publishing a Bot Artifact.

**Blocked by:** Add one-command participant validation.

- [ ] The workflow runs on Team branch commits, checks out the exact commit, installs the immutable core-tool pin, and validates against the frozen repository-owned catalog.
- [ ] It builds only `linux/amd64`, invokes `github-advisory` authority, and never uses QEMU, creates a multi-platform image, or pushes an image to a registry.
- [ ] Workflow permissions are read-only and minimal, no repository or deployment secret is exposed to Team Source, and untrusted Team code receives no privileged Docker or repository authority beyond the conformance contract.
- [ ] Superseded work on the same Team branch is cancelled without erasing the latest completed green candidate.
- [ ] The durable result identifies the exact source commit, Source Digest, catalog, core tool, suite, recipe, wrapper, runtime digest, platform, disposable image identity, execution profile, and pass or fail result.
- [ ] A practice Match's score or winner cannot fail an otherwise conforming Submission Candidate.

## Document cutoff selection and manual source export

**What to build:** Give Teams and the organizer one auditable rule for selecting
the latest successfully validated pre-cutoff Team Source commit, then manually
transporting that exact source into the organizer-controlled local workflow.

**Blocked by:** Validate every Team commit on native AMD64.

- [ ] The cutoff rule selects the latest completed green commit at or before the declared deadline and permits an explicitly chosen earlier green commit.
- [ ] The runbook shows how to confirm that the selected commit and durable GitHub result name the same Source Digest and frozen catalog.
- [ ] Manual clone, pull, checkout, and source export end at the core tool's already-present local-directory boundary; automated branch discovery, authentication, pulling, and cutoff enforcement remain out of scope.
- [ ] A no-GitHub path explains how an organizer handles a manually delivered directory or ZIP archive through the same source validator.
- [ ] The policy states that GitHub/AMD64 evidence is advisory and that only organizer Final Validation of a rebuilt ARM64 image can create a Tournament-eligible Bot Artifact.
- [ ] Post-cutoff compatibility-only repair rules preserve the original source, complete diff, explanation, replacement Source Digest, and Final Validation identity while prohibiting strategy enhancement.

## Prove the AMD64 signal against canonical ARM64 validation

**What to build:** Demonstrate that one selected Python Submission Candidate can
pass advisory validation on native AMD64 and Final Validation on native ARM64
through the same catalog and suite, while preserving architecture-specific
runtime, image, and validation identities.

**Blocked by:** Validate every Team commit on native AMD64.

- [ ] The same frozen Team Source and Language Environment assets exercise build, wrapper readiness, protocol version 1, Seed Adapter determinism, isolation, resource limits, lifecycle, and practice-Match conformance on both native platforms.
- [ ] The GitHub lane produces a disposable single-platform AMD64 confidence image, and the organizer lane produces the canonical single-platform ARM64 Bot Artifact.
- [ ] Cross-platform evidence compares source compatibility and contract behavior without requiring equal runtime digests, image digests, or language-native random streams.
- [ ] The acceptance path uses no QEMU, multi-platform build, combined OCI index, remote registry, or GitHub-built image in the official roster.
- [ ] The retained evidence is sufficient to diagnose a rare architecture-specific failure and drive the documented compatibility-only repair policy.

## Freeze and release the first event catalog

**What to build:** Publish a clean, immutable repository release that Teams can
branch from and the organizer can cite for one event, with every template,
workflow, catalog asset, core-tool pin, and validation identity frozen together.

**Blocked by:** Document cutoff selection and manual source export; Prove the AMD64 signal against canonical ARM64 validation.

- [ ] A clean clone can create a Team branch, validate the starter strategy locally or through GitHub, and reproduce the documented advisory evidence without unpublished files or maintainer state.
- [ ] The release records the exact repository commit, catalog identity, core-tool pin, conformance-suite identity, execution-profile identity, wrapper and recipe versions, and both platform-specific runtime digests.
- [ ] The release process verifies catalog content digests and rejects mutable core, runtime, action, or dependency references.
- [ ] The released Python environment uses only the standard library and organizer-pinned contents; neither participant nor GitHub validation requires build-time package downloads.
- [ ] The release notes preserve the distinction between a Submission Candidate, a disposable advisory image, and the canonical organizer-built Bot Artifact.
- [ ] A maintainer checklist freezes the catalog before coding begins and prohibits routine catalog, wrapper, recipe, base-image, or conformance changes until the event completes.
