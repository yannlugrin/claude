---
name: approve-step
description: Post-approval close of the current step — status `done`,
  entry compacted, annotated step tag on the close commit.
when_to_use: Only when the operator has declared the step approved in
  this exchange — after their manual testing, never on inference. The
  pre-test handover is /handover-step, not this.
allowed-tools:
  - Read
  - Glob
  - Grep
  - Edit
  - Write
  - Bash({{CHECK_COMMAND}}*)
  - Bash(git status*)
  - Bash(git diff*)
  - Bash(git log*)
  - Bash(git describe*)
  - Bash(git add*)
  - Bash(git commit*)
  - Bash(git tag -a*)
  - Bash(git tag -n99*)
---

# Template: approve-step (skill)

> Instantiate as `.claude/skills/approve-step/SKILL.md`. Placeholders:
> `{{PLAN}}` — the plan governing the work this file performs;
> `{{STEP_ID}}` — the step identifier form used in commit subjects and
> tag names (`step-NNN`, unless this repository qualifies it per
> track); plus
> `{{CHECK_COMMAND}}` (twice: `allowed-tools` and step 2) — the
> repository's rule-2 check entry point in its **full** form, never a
> narrowed fast pass: the close commit receives the step tag and
> is the state every later session treats as known-good. Step 4
> references `state-reviewer` and `optimize-memory`: keep the step even
> when they are not adopted — it falls back to `CLAUDE.md`'s
> not-yet-adopted list, and deleting it removes the passes' only
> in-ritual trigger. When either agent is explicitly dropped, or once
> the not-yet-adopted block is deleted with the assets directory,
> rewire step 4 to the standing fallback (a fresh subagent briefed
> inline, as `CLAUDE.md` restates it) in the same commit — the step
> must never name an agent that exists nowhere. Delete this header
> section when instantiating.

Close the approved step. The precondition is the operator's explicit
approval in this exchange; if their message leaves any doubt, ask —
never treat this skill's invocation context as the approval itself.

In order:

1. **Confirm scope:** the step being closed is the one in `awaiting
   test`; its number has been frozen since it entered `in progress`.
2. **Close commit:** in one commit — `{{PLAN}}` step status to `done`
   and the step entry compacted to its outcome (a few lines: what was
   approved, date, tag name; detail stays in git history); `CLAUDE.md`
   "Current state" pointed at the next step; anything else the
   approval made stale. Run `{{CHECK_COMMAND}}` before committing.
   Subject: `{{STEP_ID}}: close — approved, status done, entry
   compacted`.
3. **Annotated tag** `{{STEP_ID}}` on that commit. Message shape
   follows the existing tags (`git tag -n99 -l 'step-*'`): a title
   line `{{STEP_ID}} — <step title>`, then `Approved YYYY-MM-DD.` and
   a short paragraph of the step's notable outcomes.
4. **Milestone boundary:** if this was the milestone's last step, do
   not start the next one — suggest the whole-state review and then
   the memory-compaction pass. The adopted agents (`state-reviewer`,
   `optimize-memory`) perform them where they exist; where they were
   not adopted, point at `CLAUDE.md`'s not-yet-adopted list; where
   they were dropped or that list no longer exists, brief a fresh
   subagent inline from a clean context — the passes are required
   whoever performs them, and this step is their in-ritual trigger.
5. **Never push.** The next step starts only on the operator's go.
