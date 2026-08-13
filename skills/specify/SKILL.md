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
  "requirements document" or "cahier des charges". Also covers the
  implementation handoff: generating the initial prompt (bootstrap prompt)
  and workflow tooling that hand a finished SPECIFICATIONS.md to the
  implementing agent — and, afterwards, updating an already handed-over
  project when this doctrine has moved on since (auditing its CLAUDE.md,
  workflow tooling, permission baseline and harness against the doctrine
  changelog, then proposing the changes). A "plan" qualifies only
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
- `.claude/refs/` — reference material the user supplies that is not part
  of the specification (a contract of a system that will consume the
  deliverable, an inventory, a document from elsewhere). Committed, and
  kept out of `.claude/docs/`: the implementation phase sweeps that
  directory as its own memory and would eventually fold or delete
  whatever sits there. Named in the handoff, never in the specification —
  the spec states requirements, not where to read background.
- `.gitignore` — carries `.claude/worktrees/` from setup, before the first
  review is ever spawned. Worktree isolation materializes the reviewer's
  checkout inside the repository; a commit made while one exists otherwise
  swallows it (this has happened).
- `.claude/settings.json` — written and committed at workspace setup with
  `"autoMemoryEnabled": false` (merged in, never overwriting other keys, if
  the file exists). Auto memory is machine-local and unversioned — an
  ungoverned second memory outside git and outside review; neither the spec
  sessions nor the future bootstrap session may accumulate or load it. The
  implementation workflow keeps it off (its step 000 extends this same
  file).

`.claude/spec-work/` is process scaffolding, not part of the deliverable — it
lives under `.claude/` so the project root stays clean — but it is committed:
its history is what makes challenges cheap later. If the project's
`.gitignore` covers `.claude/`, un-ignore `.claude/spec-work/` — an
uncommitted log never reaches a reviewer's worktree. Commit at every
round boundary (a drafting batch applied, a review round triaged and applied),
and **always commit before spawning a review** — reviewers read from a
worktree copy of the repository and must see the current state. A decision
entry and the specification text it justifies are committed **together**:
a commit where the log asserts what the document contradicts is a state
nobody should be able to read.

If a `SPECIFICATIONS.md` already exists when the skill is invoked, read it,
then ask the user which phase to enter: extend, review round, challenge,
finalization, or handoff. Every phase but handoff also reads the decision
log; handoff reads the specification only (phase 7 says why). Otherwise
start at phase 1.

A repository holding implementation artifacts — `CLAUDE.md`, a `PLAN.md`, a
decision log — is a project already handed over, whatever its specification
says. Offer the **workflow update** of phase 8 there, and do not offer the
specification phases unless the user asks for one: a session invoked in a
working project is far likelier to want its workflow brought up to date than
its requirements reopened.

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
   they matter. A fact that genuinely cannot be settled before implementation
   is never guessed: it becomes an **open fact** with a pre-committed
   response per outcome (see [references/structure.md](references/structure.md)).
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
accepts as substantive — and never declared quiet on same-model rounds
alone; at least one round runs on a different strong model (see "Spawning
reviews"). One round equals one spawn plus one full triage —
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
   plans the implementation and reports every place it had to guess. The
   natural cross-model slot — the real implementer may not be this model;
   propose a different strong one (see "Spawning reviews").
2. **Compression pass** — shorten wording, merge redundancy; the floor is
   comprehension: nothing is removed that a requirement needs to be
   understood.
3. **Final consistency sweep** — cross-references, numbering, terminology,
   tier classification.
4. **Final audit** — a cold review with the final-audit lens on the strongest
   available model. Quiet means done.

### 7. Implementation handoff

Entered after finalization — or directly, on request, when the specification
is already final. The deliverable is `.claude/spec-work/handoff/PROMPT.md`:
the initial prompt a fresh Claude Code session reads to bootstrap the
implementation, plus the workflow tooling templates beside it. Read
[references/handoff.md](references/handoff.md) first — it holds the doctrine,
the proven prompt template with its adaptation points, and the asset table.

**Prefer entering this phase in a fresh session** (`/clear`, then ask for the
handoff): this phase works from the **specification plus the user's rulings
during the phase itself** — never from the spec-phase decision log, and never
from what an earlier conversation remembers — and a cold start proves the
specification suffices. It must be self-sufficient for the implementer, so a
slot a fresh session cannot fill from it is a finding against the document —
fix the spec through the normal process, or put the choice to the user in
the batch — never a gap to fill from remembered discussion or the log.
On entry, confirm `.claude/settings.json` carries
`autoMemoryEnabled: false` — a repository whose spec work predates the
Workspace rule may lack it; create or merge it (commit, per Workspace)
before anything else, since this setting, not step 5's residue check, is
what keeps old memory out of the session doing this work.

1. **Adapt.** Fill the template's `{{SLOT}}`s from the specification —
   never invented — and present them as a numbered batch with
   recommendations. The implementer's action boundary (what it may never run
   on its own initiative) is the one pure policy call: flag it as such. The
   user rules; only then write.
2. **Write and commit.** `PROMPT.md`, and the
   [references/handoff-assets/](references/handoff-assets/) templates copied
   verbatim to `.claude/spec-work/handoff/assets/` — the implementer
   instantiates them later, not this session.
3. **Cold review.** Spawn per "Spawning reviews" with the **handoff** lens
   from [references/reviewer.md](references/reviewer.md); triage, apply,
   repeat until quiet — phase 4 rules apply unchanged. Propose at least
   one round on a strong model *different from the session's*: measured
   on identical inputs, each model shipped defects past its own reviews
   that the other model's review caught, and "quiet" arrives earlier on
   a lenient reviewer — the divergence-proposal rule from "Spawning
   reviews" applies.
4. **Compression pass.** Review rounds append clauses; four of them
   grew a real prompt by a fifth, all of it into sentences that were
   already long. The prompt's fate is to be restated by the bootstrap
   session into a `CLAUDE.md` under 200 lines, and a rule too tangled to
   restate is a rule that loses a clause there. So once the rounds are
   quiet, compress: same floor as finalization's, comprehension, and one
   exemption — the action boundary of rule 9 is safety text and is never
   shortened. Wording only. Anything that would change meaning stops and
   goes to the user as a finding.
5. **Auto-memory residue check.** The setting has been off since workspace
   setup, but memory may predate it: look under
   `~/.claude/projects/<project-path-with-slashes-as-dashes>/memory/`. If
   anything is there, report it for the user's review — deleting is their
   call (it is machine-local and may hold things they want), but it must not
   reach the bootstrap session unreviewed.
6. **Upstream findings.** Write
   `.claude/spec-work/handoff/upstream-findings.md`: every fix applied
   during this phase that was *not* project-specific — a defect in a
   copied template, an edit to the prompt's fixed text that would be
   true of any project, a slot whose guidance turned out to be
   incomplete. One line each: what was wrong, what the fix was, which
   round found it. Then name the file in the closing message.
   This exists because the alternative has been tried: reporting such
   findings in conversation, where they die with the session. The
   generic fixes are the phase's most reusable output and the easiest
   to lose — they dissolve into commit messages of a project that has
   nothing to do with the skill. The file is also the raw material for
   the doctrine changelog of phase 8: findings flow up from projects,
   doctrine flows back down to them.
7. **History squash — gated, clean cut.** Propose collapsing the whole
   history into a single `initial commit` so the implementer's "before the
   first step tag, the range is the whole history" re-orientation sees only
   bootstrap work. Preconditions: the history is purely spec work (the skill
   created or first used this repository — if anything predates spec work,
   skip the squash and say why); warn if a pushed remote exists, since the
   squash then implies a force-push on the user's side. Only on the user's
   explicit confirmation in that exchange: squash, no archive branch,
   history rewriting is never within latitude.
8. **Hand over the one-liner:** open a fresh Claude Code session at the
   repository root and say *"Read `.claude/spec-work/handoff/PROMPT.md` in
   full and do what it says."*

### 8. Workflow update

For a project already handed over, when this skill's doctrine has moved on
since. Read [references/updates.md](references/updates.md): it holds the
pass — an audit subagent, a triage, and a decision entry recording the new
adoption point — and the index of doctrine changes, from which you read only
the revision files (`references/updates/<date>.md`) holding entries newer
than what the project has adopted. Each entry carries the test that detects
whether a project is affected.

Two things govern it, both easy to get wrong. **A project that deviates by
logged decision is not behind** — its reasoning was paid for with real work
and may still be the better answer, so a divergence is presented to the user,
never corrected on sight. And **the pass runs under the project's rules**,
not this skill's: its commit conventions, its decision-log format, its
latitude — and its permission baseline, which stays outside latitude and
goes to the user whatever the changelog says.

Every change to the doctrine gets a changelog entry as it is made. The
alternative is what this phase exists to repair.

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
- **Guard against a stale worktree — every spawn, no exceptions.** The
  isolated checkout is not reliably the commit you just made. Two failures
  have been observed and both are expensive: file contents from several
  commits back, which produced a whole review round of findings quoting
  text that no longer existed; and current file contents over stale git
  metadata, which produced confident findings about what is or is not
  tracked. So: put the expected `HEAD` hash in the context block and tell
  the reviewer to verify its checkout and correct it before reading
  anything. And tell it that **repository state is not a fact it may
  derive from git in its worktree** — whether a file is tracked, what the
  remote is, what the last commit did are facts it takes from the context
  block or verifies on disk, never from `git ls-files` or `git log`. Both
  instructions are cheap; a wasted strong-model round is not.
- Model choice per spawn: inheriting the session model is the default and
  needs no approval. Any divergence from it — up or down — is proposed to
  the user with its reason and spawned only once they approve: model choice
  is a cost-and-quality trade-off, and those calls are the arbiter's like
  every other. What to propose: the challenger and the final audit deserve
  the strongest available model, so propose an upgrade whenever the session
  runs on less. Cold context removes conversation bias, not model bias — a
  reviewer on the session's own model shares its blind spots (measured in
  this skill's phase-7 testing: each of two strong models shipped defects
  past its own reviews that the other caught, and "quiet" arrives earlier
  on a lenient reviewer) — so before a phase-4 sequence is declared quiet,
  and for the implementer probe, propose at least one round on a strong
  model *different* from the session's; the challenger and final audit stay
  on the strongest available regardless — diversity never weakens the last
  gate. Quick re-checks after fixes may go cheaper, knowing what
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
  `.claude/spec-work/reviews/NNN-<lens>.md` before triaging it, under a
  short provenance header you write: lens, model, isolation, the commit
  reviewed, and the documents given. Verbatim without provenance loses
  exactly what makes the archive useful later — which model found what,
  and against which state.
- When triage establishes that a finding rests on a false premise (the
  staleness artifacts above are the usual cause), do not edit the report:
  prepend a bracketed **archivist note** naming the finding and the
  verified truth, and leave the text otherwise untouched. The report is
  evidence of what a cold reader concluded; the note is evidence of what
  was true.
