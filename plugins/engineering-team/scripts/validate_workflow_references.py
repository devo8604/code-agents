#!/usr/bin/env python3
"""Validate cross-references among plugin skills, agents, and UI metadata."""

from __future__ import annotations

import re
import os
import shutil
import sys
from pathlib import Path


try:
    import tomllib
except ModuleNotFoundError:
    for candidate in ("python3.13", "python3.12", "python3.11"):
        executable = shutil.which(candidate)
        if executable and Path(executable).resolve() != Path(sys.executable).resolve():
            os.execv(executable, [executable, __file__, *sys.argv[1:]])
    print("Python 3.11 or newer is required to validate workflow references.", file=sys.stderr)
    raise SystemExit(2)


PLUGIN_ROOT = Path(__file__).resolve().parents[1]
SKILL_ROOT = PLUGIN_ROOT / "skills"
AGENT_ROOT = PLUGIN_ROOT / "templates" / "custom-agents"
SKILL_REFERENCE = re.compile(r"\$([a-z][a-z0-9-]+)")
ROLE_REFERENCE = re.compile(
    r"`((?:[a-z][a-z0-9]*_engineer)|docs_researcher|technical_writer)`"
)
FRONTMATTER_NAME = re.compile(r"\A---\nname:\s*([a-z][a-z0-9-]+)\n", re.MULTILINE)
DEFAULT_PROMPT = re.compile(r'^\s*default_prompt:\s*"([^"]+)"\s*$', re.MULTILINE)


def main() -> int:
    errors: list[str] = []
    agents: set[str] = set()
    for path in sorted(AGENT_ROOT.glob("*.toml")):
        data = tomllib.loads(path.read_text(encoding="utf-8"))
        name = data["name"]
        agents.add(name)
        expected_filename = name.replace("_", "-") + ".toml"
        if path.name != expected_filename:
            errors.append(
                f"{path}: filename must be {expected_filename!r} for role {name!r}"
            )

    skills: dict[str, Path] = {}
    for path in sorted(SKILL_ROOT.glob("*/SKILL.md")):
        content = path.read_text(encoding="utf-8")
        match = FRONTMATTER_NAME.search(content)
        if match is None:
            errors.append(f"{path}: cannot resolve frontmatter skill name")
            continue
        name = match.group(1)
        skills[name] = path
        if path.parent.name != name:
            errors.append(f"{path}: directory name must match skill name {name!r}")

    for path in sorted(SKILL_ROOT.glob("*/**/*")):
        if not path.is_file() or path.suffix not in {".md", ".yaml"}:
            continue
        content = path.read_text(encoding="utf-8")
        referenced_skills = {
            match.group(1)
            for match in SKILL_REFERENCE.finditer(content)
            if match.end() == len(content) or content[match.end()] != ":"
        }
        for skill in sorted(referenced_skills - skills.keys()):
            errors.append(f"{path}: unknown skill reference ${skill}")
        for role in sorted(set(ROLE_REFERENCE.findall(content)) - agents):
            errors.append(f"{path}: unknown agent role reference {role!r}")

    for name, skill_path in skills.items():
        metadata = skill_path.parent / "agents" / "openai.yaml"
        if not metadata.exists():
            errors.append(f"{skill_path.parent}: missing agents/openai.yaml")
            continue
        match = DEFAULT_PROMPT.search(metadata.read_text(encoding="utf-8"))
        if match is None or f"${name}" not in match.group(1):
            errors.append(f"{metadata}: default_prompt must reference ${name}")

    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print(f"Validated {len(skills)} skills and {len(agents)} agent role references.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
