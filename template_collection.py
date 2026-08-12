"""Discover and validate repository-owned Team Template descriptors."""

from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path, PurePosixPath
import re
from typing import Any, Dict, Mapping, Optional, Sequence, Tuple


INDEX_NAME = "team-templates.json"
LANGUAGE_ID = re.compile(r"^[a-z][a-z0-9-]*$")
FULL_DIGEST = re.compile(r"^sha256:[0-9a-f]{64}$")
TAG_NAME = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]*$")


class CollectionError(ValueError):
    """The Team Template collection is unsafe, incomplete, or ambiguous."""


@dataclass(frozen=True)
class TeamTemplate:
    language_id: str
    language_environment: str
    descriptor_path: Path
    team_source_path: Path
    participant_guidance_path: Path
    build_and_test_entrypoint: Path
    version: str
    expected_source_digest: str
    release_tag: str
    advisory_validation_workflow: Path


@dataclass(frozen=True)
class TemplateCollection:
    templates: Mapping[str, TeamTemplate]

    @property
    def language_ids(self) -> Tuple[str, ...]:
        return tuple(sorted(self.templates))

    def select(self, language_id: Optional[str] = None) -> TeamTemplate:
        available = ", ".join(self.language_ids)
        if language_id is None:
            if len(self.templates) != 1:
                raise CollectionError(
                    "Team Template selection is ambiguous; select one of: " + available
                )
            return next(iter(self.templates.values()))
        try:
            return self.templates[language_id]
        except KeyError as error:
            raise CollectionError(
                "unknown Team Template " + repr(language_id) + "; available: " + available
            ) from error


def _object(value: object, label: str) -> Mapping[str, Any]:
    if not isinstance(value, dict):
        raise CollectionError(label + " must be a JSON object")
    return value


def _string(value: object, label: str) -> str:
    if not isinstance(value, str) or not value:
        raise CollectionError(label + " must be a non-empty string")
    return value


def _exact_keys(value: Mapping[str, Any], expected: Sequence[str], label: str) -> None:
    if set(value) != set(expected):
        raise CollectionError(label + " fields mismatch")


def _read_object(path: Path, label: str) -> Mapping[str, Any]:
    try:
        return _object(json.loads(path.read_text()), label)
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as error:
        raise CollectionError(label + " is missing or unreadable: " + str(error)) from error


def _relative_path(value: object, label: str) -> Path:
    raw = _string(value, label)
    path = PurePosixPath(raw)
    if (
        path.is_absolute()
        or not path.parts
        or any(part in ("", ".", "..") for part in path.parts)
        or "\\" in raw
    ):
        raise CollectionError(label + " must be a safe repository-relative POSIX path")
    return Path(*path.parts)


def _reject_symlink_components(root: Path, relative: Path, label: str) -> None:
    candidate = root
    for part in relative.parts:
        candidate = candidate / part
        if candidate.is_symlink():
            raise CollectionError(label + " must not traverse a symbolic link")


def _repository_path(
    root: Path, value: object, label: str, *, directory: bool = False
) -> Path:
    relative = _relative_path(value, label)
    candidate = root / relative
    _reject_symlink_components(root, relative, label)
    try:
        candidate.resolve().relative_to(root.resolve())
    except (OSError, ValueError) as error:
        raise CollectionError(label + " must stay inside the repository") from error
    if directory and not candidate.is_dir():
        raise CollectionError(label + " must name an existing directory")
    if not directory and not candidate.is_file():
        raise CollectionError(label + " must name an existing regular file")
    return relative


def _descriptor(root: Path, entry: Mapping[str, Any]) -> TeamTemplate:
    _exact_keys(entry, ("language_id", "descriptor"), "Team Template index entry")
    indexed_id = _string(entry.get("language_id"), "indexed language ID")
    if not LANGUAGE_ID.fullmatch(indexed_id):
        raise CollectionError("indexed language ID is not stable")
    descriptor_relative = _relative_path(entry.get("descriptor"), "descriptor path")
    descriptor_path = root / descriptor_relative
    _reject_symlink_components(root, descriptor_relative, "descriptor path")
    try:
        descriptor_path.resolve().relative_to(root.resolve())
    except (OSError, ValueError) as error:
        raise CollectionError("descriptor path must stay inside the repository") from error
    if not descriptor_path.is_file():
        raise CollectionError(
            "missing descriptor for language ID " + repr(indexed_id) + ": "
            + descriptor_relative.as_posix()
        )
    raw = _read_object(descriptor_path, "Team Template descriptor")
    fields = (
        "format_version",
        "language_id",
        "language_environment",
        "team_source_path",
        "participant_guidance_path",
        "build_and_test_entrypoint",
        "version",
        "expected_source_digest",
        "release_tag",
        "advisory_validation_workflow",
    )
    _exact_keys(raw, fields, "Team Template descriptor")
    if raw.get("format_version") != "rps-team-template-descriptor-v1":
        raise CollectionError("Team Template descriptor format is unsupported")
    described_id = _string(raw.get("language_id"), "descriptor language ID")
    if described_id != indexed_id:
        raise CollectionError("indexed and described language IDs differ")
    environment = _string(raw.get("language_environment"), "Language Environment")
    if not LANGUAGE_ID.fullmatch(environment):
        raise CollectionError("Language Environment ID is not stable")
    version = _string(raw.get("version"), "Team Template version")
    digest = _string(raw.get("expected_source_digest"), "expected Source Digest")
    if not FULL_DIGEST.fullmatch(digest):
        raise CollectionError("expected Source Digest is invalid")
    release_tag = _string(raw.get("release_tag"), "Template Release tag")
    if not TAG_NAME.fullmatch(release_tag):
        raise CollectionError("Template Release tag is invalid")
    return TeamTemplate(
        language_id=indexed_id,
        language_environment=environment,
        descriptor_path=descriptor_relative,
        team_source_path=_repository_path(
            root, raw.get("team_source_path"), "Team Source path", directory=True
        ),
        participant_guidance_path=_repository_path(
            root, raw.get("participant_guidance_path"), "participant guidance path"
        ),
        build_and_test_entrypoint=_repository_path(
            root, raw.get("build_and_test_entrypoint"), "build-and-test entrypoint"
        ),
        version=version,
        expected_source_digest=digest,
        release_tag=release_tag,
        advisory_validation_workflow=_repository_path(
            root,
            raw.get("advisory_validation_workflow"),
            "Advisory Validation workflow path",
        ),
    )


def _verify_catalog(
    templates: Mapping[str, TeamTemplate], catalog_path: Path
) -> None:
    catalog = _read_object(catalog_path, "pinned Catalog Release")
    environments = _object(catalog.get("environments"), "catalog environments")
    for template in templates.values():
        raw_environment = environments.get(template.language_environment)
        if raw_environment is None:
            raise CollectionError(
                "Language Environment "
                + repr(template.language_environment)
                + " is absent from the pinned Catalog Release"
            )
        environment = _object(raw_environment, "Language Environment descriptor")
        if environment.get("language") != template.language_environment:
            raise CollectionError("Language Environment identity does not match its catalog key")
        if environment.get("contract_only") is not False:
            raise CollectionError(
                "Language Environment "
                + repr(template.language_environment)
                + " is not supported for Teams in the pinned Catalog Release"
            )


def load_collection(
    root: Path, catalog_path: Path, index_path: Optional[Path] = None
) -> TemplateCollection:
    """Load the index and reject any template not supported by the pinned catalog."""

    repository = root.resolve()
    if index_path is None:
        index_relative = Path(INDEX_NAME)
    elif index_path.is_absolute():
        try:
            index_relative = index_path.relative_to(repository)
        except ValueError as error:
            raise CollectionError("Team Template index must stay inside the repository") from error
    else:
        index_relative = _relative_path(index_path.as_posix(), "Team Template index path")
    _reject_symlink_components(repository, index_relative, "Team Template index path")
    path = repository / index_relative
    index = _read_object(path, "Team Template index")
    _exact_keys(index, ("format_version", "templates"), "Team Template index")
    if index.get("format_version") != "rps-team-template-index-v1":
        raise CollectionError("Team Template index format is unsupported")
    entries = index.get("templates")
    if not isinstance(entries, list) or not entries:
        raise CollectionError("Team Template index must contain at least one entry")
    templates: Dict[str, TeamTemplate] = {}
    for value in entries:
        entry = _object(value, "Team Template index entry")
        language_id = _string(entry.get("language_id"), "indexed language ID")
        if language_id in templates:
            raise CollectionError("duplicate language ID " + repr(language_id))
        template = _descriptor(repository, entry)
        templates[language_id] = template
    _verify_catalog(templates, catalog_path)
    return TemplateCollection(templates)
