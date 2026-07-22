#!/usr/bin/env python3
"""Require a plugin version change when its payload differs from a Git base."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parents[3]
PLUGIN_PATH = Path("plugins/engineering-team")
MANIFEST_PATH = PLUGIN_PATH / ".codex-plugin" / "plugin.json"


def git(*arguments: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *arguments],
        cwd=REPOSITORY_ROOT,
        check=False,
        capture_output=True,
        text=True,
    )


def version_from_text(content: str, source: str) -> str:
    try:
        data = json.loads(content)
    except json.JSONDecodeError as exc:
        raise ValueError(f"invalid plugin manifest from {source}: {exc}") from exc
    version = data.get("version")
    if not isinstance(version, str) or not version.strip():
        raise ValueError(f"plugin manifest from {source} has no version")
    return version


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base-ref", default="HEAD", help="Git revision to compare")
    args = parser.parse_args()

    diff = git("diff", "--quiet", args.base_ref, "--", str(PLUGIN_PATH))
    untracked = git(
        "ls-files", "--others", "--exclude-standard", "--", str(PLUGIN_PATH)
    )
    if untracked.returncode != 0:
        print(untracked.stderr.strip() or "Unable to inspect untracked plugin files.", file=sys.stderr)
        return 2
    if diff.returncode == 0 and not untracked.stdout.strip():
        print(f"Plugin payload is unchanged from {args.base_ref}.")
        return 0
    if diff.returncode not in {0, 1}:
        print(diff.stderr.strip() or "Unable to compare plugin payload.", file=sys.stderr)
        return 2

    base = git("show", f"{args.base_ref}:{MANIFEST_PATH.as_posix()}")
    if base.returncode != 0:
        print(base.stderr.strip() or "Unable to read the base plugin manifest.", file=sys.stderr)
        return 2
    try:
        base_version = version_from_text(base.stdout, args.base_ref)
        current_version = version_from_text(
            (REPOSITORY_ROOT / MANIFEST_PATH).read_text(encoding="utf-8"), "working tree"
        )
    except (OSError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    if current_version == base_version:
        print(
            f"ERROR: plugin payload changed but version remains {current_version!r}",
            file=sys.stderr,
        )
        return 1
    print(f"Plugin payload changed and version advanced: {base_version} -> {current_version}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
