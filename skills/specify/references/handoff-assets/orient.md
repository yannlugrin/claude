---
name: orient
description: Session-start orientation — run before touching anything.
  Establishes the current step, the last approved state and the work in
  progress, then reports and stops.
when_to_use: At the start of a normal session, after /clear, or when
  the operator asks where we are. After an interruption (usage limit,
  crash, killed console) or when the last session's claims are in
  doubt, /resume-step is the right ritual, not this.
allowed-tools:
  - Read
  - Glob
  - Grep
  - Bash(git describe*)
  - Bash(git log*)
  - Bash(git diff*)
  - Bash(git status*)
disallowed-tools: Edit, Write, NotebookEdit
---

# Template: orient (skill)

> Instantiate as `.claude/skills/orient/SKILL.md`. Placeholders: none.
> Delete this header section when instantiating.

Execute the session-start routine from CLAUDE.md, in order:

1. Read `CLAUDE.md` in full, `PLAN.md`'s current step (the pointer is
   in CLAUDE.md's "Current state"), and the tail of `DECISIONS.md`.
2. Read the spec sections the current step lists.
3. Locate the last approved state — match the step namespace only:
   `git describe --tags --abbrev=0 --match 'step-*'`
   Before the first step tag exists, the range is the whole history.
4. Review the work in progress: `git log` and `git diff` from that tag
   (or root) to `HEAD`, plus `git status` for uncommitted work.
5. Anomaly check: if what you gathered does not add up — a dirty tree
   the step's status does not explain, a `PLAN.md` status the diff
   contradicts, a stale `CLAUDE.md` pointer — do not deliver the
   normal report: report the anomaly and recommend `/resume-step`,
   then stop. This skill detects; it does not diagnose.
6. Report to the operator: current step and status, what the
   in-progress diff contains, and what remains — then stop and wait
   for instructions. Touch nothing before reporting.
