"""Verify the immutable Catalog Release materialized from the Runner bundle."""

from __future__ import annotations

import configparser
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import subprocess
from typing import Any, Mapping, Sequence


FULL_COMMIT = re.compile(r"^[0-9a-f]{40}$")
CONTENT_IDENTITY = re.compile(r"^[a-z0-9-]+@sha256:[0-9a-f]{64}$")


class CompatibilityError(ValueError):
    """The pinned Catalog Release cannot be safely consumed."""


def _mapping(value: object, label: str) -> Mapping[str, Any]:
    if not isinstance(value, dict):
        raise CompatibilityError(label + " must be a JSON object")
    return value


def _string(value: object, label: str) -> str:
    if not isinstance(value, str) or not value:
        raise CompatibilityError(label + " must be a non-empty string")
    return value


def _exact_keys(value: Mapping[str, Any], expected: Sequence[str], label: str) -> None:
    actual = set(value)
    required = set(expected)
    if actual != required:
        raise CompatibilityError(
            label
            + " fields mismatch: expected "
            + repr(sorted(required))
            + ", got "
            + repr(sorted(actual))
        )


def read_lock(path: Path) -> Mapping[str, Any]:
    try:
        lock = _mapping(json.loads(path.read_text()), "core tool lock")
    except (OSError, json.JSONDecodeError) as error:
        raise CompatibilityError("core tool lock is unreadable: " + str(error)) from error
    _exact_keys(lock, ("format_version", "runner", "catalog", "offline_bundle"), "lock")
    if lock.get("format_version") != "rps-catalog-compatibility-v1":
        raise CompatibilityError("lock format_version is unsupported")
    runner = _mapping(lock.get("runner"), "runner coordinates")
    catalog = _mapping(lock.get("catalog"), "catalog coordinates")
    bundle = _mapping(lock.get("offline_bundle"), "offline bundle coordinates")
    _exact_keys(runner, ("commit", "package_version"), "runner coordinates")
    _exact_keys(catalog, ("path", "identity", "assets"), "catalog coordinates")
    _exact_keys(bundle, ("identity",), "offline bundle coordinates")
    if not FULL_COMMIT.fullmatch(_string(runner.get("commit"), "Runner commit")):
        raise CompatibilityError("Runner commit must be a full immutable Git SHA")
    _string(runner.get("package_version"), "Runner package version")
    _catalog_relative_path(_string(catalog.get("path"), "catalog path"))
    if not CONTENT_IDENTITY.fullmatch(_string(catalog.get("identity"), "catalog identity")):
        raise CompatibilityError("catalog identity must be a full content identity")
    assets = _mapping(catalog.get("assets"), "catalog asset identities")
    if not assets:
        raise CompatibilityError("catalog asset identities must not be empty")
    for name, identity in assets.items():
        if not isinstance(name, str) or "." not in name:
            raise CompatibilityError("catalog asset identity key is invalid")
        if not CONTENT_IDENTITY.fullmatch(_string(identity, "catalog asset identity")):
            raise CompatibilityError("catalog asset identity must be immutable")
    if not CONTENT_IDENTITY.fullmatch(
        _string(bundle.get("identity"), "offline bundle identity")
    ):
        raise CompatibilityError("offline bundle identity must be a full content identity")
    return lock


def verify_independence_evidence(
    value: object,
    expected_coordinates: Mapping[str, Any] | None = None,
) -> Mapping[str, Any]:
    evidence = _mapping(value, "Runner evidence")
    if evidence.get("evidence_format_version") != "runner-catalog-independence-v1":
        raise CompatibilityError("Runner evidence format is unsupported")
    if evidence.get("status") != "passed":
        raise CompatibilityError("Runner catalog independence has not passed")
    coordinates = _mapping(
        evidence.get("compatibility_coordinates"), "compatibility coordinates"
    )
    if expected_coordinates is not None and coordinates != expected_coordinates:
        raise CompatibilityError(
            "Runner and Template compatibility coordinates differ"
        )

    release = _mapping(evidence.get("catalog_release"), "Catalog Release evidence")
    manifest = _mapping(release.get("manifest"), "Catalog Release manifest")
    if manifest.get("compatibility_coordinates") != coordinates:
        raise CompatibilityError(
            "Catalog Release manifest and independence coordinates differ"
        )

    scan = _mapping(evidence.get("repository_scan"), "Runner repository scan")
    if scan.get("companion_repository") != "absent":
        raise CompatibilityError(
            "Runner independence evidence includes the companion repository"
        )
    empty_evidence = (
        (scan, "dependency_matches", "reverse Runner dependency"),
        (scan, "participant_template_paths", "Runner Team Template path"),
        (release, "participant_template_asset_paths", "participant catalog asset"),
        (release, "participant_template_digest_fields", "Team Template digest"),
        (release, "participant_template_paths", "bundled Team Template path"),
        (release, "unowned_catalog_paths", "unowned catalog path"),
    )
    for container, field, label in empty_evidence:
        if container.get(field) != []:
            raise CompatibilityError(
                label + " remains in Runner independence evidence"
            )
    workflows = _mapping(
        evidence.get("organizer_workflows"), "organizer workflow evidence"
    )
    if workflows.get("status") != "passed":
        raise CompatibilityError("Runner organizer workflow proof has not passed")
    return coordinates


def read_independence_evidence(path: Path) -> Mapping[str, Any]:
    try:
        value = json.loads(path.read_text())
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as error:
        raise CompatibilityError(
            "Runner evidence is unreadable: " + str(error)
        ) from error
    verify_independence_evidence(value)
    return _mapping(value, "Runner evidence")


def _catalog_relative_path(value: str) -> PurePosixPath:
    path = PurePosixPath(value)
    if (
        path.is_absolute()
        or not path.parts
        or any(part in ("", ".", "..") for part in path.parts)
        or "\\" in value
    ):
        raise CompatibilityError("catalog path must be a safe repository-relative POSIX path")
    return path


def verify_bundle(bundle_path: Path, lock: Mapping[str, Any]) -> None:
    expected = _mapping(lock["offline_bundle"], "offline bundle coordinates")["identity"]
    try:
        actual = (
            "rps-runner-offline-bundle-v1@sha256:"
            + hashlib.sha256(bundle_path.read_bytes()).hexdigest()
        )
    except OSError as error:
        raise CompatibilityError("offline bundle is unreadable: " + str(error)) from error
    if actual != expected:
        raise CompatibilityError(
            "offline bundle identity mismatch: expected "
            + str(expected)
            + ", got "
            + actual
        )


def _git(checkout: Path, *arguments: str) -> str:
    completed = subprocess.run(
        ["git", "-C", str(checkout), *arguments],
        capture_output=True,
        text=True,
    )
    if completed.returncode != 0:
        raise CompatibilityError(
            "materialized Runner checkout is unreadable: "
            + (completed.stderr.strip() or completed.stdout.strip() or "git failed")
        )
    return completed.stdout.strip()


def _package_version(checkout: Path) -> str:
    configuration = configparser.ConfigParser()
    try:
        with (checkout / "setup.cfg").open() as stream:
            configuration.read_file(stream)
    except (OSError, configparser.Error) as error:
        raise CompatibilityError("Runner package version is unreadable: " + str(error)) from error
    version = configuration.get("metadata", "version", fallback="")
    if not version:
        raise CompatibilityError("Runner package version is missing from setup.cfg")
    return version


def _asset_identities(catalog_path: Path, catalog: Mapping[str, Any]) -> Mapping[str, str]:
    environments = _mapping(catalog.get("environments"), "catalog environments")
    result = {}
    catalog_root = catalog_path.parent.resolve()
    for environment_name, raw_environment in environments.items():
        environment = _mapping(raw_environment, "catalog environment " + str(environment_name))
        assets = _mapping(environment.get("assets"), "catalog assets")
        for asset_name, raw_asset in assets.items():
            asset = _mapping(raw_asset, "catalog asset")
            version = _string(asset.get("version"), "catalog asset version")
            relative = _catalog_relative_path(_string(asset.get("path"), "catalog asset path"))
            declared_digest = _string(asset.get("sha256"), "catalog asset digest")
            asset_path = catalog_path.parent / relative
            if asset_path.is_symlink():
                raise CompatibilityError("catalog asset path must not be a symbolic link")
            try:
                asset_path.resolve().relative_to(catalog_root)
                content = asset_path.read_bytes()
            except (OSError, ValueError) as error:
                raise CompatibilityError("catalog asset is missing or unreadable: " + str(error)) from error
            if not asset_path.is_file():
                raise CompatibilityError("catalog asset path must name a regular file")
            actual_digest = "sha256:" + hashlib.sha256(content).hexdigest()
            if actual_digest != declared_digest:
                raise CompatibilityError(
                    "catalog asset content digest mismatch for "
                    + str(environment_name)
                    + "."
                    + str(asset_name)
                )
            result[str(environment_name) + "." + str(asset_name)] = version + "@" + actual_digest
    return result


def verify_checkout(checkout: Path, lock: Mapping[str, Any]) -> Path:
    runner = _mapping(lock["runner"], "runner coordinates")
    catalog_claim = _mapping(lock["catalog"], "catalog coordinates")
    expected_commit = str(runner["commit"])
    actual_commit = _git(checkout, "rev-parse", "HEAD")
    if actual_commit != expected_commit:
        raise CompatibilityError(
            "Runner commit mismatch: expected " + expected_commit + ", got " + actual_commit
        )
    if _git(checkout, "status", "--porcelain"):
        raise CompatibilityError(
            "materialized Runner checkout has tracked modifications; restore commit "
            + expected_commit
        )
    actual_version = _package_version(checkout)
    if actual_version != runner["package_version"]:
        raise CompatibilityError(
            "Runner package version mismatch: expected "
            + str(runner["package_version"])
            + ", got "
            + actual_version
        )
    relative_catalog = _catalog_relative_path(str(catalog_claim["path"]))
    catalog_path = checkout / relative_catalog
    if catalog_path.is_symlink():
        raise CompatibilityError("catalog path must not be a symbolic link")
    try:
        catalog_path.resolve().relative_to(checkout.resolve())
        catalog = _mapping(json.loads(catalog_path.read_text()), "materialized catalog")
    except (OSError, ValueError, json.JSONDecodeError) as error:
        raise CompatibilityError("catalog path is missing or unreadable: " + str(error)) from error
    version = _string(catalog.get("catalog_version"), "catalog version")
    canonical = json.dumps(catalog, sort_keys=True, separators=(",", ":")).encode("utf-8")
    actual_identity = version + "@sha256:" + hashlib.sha256(canonical).hexdigest()
    if actual_identity != catalog_claim["identity"]:
        raise CompatibilityError(
            "catalog identity mismatch: expected "
            + str(catalog_claim["identity"])
            + ", got "
            + actual_identity
        )
    actual_assets = _asset_identities(catalog_path, catalog)
    if actual_assets != catalog_claim["assets"]:
        raise CompatibilityError("catalog asset identities mismatch")
    return catalog_path
