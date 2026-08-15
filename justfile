# Task runner for this repository.
#
# Prerequisites installed by hand, once: git, just, and python3 (>= 3.11)
# with its `venv` module. Everything else arrives through `just setup`.
#
# Nothing here holds its own list of checks. Both scopes of `check` and the
# installed git hook all read `.pre-commit-config.yaml`, so they can differ in
# how much of the tree they look at and never in what they look for.
#
# Only the single comment line directly above a recipe reaches `just --list`;
# anything longer belongs in the recipe body.

venv := justfile_directory() / ".venv"
pre_commit := venv / "bin" / "pre-commit"

# Show the available recipes.
default:
    @just --list --unsorted

# Fresh clone -> working toolchain. The one documented setup command.
setup:
    #!/usr/bin/env bash
    set -euo pipefail
    python3 -m venv "{{ venv }}"
    "{{ venv }}/bin/python" -m pip install --quiet --disable-pip-version-check \
        --requirement "{{ justfile_directory() }}/requirements.txt"
    "{{ pre_commit }}" install
    "{{ pre_commit }}" install-hooks
    echo "Setup complete. Try: just verify"

# Well-formedness. scope: all (whole tree, the gate) | changed (vs HEAD).
check scope="all": _require-tooling
    #!/usr/bin/env bash
    set -euo pipefail
    cd "{{ justfile_directory() }}"
    case "{{ scope }}" in
    all)
        # The gate: pre-push, CI, anything that decides the tree is sound.
        # Untracked files included, gitignored paths excluded. The
        # enumeration stays read-only: never `git add --intent-to-add`,
        # which writes index state and changes what `git status` reports.
        mapfile -d '' files < <(git ls-files --cached --others --exclude-standard -z)
        empty="No files to check."
        ;;
    changed)
        # The working form: staged, unstaged and untracked. Not a substitute
        # for scope=all before a commit that matters — it cannot see a file
        # committed earlier that a config change here has broken.
        #
        # --diff-filter=d drops deletions: a removed path must not be handed
        # to a hook. `git diff` never reports untracked files, hence the
        # second enumeration.
        mapfile -d '' files < <( {
            git diff --name-only --diff-filter=d -z HEAD
            git ls-files --others --exclude-standard -z
        } | sort -zu )
        empty="Nothing changed since HEAD. Run \`just check\` for the whole tree."
        ;;
    *)
        echo "Unknown scope '{{ scope }}'. Use: all | changed" >&2
        exit 2
        ;;
    esac
    if [ "${#files[@]}" -eq 0 ]; then
        echo "$empty"
        exit 0
    fi
    printf '%s\0' "${files[@]}" | xargs -0 "{{ pre_commit }}" run --files

# Is the implementation right?
test: _require-tooling
    #!/usr/bin/env bash
    set -euo pipefail
    cd "{{ justfile_directory() }}"
    # Only this repository's own behaviour. Third-party tools are not
    # retested here.
    #
    # The guard is executed rather than handed to an interpreter, so this
    # exercises the path Claude Code uses: the shebang and the exec bit.
    # `python3 <file>` would stay green after a lost `+x`, which is one of
    # the ways the guard silently stops running.
    echo "── bash guard: liveness, cases, rule coverage ──"
    .claude/hooks/bash_guard.py --selftest
    echo
    echo "── unit tests: manage.py, scripts/lint-assets.py ──"
    # The venv interpreter, because what these test imports its
    # dependencies from there — a system python3 that happens to have
    # PyYAML passes here and fails on a clean machine, which is what CI is
    # for. The guard above is the other way round on purpose: it must run
    # under the interpreter Claude Code invokes it with.
    "{{ venv }}/bin/python" -m unittest discover \
        --start-directory tests --top-level-directory .

# The whole-tree `check`, then `test`.
verify: check test

[private]
_require-tooling:
    #!/usr/bin/env bash
    if [ ! -x "{{ pre_commit }}" ]; then
        echo "Tooling missing. Run: just setup" >&2
        exit 1
    fi
