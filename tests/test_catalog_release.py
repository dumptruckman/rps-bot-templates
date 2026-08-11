from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import tempfile
import unittest


PROJECT_ROOT = Path(__file__).resolve().parents[1]
COMMAND = PROJECT_ROOT / "freeze-tournament-catalog"
RUNBOOK = PROJECT_ROOT / "CATALOG_RELEASE.md"
CORE_LOCK = json.loads((PROJECT_ROOT / "core-tool.lock.json").read_text())


class CatalogReleaseTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.temporary_directory = tempfile.TemporaryDirectory()
        cls.core_path = Path(cls.temporary_directory.name) / "rps-tournament"
        subprocess.run(
            [str(PROJECT_ROOT / "materialize-core-tool"), str(cls.core_path)],
            check=True,
            capture_output=True,
            text=True,
        )

    @classmethod
    def tearDownClass(cls) -> None:
        cls.temporary_directory.cleanup()

    def run_command(self, *arguments: str) -> subprocess.CompletedProcess[str]:
        environment = os.environ.copy()
        environment["RPS_CORE_PATH"] = str(self.core_path)
        return subprocess.run(
            [str(COMMAND), *arguments],
            cwd=PROJECT_ROOT,
            env=environment,
            capture_output=True,
            text=True,
        )

    def make_release_repository(self, suffix: str = "") -> Path:
        name = self.id().rsplit(".", 1)[-1] + suffix
        repository = Path(self.temporary_directory.name) / name
        shutil.copytree(
            PROJECT_ROOT,
            repository,
            ignore=shutil.ignore_patterns(
                ".git", ".core", ".scratch", "__pycache__", "*.pyc"
            ),
        )
        subprocess.run(["git", "init", "--quiet"], cwd=repository, check=True)
        subprocess.run(
            ["git", "config", "user.name", "Catalog Release Test"],
            cwd=repository,
            check=True,
        )
        subprocess.run(
            ["git", "config", "user.email", "catalog-release@example.invalid"],
            cwd=repository,
            check=True,
        )
        subprocess.run(
            ["git", "config", "commit.gpgsign", "false"],
            cwd=repository,
            check=True,
        )
        subprocess.run(
            ["git", "config", "tag.gpgsign", "true"],
            cwd=repository,
            check=True,
        )
        subprocess.run(["git", "add", "."], cwd=repository, check=True)
        subprocess.run(
            ["git", "commit", "--quiet", "-m", "frozen catalog"],
            cwd=repository,
            check=True,
        )
        return repository

    def run_repository_command(
        self, repository: Path, *arguments: str
    ) -> subprocess.CompletedProcess[str]:
        environment = os.environ.copy()
        environment["RPS_CORE_PATH"] = str(self.core_path)
        return subprocess.run(
            [str(repository / COMMAND.name), *arguments],
            cwd=repository,
            env=environment,
            capture_output=True,
            text=True,
        )

    def test_manifest_records_every_frozen_release_identity(self) -> None:
        completed = self.run_command("manifest", "catalog-v1")

        self.assertEqual(completed.returncode, 0, completed.stderr)
        manifest = json.loads(completed.stdout)
        self.assertEqual(manifest["release_format_version"], "catalog-release-v1")
        self.assertEqual(manifest["repository"]["tag"], "catalog-v1")
        self.assertRegex(manifest["repository"]["commit"], r"^[0-9a-f]{40}$")
        self.assertEqual(
            manifest["catalog"]["identity"],
            "rps-language-environment-catalog-v1@sha256:"
            "ac97b994172403f0b6b8918a9712a0a3c6ff443012ee2e469369ad4a366d280c",
        )
        self.assertEqual(manifest["core_tool"]["pin"], CORE_LOCK)
        self.assertEqual(
            manifest["core_tool"]["identity"],
            "rps-core-tool-v1@sha256:"
            "2670b046b4aad97137e07692ace180b4a1ccd6c0cabf3763a9762b7a91c92b0a",
        )
        self.assertEqual(
            manifest["conformance_suite"]["identity"],
            "python-artifact-conformance-v1@sha256:"
            "17cf3871a7ad4bf420a9cf68280c445055fcb77c73bdfcc9e441e6fc9eb4f49c",
        )
        self.assertEqual(
            manifest["execution_profile"]["identity"],
            "docker-execution-v1@sha256:"
            "54b69b7eae0b15191a13b2b14fcc75c4537358b971b8f84a65731589b8ad3bb1",
        )
        python = manifest["language_environments"]["python"]
        self.assertEqual(python["wrapper"]["version"], "python-wrapper-v3")
        self.assertEqual(python["recipe"]["version"], "python-build-recipe-v1")
        self.assertEqual(
            set(python["runtimes"]), {"linux/amd64", "linux/arm64"}
        )
        self.assertEqual(
            python["runtimes"]["linux/amd64"]["digest"],
            "sha256:69e18bd8d831d88e0ef70239dc7771ab7c28bc296ae78ac75cde71e60aa4434f",
        )
        self.assertEqual(
            python["runtimes"]["linux/arm64"]["digest"],
            "sha256:8c5de2243cba89f49a93e05cacb78e27058bcaa69c148baac127005da03af39e",
        )
        self.assertTrue(python["dependencies"]["standard_library_only"])
        self.assertFalse(python["dependencies"]["build_time_downloads"])

    def test_create_and_verify_use_an_annotated_tag_as_the_release_record(self) -> None:
        repository = self.make_release_repository()

        created = self.run_repository_command(repository, "create", "catalog-v1")
        self.assertEqual(created.returncode, 0, created.stderr)
        target = subprocess.run(
            ["git", "rev-parse", "catalog-v1^{}"],
            cwd=repository,
            check=True,
            capture_output=True,
            text=True,
        ).stdout.strip()
        self.assertEqual(json.loads(created.stdout)["repository"]["commit"], target)
        self.assertEqual(
            subprocess.run(
                ["git", "cat-file", "-t", "catalog-v1"],
                cwd=repository,
                check=True,
                capture_output=True,
                text=True,
            ).stdout.strip(),
            "tag",
        )

        verified = self.run_repository_command(repository, "verify", "catalog-v1")
        self.assertEqual(verified.returncode, 0, verified.stderr)
        self.assertEqual(json.loads(verified.stdout), json.loads(created.stdout))

    def test_manifest_rejects_every_mutable_release_input(self) -> None:
        def update_asset_digest(repository: Path, asset_name: str) -> None:
            catalog_path = repository / "language_environments/catalog-v1/catalog.json"
            catalog = json.loads(catalog_path.read_text())
            asset = catalog["environments"]["python"]["assets"][asset_name]
            content = (catalog_path.parent / asset["path"]).read_bytes()
            asset["sha256"] = "sha256:" + hashlib.sha256(content).hexdigest()
            catalog_path.write_text(json.dumps(catalog, indent=2) + "\n")

        cases = {}

        core_repository = self.make_release_repository("-core")
        core_lock = core_repository / "core-tool.lock.json"
        core = json.loads(core_lock.read_text())
        core["runner"]["commit"] = "main"
        core_lock.write_text(json.dumps(core, indent=2) + "\n")
        cases["core"] = (core_repository, "full 40-character commit")

        runtime_repository = self.make_release_repository("-runtime")
        runtimes = runtime_repository / "language_environments/catalog-v1/python/runtimes.json"
        runtime_data = json.loads(runtimes.read_text())
        runtime_data["platforms"]["linux/amd64"]["image"] = "python:latest"
        runtimes.write_text(json.dumps(runtime_data, indent=2) + "\n")
        update_asset_digest(runtime_repository, "base_runtime")
        update_asset_digest(runtime_repository, "platform")
        cases["runtime"] = (runtime_repository, "not pinned by full digest")

        action_repository = self.make_release_repository("-action")
        workflow = action_repository / ".github/workflows/catalog-contract.yml"
        workflow.write_text(
            workflow.read_text().replace(
                "actions/checkout@11bd71901bbe5b1630ceea73d27597364c9af683",
                "actions/checkout@v4",
            )
        )
        cases["action"] = (action_repository, "mutable action ref")

        dependency_repository = self.make_release_repository("-dependency")
        dependencies = (
            dependency_repository
            / "language_environments/catalog-v1/python/requirements.lock"
        )
        dependencies.write_text("requests==2.32.0\n")
        update_asset_digest(dependency_repository, "dependency_definition")
        cases["dependency"] = (dependency_repository, "standard-library-only")

        bundle_repository = self.make_release_repository("-bundle")
        bundle = bundle_repository / "core-tool.bundle"
        bundle.write_bytes(bundle.read_bytes() + b"mutable")
        cases["bundled core"] = (bundle_repository, "bundle digest")

        for name, (repository, diagnostic) in cases.items():
            with self.subTest(input=name):
                completed = self.run_repository_command(
                    repository, "manifest", "catalog-v1"
                )
                self.assertNotEqual(completed.returncode, 0)
                self.assertIn(diagnostic, completed.stderr)

    def test_release_runbook_covers_clean_clone_team_reproduction_and_freeze_policy(self) -> None:
        normalized = " ".join(RUNBOOK.read_text().split())

        for statement in (
            "before Team coding begins",
            "git clone",
            "git switch --create team/<team-slug> catalog-v1",
            "./validate-team",
            "team-advisory-<commit>",
            "Submission Candidate",
            "disposable advisory image",
            "canonical organizer-built Bot Artifact",
            "standard library",
            "no build-time package downloads",
            "until the Tournament completes",
        ):
            with self.subTest(statement=statement):
                self.assertIn(statement, normalized)
        for frozen_input in (
            "catalog",
            "wrapper",
            "recipe",
            "base runtime",
            "conformance suite",
        ):
            with self.subTest(frozen_input=frozen_input):
                self.assertRegex(
                    normalized,
                    rf"(?i)no routine changes[^.]*{re.escape(frozen_input)}",
                )

    def test_catalog_contract_workflow_verifies_published_release_tags(self) -> None:
        workflow = (PROJECT_ROOT / ".github/workflows/catalog-contract.yml").read_text()

        self.assertIn('tags: ["catalog-v*"]', workflow)
        self.assertIn("fetch-depth: 0", workflow)
        self.assertIn(
            './freeze-tournament-catalog verify "${GITHUB_REF_NAME}"', workflow
        )
        self.assertIn(
            '"refs/tags/${GITHUB_REF_NAME}:refs/tags/${GITHUB_REF_NAME}"', workflow
        )
        self.assertIn(".core/", (PROJECT_ROOT / ".gitignore").read_text().splitlines())


if __name__ == "__main__":
    unittest.main()
