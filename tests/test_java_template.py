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


def has_java_25_jdk() -> bool:
    javac = shutil.which("javac")
    java = shutil.which("java")
    if javac is None or java is None:
        return False
    completed = subprocess.run(
        [javac, "-version"], capture_output=True, text=True
    )
    if completed.returncode != 0:
        return False
    version = (completed.stdout or completed.stderr).strip().split()[-1]
    try:
        return int(version.split(".", 1)[0]) >= 25
    except (ValueError, IndexError):
        return False


class JavaTeamTemplateTests(unittest.TestCase):
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

    def test_collection_exposes_an_independent_java_template(self) -> None:
        collection = load_collection(PROJECT_ROOT, self.catalog)
        template = collection.select("java")

        self.assertEqual(template.language_environment, "java")
        self.assertEqual(template.version, "java-team-template-v1")
        self.assertEqual(template.release_tag, "java-template-v1")
        self.assertEqual(
            template.team_source_path.as_posix(), "templates/java/team_source"
        )
        self.assertNotIn(
            template.release_tag,
            {
                collection.select("python").release_tag,
                collection.select("go").release_tag,
            },
        )

    @unittest.skipUnless(has_java_25_jdk(), "Java 25 JDK is required for native mode")
    def test_native_entrypoint_builds_and_tests_seeded_behavior(self) -> None:
        completed = subprocess.run(
            [str(PROJECT_ROOT / "templates/java/build-and-test")],
            cwd=PROJECT_ROOT,
            capture_output=True,
            text=True,
        )

        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertIn("Java starter build passed", completed.stdout)
        self.assertIn("Java starter tests passed", completed.stdout)

    @unittest.skipUnless(has_java_25_jdk(), "Java 25 JDK is required for native mode")
    def test_native_entrypoint_builds_the_complete_valid_team_source(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            template = Path(directory) / "java"
            shutil.copytree(PROJECT_ROOT / "templates/java", template)
            strategy = template / "team_source/Strategy.java"
            strategy.write_text(
                strategy.read_text().replace(
                    'String[] moves = {"R", "P", "S"};',
                    "String[] moves = TeamMoves.values();",
                )
            )
            (template / "team_source/TeamMoves.java").write_text(
                "public final class TeamMoves {\n"
                "  private TeamMoves() {}\n"
                "  public static String[] values() { "
                'return new String[] {"R", "P", "S"}; }\n'
                "}\n"
            )
            resources = template / "team_source/resources"
            resources.mkdir()
            (resources / "notes.txt").write_text("valid Team resource\n")

            completed = subprocess.run(
                [str(template / "build-and-test")],
                capture_output=True,
                text=True,
            )

        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertIn("Java starter tests passed", completed.stdout)

    @unittest.skipUnless(
        os.environ.get("RPS_RUN_DOCKER_INTEGRATION") == "1",
        "set RPS_RUN_DOCKER_INTEGRATION=1 to run pinned Docker integration",
    )
    def test_pinned_docker_toolchain_runs_the_complete_java_suite(self) -> None:
        completed = subprocess.run(
            [
                str(PROJECT_ROOT / "check-team-template"),
                "--template",
                "java",
                "--mode",
                "docker",
            ],
            cwd=PROJECT_ROOT,
            capture_output=True,
            text=True,
            timeout=120,
        )

        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertIn("Java starter tests passed", completed.stdout)
        self.assertIn("Team Template check passed: java (docker)", completed.stdout)

    def test_guidance_documents_boundaries_and_validation_authority(self) -> None:
        guidance = (PROJECT_ROOT / "templates/java/TEAM_GUIDE.md").read_text()

        for phrase in (
            "Team Source",
            "Java 25",
            "--mode native",
            "--mode docker",
            "Advisory Validation",
            "Final Validation",
        ):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, guidance)


if __name__ == "__main__":
    unittest.main()
