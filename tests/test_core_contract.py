from __future__ import annotations

import configparser
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import unittest


PROJECT_ROOT = Path(__file__).resolve().parents[1]
CATALOG = PROJECT_ROOT / "language_environments" / "catalog-v1" / "catalog.json"
CORE_LOCK = PROJECT_ROOT / "core-tool.lock.json"
CORE_PATH = Path(
    os.environ.get("RPS_CORE_PATH", PROJECT_ROOT / ".core" / "rps-tournament")
)
FULL_SHA256 = re.compile(r"^sha256:[0-9a-f]{64}$")
FULL_COMMIT = re.compile(r"^[0-9a-f]{40}$")


def load_core_module():
    module_path = CORE_PATH / "rps_runner" / "language_environment.py"
    spec = importlib.util.spec_from_file_location("pinned_language_environment", module_path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load pinned core module at {module_path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


class ImmutableCoreContractTests(unittest.TestCase):
    def catalog_data(self) -> dict[str, object]:
        return json.loads(CATALOG.read_text())

    def test_core_and_catalog_versions_are_explicit_and_immutable(self) -> None:
        lock = json.loads(CORE_LOCK.read_text())
        runner = lock["runner"]
        offline_bundle = lock["offline_bundle"]
        self.assertRegex(runner["commit"], FULL_COMMIT)
        self.assertEqual(runner["package_version"], "0.1.0")
        self.assertEqual(
            offline_bundle["identity"],
            "rps-runner-offline-bundle-v1@sha256:"
            + hashlib.sha256(
                (PROJECT_ROOT / "core-tool.bundle").read_bytes()
            ).hexdigest(),
        )

        checked_out_commit = subprocess.run(
            ["git", "-C", str(CORE_PATH), "rev-parse", "HEAD"],
            check=True,
            capture_output=True,
            text=True,
        ).stdout.strip()
        self.assertEqual(checked_out_commit, runner["commit"])
        package = configparser.ConfigParser()
        package.read(CORE_PATH / "setup.cfg")
        self.assertEqual(package["metadata"]["version"], runner["package_version"])

        catalog = self.catalog_data()
        self.assertEqual(
            catalog["catalog_version"], "rps-language-environment-catalog-v1"
        )
        for environment in catalog["environments"].values():
            self.assertTrue(environment["descriptor_version"])
            self.assertTrue(environment["participant_contract"]["version"])
            self.assertTrue(environment["source_schema"]["version"])
            for asset in environment["assets"].values():
                self.assertTrue(asset["version"])
                self.assertRegex(asset["sha256"], FULL_SHA256)

        workflow_paths = [
            PROJECT_ROOT / ".github" / "workflows" / "catalog-contract.yml",
            PROJECT_ROOT
            / ".github"
            / "workflows"
            / "team-advisory-validation.yml",
            CATALOG.parent / "python" / "workflow.yml",
        ]
        for workflow_path in workflow_paths:
            workflow = workflow_path.read_text()
            self.assertNotIn("latest", workflow)
            self.assertNotRegex(workflow, r"uses:\s+[^\s]+@v\d+")
            self.assertNotIn("secrets.", workflow)
            if workflow_path == CATALOG.parent / "python" / "workflow.yml":
                self.assertIn(
                    "repository=dumptruckman/rps-bot-tournament", workflow
                )
                self.assertIn("lock[\"runner\"][\"commit\"]", workflow)
                self.assertIn("ref: ${{ steps.core_lock.outputs.commit }}", workflow)
            else:
                self.assertIn("./materialize-core-tool .core/rps-tournament", workflow)
                self.assertNotIn("repository: ${{", workflow)
            for action_ref in re.findall(r"uses:\s+[^\s]+@([^\s]+)", workflow):
                self.assertRegex(action_ref, FULL_COMMIT)

    def test_pinned_core_loads_and_content_verifies_authoritative_catalog(self) -> None:
        core = load_core_module()
        catalog = core.load_catalog(CATALOG)

        self.assertEqual(catalog.version, "rps-language-environment-catalog-v1")
        self.assertEqual(set(catalog.environments), {"contract-fixture", "python"})
        self.assertEqual(catalog.environment("python").language, "python")

        with tempfile.TemporaryDirectory() as directory:
            bundle = Path(directory) / "source-bundle"
            result = core.freeze_source_bundle(
                CATALOG.parent / "python" / "template",
                bundle,
                catalog,
                catalog.environment("python"),
            )
            self.assertEqual(result["environment"], "python")
            self.assertEqual(
                result["participant_contract"]["version"],
                "choose-move-contract-v1",
            )

            copied_catalog = Path(directory) / "catalog-v1"
            shutil.copytree(CATALOG.parent, copied_catalog)
            (copied_catalog / "python" / "wrapper.py").write_text("stale\n")
            with self.assertRaisesRegex(core.CatalogError, "does not match"):
                core.load_catalog(copied_catalog / "catalog.json")

    def test_python_environment_contains_the_complete_language_package(self) -> None:
        catalog = self.catalog_data()
        python = catalog["environments"]["python"]
        self.assertEqual(
            set(python["assets"]),
            {
                "base_runtime",
                "build_target",
                "conformance",
                "dependency_definition",
                "entrypoint",
                "platform",
                "readiness",
                "recipe",
                "workflow",
                "wrapper",
            },
        )
        template = CATALOG.parent / "python" / "template" / "strategy.py"
        self.assertTrue(template.is_file())
        conformance = json.loads(
            (CATALOG.parent / "python" / "conformance.json").read_text()
        )
        self.assertEqual(
            conformance["template_sha256"],
            "sha256:" + hashlib.sha256(template.read_bytes()).hexdigest(),
        )

        runtimes = json.loads((CATALOG.parent / "python" / "runtimes.json").read_text())
        self.assertEqual(set(runtimes["platforms"]), {"linux/amd64", "linux/arm64"})
        for runtime in runtimes["platforms"].values():
            self.assertRegex(runtime["image"].split("@", 1)[1], FULL_SHA256)

        dockerfile = (CATALOG.parent / "python" / "Dockerfile").read_text()
        self.assertNotIn("RUN ", dockerfile)
        self.assertIn('ENTRYPOINT ["python3", "-I", "/opt/rps/wrapper.py"]', dockerfile)

        wrapper = (CATALOG.parent / "python" / "wrapper.py").read_text()
        self.assertIn("def seed_adapter(", wrapper)
        self.assertIn("RPS_READY_V1", wrapper)

    def test_participant_contract_and_core_fixture_cannot_drift(self) -> None:
        catalog = self.catalog_data()
        local_fixture = catalog["environments"]["contract-fixture"]
        python = catalog["environments"]["python"]
        core_fixture_path = (
            CORE_PATH / "language_environments" / "catalog-v1" / "catalog.json"
        )
        core_fixture = json.loads(core_fixture_path.read_text())["environments"][
            "contract-fixture"
        ]

        self.assertEqual(local_fixture, core_fixture)
        self.assertEqual(
            python["participant_contract"],
            {
                "callable": "choose_move",
                "signature": (
                    "choose_move(turn, my_history, opponent_history, rng) -> move"
                ),
                "static_validation": "single-unconditional-function-v1",
                "version": "choose-move-contract-v1",
            },
        )

    def test_every_catalog_asset_digest_matches_its_content(self) -> None:
        catalog = self.catalog_data()
        for environment in catalog["environments"].values():
            for name, asset in environment["assets"].items():
                with self.subTest(environment=environment["language"], asset=name):
                    content = (CATALOG.parent / asset["path"]).read_bytes()
                    digest = "sha256:" + hashlib.sha256(content).hexdigest()
                    self.assertEqual(asset["sha256"], digest)


if __name__ == "__main__":
    unittest.main()
