from __future__ import annotations

import hashlib
import json
from pathlib import Path
import subprocess
import tempfile
import unittest


PROJECT_ROOT = Path(__file__).resolve().parents[1]
COMMAND = PROJECT_ROOT / "materialize-core-tool"
LOCK_PATH = PROJECT_ROOT / "core-tool.lock.json"


class BundledCoreToolTests(unittest.TestCase):
    def test_clean_clone_materializes_the_exact_core_commit_without_network(self) -> None:
        lock = json.loads(LOCK_PATH.read_text())
        bundle = PROJECT_ROOT / lock["offline_bundle"]["path"]
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


if __name__ == "__main__":
    unittest.main()
