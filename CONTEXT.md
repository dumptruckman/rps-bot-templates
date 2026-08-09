# RPS Bot Templates

This context describes the shared repository in which Teams develop source for
Bot Artifacts that play in a Rock–Paper–Scissors Tournament.

## Language

**Tournament**:
The complete competition for one accepted roster, comprising qualification and
playoffs and, unless no eligible Team remains, one Tournament Champion.
_Avoid_: Event, competition run

**Team**:
The competitive identity that owns one Tournament entry, appears in standings,
and may become Tournament Champion.
_Avoid_: Bot, participant, player, entrant

**Team Source**:
The Team-editable files accepted as build input under a Language Environment's
controlled source schema. Team Source is not itself a Bot Artifact.
_Avoid_: Bot Artifact, participant Docker image

**Submission Candidate**:
A specific Team Source commit that passed advisory validation and is eligible
for organizer selection under the cutoff policy. It is not an official Bot
Artifact.
_Avoid_: Bot Artifact, winning submission

**Language Environment**:
A versioned organizer-owned package containing the Team Source schema, template,
platform runtimes, build recipe, wrapper, Seed Adapter, readiness behavior,
entrypoint, and conformance fixtures for one supported language.
_Avoid_: Runtime, Team branch, Docker image

**Language Environment Catalog**:
The immutable event-facing collection of supported Language Environments frozen
before Team coding begins.
_Avoid_: Dependency registry, mutable latest catalog

**Bot Artifact**:
The immutable, single-platform container image built and accepted by the
organizer for a Team in one Tournament. Team-built and GitHub-built images are
confidence artifacts only.
_Avoid_: Team Source, submission, Team

**Advisory Validation**:
Compatibility evidence from participant-local or GitHub/AMD64 execution of the
versioned core conformance suite. It cannot authorize Tournament entry.
_Avoid_: Final Validation, official build

**Final Validation**:
The organizer's authoritative local ARM64 build and conformance result for the
exact selected Team Source and frozen Language Environment Catalog.
_Avoid_: GitHub check, advisory validation

**Source Digest**:
The deterministic identity of validated Team Source contents, independent of a
branch name, repository URL, or mutable working directory.
_Avoid_: Git commit, Bot Artifact digest

**Seed Adapter**:
The versioned part of an organizer-owned language wrapper that deterministically
maps a bot-visible 64-bit seed into that language's random-number generator.
_Avoid_: Seed derivation, system randomness

**Bot-visible Seed**:
The deterministic per-Team seed supplied to a Bot Artifact's Seed Adapter for
one Match.
_Avoid_: Tournament Seed, shared seed
