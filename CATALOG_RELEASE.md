# Freeze and release a Language Environment Catalog

The organizer publishes one immutable Language Environment Catalog release
before Team coding begins.
For the first Tournament, the release tag is `catalog-v1`. It points at one exact
repository commit and its annotated tag message is the machine-readable
`catalog-release-v1` manifest. The manifest records the catalog, pinned core,
conformance suite, execution profile, wrapper, recipe, catalog assets, dependency
policy, and both platform-specific runtime digests as one release identity.

An annotated tag is required because a file inside a commit cannot contain that
commit's own SHA without becoming self-referential. The tag object records its
exact target commit, while the JSON annotation records that same SHA with every
other frozen input. A lightweight tag is not a release record.

## Maintainer freeze checklist

Complete this checklist before Team coding begins:

- [ ] Confirm `main` contains the canonical starter in `team_source/` and all
  documentation, workflows, catalog assets, and release tooling needed by a
  clean clone.
- [ ] Run `./materialize-core-tool` and confirm it checks out the commit from
  `core-tool.lock.json` under `.core/rps-tournament`. Do not replace the bundled
  history with an unpublished editable package.
- [ ] Pre-pull the catalog's digest-pinned Linux/AMD64 and Linux/ARM64 base
  runtimes on the native hosts that will use them.
- [ ] Run `python3 -m unittest discover -s tests -v` with the pinned core checkout.
- [ ] Run `./validate-team` on a supported native Docker host to prove the
  starter strategy and retain its Advisory Validation summary.
- [ ] Run `./freeze-tournament-catalog manifest catalog-v1` and review every
  identity before creating the release.
- [ ] Commit all release content. A release must be created from a clean working
  tree; generated or unpublished maintainer files are not permitted inputs.
- [ ] Run `./freeze-tournament-catalog create catalog-v1`, then
  `./freeze-tournament-catalog verify catalog-v1`.
- [ ] Push the exact commit and its annotated tag, and wait for the Catalog
  contract workflow on the tag to pass before opening Team coding.

From the moment the release is published, make no routine changes to the
catalog, wrapper, recipe, base runtime, or conformance suite until the Tournament
completes. The same prohibition covers workflow, entrypoint, readiness,
dependency-policy, execution-profile, and core-tool changes. If an organizer-
declared infrastructure correction is unavoidable, publish a new catalog
version and release tag, invalidate eligibility against the replaced release,
and rerun affected Advisory Validation and Final Validation.

The first Python Language Environment is standard library only. Its dependency
lock has no packages, its recipe has no install step, and validation performs no
build-time package downloads. The release command rejects package entries,
mutable core commits, mutable runtime references, mutable action references, and
catalog asset digest drift.

## Publish the release

Use the bundled pinned core without cloning a private repository or downloading
build dependencies:

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

Treat the JSON printed by `create` as the release notes' identity block. The tag
annotation is canonical: `git cat-file tag catalog-v1` shows the exact repository
commit and complete frozen manifest in any clone. GitHub verifies the tag again
from the published commit and pinned core checkout.

## Reproduce from a clean clone

No unpublished files or maintainer environment are needed. A Team can start from
the released catalog and validate the unchanged starter as follows:

```sh
git clone https://github.com/dumptruckman/rps-bot-templates.git
cd rps-bot-templates
git checkout catalog-v1
./materialize-core-tool
./freeze-tournament-catalog verify catalog-v1
git switch --create team/<team-slug> catalog-v1
./validate-team
```

If local Docker is unavailable, push the `team/<team-slug>` branch instead. The
Team Advisory Validation workflow runs on native Linux/AMD64 and retains the
`team-advisory-<commit>` artifact containing `eligibility-evidence.json` and
`validation-report.json`. Re-running the same released starter locally or on
GitHub reproduces the documented advisory contract and identities; image and
validation digests remain platform- and run-specific evidence.

## Release authority notes

A green Team commit is a Submission Candidate. The Team-local or GitHub-built
container is a disposable advisory image used only for compatibility evidence.
Neither is the canonical organizer-built Bot Artifact. Only the organizer can
build that Bot Artifact from the selected exact Team Source and accept it through
Final Validation on native Linux/ARM64. Release notes and Tournament records must
preserve those three distinct terms and authority levels.
