# Team guide

Each Team works on one shared-repository branch created from the organizer's
Tournament branch. The starter strategy already runs, so you can focus on
changing how it chooses moves.

## Your editing boundary

`team_source/` is the only Team-editable directory. Start with
[`team_source/strategy.py`](team_source/strategy.py), and keep every Team Source
file inside that directory. Do not edit or replace files elsewhere in this
repository, even if Git permits it.

The starter is copied from the catalog's canonical Python template. Contract
tests deliberately keep the two initial files identical; after the organizer
creates Team branches, each Team changes only its `team_source/` copy.

The organizer owns everything outside `team_source/`, including:

- the wrapper (`wrapper.py`), build recipe (`Dockerfile`), fixed entrypoint,
  and dependency definition (`requirements.lock`);
- validation workflows under `.github`;
- Language Environment Catalog metadata such as `catalog.json`; and
- readiness, runtime, conformance, and other Tournament integration files.

These files define the frozen Python Language Environment. Changes to them are
not Team Source and will not be accepted as part of a Submission Candidate.
Third-party Python packages are not available; use Python's standard library.

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

## Shared branch policy

Use the branch name `team/<team-slug>`, where `<team-slug>` is the lowercase
name assigned by the organizer using letters, digits, and hyphens. There is one
branch per Team. Commit and push only changes under `team_source/`; Teams follow
this boundary as an honor policy in the shared repository.

Team branches and their histories are visible to people who can read the
repository. This workflow does not provide submission secrecy. Do not inspect,
copy, or modify another Team's branch, and do not place credentials or other
secrets in Team Source or Git history.
