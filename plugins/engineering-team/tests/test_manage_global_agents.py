from __future__ import annotations

import hashlib
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import tomllib


PLUGIN_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = PLUGIN_ROOT / "scripts" / "manage_global_agents.py"
BEGIN_MARKER = "# BEGIN engineering-team managed global agents"
END_MARKER = "# END engineering-team managed global agents"


class GlobalAgentManagerTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.codex_home = Path(self.temporary_directory.name) / "codex"

    def tearDown(self) -> None:
        self.temporary_directory.cleanup()

    def run_manager(self, *arguments: str, expected: int = 0) -> subprocess.CompletedProcess[str]:
        result = subprocess.run(
            [
                sys.executable,
                str(SCRIPT),
                "--codex-home",
                str(self.codex_home),
                *arguments,
            ],
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertEqual(
            result.returncode,
            expected,
            msg=f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}",
        )
        return result

    def test_install_is_idempotent_and_preserves_unrelated_config(self) -> None:
        self.codex_home.mkdir(parents=True)
        config = self.codex_home / "config.toml"
        config.write_text(
            "# keep this comment\nmodel = \"example\"\n\n[agents]\nmax_threads = 4\n",
            encoding="utf-8",
        )

        self.run_manager("install")
        first = config.read_text(encoding="utf-8")
        installed_api = self.codex_home / "agents" / "engineering-team" / "api-engineer.toml"
        install_manifest = (
            self.codex_home
            / "agents"
            / "engineering-team"
            / ".install-manifest.json"
        )
        api_mtime = installed_api.stat().st_mtime_ns
        manifest_mtime = install_manifest.stat().st_mtime_ns
        dry_run = self.run_manager("install", "--dry-run")
        self.run_manager("install")
        second = config.read_text(encoding="utf-8")

        self.assertIn("No changes required", dry_run.stdout)
        self.assertEqual(first, second)
        self.assertEqual(installed_api.stat().st_mtime_ns, api_mtime)
        self.assertEqual(install_manifest.stat().st_mtime_ns, manifest_mtime)
        self.assertEqual(second.count(BEGIN_MARKER), 1)
        self.assertEqual(second.count(END_MARKER), 1)
        self.assertIn("# keep this comment", second)
        parsed = tomllib.loads(second)
        self.assertEqual(parsed["model"], "example")
        self.assertEqual(parsed["agents"]["max_threads"], 4)
        roles = {key for key, value in parsed["agents"].items() if isinstance(value, dict)}
        self.assertEqual(len(roles), 10)
        backups = list((self.codex_home / "backups" / "engineering-team").glob("*.toml"))
        self.assertEqual(len(backups), 1)
        self.assertIn("# keep this comment", backups[0].read_text(encoding="utf-8"))
        self.run_manager("status")

    def test_status_detects_changed_registration(self) -> None:
        self.run_manager("install")
        config = self.codex_home / "config.toml"
        content = config.read_text(encoding="utf-8")
        config.write_text(
            content.replace(
                'config_file = "agents/engineering-team/api-engineer.toml"',
                'config_file = "agents/elsewhere/api-engineer.toml"',
            ),
            encoding="utf-8",
        )

        result = self.run_manager("status", expected=1)

        self.assertIn("registration block does not match", result.stdout)
        self.run_manager("install")
        self.run_manager("status")

    def test_install_refuses_external_role_collision(self) -> None:
        self.codex_home.mkdir(parents=True)
        config = self.codex_home / "config.toml"
        original = (
            "[agents.api_engineer]\n"
            "description = \"personal role\"\n"
            "config_file = \"agents/personal.toml\"\n"
        )
        config.write_text(original, encoding="utf-8")

        result = self.run_manager("install", expected=1)

        self.assertIn("defined outside the managed block", result.stderr)
        self.assertEqual(config.read_text(encoding="utf-8"), original)
        self.assertFalse((self.codex_home / "agents" / "engineering-team").exists())

    def test_modified_managed_file_requires_force(self) -> None:
        self.run_manager("install")
        target = self.codex_home / "agents" / "engineering-team" / "api-engineer.toml"
        target.write_text(target.read_text(encoding="utf-8") + "\n# local edit\n", encoding="utf-8")

        result = self.run_manager("install", expected=1)
        self.assertIn("locally modified", result.stderr)

        self.run_manager("install", "--force")
        self.assertNotIn("# local edit", target.read_text(encoding="utf-8"))
        self.run_manager("status")

    def test_update_replaces_a_file_matching_the_previous_manifest(self) -> None:
        self.run_manager("install")
        install_dir = self.codex_home / "agents" / "engineering-team"
        target = install_dir / "api-engineer.toml"
        current_content = target.read_bytes()
        previous_content = current_content + b"\n# previous release\n"
        target.write_bytes(previous_content)
        manifest_path = install_dir / ".install-manifest.json"
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        manifest["plugin_version"] = "previous"
        manifest["agents"]["api_engineer"]["sha256"] = hashlib.sha256(
            previous_content
        ).hexdigest()
        manifest_path.write_text(json.dumps(manifest), encoding="utf-8")

        self.run_manager("install")

        self.assertEqual(target.read_bytes(), current_content)
        self.run_manager("status")

    def test_install_refuses_symlinked_managed_directory(self) -> None:
        outside = Path(self.temporary_directory.name) / "outside"
        outside.mkdir()
        agents_dir = self.codex_home / "agents"
        agents_dir.mkdir(parents=True)
        (agents_dir / "engineering-team").symlink_to(
            outside, target_is_directory=True
        )

        result = self.run_manager("install", expected=1)

        self.assertIn("symlinked Codex path", result.stderr)
        self.assertEqual(list(outside.iterdir()), [])

    def test_uninstall_preserves_unrelated_config_and_modified_files(self) -> None:
        self.codex_home.mkdir(parents=True)
        config = self.codex_home / "config.toml"
        original = "model = \"example\"\n"
        config.write_text(original, encoding="utf-8")
        self.run_manager("install")
        target = self.codex_home / "agents" / "engineering-team" / "api-engineer.toml"
        target.write_text(target.read_text(encoding="utf-8") + "\n# keep me\n", encoding="utf-8")

        result = self.run_manager("uninstall")

        self.assertIn("Preserved modified", result.stdout)
        remaining = config.read_text(encoding="utf-8")
        self.assertNotIn(BEGIN_MARKER, remaining)
        self.assertEqual(remaining, original)
        self.assertEqual(tomllib.loads(remaining)["model"], "example")
        self.assertTrue(target.exists())
        self.assertFalse(
            (self.codex_home / "agents" / "engineering-team" / "client-engineer.toml").exists()
        )
        self.run_manager("status", expected=1)

    def test_uninstall_restores_config_without_a_trailing_newline(self) -> None:
        self.codex_home.mkdir(parents=True)
        config = self.codex_home / "config.toml"
        original = 'model = "example"'
        config.write_text(original, encoding="utf-8")

        self.run_manager("install")
        self.run_manager("uninstall")

        self.assertEqual(config.read_text(encoding="utf-8"), original)

    def test_dry_run_does_not_create_codex_home(self) -> None:
        self.run_manager("install", "--dry-run")
        self.assertFalse(self.codex_home.exists())


if __name__ == "__main__":
    unittest.main()
