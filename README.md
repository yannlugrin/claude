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
just setup           # create .venv from requirements.txt, install the git hook
just check           # every check over the whole tree, untracked files included
just check changed   # the same checks over what differs from HEAD
just test            # this repository's own behaviour
just verify          # check, then test
```

Requires [`just`](https://github.com/casey/just) and Python 3 with the `venv` module (`apt install python3-venv` on Debian/Ubuntu). Checks are defined once in `.pre-commit-config.yaml` — `just check` and the installed git hook both read it, so they cannot differ in *what* they look for, only in how much of the tree they look at. Lints: [ruff](https://docs.astral.sh/ruff/) for Python, [pymarkdown](https://github.com/jackdewinter/pymarkdown) for Markdown, `scripts/lint-assets.py` for asset frontmatter (skills need a `description`, agents a `name` and `description`), plus the upstream hygiene hooks and a liveness check for the Bash guard. Dependency versions are pinned in `requirements.txt`.

Note that `just check` can *modify* files: the whitespace hooks fix what they find and fail the run, so a red check may leave a changed tree to inspect and commit.

### The Bash guard

`.claude/hooks/bash_guard.py` is a `PreToolUse` hook registered in `.claude/settings.json`. It gates what a permission prefix cannot express — a flag that arrives late, a command inside a wrapper — deciding on parsed argv per subcommand. Here it carries the standard git rules, docker's publish and host-global sweeps, `manage.py`'s two acts that reach outside this clone, and an `rm` that is silent only under the rebuildable directories.

It is an instantiation of the template shipped at `skills/specify/references/handoff-assets/bash_guard.py`; everything above its `REGISTRY` banner is meant to stay identical to it, and improvements there are copied down by hand. `just test` runs its full case suite, and every commit runs `--liveness` — a hook that stops loading fails open silently, so it is gated twice.
