# RPS Bot Templates

This repository is authoritative for Team Templates and participant-facing Team
guidance for the Rock–Paper–Scissors Tournament. It publishes starter Team
Source and the local and GitHub commands through which Teams receive Advisory
Validation.

`rps-tournament` is authoritative for the Language Environment Catalog and all
organizer-owned execution assets: Team Source schemas, wrappers, Seed Adapters,
pinned runtimes, build recipes, readiness contracts, entrypoints, and
conformance fixtures. It also owns validation, building, certification,
execution, and official Tournament operation. This repository consumes one
exact Catalog Release; it does not redefine those assets.

## Team branches

A fresh Team branch starts from the Python Team Template. Its working strategy is
[`team_source/strategy.py`](team_source/strategy.py). Teams must change only
Team Source under `team_source/`; the catalog and its build, wrapper, workflow,
and protocol assets remain organizer-owned. See the [Team guide](TEAM_GUIDE.md)
for the strategy contract, approved file types and limits, branch convention,
and shared-repository honor policy.

Teams with a running Docker engine can exercise the entire Advisory Validation
path with one command:

```sh
./validate-team
```

See the [Team guide](TEAM_GUIDE.md#validate-your-team-source) for the pinned-core
checkout prerequisite, result identities, diagnostic categories, and the firm
boundary between Advisory Validation and official Tournament entry.

The [submission cutoff and manual handoff policy](SUBMISSION_CUTOFF.md) defines
how an organizer selects a completed pre-cutoff green commit, exports that exact
Team Source, reconciles its identities, and handles offline delivery or an
exceptional compatibility-only repair.

The [native AMD64-to-ARM64 proof](CROSS_PLATFORM_PROOF.md) rebuilds one selected
Submission Candidate on the organizer's native ARM64 machine, runs canonical
Final Validation, and retains a contract comparison against its GitHub Advisory
Validation evidence without conflating the two platform-specific images.

The [legacy catalog release runbook](CATALOG_RELEASE.md) documents the
pre-cutover release procedure while its duplicate assets remain in this
repository. New Catalog Releases belong to `rps-tournament`.

## Immutable compatibility contract

[`core-tool.lock.json`](core-tool.lock.json) is the compatibility claim for this
Team Template. It identifies exactly one published Runner Catalog Release by a
full Runner commit, exact package version, repository-relative catalog path,
catalog content identity, complete catalog asset identity map, and offline
bundle identity. It contains no branch, abbreviated commit, version tag, or
`latest` fallback.

`core-tool.bundle` materializes the exact Runner commit without network access.
Before validation begins, the materializer equality-checks the bundle identity,
clean Runner commit, package version, catalog path, catalog identity, and every
catalog asset identity. Local and GitHub Advisory Validation then read the
catalog only from that verified Runner checkout. See the
[catalog compatibility contract](CATALOG_COMPATIBILITY.md) for the release
boundary and lock-update rules.

The ownership boundary is deliberate:

- This repository owns the Team Template under `team_source/`, Team instructions,
  Advisory Validation entrypoints, and future Template Releases.
- `rps-tournament` owns every Language Environment and Catalog Release, including
  all organizer-controlled execution assets.
- Teams edit only `team_source/`. Organizer-owned paths are never Team Source,
  even when a transition copy is present here.

The current `language_environments/` tree is a temporary, non-authoritative
mirror retained only during the staged catalog-consumer cutover. Its presence
does not create a second catalog authority. No active validation path reads it;
it will be removed in the contraction step of the cutover.

## Verify a compatibility-lock change

Materialize the locked core commit from the repository-owned bundle, then run:

```sh
./materialize-core-tool
python3 -m unittest discover -s tests -v
```

Change the lock only by copying every coordinate from a published Runner Catalog
Release and replacing the offline bundle with the bytes named by that release.
Tests reject a mismatched Runner commit, package version, catalog identity, asset
map, or bundle identity.
