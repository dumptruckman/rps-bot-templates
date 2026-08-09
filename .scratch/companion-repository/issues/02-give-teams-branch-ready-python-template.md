# Give each Team a branch-ready Python template

Status: ready-for-agent

Blocked by: 01

## What to build

Let a Team start from an organizer-owned Python example on its own
shared-repository branch, edit only controlled Team Source, and receive fast
static feedback without learning container or Tournament internals.

## Acceptance criteria

- [ ] A fresh Team branch contains a working Python strategy that demonstrates the four-argument `choose_move` contract and uses the wrapper-provided deterministic random generator.
- [ ] Teams can add approved Python modules and controlled CSV, JSON, or text resources within the catalog's size, count, and path limits.
- [ ] The editable Team Source boundary is unmistakable; wrappers, recipes, entrypoints, dependency definitions, workflows, and catalog metadata remain organizer-owned.
- [ ] The template explains that only `R`, `P`, or `S` is a valid move and that the wrapper owns protocol I/O, readiness, seeding, and process lifecycle.
- [ ] The shared-branch honor policy and branch naming convention allow one branch per Team without claiming submission secrecy.
