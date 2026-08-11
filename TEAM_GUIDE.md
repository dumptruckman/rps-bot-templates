# Team guide

Each Team works on one shared-repository branch created from the organizer's
Tournament branch. The starter strategy already runs, so you can focus on
changing how it chooses moves.

## Your editing boundary

`team_source/` is the only Team-editable directory. Start with
[`team_source/strategy.py`](team_source/strategy.py), and keep every Team Source
file inside that directory. Do not edit or replace files elsewhere in this
repository, even if Git permits it.

The starter is the participant-facing Python Team Template. It claims
compatibility with the exact Catalog Release in `core-tool.lock.json`; it is not
a catalog-owned execution asset. After the organizer creates Team branches,
each Team changes only its `team_source/` copy.

The organizer controls everything outside `team_source/`. The authoritative
versions of these execution assets are owned by `rps-tournament`, including:

- the wrapper (`wrapper.py`), build recipe (`Dockerfile`), fixed entrypoint,
  and dependency definition (`requirements.lock`);
- validation workflows under `.github`;
- Language Environment Catalog metadata such as `catalog.json`; and
- readiness, runtime, conformance, and other Tournament integration files.

Local copies retained during the catalog-consumer cutover are not a second
authority. Organizer-owned paths are never part of Team Source and changes to
them will not be accepted as part of a Submission Candidate. Third-party Python
packages are not available; use Python's standard library.

## Strategy contract

Your `strategy.py` must define this function exactly once and unconditionally:

```python
def choose_move(turn, my_history, opponent_history, rng):
    return rng.choice(("R", "P", "S"))
```

The arguments are:

- `turn`: the current turn number, beginning with `1`;
- `my_history`: your earlier moves, oldest first;
- `opponent_history`: the other Team's earlier moves, oldest first; and
- `rng`: the wrapper-provided deterministic random generator.

Use `rng` for every random decision. Do not create another random generator or
use system randomness. Only `R`, `P`, or `S` is a valid return value.

The organizer-owned wrapper handles protocol I/O, readiness, seeding, and
process lifecycle. Team Source should only implement strategy behavior; it must
not read protocol messages from standard input, print moves directly, emit a
readiness marker, or manage the process.

## Additional Team Source

You may add:

- Python modules at any path under `team_source/`; and
- `.csv`, `.json`, or `.txt` data under `team_source/resources/`, including
  nested resource directories.

The complete Team Source is limited to 64 files, 256 KiB per file, and 1 MiB
total. `team_source/strategy.py` is required. Symbolic links and paths outside
the editing boundary are rejected. Dependency files, wrappers, container
recipes, entrypoints, workflows, and catalog metadata are not approved Team
Source.

## Validate your Team Source

With a local Docker engine running, validate the current `team_source/` with:

```sh
./validate-team
```

The command uses the compatibility claim in `core-tool.lock.json`. On every use
it verifies the content-addressed `core-tool.bundle`, exact clean Runner commit,
package version, catalog path, catalog identity, and all catalog asset
identities. It materializes the Runner under `.core/rps-tournament` on first use
without downloading packages or cloning a private repository, then reads the
catalog from that verified checkout. A maintainer may set `RPS_CORE_PATH` to an
equivalent exact clean checkout; the same verification still applies. The
pinned base runtime for your Docker server's native `linux/amd64` or
`linux/arm64` platform must already be present in that Docker context.

The command validates and freezes Team Source, builds one confidence image for
the Docker server's native platform, runs the participant-local conformance
suite, and completes its practice Matches. Its summary identifies every frozen
input and the disposable local image. Source, build, readiness, protocol,
determinism, isolation, resource, lifecycle, and Docker-host failures are
reported separately.

GitHub automatically checks every commit pushed to a `team/**` branch on native
Linux/AMD64. The check materializes the bundled Runner, verifies the complete
locked Catalog Release, and uses only its catalog while checking the exact
source commit. It builds one disposable `linux/amd64` confidence image and never
publishes that image. A practice Match proves protocol compatibility, but its
score or winner does not affect whether an otherwise conforming Submission
Candidate passes.

The Actions run summary shows the result. Its `team-advisory-<commit>` artifact
retains commit-specific eligibility evidence and the conformance report for 90
days, including the Source Digest and every frozen validation identity. A newer
push cancels a superseded in-progress run on the same Team branch without
removing the latest completed green candidate or its evidence.

Participant-local validation is Advisory Validation only. It is insufficient
for official Tournament entry and cannot produce an official Bot Artifact. If
Docker is unavailable locally, push your Team branch and use GitHub Advisory
Validation instead; that result is also insufficient for official Tournament
entry. Only organizer Final Validation can accept a Bot Artifact.

Before the declared deadline, note the full SHA of any earlier green commit you
want selected instead of your latest completed green commit. The organizer uses
the [submission cutoff and manual handoff policy](SUBMISSION_CUTOFF.md) to select
and export the exact Team Source. A GitHub result remains advisory after
selection; only organizer Final Validation of a newly built ARM64 image can
accept a Bot Artifact.

## Shared branch policy

Use the branch name `team/<team-slug>`, where `<team-slug>` is the lowercase
name assigned by the organizer using letters, digits, and hyphens. There is one
branch per Team. Commit and push only changes under `team_source/`; Teams follow
this boundary as an honor policy in the shared repository.

Team branches and their histories are visible to people who can read the
repository. This workflow does not provide submission secrecy. Do not inspect,
copy, or modify another Team's branch, and do not place credentials or other
secrets in Team Source or Git history.
