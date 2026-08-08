#!/usr/bin/env python3
"""Enable/disable Claude Code assets from this repo by symlinking them into a
Claude config directory (~/.claude by default, or a project's .claude via --target).

Usage:
  ./manage.py status
  ./manage.py enable --all
  ./manage.py enable my-skill agents/my-agent
  ./manage.py disable --all
  ./manage.py disable my-skill
"""

import argparse
import sys
from dataclasses import dataclass
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent
ASSET_TYPES = ("skills", "agents", "commands", "hooks")
DEFAULT_TARGET = Path.home() / ".claude"


@dataclass(frozen=True)
class Asset:
    kind: str        # skills | agents | commands | hooks
    name: str        # selection name (file stem or directory name)
    source: Path     # absolute path inside the repo

    @property
    def qualified(self) -> str:
        return f"{self.kind}/{self.name}"

    def link_path(self, target: Path) -> Path:
        return target / self.kind / self.source.name


def discover() -> list[Asset]:
    assets = []
    for kind in ASSET_TYPES:
        kind_dir = REPO_ROOT / kind
        if not kind_dir.is_dir():
            continue
        for entry in sorted(kind_dir.iterdir()):
            if entry.name.startswith("."):
                continue
            name = entry.stem if entry.is_file() else entry.name
            assets.append(Asset(kind, name, entry))
    return assets


def state(asset: Asset, target: Path) -> str:
    link = asset.link_path(target)
    if not link.exists() and not link.is_symlink():
        return "disabled"
    if link.is_symlink() and link.resolve() == asset.source.resolve():
        return "enabled"
    return "conflict"


def select(assets: list[Asset], selectors: list[str]) -> list[Asset]:
    """Resolve user selectors (`name` or `kind/name`) to assets."""
    chosen = []
    for sel in selectors:
        if "/" in sel:
            kind, _, name = sel.partition("/")
            matches = [a for a in assets if a.kind == kind and a.name == name]
        else:
            matches = [a for a in assets if a.name == sel]
        if not matches:
            sys.exit(f"error: no asset named '{sel}'"
                     f" (run './manage.py status' to list assets)")
        if len(matches) > 1:
            options = ", ".join(a.qualified for a in matches)
            sys.exit(f"error: '{sel}' is ambiguous, qualify it: {options}")
        chosen.extend(matches)
    return chosen


def enable(asset: Asset, target: Path, force: bool) -> str:
    link = asset.link_path(target)
    current = state(asset, target)
    if current == "enabled":
        return f"  = {asset.qualified} already enabled"
    if current == "conflict":
        if not (force and link.is_symlink()):
            what = "foreign symlink" if link.is_symlink() else "real file"
            hint = " (use --force to replace)" if link.is_symlink() else \
                   " (refusing to touch a real file; move it away yourself)"
            return f"  ! {asset.qualified} blocked by {what} at {link}{hint}"
        link.unlink()
    link.parent.mkdir(parents=True, exist_ok=True)
    link.symlink_to(asset.source)
    return f"  + {asset.qualified} enabled -> {link}"


def disable(asset: Asset, target: Path) -> str:
    link = asset.link_path(target)
    current = state(asset, target)
    if current == "disabled":
        return f"  = {asset.qualified} already disabled"
    if current == "conflict":
        what = "foreign symlink" if link.is_symlink() else "real file"
        return f"  ! {asset.qualified} not ours ({what} at {link}), left in place"
    link.unlink()
    return f"  - {asset.qualified} disabled"


def cmd_status(assets: list[Asset], target: Path) -> None:
    if not assets:
        print("no assets in the repo yet")
        return
    print(f"target: {target}")
    width = max(len(a.qualified) for a in assets)
    for asset in assets:
        marker = {"enabled": "*", "disabled": " ", "conflict": "!"}[state(asset, target)]
        print(f"  [{marker}] {asset.qualified:<{width}}  {state(asset, target)}")


def main() -> None:
    parser = argparse.ArgumentParser(
        description=__doc__.splitlines()[0],
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--target", type=Path, default=DEFAULT_TARGET,
                        help="Claude config directory to link into (default: ~/.claude)")
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("status", help="list assets and whether they are enabled")

    for verb in ("enable", "disable"):
        p = sub.add_parser(verb, help=f"{verb} assets ({verb} --all or by name)")
        p.add_argument("names", nargs="*", metavar="name",
                       help="asset name, or kind/name if ambiguous")
        p.add_argument("--all", action="store_true", help=f"{verb} every asset")
        if verb == "enable":
            p.add_argument("--force", action="store_true",
                           help="replace a foreign symlink occupying the link path")

    args = parser.parse_args()
    target = args.target.expanduser().resolve()
    assets = discover()

    if args.command == "status":
        cmd_status(assets, target)
        return

    if args.all == bool(args.names):
        sys.exit("error: pass asset names or --all (not both, not neither)")
    chosen = assets if args.all else select(assets, args.names)
    if not chosen:
        print("nothing to do: no assets in the repo yet")
        return

    blocked = False
    for asset in chosen:
        if args.command == "enable":
            line = enable(asset, target, args.force)
        else:
            line = disable(asset, target)
        print(line)
        blocked = blocked or line.lstrip().startswith("!")
    if blocked:
        sys.exit(1)


if __name__ == "__main__":
    main()
