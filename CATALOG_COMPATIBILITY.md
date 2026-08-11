# Catalog compatibility contract

A Template Release from this repository is an independent participant-facing
adapter for exactly one Catalog Release published by `rps-tournament`. The
Template Release owns its Team Template and guidance. The Catalog Release owns
the Language Environments and every organizer-controlled execution asset. A
compatibility claim does not transfer authority in either direction.

`core-tool.lock.json` records the complete immutable claim:

- `runner` names the repository, full commit, and exact package version;
- `catalog` names the repository-relative catalog path, canonical content
  identity, and complete catalog asset identity map; and
- `offline_bundle` names the repository-owned bundle path and the versioned
  SHA-256 identity of its bytes.

Every coordinate is equality-matched. A missing or different commit, package
version, path, catalog identity, asset identity, or bundle identity is a
different Catalog Release and must be rejected. Branches, abbreviated commits,
mutable tags, and `latest` values are not compatibility coordinates.

The dependency is one-way. This repository may materialize the locked Runner
offline to provide Advisory Validation, but the Runner never consumes a Team
Template or Template Release. Final Validation independently uses the
organizer-selected Catalog Release and exact selected Team Source; only that
organizer-controlled result can authorize a Bot Artifact for a Tournament.

To update the lock, begin with a published Runner Catalog Release, copy every
coordinate together, install the matching offline bundle, materialize it into a
new destination, and run the full test suite. Never edit one coordinate to make
a mismatched checkout appear compatible.
