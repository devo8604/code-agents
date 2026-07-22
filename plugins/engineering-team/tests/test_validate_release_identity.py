from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPT_SOURCE = (
    Path(__file__).resolve().parents[1] / "scripts" / "validate_release_identity.py"
)


class ReleaseIdentityTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary_directory.name)
        script = self.root / "plugins" / "engineering-team" / "scripts"
        manifest = self.root / "plugins" / "engineering-team" / ".codex-plugin"
        script.mkdir(parents=True)
        manifest.mkdir(parents=True)
        (script / SCRIPT_SOURCE.name).write_bytes(SCRIPT_SOURCE.read_bytes())
        self.manifest = manifest / "plugin.json"
        self.write_manifest("1.0.0")
        subprocess.run(["git", "init", "-q"], cwd=self.root, check=True)
        subprocess.run(["git", "config", "user.email", "test@example.invalid"], cwd=self.root, check=True)
        subprocess.run(["git", "config", "user.name", "Test"], cwd=self.root, check=True)
        subprocess.run(["git", "add", "."], cwd=self.root, check=True)
        subprocess.run(["git", "commit", "-qm", "baseline"], cwd=self.root, check=True)

    def tearDown(self) -> None:
        self.temporary_directory.cleanup()

    def write_manifest(self, version: str) -> None:
        self.manifest.write_text(json.dumps({"version": version}) + "\n", encoding="utf-8")

    def run_validator(self, expected: int) -> subprocess.CompletedProcess[str]:
        result = subprocess.run(
            [sys.executable, str(self.root / "plugins/engineering-team/scripts/validate_release_identity.py")],
            cwd=self.root,
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, expected, result.stdout + result.stderr)
        return result

    def test_requires_version_change_for_payload_change(self) -> None:
        payload = self.root / "plugins" / "engineering-team" / "payload.txt"
        payload.write_text("changed\n", encoding="utf-8")
        result = self.run_validator(1)
        self.assertIn("version remains", result.stderr)

    def test_accepts_payload_change_with_new_version(self) -> None:
        payload = self.root / "plugins" / "engineering-team" / "payload.txt"
        payload.write_text("changed\n", encoding="utf-8")
        self.write_manifest("1.1.0")
        result = self.run_validator(0)
        self.assertIn("version advanced", result.stdout)


if __name__ == "__main__":
    unittest.main()
