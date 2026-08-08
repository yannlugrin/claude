#!/usr/bin/env python3
"""Validate the YAML frontmatter of Claude Code asset files.

Rules, per asset kind (derived from the path):
  skills/<name>/SKILL.md  — frontmatter required, with a non-empty `description`;
                            a `name` field, if present, must match the directory.
  agents/<name>.md        — frontmatter required, with non-empty `name` and
                            `description`.
  commands/<name>.md      — frontmatter optional, but must be valid YAML if present.

Receives the files to check as arguments (as pre-commit passes them).
"""

import sys
from pathlib import Path

import yaml


def parse_frontmatter(text: str):
    """Return (frontmatter dict or None, error string or None)."""
    lines = text.split("\n")
    if not lines or lines[0].strip() != "---":
        return None, None
    for index, line in enumerate(lines[1:], start=1):
        if line.strip() == "---":
            try:
                data = yaml.safe_load("\n".join(lines[1:index]))
            except yaml.YAMLError as exc:
                return None, f"invalid YAML in frontmatter: {exc}"
            if not isinstance(data, dict):
                return None, "frontmatter is not a YAML mapping"
            return data, None
    return None, "frontmatter opened with `---` but never closed"


def check(path: Path) -> list[str]:
    kind = path.parts[0] if len(path.parts) > 1 else None
    frontmatter, error = parse_frontmatter(path.read_text(encoding="utf-8"))
    if error:
        return [error]

    errors = []
    if kind == "skills":
        if path.name != "SKILL.md":
            return []  # supporting file, nothing to validate
        if frontmatter is None:
            return ["missing frontmatter (a skill needs a `description`)"]
        if not str(frontmatter.get("description") or "").strip():
            errors.append("frontmatter needs a non-empty `description`")
        name = frontmatter.get("name")
        if name is not None and name != path.parent.name:
            errors.append(
                f"frontmatter `name: {name}` does not match directory `{path.parent.name}`"
            )
    elif kind == "agents":
        if frontmatter is None:
            return ["missing frontmatter (an agent needs `name` and `description`)"]
        for field in ("name", "description"):
            if not str(frontmatter.get(field) or "").strip():
                errors.append(f"frontmatter needs a non-empty `{field}`")
    return errors


def main(argv: list[str]) -> int:
    status = 0
    for arg in argv:
        for error in check(Path(arg)):
            print(f"{arg}: {error}")
            status = 1
    return status


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
