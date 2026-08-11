# Publishing a Template Release

A Template Release is the immutable participant-facing starting point for Team
coding. Its JSON manifest is the annotation on an annotated Git tag. The
manifest records the exact Template repository commit, Team Template digest,
expected starter Source Digest, complete `core-tool.lock.json` Catalog Release
compatibility claim, Advisory Validation workflow identity, and supported Team
Template version.

The release contains no Language Environment Catalog source. The catalog,
wrapper, runtimes, recipe, readiness contract, entrypoint, and conformance
fixtures remain exclusively owned and published by `rps-tournament`.

## Create the release

Use a clean checkout with complete Git history. Confirm that
`team-template.json` names the new, unused release tag and version, then review
the release identity before creating it:

```text
git status --short
./materialize-core-tool .core/rps-tournament
./release-team-template manifest template-v1
./release-team-template create template-v1
./release-team-template verify template-v1
```

Creation verifies the content-addressed Runner bundle, exact clean Runner
commit, package version, catalog path and identity, complete catalog asset map,
Team Template contents and Source Digest, supported version, and immutable
workflow action references. It refuses a dirty Template checkout, mismatched
catalog lock, changed Team Template, mutable action reference, reused tag, or
tag name that does not match `team-template.json`.

Push the exact Template commit and annotated tag together. Do not move, delete,
or recreate a published tag; its annotation is the Template Release manifest.

```text
git push origin HEAD
git push origin refs/tags/template-v1
```

## Verify from a clean clone

Fetch the published tag into a fresh clone, detach at its target, materialize
the bundled Runner dependency without network access, and verify the record:

```text
git clone <template-repository> rps-bot-templates
cd rps-bot-templates
git switch --detach template-v1^{}
./materialize-core-tool .core/rps-tournament
./release-team-template verify template-v1
```

Verification rejects a dirty tree, lightweight or malformed tag, tag aimed at
another commit, changed Team Template or Advisory Validation workflow, changed
compatibility claim, and any mismatch between the lock and materialized Runner
Catalog Release.

## Create Team branches

Create every Team branch from the dereferenced Template Release commit, never
from a catalog tag, mutable branch head, or `latest` reference:

```text
git switch --create team/<team-slug> template-v1^{}
git push --set-upstream origin team/<team-slug>
```

The branch inherits the released Team Template, compatibility lock, Team
guidance, and Advisory Validation workflow as one reviewed participant-facing
starting point. Teams then change only `team_source/`.

## Corrections and replacement versions

A published Template Release is never repaired in place. A Team Template,
workflow, guidance, or Catalog Release compatibility change requires a new
supported template version, a new release tag, and a new manifest. Release notes
must identify the superseded release and explain the replacement. Existing Team
branches remain on their original Template Release unless the organizer
explicitly restarts or migrates them before the declared cutoff.

After publication, use the
[cross-repository cutover proof](CROSS_REPOSITORY_CUTOVER.md) to retain a clean-
clone and offline reproduction of the released starter, native platform
evidence, and organizer workflow. The expected starter Source Digest is checked
through the materialized Runner catalog during both release creation and
verification; it is not derived from a catalog copy in this repository.
