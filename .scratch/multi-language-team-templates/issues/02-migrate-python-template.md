# Migrate and verify the Python Team Template

Status: ready-for-agent

Blocked by: 01; rps-tournament multi-language-environments 02

## Parent

[Multi-language Team Templates](../PRD.md)

## What to build

Move the working Python starter onto the collection-aware shape and give Teams
one Python build-and-test entrypoint that works with a local Python toolchain or
through Docker, with Docker executing that exact same script.

## Acceptance criteria

- [ ] Python has a collection entry, descriptor, controlled Team Source,
  participant guidance, and independently addressable Template Release identity.
- [ ] One Python-owned script builds and tests the starter when invoked with a
  compatible local Python installation.
- [ ] The Docker path invokes the identical Python-owned script inside the pinned
  development toolchain container; it does not reimplement the checks.
- [ ] Docker is sufficient to run the complete Python starter build and unit
  tests without relying on a host Python used for template behavior.
- [ ] The starter demonstrates the four-argument strategy contract, emits only
  legal moves, and proves deterministic seeded behavior.
- [ ] Advisory Validation uses the Python Language Environment from the exact
  pinned Catalog Release and continues to pass the complete container contract.
- [ ] Tests prove the Python starter's behavior is unchanged across the move and
  that any Source Digest or Template Release identity change is intentional.
- [ ] Native-mode missing-tool and Docker-host failures produce actionable,
  distinct diagnostics.

## Comments

The Docker path is the acceptance path. A Python installation on the maintainer
host is not part of this ticket's language-template verification contract.
