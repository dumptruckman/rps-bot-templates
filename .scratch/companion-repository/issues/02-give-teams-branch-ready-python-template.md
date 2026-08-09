# Give each Team a branch-ready Python template

Status: resolved

Blocked by: 01

## What to build

Let a Team start from an organizer-owned Python example on its own
shared-repository branch, edit only controlled Team Source, and receive fast
static feedback without learning container or Tournament internals.

## Acceptance criteria

- [x] A fresh Team branch contains a working Python strategy that demonstrates the four-argument `choose_move` contract and uses the wrapper-provided deterministic random generator.
- [x] Teams can add approved Python modules and controlled CSV, JSON, or text resources within the catalog's size, count, and path limits.
- [x] The editable Team Source boundary is unmistakable; wrappers, recipes, entrypoints, dependency definitions, workflows, and catalog metadata remain organizer-owned.
- [x] The template explains that only `R`, `P`, or `S` is a valid move and that the wrapper owns protocol I/O, readiness, seeding, and process lifecycle.
- [x] The shared-branch honor policy and branch naming convention allow one branch per Team without claiming submission secrecy.

## Answer

Added a branch-ready `team_source/strategy.py` synchronized with the frozen
catalog template, plus a Team guide that defines the sole editing boundary,
strategy and resource contracts, catalog limits, organizer ownership, branch
naming, honor policy, and lack of submission secrecy. Contract tests exercise
the starter through the organizer wrapper and prove approved modules and
resources pass the pinned core's Team Source validation.
