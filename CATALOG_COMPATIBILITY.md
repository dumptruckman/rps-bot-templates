# Catalog compatibility contract

A Template Release from this repository is an independent participant-facing
adapter for exactly one Catalog Release published by `rps-tournament`. The
Template Release owns its Team Template and guidance. The Catalog Release owns
the Language Environments and every organizer-controlled execution asset. A
compatibility claim does not transfer authority in either direction.

`core-tool.lock.json` records the complete immutable claim:

- `runner` names the full commit and exact package version;
- `catalog` names the repository-relative catalog path, canonical content
  identity, and complete catalog asset identity map; and
- `offline_bundle` names the versioned SHA-256 identity of its bytes.

The local filename `core-tool.bundle` and the Runner repository slug used by a
legacy workflow are transport wiring, not release coordinates, so they remain
outside the compatibility claim.

Every coordinate is equality-matched. A missing or different commit, package
version, path, catalog identity, asset identity, or bundle identity is a
different Catalog Release and must be rejected. Branches, abbreviated commits,
mutable tags, and `latest` values are not compatibility coordinates.

`materialize-core-tool` performs those equality checks before returning a
catalog path. It verifies the offline bundle before cloning, then verifies the
clean checkout, installed-package metadata, canonical catalog content, and each
referenced asset. Its failures identify the mismatched coordinate and direct the
organizer to restore the locked release inputs. `validate-team`, GitHub Advisory
Validation, wrapper smoke tests, and the native cross-platform proof consume
only the catalog inside that materialized checkout. This repository contains no
catalog source tree or fallback.

`release-team-template` copies the complete lock object into each annotated
Template Release manifest alongside the exact Template repository commit, Team
Template digest, and Advisory Validation workflow identity. Release creation
and verification rematerialize and equality-check the claim; a partially edited
or mismatched lock cannot publish a Template Release.

The dependency is one-way. This repository may materialize the locked Runner
offline to provide Advisory Validation, but the Runner never consumes a Team
Template or Template Release. Final Validation independently uses the
organizer-selected Catalog Release and exact selected Team Source; only that
organizer-controlled result can authorize a Bot Artifact for a Tournament.

## Update the compatibility lock safely

Begin with the offline bundle and `runner-catalog-independence-v1` evidence
published together by one new Runner Catalog Release. Prepare, rather than
hand-edit, the replacement pair:

```sh
./prepare-catalog-lock \
  --runner-bundle <published-runner-bundle> \
  --runner-evidence <catalog-independence-evidence.json> \
  --output <new-empty-directory>
```

The command requires a passed independence scan and organizer workflow proof,
equality-checks the release manifest and its copy-ready compatibility
coordinates, verifies the bundle identity, clones it without network access,
and verifies the exact Runner commit, package, catalog, and every asset. It
writes nothing at the destination unless the complete set passes.

Review the retained evidence, then copy the lock and bundle together into a
clean Template checkout. Materialize to a new destination, run the full suites
in both repositories, and publish a new Template Release. Never edit one
coordinate to make a mismatched checkout appear compatible. Never move or
recreate the earlier Catalog Release; historical tags, bundles, annotations,
and procedures remain immutable evidence even after being superseded.
