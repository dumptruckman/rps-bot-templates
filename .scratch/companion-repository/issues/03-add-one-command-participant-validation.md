# Add one-command participant validation

Status: resolved

Blocked by: 01, 02

## What to build

Give a Team with Docker one documented command that validates its current Team
Source, builds one native-platform confidence image, runs the participant-local
conformance suite, and completes a practice Match through the pinned core tool.

## Acceptance criteria

- [x] The command is a thin adapter over the pinned public core commands and contains no independent source-validation, build, protocol, isolation, resource, or scoring logic.
- [x] The command uses the repository-owned frozen catalog and builds exactly one native platform without a multi-platform image or OCI index.
- [x] Successful output identifies the Team Source digest, catalog, core tool, suite, recipe, wrapper, runtime, platform, disposable image, and advisory validation result.
- [x] Diagnostics distinguish source, build, readiness, protocol, determinism, isolation, resource, lifecycle, and Docker-host failures in Team-facing language.
- [x] A missing local Docker engine points the Team to GitHub advisory validation, and every local result is clearly insufficient for official Tournament entry.

## Answer

Added the executable `./validate-team` adapter. It verifies the immutable core
checkout and local Docker host, selects the Docker server's one native platform,
then delegates Team Source freezing, candidate building, the participant-local
conformance suite, and practice Matches to the pinned core commands. Its summary
reports every required frozen identity and the disposable confidence image, and
its Team-facing diagnostics separate all requested failure areas while preserving
the boundary between Advisory Validation and official Tournament entry. The Team
guide documents the one-command workflow, prerequisites, GitHub fallback, and
authority limit.
