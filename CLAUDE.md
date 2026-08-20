# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repository is

A personal collection of Claude Code assets — not an application; the deliverables are the asset files themselves. The toolchain is `just` over `pre-commit`: `just setup` creates `.venv/` from the pinned `requirements.txt` and installs the git hook, `just check [all|changed]` runs every lint, `just test` runs this repository's own behaviour, `just verify` runs both. Checks live once in `.pre-commit-config.yaml`, so the git hook and `just check` cannot look for different things.

## Structure

- `skills/` — one directory per skill containing a `SKILL.md` (frontmatter needs `description`; the directory name is the skill/command name)
- `agents/` — subagent definitions, one `.md` per agent with frontmatter (`name`, `description`, optionally `model`, `tools`); the `name` field, not the filename, is the identity
- `hooks/` — hook scripts; symlinking alone does nothing, they must also be registered in a `settings.json` `hooks` block
- `examples/` — scratch/reference material; git-ignored (it also contains a nested git repo — leave it alone)
- `manage.py` — enable/disable tool: symlinks assets into `~/.claude/` (or `--target <dir>`); `status`, `enable`/`disable` with names or `--all`
- `scripts/lint-assets.py` — validates asset frontmatter (skills need a `description`, agents need `name` + `description`); runs via pre-commit, whose hooks are defined in `.pre-commit-config.yaml` and use the `.venv/` tools directly
- `.claude/hooks/bash_guard.py` — this repository's own `PreToolUse` guard, registered in `.claude/settings.json`. Only its `REGISTRY` section is repository-specific; the engine above that banner is a copy of the template in `skills/specify/references/handoff-assets/` and is refreshed from it by hand. Add a rule and add a `CASES` entry: `--selftest` fails on a rule no case reaches

Assets are deployed with `./manage.py enable` (see README.md). It never deletes real files — only symlinks pointing into this repo.

Legacy slash commands (`commands/<name>.md`) are deprecated in favor of skills: the tooling still supports the type, but no `commands/` directory is kept and none should be created.

## Conventions

- New assets go in the directory matching their type; use kebab-case names.
- The `.gitkeep` files exist only so git tracks the empty directories — remove one when its directory gains real content.
- **This repository is public; the projects it draws on are not.** Never write another project's name — which may be, or may carry, a client's — into an asset, a document or a commit message. Cite provenance by what the work was ("one project's handoff run", "a completed specification run"), never by whose it was.
