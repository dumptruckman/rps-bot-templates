# Migrate and verify the Python Team Template

Status: resolved

Blocked by: 01; rps-tournament multi-language-environments 02

## Parent

[Multi-language Team Templates](../PRD.md)

## What to build

Move the working Python starter onto the collection-aware shape and give Teams
one Python build-and-test entrypoint that works with a local Python toolchain or
through Docker, with Docker executing that exact same script.

## Acceptance criteria

- [x] Python has a collection entry, descriptor, controlled Team Source,
  participant guidance, and independently addressable Template Release identity.
- [x] One Python-owned script builds and tests the starter when invoked with a
  compatible local Python installation.
- [x] The Docker path invokes the identical Python-owned script inside the pinned
  development toolchain container; it does not reimplement the checks.
- [x] Docker is sufficient to run the complete Python starter build and unit
  tests without relying on a host Python used for template behavior.
- [x] The starter demonstrates the four-argument strategy contract, emits only
  legal moves, and proves deterministic seeded behavior.
- [x] Advisory Validation uses the Python Language Environment from the exact
  pinned Catalog Release and continues to pass the complete container contract.
- [x] Tests prove the Python starter's behavior is unchanged across the move and
  that any Source Digest or Template Release identity change is intentional.
- [x] Native-mode missing-tool and Docker-host failures produce actionable,
  distinct diagnostics.

## Comments

The Docker path is the acceptance path. A Python installation on the maintainer
host is not part of this ticket's language-template verification contract.

## Answer

Migrated Python to `templates/python/` with controlled Team Source, participant
guidance, deterministic unit tests, and one `build-and-test` script shared by
native and Docker modes. `check-team-template` resolves the selected descriptor,
uses the exact digest-pinned Python 3.14.6 build toolchain from Catalog Release
`catalog-v2`, disables container networking, and reports native-toolchain and
Docker-host failures separately.

The starter bytes and Source Digest remain unchanged at
`sha256:e2890c1587c6c98acb62121e5524d8f75a53925ed738f333f63beee81e60fd1a`;
the migrated template intentionally advances to `python-team-template-v2` and
independent tag `python-template-v2`. Real Linux/ARM64 Docker build-and-test,
complete Advisory Validation with practice Match, the selected release manifest,
Python 3.9 compilation, and all 68 repository tests pass against the new pinned
Catalog Release.
