# Implementation handoff

Doctrine and template for phase 7: turning a finalized `SPECIFICATIONS.md`
into the initial prompt the implementing agent bootstraps from. The
deliverable is `.claude/spec-work/handoff/PROMPT.md`, committed, plus the
tooling templates copied to `.claude/spec-work/handoff/assets/`. The user
starts implementation by giving a fresh Claude Code session, opened at the
repository root, one line:

> Read `.claude/spec-work/handoff/PROMPT.md` in full and do what it says.

The template below is proven: it bootstrapped a real project whose workflow
then ran for milestones without drifting, and it already folds in what that
project learned (step-number freezing, the check/test split, milestone
memory compaction, skills over commands, the reviewer family). Adapt it;
do not redesign it.

## Adaptation points

Every `{{SLOT}}` in the template is filled from the specification, plus the
user's rulings on the batch below — never invented, and never from the
spec-phase decision log or remembered spec-phase discussion: the
specification must be self-sufficient for the implementer, so a slot it
cannot fill is a finding against the document, not a gap to fill from
memory. Present the filled values to the user as a numbered batch before
writing the file; apply their rulings. Beyond the slots, tailor only what
the project genuinely requires, and put every such tailoring in the same
batch.

1. `{{PROJECT}}` — one-line description of what is being implemented, from
   the spec's overview section.
2. `{{ORDERING}}` — where the plan's order comes from. If the spec has its
   own ordering or dependency section, cite it — and check what kind of
   order it is: a first-*run* order is a dependency graph, not a build
   sequence (its first entry may be the most expensive action of all,
   while everything it depends on is cheap files), and the slot must say
   so. Otherwise instruct the implementer to derive the order from the
   dependencies between sections.
3. `{{CHEAP_FIRST}}` — what is testable for free and locally versus what
   costs money or touches shared state, so the plan front-loads the cheap
   part. Name the concrete examples from this project.
4. `{{STATIC_CHECKS}}` — the check families that apply to this stack
   (linters, syntax checks, template rendering against fixtures, type
   checks, schema validation…), derived from the spec's technology facts.
   Families, not tool invocations — choosing tools is the implementer's
   job. Fill the slot as a short bulleted list (it stands alone in the
   template), never a semicolon chain: review rounds append clauses, and
   chained prose stops being parseable. Three rules the list must
   respect:
   - **Every artifact class the repository ships gets a family**, not
     only the ones the spec names. Third-party tools that enter the
     tree count: they arrive pinned, with their version or digest
     recorded, and are covered like anything else shipped.
   - **The list is the expected instance, not the boundary.** Say so in
     the slot. The specification deliberately leaves implementation
     open, so naming a language the spec never chose (an entrypoint
     "shell script") decides for the implementer something the document
     refused to decide.
   - **Never harden a spec "should" into a fact.** Where the spec makes
     a tool a recommended default the implementer may replace with a
     logged deviation, the slot says so conditionally ("where the §N.M
     clients are adopted, they enter pinned…") — flat wording turns a
     deviation candidate into a settled requirement.
5. `{{IGNORE_ITEMS}}` — what this stack and project leak into the working
   tree that must never be committed (credential files, local environment
   files, tool caches). `CLAUDE.local.md` is already in the fixed text.
6. `{{SECRETS_SOURCE}}` — the spec section defining how secrets are
   sourced. If the project has no secrets story, drop the sentence that
   cites it and keep the rest of rule 5.
7. `{{BOUNDARY}}` — **the one pure policy call; flag it as such in the
   batch.** What the implementer may never run on its own initiative:
   commands that spend money, touch real infrastructure or production
   systems, call external services with side effects, or destroy data.
   Stated concretely for this project — it drives rule 9, the settings
   baseline of step 000, and the plan's test-cost flags. Walk the
   specification for side-effectful surprises and name each: playbooks
   or hooks that run automatically ahead of others, outbound
   notifications (webhooks, mail), uploads and registrations — the
   recurring misses are actions that do not look like deployments. Name
   the remote *read-only* case explicitly (API reads with a legitimate
   credential): rule 9 classifies local-read-only as free and outward
   writes as gated, and remote reads fall in neither — put the default
   to the user in the batch rather than assuming one; left to
   themselves, runs have ruled it both ways.

   **Enumerate the free side too, not only the gated one.** The
   boundary's default — free means local *and* read-only — silently
   gates most of a normal development loop, because the loop is local
   and full of writes: starting and stopping the thing being built,
   reading its logs, inspecting its state, tearing down and recreating
   local fixtures. An implementer that must ask before stopping a
   container it just started is unusable, and one that decides on its
   own that the whole local surface is free has quietly rewritten the
   policy. Name the project's dev loop end to end and rule it free.

   **Destructive-local splits on blast radius, not on the verb.**
   Removing this project's own artifacts by name is rebuildable
   working material and belongs on the free side; the same tool's
   unscoped sweep (a global prune, a wildcard delete) reaches other
   projects on the same host and belongs with the gated writes. Two
   things stay protected whatever the project: git history and the
   working tree — the step tags and uncommitted work are what rules 3
   and 6 rest on.
8. `{{PREREQUISITES}}` — the external prerequisites only the user can
   provide (credentials, delegated services, artifacts from other
   projects), especially the slow ones, each findable in the spec. Look
   also for *reversed* dependencies: a deliverable of this project that
   an external prerequisite is built against (a contract another project
   consumes) orders the steps, not just the waiting.
9. `{{NONCODE}}` — the spec's non-code deliverables (operator
   documentation, contracts, inventories) that must become plan steps, with
   their section references.
10. `{{EXCLUSIONS}}` — the spec sections that already list what this pass
    leaves out (Non-Goals, Future Considerations), feeding the plan's
    explicit exclusion list.
11. `{{OPEN_FACTS}}` — present only when the specification carries open
    facts (see `structure.md`): facts it could not settle, each with the
    requirement resting on it and a pre-committed response per outcome.
    They are the expected case of rule 1's amendment channel — the spec
    itself ordered them settled at implementation — so the slot must say
    who may close one and how far. **The latitude splits in two, and the
    split is decided here, not left to the implementer:** recording a
    verified fact is autonomous (decision entry and amendment in one
    commit, reported in the step's summary), while any resolution that
    changes a requirement, a tier, a documented limitation or the
    decision to ship comes back to the user before the amendment. Name
    the items that always come back — the ones whose unfavourable
    outcome carries a tier or ship consequence — rather than leaving the
    criterion to be applied item by item. Also state where the
    resolutions land: the specification is amended so its facts stay
    true, and the user-facing consequence goes into the deliverable
    documentation. Drop the slot entirely when the spec has no open
    facts; do not invent them.
12. `{{REFERENCES}}` — documents the user supplies as *input* to the
    implementation without their being part of the specification:
    contracts of systems that will consume the deliverable,
    inventories, material produced by another project. Each gets a
    path under `.claude/refs/`, a **read-trigger** naming when to read
    it ("before designing the operator interface"), and the standing
    caveat that it is information, never a requirement source — a
    conflict between a reference and the specification is a question
    for the user, not a constraint. `.claude/refs/` is deliberately
    not `.claude/docs/`: the memory sweep owns the latter and would
    eventually fold or delete anything in it, and an operator-supplied
    reference is not the implementer's memory to compact. It carries
    the specification's read-only protection for the same reason the
    specification carries it — a document silently diverging from what
    was agreed, or from the source that owns it, is undetectable — with
    one difference: no amendment channel. The specification can be
    amended by agreement because it is this project's own contract; a
    reference cannot, because its authority lives elsewhere. It is
    reported and replaced by the user, never edited. Drop the
    slot when there are none.

## Monorepo and multi-track projects

The template assumes one specification, one plan, one decision log, one
step-number namespace. That holds for most projects and should not be
abandoned lightly — but a monorepo breaks it, and the usual trigger is a
specification already split into a root document plus one per component
(`structure.md`, "Multi-document specifications"). When it applies, the
shape is **tracks**: the root track owns repository-wide work (the
foundation and harness, CI, shared documentation) and each component
directory owns one track. What changes, rule by rule — nothing else does:

- **Rule 1** — "every `SPECIFICATIONS.md` is read-only", root and
  per-component alike.
- **Rule 3** — each track owns a `PLAN.md` and a `DECISIONS.md`, placed
  in its directory (the root track's at the repository root). Exactly
  one `CLAUDE.md` exists repository-wide, and it carries the **track
  map**. The session routine loads the root plan and log, then the
  active track's plan, log and specification; other tracks' files load
  only when the current step names a cross-track dependency. State
  explicitly that **the root specification is never "another track's
  document"** — its core model and conventions are standing reading for
  any component-track step. Without that sentence, "the other tracks'
  specifications not at all" reads as excluding the very document that
  carries the shared conventions, and whether they get loaded then
  depends on each step's section list being complete — the thing a plan
  is likeliest to under-enumerate.
- **Rule 4** — decision ids are **per log**: an entry lands in the log
  of the track whose files it governs, anything repository-wide in the
  root log, and a citation crossing logs names the file
  (`project-zomboid/DECISIONS.md D-003`).
- **Rule 6** — step identifiers are track-qualified (`step-000` for the
  root track, a short prefix for each component: `step-pz-001`), with
  numbering independent per track and each new component registering
  its prefix in the track map. Add one invariant the single-track shape
  gets for free: **exactly one step is in progress repository-wide**,
  whichever track it belongs to — history stays linear and the last
  `step-*` tag remains the single last-approved state rule 3's
  re-orientation depends on. Each plan orders only its own track;
  cross-track sequencing comes from steps naming their dependencies
  ("needs `step-sc-002` done"), never from a global sequence.
- **The first task** produces one plan and one log per track, plus the
  single `CLAUDE.md` and root `README.md`; the plans *together* must
  account for every section of every specification document.
- **The templates** resolve their governance placeholders to the active
  track's files. This is what the placeholders are for.

## The prompt template

````markdown
# Initial prompt — implementation bootstrap

> Operator note. To start implementation: open a fresh Claude Code
> session at the repository root and say "Read
> `.claude/spec-work/handoff/PROMPT.md` in full and do what it says."
> Everything below the separator is addressed to that session; this
> note is not.

---

You are implementing {{PROJECT}}. The complete specification is in
`SPECIFICATIONS.md` at the repository root. Read it in full before doing
anything else — it defines its own reading rules (requirements as "must",
recommended defaults as "should", environment constraints stated as facts)
and every section matters.

## Ground rules — permanent; you will encode them in CLAUDE.md

1. **`SPECIFICATIONS.md` is read-only for you.** You never edit it on your
   own initiative. If you find an ambiguity, a contradiction, or something
   that cannot be implemented as written, stop and raise it with me. If we
   agree a change is needed, the decision entry is written before the
   amendment — never a rationalization after it — and both land **in one
   commit**: the `DECISIONS.md` entry and the specification text, nothing
   else, the subject naming the decision (`step-012: spec amendment —
   D-007, …`). A commit where the log and the specification disagree is a
   state a session can resume onto and misread as drift; and `git blame`
   on an amended line must land on a diff carrying the reasoning. Code
   stays out, so `git log -- SPECIFICATIONS.md` remains a readable
   history of amendments; the code implementing the change follows in the
   step's later commits. The entry lands alone only when the amendment
   belongs to a later step — then it says so and names that step. Silent
   drift between the spec and the
   implementation is the failure mode this rule exists to prevent.

   {{OPEN_FACTS}}

   **Of the phase that produced the specification, the specification
   itself is your only input** — what I tell you in our exchanges, and
   the memory files of rule 3, are of course yours to use.
   `.claude/spec-work/` is the specification phase's own history — apart
   from this prompt, consumed at bootstrap, and `handoff/assets/`, which
   stays readable from any session for as long as a template in it
   remains un-instantiated (rule 3), you never read anything in it, in
   this session or any later one. The
   specification is self-sufficient by construction; when something seems
   missing, that is a question for me under this rule, never something to
   excavate from the spec phase's history.

2. **Work happens one step at a time, gated by me.** You implement exactly
   one plan step, then stop. A step ends with: (a) a short summary of what
   you did, (b) precise manual test instructions for me — exact commands
   and what I should observe, (c) you waiting. You do not begin the next
   step until I explicitly say so. Fixes I request belong to the current
   step, not a new one. Never batch several steps because they look small.

   **You hand nothing over unverified by yourself.** Before asking me to
   test, every check that applies to what you changed passes:

   {{STATIC_CHECKS}}

   Two families belong on that list whatever the stack. **Governance
   well-formedness:** your instantiated tooling under `.claude/skills/`
   and `.claude/agents/`, and `.claude/settings.json` — frontmatter and
   JSON parse, and every command, path and agent a file names resolves.
   A malformed skill does not fail, it silently never loads; and the
   settings file is the enforcement mechanism itself, so malforming it
   after step `000`'s one-time probe fails exactly as quietly.
   **Prose lint over the governance documents**, configured to them as
   they already are — `SPECIFICATIONS.md` is
   read-only under rule 1, so the lint bends to it and never the reverse,
   and excluding a document from a rule is a logged decision, not a quiet
   config line. And prove once, at step `000`, that each
   enforcement mechanism actually binds in your version: one probe for
   the settings baseline, a separate one for skill-frontmatter
   restrictions — two mechanisms, and one passing says nothing about
   the other; an unenforced allowlist is a guard that
   exists only on paper. These checks live behind **documented commands in
   the repository** — two questions, kept apart because each answer must
   mean something: a *check* ("is what is committed here well-formed?" —
   syntax, lint and formatting over the whole working tree, untracked
   files included and gitignored paths excluded, with one standing
   exception this prompt decides now:
   everything under `.claude/spec-work/` is excluded from the harness —
   the exclusion keys on the path, not on tracked status — because
   rule 1 makes that directory no session's reading material) and
   a *test* ("is the implementation right?" — fixtures
   and expectations proving behavior, including the cases that must fail
   and those that must only warn: a warning nobody proves is emitted
   protects nothing), plus a *verify* entry point running both. The
   commands' names and mechanism are yours to choose from whatever is
   native to the stack — a Makefile, package-manager scripts, a task
   runner — documented, kept green, and runnable by me too. A fast form
   of *check* narrowed to what changed is legitimate mid-step; the commit
   that receives a `step-NNN` tag runs the full one — that commit is the
   state every later session treats as known-good. My gate exists to
   judge behaviour against the real world, not to catch typos.

3. **All memory lives in files**, because your sessions do not persist:
   - `PLAN.md` — the implementation plan and each step's status.
   - `DECISIONS.md` — the decision log.
   - `CLAUDE.md` — your standing instructions and re-orientation routine.
   At the start of every session: read `CLAUDE.md`, `PLAN.md`,
   `DECISIONS.md` and the spec sections relevant to the current step. The
   last `step-NNN` tag (rule 6) marks the last approved state — and
   because other tags will exist (rule 6), you find it by matching the
   step namespace, never by taking the latest tag of any kind:

       git describe --tags --abbrev=0 --match 'step-*'

   `git log` and `git diff` from that tag to `HEAD` are then exactly the
   work in progress — your re-orientation when a session starts
   mid-step. Before the first step tag exists, the range is simply the
   whole history. Then tell me where we are before touching anything.

   **`CLAUDE.md` is loaded on every run, so it stays small** — under 200
   lines, treated as a hard budget that yields to exactly one thing:
   rule 9's boundary enumeration is carried whole, and the trimming
   happens elsewhere. It holds only what applies always —
   the rules, the file map, the current-step pointer, the session
   routine — and *pointers* to everything else. Knowledge needed only in
   a specific context — per-topic notes, environment details,
   troubleshooting insight you accumulate along the way — goes into its
   own file under `.claude/docs/`, referenced from `CLAUDE.md` with when
   to read it ("before touching the maintenance timers, read
   `.claude/docs/maintenance.md`"), and read only then — the read-trigger
   is what makes lazy loading actually happen. Plain path references,
   never `@` imports — imports load eagerly and cost the same as
   inlining.
   **`.claude/refs/` is a different thing and never mixes with it:**
   material I supply as input — contracts of systems that will consume
   what you build, inventories, documents produced elsewhere. Read each
   at its trigger, and treat it as information, never as a requirement
   source: a conflict between a reference and the specification is a
   question for me. **It is read-only for you, exactly as the
   specification is** — you never edit, extend, annotate, compact, fold
   or delete one, and no sweep of yours ever touches it. It is not your
   memory, and it is not even this repository's: its authority is the
   source it came from. So the amendment channel of rule 1 does not
   apply here — there is nothing to decide. A reference that looks
   wrong, stale or contradicted by what you observe is *reported to me*,
   and I supply the correction. What you learned that made you doubt it
   belongs in `.claude/docs/` or the decision log, under your own name,
   never edited into my document. {{REFERENCES}}
   *Instructions* tied to one part of the tree may instead be path-scoped
   rules in `.claude/rules/` with a `paths` frontmatter, which load
   themselves exactly when you work on matching files — but never an
   unscoped rule, which loads every session and saves nothing. Before
   relying on that mechanism, prove it loads in the version you run — a
   rules file that never loads is instructions you believe are in force
   and are not, and the failure announces nothing; a nested `CLAUDE.md`
   is the fallback. Claude Code's **auto memory is already disabled**
   for this repository
   (`.claude/settings.json`, committed during the specification phase)
   and stays disabled: it is machine-local and unversioned — a second
   memory outside git, outside review, outside these rules — and
   everything it would hold belongs in `.claude/docs/` or `DECISIONS.md`
   instead. Confirm in step `000` that your version honours the key, on
   the same reasoning as the rules-file check: an unrecognised setting
   is ignored in silence.

   **The same economy applies to the memory files as they grow.** A
   completed `PLAN.md` step compacts to its outcome, the detail staying
   in git history. When the plan is large enough to group steps under
   milestones (rule 6), closing a milestone includes a memory-compaction
   pass — mandatory whoever performs it: the `optimize-memory` agent
   where adopted (see the assets below), otherwise a fresh subagent you
   brief inline, always from
   a clean context: completed steps compact to outcomes, decision entries
   to their kernel (the decision, the reason that stops re-litigation,
   the approval), git history the sole archive — and no forward
   obligation may be orphaned by compaction. Without milestones, run the
   same pass whenever the memory files have grown noticeably.

   **Documentation for people and documentation for you never share a
   directory.** `docs/` belongs to human readers — the spec's own
   deliverables and anything else written for a person — while
   `.claude/docs/` is your working memory. An operator or a reviewer
   must be able to treat everything in `docs/` as authoritative and
   ignore `.claude/` entirely.

   **The same namespace holds your tooling.** You may create skills
   (`.claude/skills/<name>/SKILL.md` — they define slash commands) and
   subagents (`.claude/agents/`) on your own initiative when they earn
   their place — a within-latitude decision, logged per rule 4. A ritual
   repeated every step is a natural skill; work that would flood your
   context — a spec-wide coverage audit, a long failed-run log, a
   pre-handover review — belongs in a subagent, which spends its own
   context and returns a summary (a cheaper model where the work is
   mechanical). **Starter templates proven by an
   earlier project live in `.claude/spec-work/handoff/assets/`** — four
   skills (`orient`, `resume-step`, `handover-step`, `approve-step`)
   and five agents
   (`step-reviewer`, `optimize-memory`, `state-reviewer`,
   `code-reviewer`, `test-reviewer`). Instantiate only the ones that fit
   this project, adapted: fill every placeholder with this repository's
   real commands and paths — including the governance set (`{{PLAN}}`,
   `{{DECISIONS}}`, `{{SPEC}}`, `{{STEP_ID}}`), which each template
   resolves to the files and identifier form that actually govern the
   work it performs. A template arrives with those as placeholders on
   purpose: a leftover one is visible, while a plausible wrong filename
   is not. Where a template's own enumeration of a routine is narrower
   than the rule it claims to execute, the rule wins and the
   enumeration is rewritten to match. Each adoption logged; the ones that earn
   their place later can wait — and once none remains un-instantiated
   (each adopted or explicitly dropped, logged), delete the assets
   directory and every pointer and exception referring to it in the same
   commit: git history keeps the templates, and rule 1's carve-out must
   not outlive its purpose. Tooling files are documentation like any
   other, kept current per rule 6 — and a skill or agent nobody invokes
   anymore is deleted, not kept.

4. **Decisions get logged in `DECISIONS.md`.** Three kinds: choices we
   make together (spec changes, scope calls, step reordering); choices
   you make alone inside the spec's "should" latitude — the spec permits
   deviating from a recommended default *with reason*, and that reason
   goes in the log; and workflow choices this prompt leaves to you,
   where the specification says nothing to deviate from — the harness's
   shape and names, `.gitignore` contents, which tooling templates you
   adopt. The permission baseline is not in that latitude: step `000`
   always puts it to me for review. Entry format: `D-NNN` id (file order,
   frozen once assigned, never reused), date, plan step, context,
   decision, alternatives considered, approved by (me, or
   you-within-latitude, naming which latitude).

5. **Secrets never enter the repository.** Not in files, not in examples
   with real values, not in commit messages. The spec ({{SECRETS_SOURCE}})
   defines how secrets are sourced; follow it, and use obvious
   placeholders in anything committed.

6. **Commits are small and traceable, and documentation ships inside
   them.** One coherent change per commit, subject prefixed with the step
   identifier: `step-NNN: ...`, three digits, zero-padded — or `meta: ...`
   for maintenance belonging to no step. When I approve a step, its
   closing commit receives an annotated tag `step-NNN` — the same
   identifier then names the step in `PLAN.md`, prefixes every commit,
   and names the tag, and `git diff` between two tags is exactly one
   step's change. The `step-*` namespace belongs to this workflow; I will
   create other tags for my own purposes, so anything that reasons about
   steps matches `step-*` explicitly and ignores every other tag. Step
   numbers are identifiers, not positions: a step's number **freezes when
   it enters `in progress`** — commits and its tag reference it from then
   on and it is never reused — while `pending` steps may be renumbered as
   the plan evolves; a renumbering commit sweeps and updates every step
   reference in `PLAN.md` and `DECISIONS.md`, and decision entries cite
   not-yet-started steps by number *plus title*, so a missed sweep stays
   decodable. `PLAN.md`'s order and headings — grouped under milestones
   when the plan is big enough that grouping helps — define the sequence,
   not the numbering. Everything a change makes stale updates in the same
   commit, on your own initiative, never because I asked: `PLAN.md`
   status, `DECISIONS.md` entries, `CLAUDE.md`'s current-step pointer and
   file references, `README.md`'s file map, and any `docs/` deliverable
   the change touches — documentation updated later is documentation that
   drifts. Likewise, when a step teaches you something a future session
   will need — an environment quirk, a hard-won diagnosis — writing it
   into `.claude/docs/` is part of finishing the step, not a favour. You
   commit locally; pushing to any remote happens only when I ask for it.

7. **Language.** Repository files, code and comments are in English.
   Converse with me in whichever language I use.

8. **`README.md` is the repository's neutral entry point** — for humans
   and for any other AI brought in to review. It is descriptive, never
   directive toward the implementer: your standing orders live in
   `CLAUDE.md` and are for you alone. Keep README.md's file map accurate
   as the repository evolves; for current state it points at `PLAN.md`
   rather than duplicating it.

9. **Bug reports on the current step are yours to drive.** When I report
   a failure, reproduce it, diagnose it, fix it, and re-run your own
   checks until they pass — then hand back with what changed and how I
   re-test. Do not return to me after every attempt; return with a fix —
   or, when rule 10's budget is spent, with a clear question.
   The boundary: anything local and read-only you run freely and without
   asking — installing the repository's pinned dependencies through the
   documented setup command included; fetching anything *not* pinned in
   the repository is not local. {{BOUNDARY}} happens only when I
   explicitly ask for or allow
   it in that exchange, never on your own initiative — a boundary the
   settings baseline of step `000` also enforces mechanically. The
   enumeration above is safety text: `CLAUDE.md` carries it whole, never
   compressed, summarized, or moved to a lazily-read file. When you
   cannot reproduce a failure within that boundary, ask me for the
   command output or logs instead of guessing.

10. **Persistence has a budget — asking is part of the workflow.** You
    can and must ask questions when they are needed: an ambiguity in the
    spec (rule 1), a choice hidden inside a step that is mine to make, or
    a failure you cannot resolve quickly. On failures specifically: two
    or three genuinely different approaches that fail — not variations of
    the same guess — is the signal to stop. Come back with what you
    tried, what you observed, your current hypotheses, and the question
    or information that would unblock you. Grinding indefinitely consumes
    usage without converging; a clear question after a written summary of
    failed attempts is cheaper and usually faster — and the summary
    itself is progress, not an admission of failure.

## Your first task — this session, no implementation yet

Produce four files, then stop for my review:

1. **`PLAN.md`** — the implementation plan, derived from the
   specification:
   - {{ORDERING}}. Where that order allows, put the cheap steps first:
     {{CHEAP_FIRST}}.
   - **The first step is the repository foundation**, before any project
     code: a `.gitignore` written with rule 5 in mind ({{IGNORE_ITEMS}};
     `.claude/reviews/`, which the reviewer templates assume is ignored —
     an untracked report otherwise blocks every clean-tree precondition
     downstream; `CLAUDE.local.md`); pinned base dependencies installable
     through one
     documented setup command; the check/test/verify harness of rule 2,
     with pre-commit hooks **and a CI workflow running the same harness**
     (ask me which forge the repository will live on — a freshly handed
     repository has no remote — and treat the workflow as verified only
     once I authorise the first push, since nothing local can exercise
     it; GitHub Actions when the repository is hosted there; check and
     test as separate jobs once both exist; cache the toolchain, but
     keep a
     periodic uncached run proving a fresh setup still works) so nothing
     diverges among the three runners — and the lint covering
     the governance documents themselves (`SPECIFICATIONS.md`, `PLAN.md`,
     the rest), since in this repository documents are load-bearing;
     **extending the committed `.claude/settings.json`** (auto memory is
     already off — keep it off) with a permission-and-hook baseline
     enforcing rule 9's boundary, proposed for my review: allow the
     harness, the setup command, the free side of rule 9's boundary and
     the *additive and read-only* subset of local git
     (add, commit, status, diff, log, show, rev-parse, describe, tag
     listing, annotated tags); **ask**
     for everything
     rule 9 gates, `git push` included — a denied pattern cannot be
     overridden in the very exchange rule 9 relies on — and for
     state-destroying local git. State that last one as a classifier,
     not a list, because a list is what gets outgrown: anything that
     rewrites history (`commit --amend`, `rebase`), moves or deletes
     tags or branches, or destroys uncommitted or untracked work
     (`reset --hard`, `git clean`) asks first — and an allow pattern
     must not silently admit one of them, the trap being that a bare
     `git commit` allowance admits `--amend`. The step tags, the linear
     history and the working tree are the memory rules
     3 and 6 rest on; reserve **deny**
     for what has no authorised use at all, naming each in the proposal
     rather than leaving "destructive" to interpretation; and a guard
     hook where a permission
     pattern cannot express the rule — instructions shape your behaviour,
     but only settings and hooks enforce it; and **your workflow tooling
     instantiated from `.claude/spec-work/handoff/assets/`** per rule 3 —
     `orient`, `resume-step`, `handover-step`, `approve-step` and the
     `step-reviewer` agent almost always earn their place from the
     start (a recovery ritual created during the crisis it is needed
     for is too late); propose the
     rest only when their trigger exists — and an instantiated file must
     never name a skill or agent you did not adopt: trim the reference
     or adopt it, because a dangling name is a ritual that silently
     skips a step. One carve-out: a name that sits on `CLAUDE.md`'s
     not-yet-adopted list is not dangling — it is the documented
     fallback the milestone ritual relies on. Its test: a fresh clone, the
     setup command, the check command, one commit — all green. Step
     `000`'s breadth is deliberate — one composite foundation step,
     this prompt's stated exception to the small-step rule, because its
     parts gate nothing separately testable: the fresh-clone test is
     the gate, the enforcement probes report their results in the
     step's summary, and anything only a remote can exercise is
     verified at first push. The plan cold-review below treats that
     breadth as decided here, never as a granularity finding.
   - Steps carry three-digit identifiers per rule 6 — `000`, the
     foundation, onward — grouped under milestones or feature headings
     when the plan is big enough that grouping helps. Steps must be small
     enough that I can test each one alone. For every step:
     **objective**, **spec sections implemented**, **deliverables**,
     **how I test it** — stating, when the test crosses rule 9's
     boundary, that it does, what it costs, and how I clean up
     afterwards — and **status** (`pending` / `in progress` /
     `awaiting test` / `done`).
   - Include the spec's non-code deliverables as steps in their own
     right: {{NONCODE}}.
   - **The plan accounts for the whole specification**: every section
     appears in at least one step, or in a short explicit list of what
     this pass leaves out with the reason — {{EXCLUSIONS}} give you most
     of that list. An orphaned section is how a requirement gets lost.
   - **Flag external prerequisites early**: things only I can prepare —
     {{PREREQUISITES}}. List each with the step that first needs it, so
     waiting on me never interrupts a step mid-flight.
   - End the plan with a section listing anything you consider
     underspecified, risky, or worth reordering — questions for me, never
     silent assumptions.
2. **`DECISIONS.md`** — initialised with the entry format and a first
   entry recording the adoption of this workflow.
3. **`CLAUDE.md`** — the ground rules above restated as your own standing
   instructions — concise, not verbatim, and keeping this numbering:
   tooling and decision entries cite the rules by number, and
   renumbering orphans every citation — plus the repository layout as
   it will emerge, a section headed exactly **`Current state`** holding
   the pointer to the current step (that wording — your tooling
   templates reference the section by name), and the session-start
   routine — including the standing instruction that a session resumed
   after an interruption, or told the work was interrupted, runs
   `/resume-step` before touching anything, never trusting the
   transcript, and — until step `000` has instantiated that skill —
   applies rule 3's re-orientation routine directly instead: the
   pointer to a not-yet-existing command must not strand the one
   interruption most likely to happen early, the one during step `000`
   itself. It also carries the plan-step entry shape and the
   boundary-crossing-cost rule from the plan instructions above: later
   sessions extend the plan, and the bootstrap cold review sources
   those conventions from `CLAUDE.md`, so they must actually be there.
   For as long as any tooling template remains un-instantiated
   it also carries the pointer to `.claude/spec-work/handoff/assets/`,
   rule 1's standing exception for that one directory, and the list of
   templates not yet adopted — a block deleted, together with the
   directory itself, once the last template is adopted or dropped
   (rule 3): after this session `CLAUDE.md`, not this prompt, is what a
   session reads, and a later milestone close that cannot find
   `optimize-memory` has no way to know it was ever offered. Kept
   deliberately small per rule 3: what applies always stays
   in, everything context-specific becomes a `.claude/docs/` file it
   points to. Write it so that a fresh session with no memory of this
   conversation behaves exactly as this one.
4. **`README.md`** — the neutral entry point for anyone who is not you: a
   human later, or another AI asked to review. Descriptive only: what the
   repository is, what each file is for, and the authority order —
   `SPECIFICATIONS.md`, then `DECISIONS.md`, then `PLAN.md`, then code.
   Include a short **For reviewers** section framing a review: the spec's
   must/should reading rules apply; code contradicting a *must* is a
   defect; a deviation from a *should* without a `DECISIONS.md` entry is
   a finding, while one with an entry is a judgement to assess; anything
   missing is checked against `PLAN.md`'s current step before being
   flagged; and a problem in the specification itself is a question for
   the human, never a change to propose. Note that each plan step's list
   of spec sections is the review checklist for that step.

Then, before presenting anything: **commit the four files** — one
`meta:` commit; rule 3's re-orientation reads git history, and an
uncommitted deliverable is invisible to it — and **have the plan
cold-reviewed**: this
session has no harness yet, so the cold review is rule 2's gate for it,
and step `000` brings these four files under the harness retroactively.
Spawn a fresh-context, read-only subagent with an inline prompt (the
agent files come later, in step 000) that reads only `SPECIFICATIONS.md`
and the four files you have just written — never this conversation, and
nothing under `.claude/spec-work/`: it holds the specification phase's
history, this prompt included, and a reviewer that reads any of it is no
longer cold. The workflow conventions its criteria cite — the step
entry shape, boundary-crossing test costs, what counts as cheap — live
in the `CLAUDE.md` you have just written, not in the specification:
name it in the reviewer's prompt as the source of those conventions,
and tell the reviewer that `CLAUDE.md`'s pointer to
`.claude/spec-work/handoff/assets/` is out of bounds like the rest of
that directory. It audits `PLAN.md` against `SPECIFICATIONS.md`:

- **coverage** — every spec section mapped to a step or explicitly
  excluded with reason, verified section by section, not trusted;
- **ordering** — dependencies respected, the cheap steps genuinely
  first, and no step depending on a capability a later step delivers
  (the classic: something goes live before its day-two operations
  exist);
- **granularity** — each step testable by me alone, boundary-crossing
  tests naming their cost and cleanup;
- **prerequisites** — the external list complete, each with the step
  that first needs it;
- **consistency** — no dangling references between steps;
- **premises** — any factual claim in the plan the specification does
  not state is flagged for verification, never trusted: training
  knowledge goes stale.

Triage its findings — accept, reject with reason, or genuinely my
call — and present the triage together with the plan for discussion.
Step `000` begins only after I approve the plan.
````

## Tooling assets

The nine templates beside this file (`handoff-assets/`) are copied verbatim
to `.claude/spec-work/handoff/assets/` when the prompt is written — the
*implementer* instantiates and adapts them, not the spec session, because
the real adaptation (the harness commands' names, what the guard must
block) only exists once step 000 designs the harness. One exception has a
channel: when a cold review round finds a defect in a copied template
itself — generic, nothing project-specific in the fix — correct the local
copy during triage, and record it in the upstream findings file (phase 7,
step 6) so the template is fixed at its source too. Each template states
its target path and placeholders in a header comment.

### Governance placeholders

Four placeholders recur across the templates and mean the same thing
everywhere. They exist because the failure they prevent is silent: a
template that ships a literal `PLAN.md` instantiates cleanly into a
repository whose plan is somewhere else, and the ritual then reads the
wrong file — or nothing — without complaining. A leftover `{{PLAN}}`,
by contrast, is visible on sight.

| Placeholder      | Resolves to                                                       | Single-track value |
| ---------------- | ----------------------------------------------------------------- | ------------------ |
| `{{PLAN}}`       | the plan governing the work this template performs                 | `PLAN.md`          |
| `{{DECISIONS}}`  | the decision log governing it                                      | `DECISIONS.md`     |
| `{{SPEC}}`       | the specification document(s) it must read                         | `SPECIFICATIONS.md`|
| `{{STEP_ID}}`    | the step identifier form used in commit subjects and tag names     | `step-NNN`         |

The tag *glob* is not one of them: `step-*` matches every form, so
`git describe --match 'step-*'` stays literal in every project.

This table is for the session writing the prompt. **The templates never
point at it, or at anything else on this side:** a template is copied into
the project and read there, at step 000, by a session that has no access to
the skill and that rule 1 forbids from going hunting through
`.claude/spec-work/`. Every template header therefore states its
placeholders' meaning inline, however much that repeats. Pointing at
`PROMPT.md` instead is no better — the prompt is consumed once at
bootstrap, while the templates are read later — so the only correct
target for a template's own explanation is the template.

| Template            | Becomes                                | Adoption default                              |
| ------------------- | -------------------------------------- | --------------------------------------------- |
| `orient.md`         | `.claude/skills/orient/SKILL.md`       | step 000 — session-start ritual               |
| `resume-step.md`    | `.claude/skills/resume-step/SKILL.md`  | step 000 — post-interruption verification     |
| `handover-step.md`  | `.claude/skills/handover-step/SKILL.md`| step 000 — pre-test handover ritual           |
| `approve-step.md`   | `.claude/skills/approve-step/SKILL.md` | step 000 — post-approval close ritual         |
| `step-reviewer.md`  | `.claude/agents/step-reviewer.md`      | step 000 — runs before every handover         |
| `optimize-memory.md`| `.claude/agents/optimize-memory.md`    | when milestones exist, or memory files grow   |
| `state-reviewer.md` | `.claude/agents/state-reviewer.md`     | suggested at the first milestone close        |
| `code-reviewer.md`  | `.claude/agents/code-reviewer.md`      | on request only — offer it, don't install it  |
| `test-reviewer.md`  | `.claude/agents/test-reviewer.md`      | on request only — offer it, don't install it  |

Shared conventions the templates carry, worth preserving at instantiation:
skills declare turn-scoped `allowed-tools`, but never `disallowed-tools`
— a deny rule binds for the whole turn that invoked the skill and never
prompts, so a read-only skill invoked mid-turn silently strands the rest
of that turn with no way to write; read-only skills carry "report and
stop" as prose instead; reviewer agents are read-only except for their own
report under the untracked `.claude/reviews/`; review reports **become a
plan of decisions for the user's approval — nothing is fixed straight from
a report**; `handover-step` (pre-test) and `approve-step` (post-approval)
are different moments and never merge; `approve-step`'s hard precondition
is the user's explicit approval in the exchange, never inference. Agents
marked `model: fable` should run on the strongest model available at
instantiation time.
