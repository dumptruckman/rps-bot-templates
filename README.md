# RPS Bot Templates

This repository will be the Team-facing source of truth for the Rock–Paper–
Scissors Tournament's Language Environment catalog, Team templates,
organizer-owned wrappers and build recipes, participant smoke-test commands,
and advisory GitHub validation.

The `rps-tournament` repository remains authoritative for the generic source
validator, builder, conformance suite, container executor, and official
Tournament workflow. This repository consumes that tooling by immutable version
or commit and does not reimplement it.

Initial implementation work is tracked as numbered issues under
`.scratch/companion-repository/issues/`.

## Immutable contract

The authoritative Language Environment Catalog is
`language_environments/catalog-v1/catalog.json`, with catalog version
`rps-language-environment-catalog-v1`. The generic core consumer is locked by
full commit and package version in `core-tool.lock.json`. Workflows read the core
repository and commit from that lock and pin third-party actions by full commit;
they do not resolve a branch, version tag, or `latest` value.

The catalog owns the Python Team Source schema and template, platform runtime
digests, networkless build recipe, wrapper and Seed Adapter, readiness contract,
entrypoint, standard-library-only dependency policy, and conformance fixtures.
Every organizer-owned asset is content-addressed from the catalog. The template
digest is sealed by the content-addressed conformance definition.

The ownership boundary is deliberate:

- This repository is authoritative for the event-facing Language Environment
  Catalog and all assets it names.
- `rps-tournament` is authoritative for generic source validation, building,
  certification, execution, scheduling, scoring, state, storage, projections,
  and official Tournament operation.

## Verify a catalog or core-pin change

Check out the locked core commit beside this repository (or set
`RPS_CORE_PATH` to it), then run:

```sh
python3 -m unittest discover -s tests -v
```

An asset edit intentionally fails until its SHA-256 entry is updated. A template
edit also requires updating `template_sha256` in `python/conformance.json`, then
updating the conformance asset digest in `catalog.json`. A core-pin change fails
unless the exact locked checkout's package version, generic fixture, and
participant contract still match.
