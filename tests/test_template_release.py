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
COMMAND = PROJECT_ROOT / "release-team-template"
RUNBOOK = PROJECT_ROOT / "TEMPLATE_RELEASE.md"
DESCRIPTOR = PROJECT_ROOT / "team-template.json"
WORKFLOW = PROJECT_ROOT / ".github/workflows/template-release.yml"
ADVISORY_WORKFLOW = PROJECT_ROOT / ".github/workflows/team-advisory-validation.yml"
CORE_LOCK = json.loads((PROJECT_ROOT / "core-tool.lock.json").read_text())


class TemplateReleaseTests(unittest.TestCase):
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
            ["git", "config", "user.name", "Template Release Test"],
            cwd=repository,
            check=True,
        )
        subprocess.run(
            ["git", "config", "user.email", "template-release@example.invalid"],
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
            ["git", "commit", "--quiet", "-m", "releasable Team Template"],
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

    def git(self, repository: Path, *arguments: str) -> str:
        return subprocess.run(
            ["git", *arguments],
            cwd=repository,
            check=True,
            capture_output=True,
            text=True,
        ).stdout.strip()

    def commit_all(self, repository: Path, message: str) -> None:
        self.git(repository, "add", ".")
        self.git(repository, "commit", "--quiet", "-m", message)

    def retag_with_annotation(
        self, repository: Path, tag: str, annotation: str
    ) -> None:
        self.git(repository, "tag", "--delete", tag)
        subprocess.run(
            ["git", "tag", "--no-sign", "--annotate", tag, "--file", "-"],
            cwd=repository,
            check=True,
            input=annotation,
            text=True,
            capture_output=True,
        )

    def test_manifest_records_every_template_release_identity(self) -> None:
        completed = self.run_command("manifest", "template-v1")

        self.assertEqual(completed.returncode, 0, completed.stderr)
        manifest = json.loads(completed.stdout)
        descriptor = json.loads(DESCRIPTOR.read_text())
        self.assertEqual(manifest["release_format_version"], "template-release-v1")
        self.assertEqual(manifest["template_repository"]["tag"], "template-v1")
        self.assertRegex(
            manifest["template_repository"]["commit"], r"^[0-9a-f]{40}$"
        )
        template = manifest["team_template"]
        self.assertEqual(template["version"], descriptor["version"])
        self.assertEqual(template["path"], "team_source")
        self.assertEqual(
            template["expected_source_digest"],
            descriptor["expected_source_digest"],
        )
        self.assertEqual(
            template["expected_source_digest"],
            "sha256:e2890c1587c6c98acb62121e5524d8f75a53925ed738f333f63beee81e60fd1a",
        )
        self.assertRegex(template["digest"], r"^sha256:[0-9a-f]{64}$")
        self.assertEqual(
            template["files"],
            {
                "strategy.py": "sha256:"
                + hashlib.sha256(
                    (PROJECT_ROOT / "team_source/strategy.py").read_bytes()
                ).hexdigest()
            },
        )
        self.assertEqual(manifest["catalog_compatibility"], CORE_LOCK)
        advisory = manifest["advisory_validation"]
        self.assertEqual(
            advisory["workflow_path"],
            ".github/workflows/team-advisory-validation.yml",
        )
        self.assertEqual(
            advisory["workflow_identity"],
            "team-advisory-validation-v1@sha256:"
            + hashlib.sha256(ADVISORY_WORKFLOW.read_bytes()).hexdigest(),
        )
        self.assertEqual(advisory["supported_template_version"], descriptor["version"])

    def test_create_and_verify_use_the_expected_annotated_tag(self) -> None:
        repository = self.make_release_repository()

        created = self.run_repository_command(repository, "create", "template-v1")
        self.assertEqual(created.returncode, 0, created.stderr)
        manifest = json.loads(created.stdout)
        self.assertEqual(self.git(repository, "cat-file", "-t", "template-v1"), "tag")
        self.assertEqual(
            self.git(repository, "rev-parse", "template-v1^{}"),
            manifest["template_repository"]["commit"],
        )

        verified = self.run_repository_command(repository, "verify", "template-v1")
        self.assertEqual(verified.returncode, 0, verified.stderr)
        self.assertEqual(json.loads(verified.stdout), manifest)

        self.git(repository, "commit", "--quiet", "--allow-empty", "-m", "next")
        wrong_target = self.run_repository_command(
            repository, "verify", "template-v1"
        )
        self.assertNotEqual(wrong_target.returncode, 0)
        self.assertIn("wrong Template repository commit", wrong_target.stderr)

    def test_release_operations_reject_a_dirty_repository(self) -> None:
        repository = self.make_release_repository()
        (repository / "untracked.txt").write_text("dirty\n")

        created = self.run_repository_command(repository, "create", "template-v1")
        self.assertNotEqual(created.returncode, 0)
        self.assertIn("repository must be clean", created.stderr)

        (repository / "untracked.txt").unlink()
        created = self.run_repository_command(repository, "create", "template-v1")
        self.assertEqual(created.returncode, 0, created.stderr)
        (repository / "untracked.txt").write_text("dirty\n")
        verified = self.run_repository_command(repository, "verify", "template-v1")
        self.assertNotEqual(verified.returncode, 0)
        self.assertIn("repository must be clean", verified.stderr)

    def test_manifest_rejects_mutable_actions_and_a_mismatched_catalog_lock(self) -> None:
        action_repository = self.make_release_repository("-action")
        workflow = action_repository / ".github/workflows/team-advisory-validation.yml"
        workflow.write_text(
            workflow.read_text().replace(
                "actions/checkout@11bd71901bbe5b1630ceea73d27597364c9af683",
                "actions/checkout@v4",
            )
        )
        self.commit_all(action_repository, "use mutable action")

        mutable = self.run_repository_command(
            action_repository, "manifest", "template-v1"
        )
        self.assertNotEqual(mutable.returncode, 0)
        self.assertIn("mutable action ref", mutable.stderr)

        lock_repository = self.make_release_repository("-lock")
        lock_path = lock_repository / "core-tool.lock.json"
        lock = json.loads(lock_path.read_text())
        lock["catalog"]["identity"] = (
            "rps-language-environment-catalog-v1@sha256:" + "0" * 64
        )
        lock_path.write_text(json.dumps(lock, indent=2) + "\n")
        self.commit_all(lock_repository, "mismatch catalog lock")

        mismatched = self.run_repository_command(
            lock_repository, "manifest", "template-v1"
        )
        self.assertNotEqual(mismatched.returncode, 0)
        self.assertIn("catalog identity mismatch", mismatched.stderr)

    def test_verify_rejects_a_changed_template_and_incorrect_tag(self) -> None:
        repository = self.make_release_repository()
        created = self.run_repository_command(repository, "create", "template-v1")
        self.assertEqual(created.returncode, 0, created.stderr)
        annotation = json.dumps(json.loads(created.stdout), indent=2, sort_keys=True)

        strategy = repository / "team_source/strategy.py"
        strategy.write_text(strategy.read_text() + "\n# changed starter\n")
        self.commit_all(repository, "change Team Template")
        self.retag_with_annotation(repository, "template-v1", annotation)

        changed = self.run_repository_command(repository, "verify", "template-v1")
        self.assertNotEqual(changed.returncode, 0)
        self.assertIn("Team Template changed", changed.stderr)

        self.git(repository, "tag", "--delete", "template-v1")
        self.git(repository, "tag", "--no-sign", "template-v1")
        lightweight = self.run_repository_command(repository, "verify", "template-v1")
        self.assertNotEqual(lightweight.returncode, 0)
        self.assertIn("must be an annotated tag", lightweight.stderr)

    def test_runbook_and_ci_publish_template_releases_for_team_branches(self) -> None:
        normalized = " ".join(RUNBOOK.read_text().split())
        workflow = WORKFLOW.read_text()

        for statement in (
            "Template Release",
            "./release-team-template manifest template-v1",
            "./release-team-template create template-v1",
            "./release-team-template verify template-v1",
            "git switch --create team/<team-slug> template-v1^{}",
            "core-tool.lock.json",
            "Team Template digest",
            "Advisory Validation workflow identity",
        ):
            with self.subTest(statement=statement):
                self.assertIn(statement, normalized)

        self.assertIn('tags: ["template-v*"]', workflow)
        self.assertIn("fetch-depth: 0", workflow)
        self.assertIn('./release-team-template verify "${GITHUB_REF_NAME}"', workflow)
        self.assertNotIn("catalog-v*", workflow)
        for action_ref in re.findall(r"uses:\s+[^\s]+@([^\s]+)", workflow):
            self.assertRegex(action_ref, r"^[0-9a-f]{40}$")


if __name__ == "__main__":
    unittest.main()
