# Doctrine updates — index and the update pass

Two things live here: the index of every change to this skill's doctrine,
and the procedure for carrying those changes into a project that was handed
over under an earlier version (phase 8).

A handed-over project runs on a restatement of the doctrine, not a copy of
it — its `CLAUDE.md` says the rules in its own words, its tooling is
instantiated and adapted, its permission baseline is its own. Nothing
propagates by itself, and no textual diff finds the gap. The changelog is
what makes the gap findable: each entry carries the test that detects
whether a given project is affected.

Entries flow in from two directions. Changes made here go in as they are
made; and phase 7's `upstream-findings.md` — the generic fixes a project's
handoff review rounds produced — is the raw material for the rest.

## Index

Empty, and that is a state rather than a gap: **everything through U-021 is
applied in every project that exists**, and the entries themselves are in git
history — `git log -- skills/specify/references/updates/` reaches them, which
is where a citation like "adopted through U-021" resolves.

Ids are permanent and never reused, so the next entry is **U-022**. The index
resumes with it, one revision section per date:

```text
### [YYYY-MM-DD](updates/YYYY-MM-DD.md) — what this revision was about

| Id    | Applies to | Title |
| ----- | ---------- | ----- |
| U-0NN | running    | …     |
```

**Applies to** says who an entry concerns: *running* — a handed-over project,
so the update pass walks it; *bootstrap* — only the generation of a new
handoff prompt; *spec phase* — only the specification process itself. The
index is the whole of what a pass reads up front, so each row carries enough
to skip an entry without opening anything.

The clearing happened on 2026-08-15, when the last project running an older
doctrine was brought current. It is not a habit: entries accumulate until
every project has them, and only then is emptying them free. What was kept is
the mechanism — this file — because the next divergence is a certainty rather
than a possibility: doctrine moves while a project is mid-plan, and the
changelog is what makes the gap findable rather than remembered.

## Adding an entry

Append to the current date's file, creating it and its index section on the
first entry of a revision. Each entry states:

- **Applies to** — running, bootstrap, or spec phase, with the condition
  where one narrows it.
- **Change** — what the doctrine now says, and the reasoning. The reasoning
  is what lets a project argue back.
- **Detect** — the observable test. This is the field that makes the entry
  worth having: "the project's read-only rule orders the entry logged
  first" is a test; "the project's amendment flow is outdated" is not.
- **Remedy** — what to change, and where the user's approval is required.

An entry is **corrected in place**, with a dated note saying what was
added, when it misstates or under-states the doctrine it already
describes — a project reading it must get the doctrine as it stands, not
as it was first drafted. A **new id** is for a later change *of* the
doctrine. The distinction is whether the earlier entry was wrong or has
been superseded; where both readings fit, prefer the new id, since a
project that has already adopted the old entry will otherwise never see
the difference.

## The update pass (phase 8)

Entered on request, from the project's own repository: the user opens a
session there and asks for a workflow update. Offer it whenever the skill
is invoked in a repository that holds implementation artifacts (`CLAUDE.md`,
`PLAN.md`, a decision log) rather than an in-progress specification.

**Preconditions, verified before anything else:** the working tree is
clean, and no plan step is `in progress`. This pass edits the enforcement
layer — `CLAUDE.md`, the instantiated tooling, `.claude/settings.json` —
and a half-applied doctrine change under an in-flight step is precisely
what the re-orientation routine cannot make sense of. Stop and say so if
either fails.

**Scope, hard:** workflow doctrine only. Never the specification, never the
plan's content. A problem noticed in the specification is a question for
the user under the project's own read-only rule, not a finding here.

1. **Find the adoption point.** The project's decision log carries an entry
   naming the last doctrine entry it adopted. From the index, take the
   *running* entries above that id, and read only the revision files that
   hold them. With no such entry — a project handed over before this
   mechanism existed — walk everything, and expect most findings to come
   back "already satisfied": the project may well have received the change
   as part of its original handoff.
2. **Audit, in a subagent.** Fresh context, read-only, one inline brief (see
   below), carrying the entries you selected. Not for coldness — for context
   economy: the audit reads the whole `.claude/` tree, the harness
   configuration, `CLAUDE.md` and the decision log, and returns a classified
   list. Mechanical work, so a cheaper model is defensible; the
   classification is not, so read its output sceptically.
3. **Triage with the user, point by point.** Standard arbitration: your
   recommendation, their ruling. The one classification that must never be
   applied silently is *decided otherwise* — a project that deviates by
   logged decision is not behind, and its reasoning may still be the better
   one. Present the entry and the deviation side by side and let the user
   rule; re-imposing doctrine over a decision destroys the answer that was
   paid for with real work.
4. **Apply under the project's rules, not this skill's.** You are a guest:
   its commit conventions (`meta:` for work belonging to no step), its
   decision-log format and latitude, its harness. The permission baseline
   is never within latitude — any change to it goes to the user for review,
   whatever the changelog says.
5. **Record the new adoption point** as a decision entry in the project's
   log, naming the highest changelog id now adopted. Each *deliberate*
   deviation gets its own entry citing the id it declines and why — the same
   log then answers both questions a future pass asks: how far is this
   project, and what did it decide not to take.

### Audit brief for the subagent

```text
You audit this repository's implementation workflow against a list of
doctrine changes, given below. You are read-only: you edit nothing and your
report is your only output.

Read: CLAUDE.md, the plan(s), the decision log(s), everything under
.claude/ (skills, agents, settings, hooks), and the harness configuration
its check command runs. Then, for each entry, apply its detection test and
classify:

- BEHIND — the project predates the change and nothing local contradicts
  it. Quote what you found, and name every file the remedy would touch.
- DECIDED OTHERWISE — a decision entry covers this ground. Cite the entry
  id and summarize its reasoning. Do not judge whether it is still right;
  that is the user's call.
- SATISFIED — already in force. Say where, in one line. This half of the
  report matters as much as the other: it is what stops the same ground
  being re-argued every pass.

Report as a table of id → classification → evidence, followed by the
BEHIND entries in full. Flag separately anything you noticed that no entry
covers but that looks like drift from the project's own stated rules —
labelled as such, since it is outside your brief.
```
