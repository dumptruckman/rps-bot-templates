# Consume the Runner-owned catalog

Status: resolved

Implementation status: complete (tickets 01-04 resolved)

## Purpose

Make this repository the sole participant-facing home for Team Templates while
consuming, rather than owning, one exact Language Environment Catalog published
by `rps-tournament`.

## Repository seam

One immutable lock identifies the Runner commit, package version, catalog path
and identity, and offline bundle. Template validation materializes that exact
Runner checkout and crosses its public source-validation and certification
interfaces. No catalog asset is maintained a second time here.

## Delivery order

1. Reframe this repository as a pinned catalog consumer.
2. Validate Team Source through the materialized Runner catalog.
3. Remove the duplicate catalog and publish a Template Release.
4. Prove the clean-clone, offline, Advisory-to-Final cutover.

Ticket 02 also requires the Runner-owned catalog release. Ticket 04 requires
both the local Template Release and the Runner's catalog-independence proof.

## Completion

This effort is complete when this repository contains every participant-facing
Team Template and no authoritative catalog copy, a clean clone validates offline
against one pinned Runner catalog identity, and the organizer can Final Validate
the same selected Team Source with that identity.

## Authority effort

The publishing work is tracked in
`rps-tournament/.scratch/catalog-authority/`.
