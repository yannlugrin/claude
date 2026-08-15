#!/usr/bin/env python3
"""Validate the YAML frontmatter of Claude Code asset files.

Rules, per asset kind (derived from the path):
  skills/<name>/SKILL.md  — frontmatter required, with a non-empty `description`;
                            a `name` field, if present, must match the directory;
                            and none of the keys under INERT_SKILL_KEYS.
  skills/<name>/**        — any file in a skill directory: its frontmatter must
                            parse if it has any, and a `SKILL.md` must exist
                            beside it — a directory without one is not a skill.
  agents/<name>.md        — frontmatter required, with non-empty `name` and
                            `description`.
  commands/<name>.md      — frontmatter optional, but must be valid YAML if present.

Everything here guards a silent failure: malformed frontmatter does not raise
at load time, the asset simply never loads.

Receives the files to check as arguments (as pre-commit passes them), relative
to the repository root. A path outside it is refused rather than passed, since
a check that silently validates nothing is worse than no check.
"""

import sys
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
ASSET_KINDS = ("skills", "agents", "commands", "hooks")

# Skill frontmatter keys that look like they do something and do not. Measured
# on Claude Code 2.1.231–2.1.233; re-measure before removing an entry.
INERT_SKILL_KEYS = {
    "allowed-tools": "restricts nothing — a skill's allowlist is not enforced, "
                     "so it reads as a guard while being none",
    "disallowed-tools": "binds for the whole turn that invoked the skill and "
                        "never prompts, stranding the rest of that turn",
    "when_to_use": "is not a key Claude Code defines; put it in `description` "
                   "and restate it in the body",
}


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


def relative_to_repo(path: Path) -> Path | None:
    """The path as the repository sees it, or None if it lies outside."""
    try:
        return path.resolve().relative_to(REPO_ROOT)
    except ValueError:
        return None


def check(path: Path) -> list[str]:
    inside = relative_to_repo(path)
    if inside is None:
        return [f"outside the repository ({REPO_ROOT}), so no rules apply to it"]
    kind = inside.parts[0] if len(inside.parts) > 1 else None
    if kind is not None and kind not in ASSET_KINDS:
        kind = None
    frontmatter, error = parse_frontmatter(path.read_text(encoding="utf-8"))
    if error:
        return [error]

    errors = []
    if kind == "skills":
        skill_dir = REPO_ROOT / "skills" / inside.parts[1]
        if len(inside.parts) > 2 and not (skill_dir / "SKILL.md").exists():
            errors.append(
                f"`skills/{inside.parts[1]}/` has no SKILL.md, so it is not a skill "
                "and nothing in it loads"
            )
        if path.name != "SKILL.md":
            return errors  # supporting file, nothing else to validate
        if frontmatter is None:
            return ["missing frontmatter (a skill needs a `description`)"]
        if not str(frontmatter.get("description") or "").strip():
            errors.append("frontmatter needs a non-empty `description`")
        name = frontmatter.get("name")
        if name is not None and name != path.parent.name:
            errors.append(
                f"frontmatter `name: {name}` does not match directory `{path.parent.name}`"
            )
        for key, why in INERT_SKILL_KEYS.items():
            if key in frontmatter:
                errors.append(f"frontmatter key `{key}` {why}")
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
