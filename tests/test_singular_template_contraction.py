from __future__ import annotations

from pathlib import Path
import re
import unittest


PROJECT_ROOT = Path(__file__).resolve().parents[1]


class SingularTemplateContractionTests(unittest.TestCase):
    def test_legacy_singular_template_files_are_removed(self) -> None:
        for relative in (
            "team-template.json",
            "team_source/strategy.py",
        ):
            with self.subTest(path=relative):
                self.assertFalse((PROJECT_ROOT / relative).exists())

    def test_shared_collection_tooling_has_no_python_specific_paths_or_ids(self) -> None:
        shared_paths = (
            "check-team-template",
            "validate-team",
            "release-team-template",
            "template_collection.py",
            "prove-cross-repository-cutover",
            "prove-amd64-against-arm64",
            ".github/workflows/team-advisory-validation.yml",
            ".github/workflows/template-release.yml",
        )
        forbidden = (
            r"templates/python",
            r"ROOT\s*/\s*[\"']team_source[\"']",
            r"PROJECT_ROOT\s*/\s*[\"']team-template\.json[\"']",
            r"environment\([\"']python[\"']\)",
            r"\[[\"']python[\"']\]",
            r"--(?:environment|template) python(?:\s|$)",
            r"get\([\"']language_environment[\"'],\s*[\"']python[\"']\)",
        )
        for relative in shared_paths:
            content = (PROJECT_ROOT / relative).read_text()
            for pattern in forbidden:
                with self.subTest(path=relative, pattern=pattern):
                    self.assertIsNone(re.search(pattern, content))

    def test_collection_docs_record_stable_layout_checklist_and_migration(self) -> None:
        guide = (PROJECT_ROOT / "TEAM_TEMPLATE_COLLECTION.md").read_text()
        normalized = " ".join(guide.split())

        for statement in (
            "templates/<language-id>/team-template.json",
            "Checklist for adding a Team Template",
            "Migration from the singular shape",
            "root-level `team-template.json` and `team_source/`",
            "./check-team-template --template <language-id> --mode docker",
            "./validate-team --template <language-id>",
            "./release-team-template --template <language-id>",
        ):
            with self.subTest(statement=statement):
                self.assertIn(statement, normalized)


if __name__ == "__main__":
    unittest.main()
