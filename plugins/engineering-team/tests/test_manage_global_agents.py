from __future__ import annotations

import hashlib
import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from unittest import mock
from pathlib import Path

import tomllib


PLUGIN_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = PLUGIN_ROOT / "scripts" / "manage_global_agents.py"
BEGIN_MARKER = "# BEGIN engineering-team managed global agents"
END_MARKER = "# END engineering-team managed global agents"
EXPECTED_ROLES = {
    "ai_ml_engineer",
    "api_engineer",
    "client_engineer",
    "data_engineer",
    "docs_researcher",
    "govcloud_engineer",
    "quality_engineer",
    "security_engineer",
    "system_architect",
    "technical_writer",
    "ui_engineer",
    "ux_engineer",
}
EXPECTED_FILENAMES = {name.replace("_", "-") + ".toml" for name in EXPECTED_ROLES}


def load_manager_module():
    spec = importlib.util.spec_from_file_location("tested_global_agent_manager", SCRIPT)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot load manager module from {SCRIPT}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


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

    def add_prior_release_role(
        self, *, content: bytes = b'name = "mcp_engineer"\n'
    ) -> tuple[Path, Path]:
        install_dir = self.codex_home / "agents" / "engineering-team"
        target = install_dir / "mcp-engineer.toml"
        target.write_bytes(content)
        manifest_path = install_dir / ".install-manifest.json"
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        manifest["plugin_version"] = "0.6.0"
        manifest["agents"]["mcp_engineer"] = {
            "filename": "mcp-engineer.toml",
            "sha256": hashlib.sha256(content).hexdigest(),
        }
        manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
        return target, manifest_path

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
        self.assertEqual(roles, EXPECTED_ROLES)
        manifest_data = json.loads(install_manifest.read_text(encoding="utf-8"))
        self.assertEqual(set(manifest_data["agents"]), EXPECTED_ROLES)
        self.assertEqual(
            {entry["filename"] for entry in manifest_data["agents"].values()},
            EXPECTED_FILENAMES,
        )
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

    def test_upgrade_reports_and_removes_unmodified_retired_role(self) -> None:
        self.run_manager("install")
        retired, manifest_path = self.add_prior_release_role()

        status = self.run_manager("status", expected=1)
        dry_run = self.run_manager("install", "--dry-run")

        self.assertIn("Unmodified retired roles pending removal: mcp_engineer", status.stdout)
        self.assertIn("Retired roles from the prior install manifest: mcp_engineer", dry_run.stdout)
        self.assertIn("Would remove 1 unmodified retired role file", dry_run.stdout)
        self.assertTrue(retired.exists())

        installed = self.run_manager("install")

        self.assertIn("Updated 12 global agents", installed.stdout)
        self.assertFalse(retired.exists())
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        self.assertEqual(set(manifest["agents"]), EXPECTED_ROLES)
        self.run_manager("status")

    def test_late_failure_rolls_back_prior_release_upgrade_byte_for_byte(self) -> None:
        self.run_manager("install")
        retired, manifest_path = self.add_prior_release_role()
        install_dir = retired.parent
        role_path = install_dir / "api-engineer.toml"
        previous_role = role_path.read_bytes() + b"\n# previous release\n"
        role_path.write_bytes(previous_role)
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        manifest["agents"]["api_engineer"]["sha256"] = hashlib.sha256(
            previous_role
        ).hexdigest()
        manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
        config_path = self.codex_home / "config.toml"
        previous_config = config_path.read_bytes().replace(
            b"Generated by engineering-team ",
            b"Generated by engineering-team prior-",
            1,
        )
        config_path.write_bytes(previous_config)
        previous_retired = retired.read_bytes()
        prior_manifest = manifest_path.read_bytes()
        manager = load_manager_module()
        real_unlink = Path.unlink
        cleanup_failed = False

        def fail_retired_cleanup(path: Path, *args, **kwargs) -> None:
            nonlocal cleanup_failed
            if ".mcp-engineer.toml.retired." in path.name and not cleanup_failed:
                cleanup_failed = True
                raise OSError("simulated post-manifest cleanup failure")
            real_unlink(path, *args, **kwargs)

        with mock.patch.object(Path, "unlink", new=fail_retired_cleanup):
            with self.assertRaisesRegex(OSError, "simulated post-manifest cleanup failure"):
                manager.install(self.codex_home, dry_run=False, force=False)

        self.assertTrue(retired.exists())
        self.assertEqual(retired.read_bytes(), previous_retired)
        self.assertEqual(role_path.read_bytes(), previous_role)
        self.assertEqual(config_path.read_bytes(), previous_config)
        self.assertEqual(manifest_path.read_bytes(), prior_manifest)
        self.assertEqual(
            list(retired.parent.glob(".mcp-engineer.toml.retired.*")), []
        )

    def test_same_name_different_filename_retirement_fails_closed(self) -> None:
        self.run_manager("install")
        install_dir = self.codex_home / "agents" / "engineering-team"
        manifest_path = install_dir / ".install-manifest.json"
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        old_target = install_dir / "api-specialist.toml"
        old_content = b'name = "api_engineer"\n'
        old_target.write_bytes(old_content)
        manifest["agents"]["api_engineer"] = {
            "filename": old_target.name,
            "sha256": hashlib.sha256(old_content).hexdigest(),
        }
        manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
        old_target.write_bytes(old_content + b"# local edit\n")
        prior_manifest = manifest_path.read_bytes()

        result = self.run_manager("install", expected=1)

        self.assertIn(
            "Cannot retain conflicting ownership entry for agent api_engineer",
            result.stderr,
        )
        self.assertTrue(old_target.exists())
        self.assertEqual(manifest_path.read_bytes(), prior_manifest)

    def test_upgrade_preserves_modified_retired_role_and_ownership(self) -> None:
        self.run_manager("install")
        retired, manifest_path = self.add_prior_release_role()
        retired.write_bytes(retired.read_bytes() + b"# local edit\n")

        status = self.run_manager("status", expected=1)
        dry_run = self.run_manager("install", "--dry-run")
        self.run_manager("install", "--force")

        self.assertIn("Modified or symlinked retired roles preserved: mcp_engineer", status.stdout)
        self.assertIn("Would preserve 1 modified or symlinked retired role file", dry_run.stdout)
        self.assertTrue(retired.exists())
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        self.assertIn("mcp_engineer", manifest["agents"])

        uninstall = self.run_manager("uninstall", "--force")

        self.assertIn("Preserved modified or symlinked files", uninstall.stdout)
        self.assertTrue(retired.exists())
        retained = json.loads(manifest_path.read_text(encoding="utf-8"))
        self.assertEqual(set(retained["agents"]), {"mcp_engineer"})
        self.assertEqual(
            retained["agents"]["mcp_engineer"]["filename"], "mcp-engineer.toml"
        )

    def test_upgrade_preserves_symlinked_retired_role(self) -> None:
        self.run_manager("install")
        retired, manifest_path = self.add_prior_release_role()
        retired.unlink()
        outside = Path(self.temporary_directory.name) / "retired-role.toml"
        outside.write_text('name = "personal"\n', encoding="utf-8")
        retired.symlink_to(outside)

        result = self.run_manager("install")

        self.assertIn("Updated 12 global agents", result.stdout)
        self.assertTrue(retired.is_symlink())
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        self.assertIn("mcp_engineer", manifest["agents"])

    def test_uninstall_removes_unmodified_role_from_prior_release(self) -> None:
        self.run_manager("install")
        retired, manifest_path = self.add_prior_release_role()

        dry_run = self.run_manager("uninstall", "--dry-run")
        self.assertIn("Retired roles from the prior install manifest: mcp_engineer", dry_run.stdout)
        self.run_manager("uninstall")

        self.assertFalse(retired.exists())
        self.assertFalse(manifest_path.exists())

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
