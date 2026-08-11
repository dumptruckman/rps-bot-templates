# Prove the cross-repository catalog cutover

Status: ready-for-agent

Priority: 2

Blocked by: 03; rps-tournament catalog-authority 04

## Parent

[Consume the Runner-owned catalog](../PRD.md)

## What to build

Demonstrate from clean clones and offline inputs that one Template Release
produces Team Source accepted by Advisory Validation and organizer Final
Validation against the same Runner-owned catalog identity, with no duplicated
catalog authority.

## Acceptance criteria

- [ ] Clean-clone Template validation materializes and verifies the pinned Runner
  and catalog identities before accepting Team Source.
- [ ] The unchanged starter produces the expected Source Digest through the new
  path, with any intentional migration difference documented and reviewed.
- [ ] Native AMD64 Advisory Validation and native ARM64 Final Validation retain
  their distinct platform-specific evidence while agreeing on Team Source and
  catalog identity.
- [ ] The organizer builds, certifies, preserves, plans, and executes a Bot
  Artifact from selected Team Source without reading a catalog from this
  repository.
- [ ] Offline reproduction succeeds from the retained Template release, Runner
  bundle, catalog release, pinned runtimes, and selected Team Source.
- [ ] All documentation describes the new authority direction, archives the old
  catalog release procedure, and gives maintainers a safe lock-update workflow
  for future catalog releases.
- [ ] Full suites in both repositories pass and repository scans find no reverse
  Runner dependency on Team Templates and no duplicate authoritative catalog.

## Comments

This is the final cutover gate. Do not delete or rewrite historical release tags;
archive their procedure as superseded evidence.
