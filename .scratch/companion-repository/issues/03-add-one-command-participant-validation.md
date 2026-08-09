# Add one-command participant validation

Status: ready-for-agent

Blocked by: 01, 02

## What to build

Give a Team with Docker one documented command that validates its current Team
Source, builds one native-platform confidence image, runs the participant-local
conformance suite, and completes a practice Match through the pinned core tool.

## Acceptance criteria

- [ ] The command is a thin adapter over the pinned public core commands and contains no independent source-validation, build, protocol, isolation, resource, or scoring logic.
- [ ] The command uses the repository-owned frozen catalog and builds exactly one native platform without a multi-platform image or OCI index.
- [ ] Successful output identifies the Team Source digest, catalog, core tool, suite, recipe, wrapper, runtime, platform, disposable image, and advisory validation result.
- [ ] Diagnostics distinguish source, build, readiness, protocol, determinism, isolation, resource, lifecycle, and Docker-host failures in Team-facing language.
- [ ] A missing local Docker engine points the Team to GitHub advisory validation, and every local result is clearly insufficient for official Tournament entry.
