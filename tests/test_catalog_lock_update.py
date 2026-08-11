from __future__ import annotations

import json
from pathlib import Path
import subprocess
import tempfile
import unittest


PROJECT_ROOT = Path(__file__).resolve().parents[1]
COMMAND = PROJECT_ROOT / "prepare-catalog-lock"
LOCK = json.loads((PROJECT_ROOT / "core-tool.lock.json").read_text())
BUNDLE = PROJECT_ROOT / "core-tool.bundle"
RUNBOOK = PROJECT_ROOT / "CATALOG_COMPATIBILITY.md"


def independence_evidence(coordinates: dict[str, object]) -> dict[str, object]:
    return {
        "evidence_format_version": "runner-catalog-independence-v1",
        "status": "passed",
        "compatibility_coordinates": coordinates,
        "repository_scan": {
            "companion_repository": "absent",
            "dependency_matches": [],
            "participant_template_paths": [],
        },
        "catalog_release": {
            "manifest": {"compatibility_coordinates": coordinates},
            "participant_template_asset_paths": [],
            "participant_template_digest_fields": [],
            "participant_template_paths": [],
            "unowned_catalog_paths": [],
        },
        "organizer_workflows": {"status": "passed"},
    }


class CatalogLockUpdateTests(unittest.TestCase):
    def run_command(
        self,
        evidence: dict[str, object],
        *,
        bundle: Path = BUNDLE,
    ) -> tuple[subprocess.CompletedProcess[str], Path, tempfile.TemporaryDirectory[str]]:
        temporary = tempfile.TemporaryDirectory()
        root = Path(temporary.name)
        evidence_path = root / "runner-evidence.json"
        evidence_path.write_text(json.dumps(evidence))
        output = root / "prepared-update"
        completed = subprocess.run(
            [
                str(COMMAND),
                "--runner-bundle",
                str(bundle),
                "--runner-evidence",
                str(evidence_path),
                "--output",
                str(output),
            ],
            cwd=PROJECT_ROOT,
            capture_output=True,
            text=True,
        )
        return completed, output, temporary

    def test_prepares_one_verified_lock_bundle_and_evidence_set(self) -> None:
        completed, output, temporary = self.run_command(independence_evidence(LOCK))
        self.addCleanup(temporary.cleanup)

        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertEqual(
            json.loads((output / "core-tool.lock.json").read_text()), LOCK
        )
        self.assertEqual((output / "core-tool.bundle").read_bytes(), BUNDLE.read_bytes())
        self.assertEqual(
            json.loads((output / "runner-catalog-independence.json").read_text()),
            independence_evidence(LOCK),
        )

    def test_rejects_evidence_or_bundle_drift_without_partial_output(self) -> None:
        mismatched = json.loads(json.dumps(LOCK))
        mismatched["catalog"]["identity"] = (
            "rps-language-environment-catalog-v1@sha256:" + "0" * 64
        )

        completed, output, temporary = self.run_command(
            independence_evidence(mismatched)
        )
        self.addCleanup(temporary.cleanup)

        self.assertNotEqual(completed.returncode, 0)
        self.assertFalse(output.exists())
        self.assertIn("catalog identity mismatch", completed.stderr)

    def test_runbook_uses_the_verified_preparation_command(self) -> None:
        normalized = " ".join(RUNBOOK.read_text().split())

        for argument in (
            "./prepare-catalog-lock",
            "--runner-bundle <published-runner-bundle>",
            "--runner-evidence <catalog-independence-evidence.json>",
            "--output <new-empty-directory>",
        ):
            with self.subTest(argument=argument):
                self.assertIn(argument, normalized)
        self.assertIn("copy the lock and bundle together", normalized)
        self.assertIn(
            "never move or recreate the earlier catalog release", normalized.lower()
        )


if __name__ == "__main__":
    unittest.main()
