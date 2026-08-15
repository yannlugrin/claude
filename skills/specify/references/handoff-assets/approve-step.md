---
name: approve-step
description: Post-approval close of the current step — run only when the
  operator has declared the step approved in this exchange, after their
  manual testing. Sets status `done`, compacts the entry to its outcome,
  puts the annotated step tag on the close commit, and attempts the push
  so the permission gate puts the publish decision to the operator.
---

# Template: approve-step (skill)

> Instantiate as `.claude/skills/approve-step/SKILL.md`. Placeholders:
> `{{PLAN}}` — the plan governing the work this file performs;
> `{{STEP_ID}}` — the step identifier form used in commit subjects and
> tag names (`step-NNN`, unless this repository qualifies it per
> track); plus
> `{{CHECK_COMMAND}}` (step 3) — the
> repository's rule-2 check entry point in its **full** form, never a
> narrowed fast pass: the close commit receives the step tag and
> is the state every later session treats as known-good. Step 5
> references `state-reviewer` and `optimize-memory`: keep the step even
> when they are not adopted — it falls back to `CLAUDE.md`'s
> not-yet-adopted list, and deleting it removes the passes' only
> in-ritual trigger. When either agent is explicitly dropped, or once
> the not-yet-adopted block is deleted with the assets directory,
> rewire step 5 to the standing fallback (a fresh subagent briefed
> inline, as `CLAUDE.md` restates it) in the same commit — the step
> must never name an agent that exists nowhere.
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
> Re-probe before reintroducing any of them. Delete this header
> section when instantiating.

**When to use.** Only after the operator has declared the step approved
in this exchange, following their own manual test. The pre-test handover
is `/handover-step`, not this.

Close the approved step. The precondition is the operator's explicit
approval in this exchange; if their message leaves any doubt, ask —
never treat this skill's invocation context as the approval itself.

In order:

1. **Confirm scope:** the step being closed is the one in `awaiting
   test`; its number has been frozen since it entered `in progress`.
2. **Compact the step entry — replace it, do not annotate it.** The
   entry described a plan; the step is now history, so everything that
   was a plan goes: objective, spec sections, dependencies,
   deliverables, how the operator tests it. What remains is the
   heading marked `done` and a single outcome bullet carrying the
   approval date, the tag, what now exists and what it decided, and a
   pointer to the tag range where the detail lives:

       ### {{STEP_ID}} — <step title> — `done`

       - **Outcome (approved YYYY-MM-DD, tag `{{STEP_ID}}`):** what now
         exists and what it decided, in a few lines, citing the decision
         entries it rests on. Detail in git history between tags
         `<previous step tag>` and `{{STEP_ID}}`.

   `CLAUDE.md`'s plan conventions state the same invariant in one line,
   because the first closes happen before this skill exists; this file
   carries how to reach it, which only matters while performing a
   close. If the two ever disagree about the shape, `CLAUDE.md` wins —
   it is what the plan is actually written against.

   Write the bullet as the tag message's opening paragraph condensed
   (step 4 writes that message in the same commit-and-tag pass), so the
   two cannot disagree. Deleting the plan text is the point: an
   approved step's deliverable list keeps asserting intentions the step
   itself changed, in the file every session reads at start.
3. **Close commit:** in one commit — that compacted entry with its
   status `done`; `CLAUDE.md`'s "Current state" pointed at the next
   step **and the closed step's paragraph deleted, not demoted**: its
   outcome is in the entry and the tag this same commit writes, a
   durable fact belongs in `.claude/docs/`, an obligation in the plan,
   an invariant in the decision log. A third copy in `CLAUDE.md` is how
   that section becomes a changelog — measured once at 131 lines, a
   paragraph at a time, each defensible on its own. Anything else the
   approval made stale. Run
   `{{CHECK_COMMAND}}` before committing.
   Subject: `{{STEP_ID}}: close — approved, status done, entry
   compacted`.
4. **Annotated tag** `{{STEP_ID}}` on that commit. Message shape
   follows the existing tags (`git tag -n99 -l 'step-*'`): a title
   line `{{STEP_ID}} — <step title>`, then `Approved YYYY-MM-DD.` and
   a short paragraph of the step's notable outcomes.
5. **Milestone boundary:** if this was the milestone's last step, do
   not start the next one — suggest the whole-state review and then
   the memory-compaction pass, in that order, so the compaction runs
   after the review has read the uncompacted memory. The adopted
   agents (`state-reviewer`, `optimize-memory`) perform them where they
   exist; where they were not adopted, point at `CLAUDE.md`'s
   not-yet-adopted list; where they were dropped or that list no longer
   exists, brief a fresh subagent inline from a clean context — the
   passes are required whoever performs them, and this step is their
   in-ritual trigger.
   **Spawn both on a model that did not write the milestone's work.**
   Normally that is any model other than yours — but a milestone spans
   many steps and may span models, so the one to exclude is whichever
   implemented, not merely your own. Pass the override explicitly at
   invocation: neither agent pins a model, and omitting the override
   does not mean "no opinion", it means they inherit yours, which is
   the one outcome to avoid. If no second model is available, say so
   when reporting the passes rather than presenting them as
   independent. This applies to these two passes only — the
   pre-handover review of `/handover-step` buys a cold context, which
   any model gives, and may run on yours.
6. **Report, then attempt the push.** Show the step summary and what
   the close commit and tag contain — with `CLAUDE.md`'s line count and
   its change since the last close, so growth is visible at the moment
   it happens and in front of the operator. Over budget, present
   **both** remedies and let them rule: what could move out, and
   raising the budget. Never resolve it by compressing something that
   cannot be compressed without loss — the number is a signal, and a
   gate here would make deletion the cheapest way to go green. Then run
   `git push --follow-tags`
   — `--follow-tags` carries the annotated tag with the commit, where a
   bare `git push` leaves the step tag behind, and a tag that exists
   only locally is invisible to everything reading the remote.

   **This is a named exception to rule 9's "never on your own
   initiative", and it does not generalise.** It holds here because the
   operator has just approved the step, the only open question is
   whether this closed state should be published now, and the
   permission gate answers exactly that question at exactly that
   moment — better than an offer they have to remember to answer. It
   does *not* license attempting any other gated act on the grounds
   that something downstream will catch it: everywhere else the guard
   is a backstop, never a substitute for asking. It rests on the push
   being gated here — a property recorded with this repository's other
   measured permission behaviour, established once and re-measured when
   the harness changes, never re-established at each close. If a close
   ever pushes with no prompt, stop and report it: the exception has
   lost its footing and the ritual goes back to asking in prose.

   **A refusal is final.** If the push is declined or denied, say so,
   leave the commit and its tag local, and stop — no retry, no
   narrower spelling, no pushing the branch without the tag. Where no
   remote exists yet, say that instead of attempting anything. Either
   way the next step starts only on the operator's go.
