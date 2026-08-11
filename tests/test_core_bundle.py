from __future__ import annotations

import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest


PROJECT_ROOT = Path(__file__).resolve().parents[1]
COMMAND = PROJECT_ROOT / "materialize-core-tool"
LOCK_PATH = PROJECT_ROOT / "core-tool.lock.json"


class BundledCoreToolTests(unittest.TestCase):
    def test_clean_clone_materializes_the_exact_core_commit_without_network(self) -> None:
        lock = json.loads(LOCK_PATH.read_text())
        bundle = PROJECT_ROOT / "core-tool.bundle"
        self.assertEqual(
            "rps-runner-offline-bundle-v1@sha256:"
            + hashlib.sha256(bundle.read_bytes()).hexdigest(),
            lock["offline_bundle"]["identity"],
        )

        with tempfile.TemporaryDirectory() as directory:
            destination = Path(directory) / "rps-tournament"
            completed = subprocess.run(
                [str(COMMAND), str(destination)],
                cwd=PROJECT_ROOT,
                capture_output=True,
                text=True,
            )

            self.assertEqual(completed.returncode, 0, completed.stderr)
            self.assertEqual(
                subprocess.run(
                    ["git", "-C", str(destination), "rev-parse", "HEAD"],
                    check=True,
                    capture_output=True,
                    text=True,
                ).stdout.strip(),
                lock["runner"]["commit"],
            )
            self.assertEqual(
                subprocess.run(
                    ["git", "-C", str(destination), "status", "--porcelain"],
                    check=True,
                    capture_output=True,
                    text=True,
                ).stdout,
                "",
            )

    def test_materialization_verifies_every_catalog_release_coordinate(self) -> None:
        lock = json.loads(LOCK_PATH.read_text())

        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for name in (
                "catalog_compatibility.py",
                "core-tool.bundle",
                "core-tool.lock.json",
                "materialize-core-tool",
            ):
                shutil.copy2(PROJECT_ROOT / name, root / name)

            cases = (
                (("runner", "package_version"), "9.9.9", "package version"),
                (("catalog", "path"), "language_environments/missing.json", "catalog path"),
                (
                    ("catalog", "identity"),
                    "rps-language-environment-catalog-v1@sha256:" + "0" * 64,
                    "catalog identity",
                ),
                (
                    ("catalog", "assets"),
                    {},
                    "catalog asset identities",
                ),
            )
            for index, (keys, value, diagnostic) in enumerate(cases):
                with self.subTest(diagnostic=diagnostic):
                    changed = json.loads(json.dumps(lock))
                    target = changed
                    for key in keys[:-1]:
                        target = target[key]
                    target[keys[-1]] = value
                    (root / "core-tool.lock.json").write_text(
                        json.dumps(changed, indent=2) + "\n"
                    )
                    completed = subprocess.run(
                        [str(root / "materialize-core-tool"), str(root / f"runner-{index}")],
                        cwd=root,
                        capture_output=True,
                        text=True,
                    )
                    self.assertNotEqual(completed.returncode, 0)
                    self.assertIn(diagnostic, completed.stderr.lower())
                    self.assertIn("organizer", completed.stderr.lower())

    def test_corrupt_offline_bundle_fails_before_checkout(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for name in (
                "catalog_compatibility.py",
                "core-tool.bundle",
                "core-tool.lock.json",
                "materialize-core-tool",
            ):
                shutil.copy2(PROJECT_ROOT / name, root / name)
            with (root / "core-tool.bundle").open("ab") as stream:
                stream.write(b"corrupt")
            destination = root / "runner"

            completed = subprocess.run(
                [str(root / "materialize-core-tool"), str(destination)],
                cwd=root,
                capture_output=True,
                text=True,
            )

            self.assertNotEqual(completed.returncode, 0)
            self.assertIn("offline bundle identity", completed.stderr.lower())
            self.assertIn("organizer", completed.stderr.lower())
            self.assertFalse(destination.exists())


if __name__ == "__main__":
    unittest.main()
