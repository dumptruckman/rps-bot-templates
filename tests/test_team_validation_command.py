from __future__ import annotations

import json
import os
from pathlib import Path
import stat
import subprocess
import tempfile
import textwrap
import unittest


PROJECT_ROOT = Path(__file__).resolve().parents[1]
COMMAND = PROJECT_ROOT / "validate-team"
LOCK = json.loads((PROJECT_ROOT / "core-tool.lock.json").read_text())


class TeamValidationCommandTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)
        self.bin = self.root / "bin"
        self.bin.mkdir()
        self.core = self.root / "core"
        subprocess.run(
            [str(PROJECT_ROOT / "materialize-core-tool"), str(self.core)],
            cwd=PROJECT_ROOT,
            check=True,
            capture_output=True,
            text=True,
        )
        package = self.core / "rps_runner"
        (package / "__init__.py").write_text("")
        self.log = self.root / "calls.jsonl"
        self._write_executable(
            "git",
            """
            #!/bin/sh
            if [ "$3" = rev-parse ]; then
              printf '%s\\n' "$RPS_TEST_CORE_COMMIT"
            elif [ "${RPS_TEST_CORE_DIRTY:-}" ]; then
              printf '%s\\n' ' M rps_runner/source_cli.py'
            fi
            """,
        )
        self._write_executable(
            "docker",
            """
            #!/bin/sh
            if [ "${RPS_TEST_DOCKER_FAILURE:-}" ]; then
              printf '%s\\n' "$RPS_TEST_DOCKER_FAILURE" >&2
              exit 1
            fi
            if [ "$1" = version ]; then
              printf '%s\\n' "${RPS_TEST_PLATFORM:-linux/arm64}"
              exit 0
            fi
            exit 0
            """,
        )
        helper = textwrap.dedent(
            """
            import json
            import os
            from pathlib import Path
            import sys

            def option(name):
                return Path(sys.argv[sys.argv.index(name) + 1])

            def record(stage):
                with Path(os.environ["RPS_TEST_LOG"]).open("a") as stream:
                    stream.write(json.dumps({"stage": stage, "arguments": sys.argv[1:]}) + "\\n")
                if os.environ.get("RPS_TEST_FAIL_STAGE") == stage:
                    print(os.environ["RPS_TEST_FAILURE"], file=sys.stderr)
                    raise SystemExit(2)
            """
        )
        (package / "fake.py").write_text(helper)
        (package / "source_cli.py").write_text(
            textwrap.dedent(
                """
                import json
                from .fake import option, record

                record("source")
                bundle = option("--bundle")
                bundle.mkdir()
                result = {"source_digest": "sha256:" + "1" * 64}
                (bundle / "source-bundle.json").write_text(json.dumps(result))
                print(json.dumps(result))
                """
            )
        )
        (package / "artifact_cli.py").write_text(
            textwrap.dedent(
                """
                import json
                from .fake import option, record

                record("build")
                candidate = option("--candidate")
                candidate.mkdir()
                result = {
                    "artifact_digest": "sha256:" + "2" * 64,
                    "runtime": {"identity": "python-runtime-v1@sha256:" + "3" * 64},
                    "retention": {
                        "local_image_id": "sha256:" + "4" * 64,
                        "local_image_reference": "rps-tournament-candidate:test",
                    },
                    "identities": {
                        "catalog": "catalog-v1@sha256:" + "5" * 64,
                        "core_tool": "rps-core-tool-v1@sha256:" + "6" * 64,
                        "recipe": "python-build-recipe-v1@sha256:" + "7" * 64,
                        "wrapper": "python-wrapper-v3@sha256:" + "8" * 64,
                    },
                }
                (candidate / "artifact-candidate.json").write_text(json.dumps(result))
                print(json.dumps(result))
                """
            )
        )
        (package / "certification_cli.py").write_text(
            textwrap.dedent(
                """
                import json
                from .fake import option, record

                record("certification")
                output = option("--output")
                output.mkdir()
                result = {
                    "status": "passed",
                    "advisory": True,
                    "canonical_tournament_eligible": False,
                    "platform": "linux/arm64",
                    "identities": {
                        "source": "sha256:" + "1" * 64,
                        "image": "sha256:" + "2" * 64,
                        "runtime": "python-runtime-v1@sha256:" + "3" * 64,
                        "wrapper": "python-wrapper-v3@sha256:" + "8" * 64,
                        "recipe": "python-build-recipe-v1@sha256:" + "7" * 64,
                        "catalog": "catalog-v1@sha256:" + "5" * 64,
                        "suite": "python-artifact-conformance-v1@sha256:" + "9" * 64,
                        "core_tool": "rps-core-tool-v1@sha256:" + "6" * 64,
                    },
                    "checks": {"complete_smoke_match": "passed"},
                    "notice": "participant-local results are advisory",
                }
                (output / "validation-report.json").write_text(json.dumps(result))
                print(json.dumps(result))
                """
            )
        )

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def _write_executable(self, name: str, source: str) -> None:
        path = self.bin / name
        path.write_text(textwrap.dedent(source).lstrip())
        path.chmod(path.stat().st_mode | stat.S_IXUSR)

    def run_command(self, **environment: str) -> subprocess.CompletedProcess[str]:
        process_environment = os.environ.copy()
        process_environment.update(
            {
                "PATH": str(self.bin) + os.pathsep + process_environment["PATH"],
                "RPS_CORE_PATH": str(self.core),
                "RPS_TEST_CORE_COMMIT": LOCK["runner"]["commit"],
                "RPS_TEST_LOG": str(self.log),
            }
        )
        process_environment.update(environment)
        return subprocess.run(
            [str(COMMAND)],
            cwd=PROJECT_ROOT,
            env=process_environment,
            capture_output=True,
            text=True,
            timeout=10,
        )

    def calls(self) -> list[dict[str, object]]:
        return [json.loads(line) for line in self.log.read_text().splitlines()]

    def test_one_command_delegates_the_native_advisory_workflow_to_pinned_core(self) -> None:
        completed = self.run_command(RPS_TEST_PLATFORM="linux/arm64")

        self.assertEqual(completed.returncode, 0, completed.stderr)
        calls = self.calls()
        self.assertEqual([call["stage"] for call in calls], ["source", "build", "certification"])
        catalog = str(self.core.resolve() / LOCK["catalog"]["path"])
        self.assertIn(catalog, calls[0]["arguments"])
        self.assertIn(str(PROJECT_ROOT / "team_source"), calls[0]["arguments"])
        self.assertEqual(
            calls[1]["arguments"][calls[1]["arguments"].index("--platform") + 1],
            "linux/arm64",
        )
        self.assertNotIn("--push", calls[1]["arguments"])
        self.assertEqual(
            calls[2]["arguments"][calls[2]["arguments"].index("--mode") + 1],
            "participant-local",
        )
        self.assertEqual(
            calls[2]["arguments"][calls[2]["arguments"].index("--platform") + 1],
            "linux/arm64",
        )

        for label in (
            "Team Source digest:",
            "Catalog:",
            "Core tool:",
            "Conformance suite:",
            "Build recipe:",
            "Wrapper:",
            "Runtime:",
            "Native platform: linux/arm64",
            "Disposable image:",
            "Advisory Validation: passed",
            "Practice Match: passed",
        ):
            with self.subTest(label=label):
                self.assertIn(label, completed.stdout)
        self.assertIn("insufficient for official Tournament entry", completed.stdout)

        for call in calls:
            self.assertIn(catalog, call["arguments"])
        self.assertNotIn(
            str(PROJECT_ROOT / "language_environments"),
            json.dumps(calls),
        )

    def test_team_facing_diagnostics_name_each_failure_area(self) -> None:
        cases = (
            ("source", "invalid strategy signature", "Team Source failure"),
            ("build", "Docker build failed", "Build failure"),
            (
                "certification",
                "launch/readiness/lifecycle conformance failed: wrapper readiness marker was not observed",
                "Readiness failure",
            ),
            (
                "certification",
                "protocol/timing/stream/resource conformance failed: invalid protocol move at Turn 4",
                "Protocol failure",
            ),
            ("certification", "same-seed behavior was nondeterministic", "Determinism failure"),
            ("certification", "candidate produced security evidence", "Isolation failure"),
            (
                "certification",
                "protocol/timing/stream/resource conformance failed: container OOM resource fault",
                "Resource failure",
            ),
            (
                "certification",
                "launch/readiness/lifecycle conformance failed: candidate exited before clean shutdown",
                "Lifecycle failure",
            ),
        )
        for stage, message, label in cases:
            with self.subTest(stage=stage, label=label):
                if self.log.exists():
                    self.log.unlink()
                completed = self.run_command(
                    RPS_TEST_FAIL_STAGE=stage,
                    RPS_TEST_FAILURE=message,
                )
                self.assertNotEqual(completed.returncode, 0)
                self.assertIn(label, completed.stderr)
                self.assertIn(message, completed.stderr)

        completed = self.run_command(
            RPS_TEST_DOCKER_FAILURE="Cannot connect to the Docker daemon"
        )
        self.assertNotEqual(completed.returncode, 0)
        self.assertIn("Docker-host failure", completed.stderr)
        self.assertIn("GitHub Advisory Validation", completed.stderr)

    def test_wrong_core_checkout_is_rejected_before_team_source_is_touched(self) -> None:
        completed = self.run_command(RPS_TEST_CORE_COMMIT="f" * 40)

        self.assertNotEqual(completed.returncode, 0)
        self.assertIn("Pinned core tool failure", completed.stderr)
        self.assertIn(LOCK["runner"]["commit"], completed.stderr)
        self.assertFalse(self.log.exists())

    def test_modified_core_checkout_is_rejected_before_team_source_is_touched(self) -> None:
        completed = self.run_command(RPS_TEST_CORE_DIRTY="1")

        self.assertNotEqual(completed.returncode, 0)
        self.assertIn("Pinned core tool failure", completed.stderr)
        self.assertIn("tracked modifications", completed.stderr)
        self.assertFalse(self.log.exists())

    def test_team_guide_documents_the_one_command_and_advisory_limit(self) -> None:
        guide = (PROJECT_ROOT / "TEAM_GUIDE.md").read_text()
        normalized_guide = " ".join(guide.split())

        self.assertIn("./validate-team", guide)
        self.assertIn("GitHub Advisory Validation", normalized_guide)
        self.assertIn("insufficient for official Tournament entry", normalized_guide)


if __name__ == "__main__":
    unittest.main()
