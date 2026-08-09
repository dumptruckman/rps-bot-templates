# Document cutoff selection and manual source export

Status: ready-for-agent

Blocked by: 04

## What to build

Give Teams and the organizer one auditable rule for selecting the latest
successfully validated pre-cutoff Team Source commit, then manually transporting
that exact source into the organizer-controlled local workflow.

## Acceptance criteria

- [ ] The cutoff rule selects the latest completed green commit at or before the declared deadline and permits an explicitly chosen earlier green commit.
- [ ] The runbook shows how to confirm that the selected commit and durable GitHub result name the same Source Digest and frozen catalog.
- [ ] Manual clone, pull, checkout, and source export end at the core tool's already-present local-directory boundary; automated branch discovery, authentication, pulling, and cutoff enforcement remain out of scope.
- [ ] A no-GitHub path explains how an organizer handles a manually delivered directory or ZIP archive through the same source validator.
- [ ] The policy states that GitHub/AMD64 evidence is advisory and that only organizer Final Validation of a rebuilt ARM64 image can create a Tournament-eligible Bot Artifact.
- [ ] Post-cutoff compatibility-only repair rules preserve the original source, complete diff, explanation, replacement Source Digest, and Final Validation identity while prohibiting strategy enhancement.
