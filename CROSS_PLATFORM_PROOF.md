# Native AMD64-to-ARM64 proof

This acceptance run proves that the same selected Team Source passes the same
frozen Python Language Environment contract first through native Linux/AMD64
GitHub Advisory Validation and then through native Linux/ARM64 organizer Final
Validation. The GitHub lane's output is a disposable confidence image. Only the
organizer lane's newly built, single-platform ARM64 image is the canonical Bot
Artifact eligible for the official roster.

## Inputs

Start with one completed green `Team Advisory Validation` artifact selected
under [`SUBMISSION_CUTOFF.md`](SUBMISSION_CUTOFF.md). Preserve its
`eligibility-evidence.json` and `validation-report.json`. Manually export the
exact selected Team Source as that runbook directs; do not bring the GitHub
image into the organizer Docker context.

On the organizer's native ARM64 machine, check out this repository release and
run `./materialize-core-tool` unless its locked Runner checkout is already
present. The proof verifies the bundle and full Catalog Release coordinates
again before using the catalog in that checkout. The active Docker server must
report `linux/arm64`, and the catalog's pinned ARM64 runtime must already be
present.
Run, using the selected full Git commit and new output path:

```sh
./prove-amd64-against-arm64 \
  --advisory-evidence <downloaded-team-advisory-artifact> \
  --source <exported-team-source> \
  --selected-commit <40-character-commit> \
  --output <new-proof-directory>
```

The command fails closed unless the core checkout is pinned and Docker is
native ARM64. It freezes the exported source through the same catalog, compares
its Source Digest with GitHub evidence, builds one ARM64 candidate, and invokes
the same suite in `organizer-final` mode. It does not fetch source or images.

## What the comparison proves

`cross-platform-proof.json` requires both reports to pass every conformance
check: build, wrapper readiness, protocol transcripts, Seed Adapter same-seed
behavior, isolation, resource and timing limits, clean lifecycle, diagnostics,
and complete practice-Match conformance. Protocol transcripts exercise protocol
version 1 through the frozen suite and wrapper. The proof also requires
identical Source Digest, catalog, suite, wrapper, recipe, entrypoint,
platform-definition, execution-profile, and pinned-core identities.

The proof deliberately retains architecture-specific runtime digest, image
digest, and validation identity under separate `linux/amd64` and `linux/arm64`
records. It compares source compatibility and contract behavior, not binary
identity. Equal language-native random streams are not required: determinism is
proved independently inside each platform's Seed Adapter and runtime.

This path uses no QEMU, no multi-platform build, and no combined OCI index. An
ephemeral runner may fetch a pinned base runtime by its catalog digest, but Bot
Artifact images are never pushed to or pulled from a registry. The disposable
GitHub confidence image never enters the official roster or the ARM64 Docker
context; the two builds remain independent single-platform builds.

## Retention and failure handling

Retain the entire proof directory with the Team's selection record. It contains
the original GitHub evidence, each organizer command's stdout and stderr, the
frozen source bundle, ARM64 candidate manifest and build diagnostics, Final
Validation report, canonical Bot Artifact Manifest, stage progress, and the
cross-platform comparison. A failed stage leaves its completed inputs, partial
outputs, progress state, and a stage-specific error log in place so an
architecture-specific failure can be diagnosed without substituting a different
source or image.

If ARM64 exposes a rare compatibility defect, follow the compatibility-only
repair policy in `SUBMISSION_CUTOFF.md`. Preserve this failed proof, the original
source and Source Digest, the complete diff, explanation and approvals, the
replacement Source Digest, and its distinct Final Validation and Bot Artifact
identities. Never treat strategy enhancement as compatibility repair, and never
transfer the original Advisory Validation result to repaired Team Source.
