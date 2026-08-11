# Prove the cross-repository catalog cutover

Status: resolved

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

- [x] Clean-clone Template validation materializes and verifies the pinned Runner
  and catalog identities before accepting Team Source.
- [x] The unchanged starter produces the expected Source Digest through the new
  path, with any intentional migration difference documented and reviewed.
- [x] Native AMD64 Advisory Validation and native ARM64 Final Validation retain
  their distinct platform-specific evidence while agreeing on Team Source and
  catalog identity.
- [x] The organizer builds, certifies, preserves, plans, and executes a Bot
  Artifact from selected Team Source without reading a catalog from this
  repository.
- [x] Offline reproduction succeeds from the retained Template release, Runner
  bundle, catalog release, pinned runtimes, and selected Team Source.
- [x] All documentation describes the new authority direction, archives the old
  catalog release procedure, and gives maintainers a safe lock-update workflow
  for future catalog releases.
- [x] Full suites in both repositories pass and repository scans find no reverse
  Runner dependency on Team Templates and no duplicate authoritative catalog.

## Comments

This is the final cutover gate. Do not delete or rewrite historical release tags;
archive their procedure as superseded evidence.

## Answer

The Template compatibility lock now names Runner commit
`e032114ac567fa6a454796862df3fed855b29058` and Catalog identity
`rps-language-environment-catalog-v1@sha256:8724e24a870b6004a01bca95d23059c94cb9abe2c73e15018db2ad0d0a02c181`.
The corresponding offline Runner bundle reproduces that checkout and the
Runner's retained `runner-catalog-independence-v1` evidence proves that its
release and organizer workflows have no Template dependency or participant
asset.

`release-team-template` now binds and revalidates the starter's Source Digest
through the pinned Runner-owned catalog. The unchanged starter remains
`sha256:e2890c1587c6c98acb62121e5524d8f75a53925ed738f333f63beee81e60fd1a`;
there is no Source Digest migration difference.

`prove-cross-repository-cutover` is the retained release gate. It creates and
clones the exact Template Release bundle, materializes Runner only from the
clone's offline bundle, validates the released starter, reconciles the native
Linux/AMD64 Advisory and Linux/ARM64 Final evidence identities, then builds,
certifies, preserves, plans, and executes the selected source with Runner-owned
catalog paths. It fails closed unless the terminal Competition Record's Team
IDs and Bot Artifact digests match the Tournament plan. The runbook records the
offline inputs and the old Template-owned catalog procedure is archived as
historical evidence only. A verified preparation command stages future lock,
bundle, and independence-evidence updates atomically without changing release
history.

Verification passed in both repositories: all 53 Template tests; all 406 Runner
tests with the three documented opt-in Docker skips; all seven Runner browser
scenarios; the Runner's 117-test isolated catalog proof; clean-clone Template
Release creation and verification; and native Linux/ARM64 Template validation.
Repository scans found neither a reverse Runner dependency nor a duplicate
authoritative catalog. Two-axis review found no remaining standards or spec
gaps after the shared evidence validator, native identity, Competition Record,
and clean-clone reproduction findings were corrected.
