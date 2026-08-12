from __future__ import annotations

from pathlib import Path
import unittest


PROJECT_ROOT = Path(__file__).resolve().parents[1]
RUNBOOK = PROJECT_ROOT / "SUBMISSION_CUTOFF.md"
README = PROJECT_ROOT / "README.md"
TEAM_GUIDE = PROJECT_ROOT / "templates/python/TEAM_GUIDE.md"


class SubmissionCutoffRunbookTests(unittest.TestCase):
    runbook = RUNBOOK.read_text() if RUNBOOK.exists() else ""
    normalized = " ".join(runbook.split())

    def test_cutoff_rule_is_auditable_and_allows_an_earlier_green_commit(self) -> None:
        for statement in (
            "latest completed green commit",
            "at or before the declared deadline",
            "explicitly select an earlier",
            "Coordinated Universal Time (UTC)",
            "source commit",
            "Template Release",
        ):
            with self.subTest(statement=statement):
                self.assertIn(statement, self.normalized)

    def test_manual_git_transport_stops_at_the_core_local_directory_boundary(self) -> None:
        for command in (
            "git clone",
            "fetch origin",
            "checkout --detach",
            "archive --format=tar",
            "python3 -m rps_runner.source_cli",
            "--source",
            "--bundle",
        ):
            with self.subTest(command=command):
                self.assertIn(command, self.runbook)

        for out_of_scope in (
            "automated branch discovery",
            "automated authentication",
            "automated pulling",
            "automated cutoff enforcement",
        ):
            with self.subTest(out_of_scope=out_of_scope):
                self.assertIn(out_of_scope, self.normalized)

    def test_source_and_catalog_are_reconciled_with_durable_evidence(self) -> None:
        for identity in (
            "eligibility-evidence.json",
            "source_commit",
            "source_digest",
            "versions.catalog",
            "catalog",
            "template_release",
            "Team Template version and digest",
            "Advisory Validation workflow identity",
        ):
            with self.subTest(identity=identity):
                self.assertIn(identity, self.normalized)
        self.assertIn("must match", self.normalized)

    def test_no_github_delivery_uses_the_same_source_validator(self) -> None:
        for statement in (
            "No-GitHub delivery",
            "directory",
            "ZIP archive",
            "same pinned source validator",
        ):
            with self.subTest(statement=statement):
                self.assertIn(statement, self.runbook)

    def test_authority_and_repair_policy_are_explicit(self) -> None:
        for statement in (
            "GitHub/AMD64 evidence is Advisory Validation only",
            "rebuilt on native Linux/ARM64",
            "Final Validation",
            "Tournament-eligible Bot Artifact",
            "compatibility-only repair",
            "original source",
            "complete diff",
            "explanation",
            "replacement Source Digest",
            "Final Validation identity",
            "strategy enhancement",
        ):
            with self.subTest(statement=statement):
                self.assertIn(statement, self.normalized)

    def test_team_and_repository_guides_link_to_the_policy(self) -> None:
        for document in (README, TEAM_GUIDE):
            with self.subTest(document=document.name):
                self.assertIn("SUBMISSION_CUTOFF.md", document.read_text())


if __name__ == "__main__":
    unittest.main()
