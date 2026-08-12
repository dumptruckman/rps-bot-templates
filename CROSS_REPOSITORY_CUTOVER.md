# Cross-repository Catalog cutover proof

This is the final acceptance path for the one-way catalog authority boundary.
A Template Release consumes one exact Catalog Release published by
`rps-tournament`; the Runner neither fetches nor reads this repository. The
proof begins in a clean Template Release checkout and finishes with an executed
organizer-owned Bot Artifact, retaining every identity needed for an audit or
offline replay.

## Retained inputs

Preserve these inputs together before starting:

- the exact annotated Template Release tag and a clean checkout at `tag^{}`;
- the offline Runner bundle named by that release's `core-tool.lock.json`;
- the matching `runner-catalog-independence-v1` evidence and embedded Catalog
  Release manifest;
- one selected Team Source directory and its retained native Linux/AMD64
  Advisory Validation evidence;
- the digest-pinned Linux/AMD64 and Linux/ARM64 runtime images from the Catalog
  Release, retained in the native hosts' offline image stores or approved image
  archives; and
- a new output path outside the Template checkout.

Do not fetch a branch, catalog, runtime, source directory, or Bot Artifact while
the proof is running. The native Linux/AMD64 Advisory Validation must already
have completed on the selected commit. Run the remaining lane on a native
Linux/ARM64 organizer host with the pinned ARM64 runtime already available.

## Run the proof

From the clean Template Release checkout, run:

```sh
./prove-cross-repository-cutover \
  --template <language-id> \
  --runner-evidence <catalog-independence-evidence.json> \
  --advisory-evidence <downloaded-team-advisory-artifact> \
  --source <exported-selected-team-source> \
  --selected-commit <40-character-commit> \
  --output <new-proof-directory>
```

Before accepting the selected Team Source, the command verifies the annotated
Template Release, creates its retained Git bundle, clones that bundle into a
new checkout, and detaches at the recorded tag. From that clean clone it
materializes the clone's offline Runner bundle and verifies its exact commit,
package, catalog identity, and complete asset map. It checks that the Runner
independence evidence has no reverse dependency or participant asset, then
validates the released starter through the clean clone's materialized catalog.

The unchanged starter's expected and observed Source Digest is
`sha256:e2890c1587c6c98acb62121e5524d8f75a53925ed738f333f63beee81e60fd1a`.
There is no Source Digest migration difference: moving catalog authority to the
Runner changed the catalog identity because its workflow action became
immutable, but it did not change the starter bytes or Team Source identity.

The command then runs from the clean clone without a network command. It
consumes the native Linux/AMD64 Advisory Validation evidence, rebuilds the same
source for native Linux/ARM64 Final Validation, and requires both lanes'
runtime, image, and validation identities. It also uses the materialized
Runner's batch and Tournament commands to prove the organizer builds, Final
Validates, preserves, plans, and executes the selected Bot Artifact. The
terminal Competition Record's Team IDs and Bot Artifact digests must match the
plan. The four-entry proof roster intentionally maps four proof Team IDs to the
same selected source so the Runner's real minimum-roster path is exercised
without introducing another source input.

Every catalog argument names the verified materialized Runner checkout. The
organizer never reads a catalog from the Template repository, and this
repository contains no catalog tree or fallback.

## Evidence and offline reproduction

Retain the complete output directory. `cutover-proof.json` reconciles the
Template Release, Runner commit and bundle, Catalog Release, starter and
selected Source Digests, both native lanes, canonical Bot Artifact, artifact
store, Tournament plan, and first terminal Match record. The directory also
contains:

- `template-release.bundle` and the verified tag manifest;
- `offline-template/` cloned from that bundle and `offline-runner/`
  materialized exclusively from the clone's Runner bundle;
- the exact Runner catalog-independence evidence;
- frozen starter and selected-source bundles;
- the original Advisory Validation evidence and new Final Validation evidence;
- build, certification, preservation, planning, and execution outputs; and
- stdout and stderr for every delegated command.

To reproduce without network access, clone `template-release.bundle`, detach at
the recorded annotated tag, restore its repository-owned `core-tool.bundle`,
provide the retained Runner evidence and selected Team Source, load only the two
runtime images whose digests appear in the Catalog Release manifest, and rerun
the command on the corresponding native hosts. A different tag, bundle byte,
catalog coordinate, runtime digest, Source Digest, or platform evidence fails
closed.

## Superseded procedure

Before this cutover, this repository both owned the participant template and
froze a duplicate Language Environment Catalog. That superseded catalog release
procedure is archived at
[`docs/superseded/TEMPLATE_OWNED_CATALOG_RELEASE.md`](docs/superseded/TEMPLATE_OWNED_CATALOG_RELEASE.md)
as historical evidence only. Do not restore its tooling, move its historical
tags, rewrite its annotations, or use it for a new release. Future Catalog
Releases come only from `rps-tournament`; use
[`CATALOG_COMPATIBILITY.md`](CATALOG_COMPATIBILITY.md) to prepare a verified
lock update and publish a separate new Template Release.
