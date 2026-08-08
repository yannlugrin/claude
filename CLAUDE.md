# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repository is

A personal collection of Claude Code assets — not an application. There is no build or test tooling; the deliverables are the asset files themselves. Linting exists: `make setup` creates `.venv/` and installs the pre-commit git hook; `make check` runs all lints (ruff, pymarkdown, asset frontmatter validation) on every file.

## Structure

- `skills/` — one directory per skill containing a `SKILL.md` (frontmatter needs `description`; the directory name is the skill/command name)
- `agents/` — subagent definitions, one `.md` per agent with frontmatter (`name`, `description`, optionally `model`, `tools`); the `name` field, not the filename, is the identity
- `hooks/` — hook scripts; symlinking alone does nothing, they must also be registered in a `settings.json` `hooks` block
- `examples/` — scratch/reference material; git-ignored (it also contains a nested git repo — leave it alone)
- `manage.py` — enable/disable tool: symlinks assets into `~/.claude/` (or `--target <dir>`); `status`, `enable`/`disable` with names or `--all`
- `scripts/lint-assets.py` — validates asset frontmatter (skills need a `description`, agents need `name` + `description`); runs via pre-commit, whose hooks are defined in `.pre-commit-config.yaml` and use the `.venv/` tools directly

Assets are deployed with `./manage.py enable` (see README.md). It never deletes real files — only symlinks pointing into this repo.

Legacy slash commands (`commands/<name>.md`) are deprecated in favor of skills: the tooling still supports the type, but no `commands/` directory is kept and none should be created.

## Conventions

- New assets go in the directory matching their type; use kebab-case names.
- The `.gitkeep` files exist only so git tracks the empty directories — remove one when its directory gains real content.
