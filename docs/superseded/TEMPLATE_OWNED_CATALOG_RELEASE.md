# Superseded Template-owned Catalog Release procedure

Status: archived historical evidence; do not run

This file preserves the release direction used before the cross-repository
cutover. At that time this repository owned both the participant-facing Team
Template and a duplicate Language Environment Catalog. The root command
`freeze-tournament-catalog`, its catalog tree, and its Catalog Release workflow
were removed when `rps-tournament` became the sole catalog authority.

The historical procedure created an annotated `catalog-v1` tag from a clean
Template repository checkout. Its JSON annotation recorded the Template
repository commit, repository-owned catalog assets, pinned core tool,
conformance suite, execution profile, wrapper, recipe, dependency policy, and
both platform runtime digests. Maintainers ran:

```sh
./materialize-core-tool
python3 -m unittest discover -s tests -v
./validate-team
./freeze-tournament-catalog manifest catalog-v1
git status --short
./freeze-tournament-catalog create catalog-v1
./freeze-tournament-catalog verify catalog-v1
git push origin HEAD
git push origin refs/tags/catalog-v1
```

Teams then created branches from `catalog-v1`. The procedure froze catalog,
wrapper, recipe, runtime, conformance, workflow, entrypoint, readiness,
dependency, execution-profile, and core-tool changes for the coding period. A
correction required a new version and tag; existing release records were never
moved or rewritten.

That authority direction is now invalid. A Template Release is created with
`release-team-template` and records a compatibility claim copied from one
Runner-owned Catalog Release. Only `rps-tournament` may publish a new Catalog
Release or define catalog assets. Historical tags and their annotations remain
immutable evidence and must not be deleted, recreated, or repurposed.
