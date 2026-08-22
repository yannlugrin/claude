---
name: handover-step
description: Pre-test handover sequence — run when the current step's
  implementation is complete and ready for operator testing, when a
  gated step's cases are written and ready for approval, or when the
  operator asks for the handover. Checks, staleness sweep, review, then
  hand the step to the operator.
---

# Template: handover-step (skill)

> Instantiate as `.claude/skills/handover-step/SKILL.md`. Placeholders:
> `{{PLAN}}` and `{{DECISIONS}}` — the plan and decision log governing
> the work this file performs; `{{STEP_ID}}` — the step identifier form
> used in commit subjects and tag names (`step-NNN`, unless this
> repository qualifies it per track);
> `{{VERIFY_COMMAND}}` — the repository's rule-2 verification entry
> point, the one that runs both check and test (e.g. `make verify`,
> `just verify`); `{{TEST_GATE}}` — whether the plan gates any step's
> tests, which decides whether the two-handover clause below and the
> closing section survive instantiation. Where the plan has no gate,
> delete both and drop the gated-step clause from the `description`,
> rather than shipping a mode this project never enters.
> Frontmatter carries `name` and `description` only, deliberately: a
> skill's `allowed-tools` list restricts nothing (probed live, Claude
> Code 2.1.231 — a `Write` and a plain `ls` both ran while a read-only
> ritual was active), `disallowed-tools` binds the whole invoking turn
> and never prompts, and a key Claude Code does not
> define (`when_to_use`) buys nothing while its handling is
> unspecified — keep frontmatter to keys the version you run
> defines. That last one is a precaution, not a measurement,
> unlike the two before it. What
> actually binds lives in `.claude/settings.json` and the guard hook.
> Re-probe before reintroducing any of them — and if a version ever
> makes allowlists bind, the list must keep the subagent-invocation tool
> (`Agent` in Claude Code; verify the name in the version you run),
> since step 3 invokes the `step-reviewer` agent and a missing entry
> would make that review silently not happen.
>
> **Once this project has measured that for itself, this block becomes a
> one-line pointer** at the `.claude/docs/` file holding the measurement,
> naming its section — the reasoning is a fact about the installed
> tooling, and a fact restated in four ritual files ages four times over
> in files a session opens to perform a ritual, not to learn about
> frontmatter. It stays written out here because the first instantiation
> has nothing to point at yet. Check the section number resolves after
> you write it.
> Delete this header section when instantiating.

**When to use.** When the step is implemented and ready for the
operator's manual test, or when they ask for the handover. The
post-approval close is `/approve-step`, not this.

**A gated step hands over twice.** `{{PLAN}}` says which steps are gated:
there the cases are handed over first, on their own, and the
implementation does not start until the operator has approved them. Run
this skill both times — once at the **test gate**, once at the ordinary
handover — and read the closing section for what differs at the first.
Every other step has one handover.

Hand the current step over for operator testing. In order:

1. **Checks green:** run `{{VERIFY_COMMAND}}` (the verification rule:
   the check and the test halves both pass); fix until it does. If the
   step added artifacts the harness should cover, confirm it actually
   covers them — a check that never ran is not green.
2. **Staleness sweep (the same-commit rule):** update in the same
   commit(s) as the
   work everything the step made stale — `{{PLAN}}` step status (to
   `awaiting test`, or to `awaiting case approval` at a test gate) and
   any renumber references, `CLAUDE.md`'s
   current-step pointer and file map, `README.md`'s map, `docs/`
   deliverables, `{{DECISIONS}}` entries, and any `.claude/docs/`
   lesson worth keeping for future sessions.
3. **Review:** run the `step-reviewer` agent over the step's diff
   (last `step-*` tag → HEAD). The diff shows committed work only, so
   the step's work and the sweep must be in commits before it runs.
   Address or explicitly rebut each finding before handover. **A
   finding is true of the tree the reviewer read**, and fixes move that
   tree — so before applying one, check it still holds against the tree
   you now have, changes made answering the same review included. Any
   finding whose justification is *nothing needs this* gets that claim
   re-derived rather than inherited: a deletion argued on absence of
   need is the finding most likely to have expired.
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

## At the test gate, five things differ

- **Step 1 inverts.** The check half must be green — the cases are code
  and are held to it — while the test half must be **red**, failing on
  the new cases and on nothing else. Quote the failing output and trace
  each failure to the assertion it comes from: an import error, a fixture
  typo and a suite that never ran are all red, and none of them is a
  case.
- **Every case declares its source.** *Transcribed* from a specification
  section, cited; or *decided*, fixing something the specification left
  open — logged where it is within your latitude, put to the operator
  before the gate closes where it is not. A case that decides is fine. A
  case that decides while presenting itself as required is the defect
  this handover exists to catch. Where a case settles a fact the
  specification ordered settled during implementation, the amendment
  lands under rule 1 once the operator approves.
- **Step 3 runs `test-reviewer` alone**, and its question is different:
  do these cases state what the specification requires or declare what
  they decide, and would each fail for the reason it names. The reviewers
  that read an implementation wait for the second handover.
- **Step 5 asks for approval of the cases, not a manual test.** There is
  nothing to run yet but the red run itself. Name what the cases pin,
  what they deliberately leave open, and what is *not* covered.
- **The status is `awaiting case approval`, never `awaiting test`.**
  There is no implementation to test, and `/approve-step` closes a step
  in `awaiting test` — so the wrong status here lets an approval of the
  cases close, compact and tag a step that was never built. Approval
  moves the step back to `in progress` for the implementation; it does
  not advance it.
- **Approved cases are frozen, and say so in the handover.** Adding a
  case during implementation is free. Changing or deleting one comes back
  to the operator as a change — and so does a new case that narrows or
  contradicts an approved one, which is a change whatever operation
  performs it.

At the second handover everything above returns to normal, with one
addition: **the summary names every case added since the gate**, and
which of them decided anything.
