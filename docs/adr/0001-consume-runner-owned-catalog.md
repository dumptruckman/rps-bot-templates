# Consume the Runner-owned Language Environment Catalog

Status: accepted

This repository owns participant-facing Team Templates and Team guidance, while
`rps-tournament` exclusively owns the Language Environment Catalog and every
organizer-controlled execution asset. A Template Release claims compatibility
with one exact Catalog Release through `core-tool.lock.json` because a one-way,
immutable dependency avoids duplicate catalog authorities while preserving
offline Advisory Validation for Teams.

The transitional `language_environments/` copy and catalog-release tooling are
non-authoritative migration material. They may remain until validation consumes
the materialized Runner catalog, but they cannot publish a new authoritative
Catalog Release.
