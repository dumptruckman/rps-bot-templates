# RPS Bot Templates

This repository will be the Team-facing source of truth for the Rock–Paper–
Scissors Tournament's Language Environment catalog, Team templates,
organizer-owned wrappers and build recipes, Team smoke-test commands, and
GitHub Advisory Validation.

The `rps-tournament` repository remains authoritative for the generic source
validator, builder, conformance suite, container executor, and official
Tournament workflow. This repository ships a content-addressed Git bundle of
the exact locked core commit so a clean clone can consume that tooling without
network access; it does not reimplement it.

Initial implementation work is tracked as numbered issues under
`.scratch/companion-repository/issues/`.

## Team branches

A fresh Team branch is ready to edit: its working strategy is
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

The [Language Environment Catalog release runbook](CATALOG_RELEASE.md) freezes
all catalog, core, suite, profile, wrapper, recipe, dependency, action, and
platform-runtime identities into an annotated tag before Team coding begins. It
also gives Teams a clean-clone reproduction path and maintainers the until-
completion freeze policy.

## Immutable contract

The authoritative Language Environment Catalog is
`language_environments/catalog-v1/catalog.json`, with catalog version
`rps-language-environment-catalog-v1`. The generic core consumer is locked by
full commit, package version, and bundled-history digest in
`core-tool.lock.json`. Active workflows materialize that exact commit from
`core-tool.bundle` and pin third-party actions by full commit; they do not
resolve a branch, version tag, or `latest` value.

The catalog owns the Python Team Source schema and template, platform runtime
digests, networkless build recipe, wrapper and Seed Adapter, readiness contract,
entrypoint, standard-library-only dependency policy, and conformance fixtures.
Every organizer-owned asset is content-addressed from the catalog. The template
digest is sealed by the content-addressed conformance definition.

The ownership boundary is deliberate:

- This repository is authoritative for the Tournament-facing Language Environment
  Catalog and all assets it names.
- `rps-tournament` is authoritative for generic source validation, building,
  certification, execution, scheduling, scoring, state, storage, projections,
  and official Tournament operation.

## Verify a catalog or core-pin change

Materialize the locked core commit from the repository-owned bundle, then run:

```sh
./materialize-core-tool
python3 -m unittest discover -s tests -v
```

An asset edit intentionally fails until its SHA-256 entry is updated. A template
edit also requires updating `template_sha256` in `python/conformance.json`, then
updating the conformance asset digest in `catalog.json`. A core-pin change fails
unless the exact locked checkout's package version, generic fixture, and Team
contract still match.
