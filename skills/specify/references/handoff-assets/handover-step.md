---
name: handover-step
description: Pre-test handover sequence — checks, staleness sweep,
  review, then hand the step to the operator for testing.
when_to_use: When the current step's implementation is complete and
  ready for operator testing, or when the operator asks for the
  handover. The post-approval close is /approve-step, not this.
allowed-tools:
  - Read
  - Glob
  - Grep
  - Edit
  - Write
  - Agent
  - Bash({{VERIFY_COMMAND}}*)
  - Bash({{CHECK_COMMAND}}*)
  - Bash({{TEST_COMMAND}}*)
  - Bash(git status*)
  - Bash(git diff*)
  - Bash(git log*)
  - Bash(git describe*)
  - Bash(git add*)
  - Bash(git commit*)
---

# Template: handover-step (skill)

> Instantiate as `.claude/skills/handover-step/SKILL.md`. Placeholders:
> the governance set (`{{PLAN}}`, `{{DECISIONS}}`, `{{STEP_ID}}` — see
> the glossary in `handoff.md`);
> `{{VERIFY_COMMAND}}`, `{{CHECK_COMMAND}}`, `{{TEST_COMMAND}}` — the
> repository's rule-2 harness entry points (e.g. `make verify`,
> `npm run check`, `rake test`), here and in `allowed-tools`. Step 3
> invokes the `step-reviewer` agent, so `allowed-tools` must keep the
> subagent-invocation tool (`Agent`) — an allowlist that omits it makes
> the review silently not happen. Delete this header section when
> instantiating.

Hand the current step over for operator testing. In order:

1. **Checks green:** run `{{VERIFY_COMMAND}}` (the verification rule:
   the check and the test halves both pass); fix until it does. If the
   step added artifacts the harness should cover, confirm it actually
   covers them — a check that never ran is not green.
2. **Staleness sweep (the same-commit rule):** update in the same
   commit(s) as the
   work everything the step made stale — `{{PLAN}}` step status (to
   `awaiting test`) and any renumber references, `CLAUDE.md`'s
   current-step pointer and file map, `README.md`'s map, `docs/`
   deliverables, `{{DECISIONS}}` entries, and any `.claude/docs/`
   lesson worth keeping for future sessions.
3. **Review:** run the `step-reviewer` agent over the step's diff
   (last `step-*` tag → HEAD). The diff shows committed work only, so
   the step's work and the sweep must be in commits before it runs.
   Address or explicitly rebut each finding before handover.
4. **Tree clean:** everything above — the step's work, the sweep, the
   review fixes — is already in small, coherent commits with
   `{{STEP_ID}}:` subjects (committed as the work happened, not batched
   here); `git status` shows nothing pending. No catch-all closing
   commit. Never push.
5. **Handover message:** (a) short summary of what the step did;
   (b) precise manual test instructions — exact commands and what the
   operator should observe, including cost and cleanup if the test
   crosses the action boundary; (c) state that you are waiting for
   the operator's verdict. Do not begin the next step.
