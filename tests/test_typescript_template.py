from __future__ import annotations

import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

from template_collection import load_collection


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def has_typescript_toolchain() -> bool:
    node = shutil.which("node")
    if node is None:
        return False
    completed = subprocess.run(
        [node, "--version"], capture_output=True, text=True
    )
    if completed.returncode != 0:
        return False
    compiler = shutil.which("tsc")
    if compiler is None:
        return False
    compiler_version = subprocess.run(
        [compiler, "--version"], capture_output=True, text=True
    )
    try:
        return (
            int(completed.stdout.strip().lstrip("v").split(".", 1)[0]) >= 24
            and compiler_version.returncode == 0
            and compiler_version.stdout.strip() == "Version 6.0.3"
        )
    except (ValueError, IndexError):
        return False


class TypeScriptTeamTemplateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.temporary = tempfile.TemporaryDirectory()
        cls.core = Path(cls.temporary.name) / "rps-tournament"
        subprocess.run(
            [str(PROJECT_ROOT / "materialize-core-tool"), str(cls.core)],
            cwd=PROJECT_ROOT,
            check=True,
            capture_output=True,
            text=True,
        )
        lock = json.loads((PROJECT_ROOT / "core-tool.lock.json").read_text())
        cls.catalog = cls.core / lock["catalog"]["path"]

    @classmethod
    def tearDownClass(cls) -> None:
        cls.temporary.cleanup()

    def test_collection_exposes_an_independent_typescript_template(self) -> None:
        collection = load_collection(PROJECT_ROOT, self.catalog)
        template = collection.select("typescript")

        self.assertEqual(template.language_environment, "typescript")
        self.assertEqual(template.version, "typescript-team-template-v1")
        self.assertEqual(template.release_tag, "typescript-template-v1")
        self.assertEqual(
            template.team_source_path.as_posix(),
            "templates/typescript/team_source",
        )
        self.assertNotIn(
            template.release_tag,
            {collection.select(name).release_tag for name in ("python", "go", "java")},
        )

    @unittest.skipUnless(
        has_typescript_toolchain(), "Node.js 24 or newer is required for native mode"
    )
    def test_native_entrypoint_builds_and_tests_seeded_behavior(self) -> None:
        completed = subprocess.run(
            [str(PROJECT_ROOT / "templates/typescript/build-and-test")],
            cwd=PROJECT_ROOT,
            capture_output=True,
            text=True,
        )

        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertIn("TypeScript starter build passed", completed.stdout)
        self.assertIn("TypeScript starter tests passed", completed.stdout)

    @unittest.skipUnless(
        os.environ.get("RPS_RUN_DOCKER_INTEGRATION") == "1",
        "set RPS_RUN_DOCKER_INTEGRATION=1 to run pinned Docker integration",
    )
    def test_pinned_docker_toolchain_runs_the_complete_typescript_suite(self) -> None:
        environment = os.environ.copy()
        environment["RPS_CORE_PATH"] = str(self.core)
        completed = subprocess.run(
            [
                str(PROJECT_ROOT / "check-team-template"),
                "--template", "typescript", "--mode", "docker",
            ],
            cwd=PROJECT_ROOT,
            env=environment,
            capture_output=True,
            text=True,
            timeout=120,
        )

        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertIn("TypeScript starter tests passed", completed.stdout)
        self.assertIn(
            "Team Template check passed: typescript (docker)", completed.stdout
        )

    def test_guidance_documents_boundaries_and_validation_authority(self) -> None:
        guidance = (
            PROJECT_ROOT / "templates/typescript/TEAM_GUIDE.md"
        ).read_text()

        for phrase in (
            "Team Source", "Node.js 24.19.0", "TypeScript 6.0.3",
            "64 files", "256 KiB per file", "1 MiB total",
            "turn` begins at `0", "supplied deterministic `rng`",
            'only `"R"`, `"P"`, or `"S"`',
            "--mode native", "--mode docker", "Advisory Validation",
            "Final Validation",
        ):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, guidance)

    def test_shared_checker_has_no_typescript_language_switch(self) -> None:
        checker = (PROJECT_ROOT / "check-team-template").read_text()

        self.assertNotIn('language_environment == "typescript"', checker)
        self.assertNotIn("RPS_TYPESCRIPT_ARCHIVE", checker)
        self.assertIn("RPS_DEPENDENCY_DEFINITION", checker)


if __name__ == "__main__":
    unittest.main()
