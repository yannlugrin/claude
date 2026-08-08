---
name: specify
description: >-
  Write project specifications (SPECIFICATIONS.md) intended for AI
  implementation: a staged, decision-centric process where the user arbitrates
  every decision — intake and exploration, structured drafting under the
  must/should/facts contract, cold subagent review rounds, premise challenges
  of foundational decisions, and a final audit. Use whenever the deliverable
  is the specification document itself — creating, extending, reviewing,
  challenging or finalizing requirements for a project an AI (Claude or
  another) will implement — whether the user says "specification", "specs",
  "requirements document" or "cahier des charges". A "plan" qualifies only
  when it means a plan of what to build; planning how to build
  (implementation, refactoring or integration plans for a coding task) is
  out of scope.
---

# Specify

Produce and maintain a `SPECIFICATIONS.md`: a statement of **intent and
constraints** for a project, written to be implemented by an AI (typically
Claude Code) without babysitting. A specification here is never an
implementation guide — it states what must exist and why, and leaves file
layouts, tool syntax and code to the implementer. Its only reader is the
implementer; documents for anyone else are deliverables *of* the
implementation, named in the spec but not written there.

Three roles, never blurred:

- **The user is the sole arbiter.** Every decision and every review finding
  passes through them. You propose with a recommendation and reasoning; they
  rule; only then do you apply.
- **You (the main session) are the editor and keeper of intent.** You hold the
  history of why things are the way they are, draft and amend the document,
  triage findings, and maintain the decision log.
- **Cold subagents are the reviewers.** Fresh context is what makes their
  reviews worth having; they see only the documents, never this conversation.

The specification is written in English. Converse with the user in whatever
language they use.

## Workspace

Work inside a git repository (offer `git init` if there is none):

- `SPECIFICATIONS.md` — the deliverable, at the repository root.
- `.claude/spec-work/decisions.md` — the decision log (format below).
- `.claude/spec-work/reviews/` — archived review reports, `NNN-<lens>.md` in
  chronological order.

`.claude/spec-work/` is process scaffolding, not part of the deliverable — it
lives under `.claude/` so the project root stays clean — but it is committed:
its history is what makes challenges cheap later. If the project's
`.gitignore` covers `.claude/`, un-ignore `.claude/spec-work/` — an
uncommitted log never reaches a reviewer's worktree. Commit at every
round boundary (a drafting batch applied, a review round triaged and applied),
and **always commit before spawning a review** — reviewers read from a
worktree copy of the repository and must see the current state.

If a `SPECIFICATIONS.md` already exists when the skill is invoked, read it and
the decision log, then ask the user which phase to enter: extend, review
round, challenge, or finalization. Otherwise start at phase 1.

## The decision log

The process is decision-centric: the specification is the serialization of
arbitrated decisions with their reasons. The log is not a duplicate of the
spec: for local decisions, the spec text with its attached reasoning is the
record. The log holds what the spec deliberately cannot carry — premises as
auditable facts, dates, statuses, rejected alternatives — and a full `D-NNN`
entry exists for exactly three kinds of decision:

- **foundational decisions** — entry and premises mandatory;
- **decisions whose justification stays out of the spec** — a rejected
  alternative worth remembering, a structure deviation or trimming decision;
- **anything the user asks to track.**

Entry format:

```markdown
## D-NNN (YYYY-MM-DD) — short title

- **Status:** open | decided | reaffirmed (date) | reopened | superseded by D-MMM
- **Foundational:** yes | no
- **Decision:** what was decided (or the options, while open)
- **Why:** the reasoning, including alternatives rejected and why
- **Premises:** the facts and context this decision depends on
```

An example of a filled entry — the kind that pays off later:

```markdown
## D-004 (2026-08-05) — Docker Swarm as the orchestrator

- **Status:** decided
- **Foundational:** yes
- **Decision:** use Docker Swarm to place containers across nodes
- **Why:** native to Docker, nothing new to learn; simpler than k3s at
  this scale; k3s rejected as more machinery for the same placement needs
- **Premises:** several stateless web apps will need cross-node
  scheduling; games and apps share one deployment mechanism
```

Written like this, the entry contains its own expiry condition: the day the
workloads turn out to be pinned, host-networked and node-local, both premises
are visibly false and the challenger catches it — instead of the decision
silently outliving its reasons.

Rules:

- **Premises are mandatory and concrete** ("no web application exists yet",
  "the provider's API cannot do X"). They are what the challenger audits — a
  decision whose premises were never written down cannot be challenged, only
  inherited.
- **Foundational** marks decisions that shape many downstream sections:
  platform, architecture pattern, provider, core data model. When in doubt,
  ask the user.
- `D-NNN` entries are never deleted; they are superseded or reopened.
  Reaffirmations are recorded with their date — staleness is measured from
  the last affirmation, not from creation.
- **Open questions** live as a lightweight one-line-each list at the top of
  the same file, deleted once ruled and serialized (git history keeps them);
  only those matching the three kinds above graduate to a `D-NNN` entry.

## Standing rules

These apply in every phase:

1. **Arbitration.** Present choices and findings as numbered points, each with
   your recommendation and its reasoning. Batch related questions rather than
   dribbling them. Apply nothing substantive without a ruling; purely
   editorial fixes (typos, broken cross-references) are exempt.
2. **Challenge duty — economical, not performative.** When the user hands you
   a solution ("use X") rather than a need, ask for the underlying need
   first, so X enters as a reasoned decision rather than an assumption —
   with a log entry when it is one of the tracked kinds. When a new fact contradicts a logged premise, flag it
   immediately, naming the decision (`this touches D-007's premise that…`) —
   do not wait for a checkpoint. Never relitigate local decisions for sport.
3. **Facts are researched, not assumed.** Environment constraints (provider
   behavior, product limits, protocol quirks) are verified — web search when
   knowledge could be stale — and stated in the spec as facts with the reason
   they matter.
4. **Document doctrine.** Structure, tone and precision rules live in
   [references/structure.md](references/structure.md); read it before the
   skeleton phase and keep the document conforming to it thereafter.
5. **Consistency pass after every edit round:** every `§N.M` cross-reference
   resolves, numbering is stable, terminology is uniform, and each statement
   sits in the right tier (must / should / fact). Then commit.

## Phases

### 1. Intake and exploration

Elicit before drafting: the goal and why it exists, the actors, what already
exists, hard constraints versus preferences, budget and scale, and the
now-versus-later split (which feeds Non-Goals and Future Considerations).
Research the environment facts the project will rest on. Free discussion is
welcome here — exploration, comparisons, even throwaway prototyping — but its
conclusions must land in the log.

Output: a short project brief and the list of **core decisions**, each with
options and a recommendation. The user arbitrates; decisions at this stage
are almost always foundational, so they are logged with premises. Only then
move on.

### 2. Skeleton

Instantiate the document structure from
[references/structure.md](references/structure.md): reading contract, numbered
sections, Non-Goals and Future Considerations present from day one. The full
structure is the default whatever the project size; trimming it is itself a
decision — argued, user-approved, logged.

### 3. Drafting

Section by section: serialize the relevant decisions with their reasoning,
state the researched facts, and where a decision is missing, stop and ask (a
numbered batch per section works well). For each section, run a
silent-failure sweep — "what can go wrong here without producing an error?" —
and give dangerous conditional behavior a decision table. Keep precision
proportional to risk. Mini consistency pass per batch.

### 4. Review rounds

Spawn a cold review (see "Spawning reviews") with the **cold read** lens from
[references/reviewer.md](references/reviewer.md). Then:

1. Triage the findings: for each, your recommendation — accept, reject with
   reason, or genuinely the user's call.
2. Present the triage; the user rules point by point.
3. Apply the accepted items, run the consistency pass, commit, archive the
   report under `.claude/spec-work/reviews/`.

Repeat with a fresh spawn until a round is **quiet**: no finding the user
accepts as substantive. One round equals one spawn plus one full triage —
never a fix-per-finding loop.

On request, prepare an **external review packet** (see
[references/reviewer.md](references/reviewer.md)) for the user to run on
another platform; ingest whatever comes back as a findings list into the same
triage flow, labeled with its source.

### 5. Challenge checkpoints

Mandatory twice — after the first complete draft, and before finalization —
plus whenever standing rule 2 fires on a contradicted premise. Spawn the
challenger from [references/challenger.md](references/challenger.md) with the
specification **and the decision log**. Triage as in phase 4. Record outcomes
in the log: reaffirmed (with date) or reopened — a reopened foundational
decision usually means returning to phase 3 for the affected sections.

### 6. Finalization

In order, each gated by the user:

1. **Implementer probe** — a cold review with the probe lens: the reviewer
   plans the implementation and reports every place it had to guess.
2. **Compression pass** — shorten wording, merge redundancy; the floor is
   comprehension: nothing is removed that a requirement needs to be
   understood.
3. **Final consistency sweep** — cross-references, numbering, terminology,
   tier classification.
4. **Final audit** — a cold review with the final-audit lens on the strongest
   available model. Quiet means done.

## Spawning reviews

- Use the Agent tool with `subagent_type: "general-purpose"` and
  `isolation: "worktree"`. **Never use a fork** — forks inherit this
  conversation, and the cold start is the point. Worktree isolation keeps any
  accidental write off the real tree; reviewers return their report as text
  and never edit files.
- Build the prompt from the reference file: the role block, exactly one lens
  block, and the context block filled in (repository-relative paths, project
  one-liner). Reviewers get the specification only; the challenger also gets
  the decision log.
- Model choice per spawn: inheriting the session model is the default and
  needs no approval. Any divergence from it — up or down — is proposed to
  the user with its reason and spawned only once they approve: model choice
  is a cost-and-quality trade-off, and those calls are the arbiter's like
  every other. What to propose: the challenger and the final audit deserve
  the strongest available model, so propose an upgrade whenever the session
  runs on less; quick re-checks after fixes may go cheaper, knowing what
  that trades away: small models keep the report format but lose calibration
  (severity inflation, doctrine drift, the occasional false finding), so
  their output gets extra-skeptical triage. The final audit is never
  delegated down.
- Reasoning effort follows the same rule with a different lever: it cannot
  be set per spawn — a subagent runs at the session's configured effort — so
  when a round deserves more than the session is set to (the final audit
  above all), name it in the divergence proposal and let the user decide:
  raise it session-wide (`/effort`) for that round, or accept as-is. A
  session-wide raise is not wasted — it also sharpens the triage of the
  report that comes back.
- Save the returned report verbatim to
  `.claude/spec-work/reviews/NNN-<lens>.md` before triaging it.
