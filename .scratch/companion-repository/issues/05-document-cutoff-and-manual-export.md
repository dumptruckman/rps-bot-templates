# Document cutoff selection and manual source export

Status: resolved

Blocked by: 04

## What to build

Give Teams and the organizer one auditable rule for selecting the latest
successfully validated pre-cutoff Team Source commit, then manually transporting
that exact source into the organizer-controlled local workflow.

## Acceptance criteria

- [x] The cutoff rule selects the latest completed green commit at or before the declared deadline and permits an explicitly chosen earlier green commit.
- [x] The runbook shows how to confirm that the selected commit and durable GitHub result name the same Source Digest and frozen catalog.
- [x] Manual clone, pull, checkout, and source export end at the core tool's already-present local-directory boundary; automated branch discovery, authentication, pulling, and cutoff enforcement remain out of scope.
- [x] A no-GitHub path explains how an organizer handles a manually delivered directory or ZIP archive through the same source validator.
- [x] The policy states that GitHub/AMD64 evidence is advisory and that only organizer Final Validation of a rebuilt ARM64 image can create a Tournament-eligible Bot Artifact.
- [x] Post-cutoff compatibility-only repair rules preserve the original source, complete diff, explanation, replacement Source Digest, and Final Validation identity while prohibiting strategy enhancement.

## Answer

Added a shared submission cutoff and manual handoff policy. It defines an
auditable UTC cutoff rule, explicit earlier-green selection, durable GitHub
evidence records, exact-commit export, and reconciliation of commit, Source
Digest, and frozen catalog identities at the pinned core's local-directory
source-validation boundary.

The policy also covers manually delivered directories and ZIP archives through
the same validator, preserves the authority boundary between advisory AMD64
evidence and organizer Final Validation of a rebuilt ARM64 Bot Artifact, and
sets a recorded compatibility-only repair process that prohibits competitive
strategy enhancement. The repository and Team guides link to the policy, and
contract tests protect every requirement.
