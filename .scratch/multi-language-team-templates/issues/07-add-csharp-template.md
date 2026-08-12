# Add the C# Team Template

Status: ready-for-agent

Blocked by: 04; rps-tournament multi-language-environments 06

## Parent

[Multi-language Team Templates](../PRD.md)

## What to build

Deliver an independently releasable C# Team Template with equivalent strategy,
build, test, native-development, Docker-development, and Runner compatibility
behavior.

## Acceptance criteria

- [ ] The .NET SDK is the latest upstream-supported LTS release at preparation
  time and is pinned immutably in the matching Catalog and Template Releases.
- [ ] The C# starter implements the common strategy contract and includes
  deterministic unit tests for legal moves and seeded behavior.
- [ ] One C#-owned script builds and tests the starter with a compatible local
  .NET SDK.
- [ ] Docker invokes that identical C#-owned script and passes the complete build
  and unit-test suite without .NET installed on the host.
- [ ] Dependency restoration is deterministic and complies with the matching
  Language Environment's networkless build policy.
- [ ] Advisory Validation consumes the matching C# Language Environment from the
  exact pinned Catalog Release and passes its complete conformance contract.
- [ ] C# guidance documents Team Source boundaries, native prerequisites, Docker
  usage, and the distinction between Advisory and Final Validation.
- [ ] C# can be selected, checked, and released without changing another Team
  Template's descriptor or release identity.
