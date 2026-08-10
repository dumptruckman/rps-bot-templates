from __future__ import annotations

from pathlib import Path
import re
import unittest


PROJECT_ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = PROJECT_ROOT / ".github" / "workflows" / "team-advisory-validation.yml"
TEAM_GUIDE = PROJECT_ROOT / "TEAM_GUIDE.md"


class GithubAdvisoryWorkflowTests(unittest.TestCase):
    workflow = WORKFLOW.read_text()

    def test_every_team_commit_uses_exact_source_and_core_commits_on_native_amd64(self) -> None:
        workflow = self.workflow

        self.assertIn("branches: [\"team/**\"]", workflow)
        self.assertIn("ref: ${{ github.sha }}", workflow)
        self.assertIn("persist-credentials: false", workflow)
        self.assertIn('runs-on: ubuntu-24.04', workflow)
        self.assertIn('PLATFORM: linux/amd64', workflow)
        self.assertIn('lock["repository"]', workflow)
        self.assertIn('lock["commit"]', workflow)
        self.assertIn("ref: ${{ steps.core_lock.outputs.commit }}", workflow)
        self.assertNotIn("qemu", workflow.lower())
        self.assertNotIn("buildx", workflow.lower())
        self.assertNotIn("--push", workflow)

    def test_pinned_core_owns_the_frozen_catalog_build_and_advisory_conformance(self) -> None:
        workflow = self.workflow

        catalog = "language_environments/catalog-v1/catalog.json"
        self.assertIn("PYTHONPATH: .core/rps-tournament", workflow)
        self.assertIn("python3 -m rps_runner.source_cli", workflow)
        self.assertIn("--source team_source", workflow)
        self.assertIn("--catalog \"$CATALOG\"", workflow)
        self.assertEqual(workflow.count("python3 -m rps_runner.artifact_cli"), 1)
        self.assertIn("python3 -m rps_runner.certification_cli", workflow)
        self.assertIn("--mode github-advisory", workflow)
        self.assertIn("--platform \"$PLATFORM\"", workflow)
        self.assertIn("--profile docker-execution-v1", workflow)
        self.assertIn("CATALOG: " + catalog, workflow)

    def test_job_has_read_only_authority_and_cancels_only_superseded_branch_work(self) -> None:
        workflow = self.workflow

        self.assertIn("permissions:\n  contents: read", workflow)
        self.assertIn("group: team-advisory-${{ github.ref }}", workflow)
        self.assertIn("cancel-in-progress: true", workflow)
        self.assertNotIn("secrets.", workflow)
        self.assertNotIn("docker login", workflow.lower())
        self.assertNotIn("pull_request_target", workflow)

    def test_commit_specific_evidence_is_retained_for_pass_and_failure(self) -> None:
        workflow = self.workflow

        for field in (
            '"source_commit"',
            '"source_digest"',
            '"catalog"',
            '"core_tool"',
            '"suite"',
            '"recipe"',
            '"wrapper"',
            '"runtime_digest"',
            '"platform"',
            '"disposable_image_identity"',
            '"execution_profile"',
            '"result"',
        ):
            with self.subTest(field=field):
                self.assertIn(field, workflow)
        self.assertIn("if: always()", workflow)
        self.assertIn("name: team-advisory-${{ github.sha }}", workflow)
        self.assertRegex(
            workflow,
            r"uses: actions/upload-artifact@[0-9a-f]{40}",
        )
        self.assertIn("retention-days: 90", workflow)
        self.assertIn("practice_match_result_gate", workflow)
        self.assertIn("id: evidence", workflow)
        self.assertIn("steps.evidence.outputs.result != 'passed'", workflow)
        self.assertNotRegex(workflow, r"(?i)(smoke_match|practice_match).*(winner|score)")
        self.assertNotIn("bot-artifact-manifest.json\n", workflow)

    def test_team_guide_explains_github_evidence_and_authority(self) -> None:
        guide = " ".join(TEAM_GUIDE.read_text().split())

        for statement in (
            "every commit pushed to a `team/**` branch",
            "native Linux/AMD64",
            "exact source commit",
            "90 days",
            "superseded in-progress run",
            "latest completed green candidate",
            "score or winner",
            "insufficient for official Tournament entry",
        ):
            with self.subTest(statement=statement):
                self.assertIn(statement, guide)


if __name__ == "__main__":
    unittest.main()
