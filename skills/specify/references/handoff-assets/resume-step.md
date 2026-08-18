---
name: resume-step
description: Post-interruption verification — run after work ended
  abnormally (a usage limit, a crash, a reboot, a killed console) or
  whenever the operator doubts what the last session claims to have done.
  Distrusts the transcript, verifies the claimed state against the
  repository and the world, then reports discrepancies and repair
  options. Verifies and reports only; it never repairs.
---

# Template: resume-step (skill)

> Instantiate as `.claude/skills/resume-step/SKILL.md`. Placeholders:
> `{{PLAN}}` and `{{DECISIONS}}` — the plan and decision log governing
> the work this file performs;
> `{{CHECK_COMMAND}}` — the rule-2 check entry point;
> `{{STATE_CHECKS}}` — the project's read-only
> world-state commands (service status, container lists, mounted
> volumes…), each marked free or gated per the rule-9 boundary.
> Frontmatter carries `name` and `description` only, deliberately: a
> skill's `allowed-tools` list restricts nothing (probed live, Claude
> Code 2.1.231 — a `Write` and a plain `ls` both ran while a read-only
> ritual was active), `disallowed-tools` binds the whole invoking turn
> and never prompts, and a key Claude Code does not
> define (`when_to_use`) buys nothing while its handling is
> unspecified — keep frontmatter to keys the version you run
> defines. That last one is a precaution, not a measurement,
> unlike the two before it. This
> ritual's verify-only discipline is prose, below; what actually binds
> lives in `.claude/settings.json` and the guard hook. Re-probe before
> reintroducing any of them.>
> **Once this project has measured that for itself, this block becomes a
> one-line pointer** at the `.claude/docs/` file holding the measurement,
> naming its section — the reasoning is a fact about the installed
> tooling, and a fact restated in four ritual files ages four times over
> in files a session opens to perform a ritual, not to learn about
> frontmatter. It stays written out here because the first instantiation
> has nothing to point at yet. Check the section number resolves after
> you write it.
> Delete this header section when instantiating.

Work was interrupted or the last session's claims are in doubt. Your
job is to establish what is actually true, then stop.

**When to use.** Instead of `/orient` — it embeds the same orientation —
after an abnormal end, or whenever the operator doubts the last
session's account. Prefer invoking it from a fresh session, which cannot
be tempted to trust the old transcript.

**Doctrine: the transcript is a claim, not evidence.** What the
conversation — or its summary, or your own memory of it — says was
completed is exactly what an interruption falsifies: the narrative
was written before the interrupt, the state after. Evidence is the
repository and the world; every claim is checked against them.

In order:

1. **Anchor on approved truth.** The last annotated step tag is the
   last operator-approved state:
   `git describe --tags --abbrev=0 --match 'step-*'`
   (before the first tag, the anchor is the repository root).
   `git log` and `git diff` from there to `HEAD`, plus `git status`,
   are the complete evidence of everything since — committed and
   uncommitted.
2. **Cross-check the memory files.** Read `CLAUDE.md`'s pointers,
   `{{PLAN}}`'s current-step entry and status, and the tail of
   `{{DECISIONS}}`, and check each claim against the git evidence.
   They were written by the same interrupted session, so a mismatch
   is a finding, never something to reconcile silently — a status of
   `awaiting test` over a half-delivered diff is precisely what you
   are looking for.
3. **Working-tree forensics.** Examine uncommitted changes for
   half-written work (a file edited where its counterpart was not, a
   reference to something that does not exist yet). Run
   `{{CHECK_COMMAND}}`: green is cheap evidence the tree is at least
   well-formed; red localizes the interruption.
4. **World state, inside the boundary.** The step may have touched
   things no file records — consult the current step's "how I test
   it" and cleanup notes in `{{PLAN}}` for what it may have
   half-applied. Run the free checks from: {{STATE_CHECKS}}. Anything
   gated by the rule-9 boundary you request from the operator, never
   run; anything unverifiable from here you report as unverified —
   an honest gap beats a guessed answer.
5. **Report, then stop — two shapes:**
   - **Discrepancies found:** the resume point and its evidence;
     each discrepancy as the claim plus the contradicting evidence;
     what could not be verified; and the repair options — continue
     the step from the verified state, roll back to the last
     `step-*` tag, or redo the partial work — with your
     recommendation. The repair is the operator's ruling; you
     execute nothing until they choose.
   - **Everything consistent:** deliver /orient's report — current
     step and status, what the in-progress diff contains, what
     remains — plus one line: verification found no discrepancies,
     and what was checked. Then wait for the operator's go.
