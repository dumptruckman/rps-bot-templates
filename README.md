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

A fresh Team branch starts from one exact annotated Template Release of the
Python Team Template. Its working strategy is
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

The [cross-repository cutover proof](CROSS_REPOSITORY_CUTOVER.md) starts from a
clean Template Release and offline Runner inputs, verifies the one-way authority
boundary and unchanged starter Source Digest, then carries selected Team Source
through native evidence, preserved Bot Artifact, Tournament plan, and execution.

The [Template Release runbook](TEMPLATE_RELEASE.md) defines how maintainers
publish the participant-facing starter, pin one Runner-owned Catalog Release,
and create Team branches from the exact annotated release tag. Catalog Releases
remain exclusively owned by `rps-tournament`.

The [Team Template collection guide](TEAM_TEMPLATE_COLLECTION.md) documents the
new language-indexed maintainer interface and its compatibility boundary. During
the expand phase, `./validate-team --template python` and
`./release-team-template --template python manifest template-v1` coexist with
the unchanged singular Python commands.

## Immutable compatibility contract

[`core-tool.lock.json`](core-tool.lock.json) is the compatibility claim copied
into this Team Template's release manifest. It identifies exactly one published
Runner Catalog Release by a full Runner commit, exact package version,
repository-relative catalog path, catalog content identity, complete catalog
asset identity map, and offline bundle identity. It contains no branch,
abbreviated commit, version tag, or `latest` fallback.

`core-tool.bundle` materializes the exact Runner commit without network access.
Before validation begins, the materializer equality-checks the bundle identity,
clean Runner commit, package version, catalog path, catalog identity, and every
catalog asset identity. Local and GitHub Advisory Validation then read the
catalog only from that verified Runner checkout. See the
[catalog compatibility contract](CATALOG_COMPATIBILITY.md) for the release
boundary and lock-update rules.

The ownership boundary is deliberate:

- This repository owns the Team Template under `team_source/`, Team instructions,
  Advisory Validation entrypoints, and Template Releases.
- `rps-tournament` owns every Language Environment and Catalog Release, including
  all organizer-controlled execution assets.
- Teams edit only `team_source/`. Organizer-owned paths are never Team Source,
  and no catalog source tree is maintained in this repository.

[`team-template.json`](team-template.json) names the supported Team Template
version, participant-facing source path, Advisory Validation workflow, and
release tag. The annotated tag manifest binds those values to the exact
Template commit, Team Template digest, workflow identity, and complete catalog
compatibility claim.

[`team-templates.json`](team-templates.json) is the collection-aware discovery
index. Its descriptor for Python binds the same existing source and release
identity without moving or removing the legacy paths.

## Verify a compatibility-lock change

Materialize the locked core commit from the repository-owned bundle, then run:

```sh
./materialize-core-tool
python3 -m unittest discover -s tests -v
```

Change the lock only with the verified preparation workflow in
[`CATALOG_COMPATIBILITY.md`](CATALOG_COMPATIBILITY.md). It consumes the
Runner-published bundle and catalog-independence evidence as one set; tests
reject a mismatched Runner commit, package version, catalog identity, asset map,
or bundle identity.
