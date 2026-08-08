# Claude assets

Personal collection of Claude Code skills, agents, and hooks.

## Layout

- `skills/` — [Agent Skills](https://code.claude.com/docs/en/skills): one directory per skill with a `SKILL.md` entrypoint (YAML frontmatter with a `description`, then instructions) plus optional supporting files. The directory name becomes the `/<name>` command; Claude can also load a skill automatically when its description matches the task. Deploys to `~/.claude/skills/<name>/` — symlinked entries are officially supported.
- `agents/` — [Subagents](https://code.claude.com/docs/en/sub-agents): one Markdown file per agent with YAML frontmatter (`name`, `description`, optional `tools`, `model`) followed by the agent's system prompt. Identity comes from the `name` field, not the filename. Deploys to `~/.claude/agents/`.
- `hooks/` — [Hooks](https://code.claude.com/docs/en/hooks): scripts run at lifecycle events (`PreToolUse`, `Stop`, `SessionStart`, …). There is no autoload directory: linking a script into `~/.claude/hooks/` only places the file — it must also be registered by path under `hooks` in `settings.json` to run.
- `examples/` — scratch material, git-ignored

Legacy [slash commands](https://code.claude.com/docs/en/skills) (a bare `commands/<name>.md`) are still understood by the tooling, but no `commands/` directory is kept — new work should be a skill, which covers the same `/<name>` invocation and more.

## Usage

`manage.py` enables/disables assets by symlinking them into `~/.claude/` (user-wide) or, with `--target`, a project's `.claude/` directory:

```sh
./manage.py status                        # list assets and their state
./manage.py enable --all                  # link everything
./manage.py enable my-skill               # link selected assets by name
./manage.py enable agents/my-agent        # qualify with kind/ if a name is ambiguous
./manage.py disable my-skill              # remove the symlink
./manage.py --target ../app/.claude enable my-skill
```

It only ever removes symlinks pointing into this repo — real files and foreign symlinks at a link path are reported, never deleted (`enable --force` replaces foreign symlinks only).

## Development

```sh
make setup   # create .venv, install dependencies, install the pre-commit git hook
make check   # run all lints on all files (also run automatically on commit)
```

Requires Python 3 with the `venv` module (`apt install python3-venv` on Debian/Ubuntu). Lints: [ruff](https://docs.astral.sh/ruff/) for Python, [pymarkdown](https://github.com/jackdewinter/pymarkdown) for Markdown, and `scripts/lint-assets.py` for asset frontmatter (skills need a `description`, agents a `name` and `description`). Hooks are defined in `.pre-commit-config.yaml` and run the `.venv/` tools directly, so `make check` and the git hook share one toolchain.
