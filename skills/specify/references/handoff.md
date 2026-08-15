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
memory. **Three are exempt by construction**, and raising them as
findings against a finalized specification is the mistake this sentence
otherwise invites: `{{BOUNDARY}}` is a policy call, `{{REFERENCES}}` and
`{{HOUSE_TOOLING}}` are the user's own context. None has a source in the
specification, all three are asked for in the batch, and not finding
them there is not a finding.

Present the filled values to the user as a numbered batch before writing
the file; apply their rulings. Beyond the slots, tailor only what
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
   part. Name the concrete examples from this project. **The foundation
   milestone is outside this ordering**, and the slot should say so: it
   ends with CI, which by definition leaves the machine, and a plan that
   sorts its milestones by cost class will push that step out of the
   bootstrap and call the project bootstrapped without it.
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
     recorded — and for a third-party binary, which no linter of yours
     can read, **that pin and record is the whole coverage
     obligation**. Say so in the slot: "covered like anything else
     shipped", left undefined, invites invented verification
     machinery around someone else's executable. *Ships*
     is present tense, and the slot must say so: **a family arrives
     with the first file of its class, in the step that lands it** —
     never ahead of it. A family (and its fixtures) for an artifact
     the repository does not yet contain is scaffolding, not
     coverage, and it is the reading a bare "every artifact the
     repository ships" reliably produces when the plan says those
     artifacts are coming.
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
   baseline of step `001`, and the plan's test-cost flags. Walk the
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
   projects), especially the slow ones, each findable in the spec. **The
   forge, the remote and the authorisation of the first push are always
   on this list, needed at the foundation's last step** — the bootstrap
   does not close until CI has run there. Look
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
    inventories, material produced by another project — and **their
    own existing conventions**: a sibling repository's CI workflow,
    their linter configuration, the house shape of a Makefile. **Ask
    for these; they are never volunteered.** A user who has settled
    on a CI style will not think to mention it, and the implementer
    invents a different one because nothing told it one existed —
    then rewrites it after the fact, which is the expensive order.
    The question belongs in the same batch: *which of your existing
    repositories should the implementer read before writing CI,
    lint configuration or the harness?* Each gets a
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
13. `{{HOUSE_TOOLING}}` — the tools the user already uses for the jobs
    the foundation steps have to do: the hook runner, the task runner,
    the linters, the CI forge. **Ask, and name what comes back in the
    prompt.** The
    slot exists because the alternative was measured: a prompt saying
    the mechanism is the implementer's choice, plus a plan line reading
    "pre-commit hooks" in lower case, produced six hundred lines of
    bespoke runner, file-discovery library, pinned-binary installer and
    fixture driver — a reimplementation of `pre-commit`, which the user
    already ran in their other repositories. "Of your choice" is read as
    permission to build, and a tool named in lower case is read as the
    generic thing (git hooks), not as the tool of that name. So write
    the tools with their identity unmissable ("the `pre-commit`
    framework, not merely git hooks"). The slot is never dropped: where
    the user has no preference for a given job, it says so in as many
    words ("no house preference for the task runner"), which leaves
    rule 11's standing preference — the boring standard tool of the
    ecosystem — in charge rather than leaving the choice unqualified.

    **Standing defaults to propose, not to assume.** This skill's user
    has settled these; put them in the batch as the recommendation and
    let them confirm or override per project:
    - the **`pre-commit` framework** (<https://pre-commit.com>) as the
      hook runner, named as the tool, never as "pre-commit hooks";
    - **`just`** (<https://github.com/casey/just>) as the task runner
      **where the project's main language brings none of its own** —
      where it does, that ecosystem's runner wins;
    - **no house preference for linters**: each ecosystem's standard
      tool, pinned in one place;
    - CI on the forge the specification settles, in the shape of the
      user's existing workflows — which is a `{{REFERENCES}}` item
      (their own repository, dropped into `.claude/refs/` with a
      read-trigger), not something to reconstruct from memory.
    A default is a starting point for the batch. If the user answers
    differently, the answer wins and this list is not argued back at
    them.

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
  (`project-zomboid/DECISIONS.md D-003`). Say where the case that
  crosses lands, because it arrives early and stalls when unstated:
  **a component-track step amending the root specification logs its
  decision in the root log**, in the same commit as the amendment
  (rule 1), with the component step id in the subject — the log
  follows the document being amended, not the step doing the work.
  An amendment touching both a root and a component document is two
  entries, one per log, cross-citing.
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
- **The templates** are instantiated **once each**, and their governance
  placeholders resolve to the active track **at invocation** — from the
  track map and the `Current state` pointer — not to one literal path.
  This is what the placeholders are for. On a component track, `{{SPEC}}`
  includes the root specification, per rule 3. **One exception, and it
  is the one that fails silently:** rituals fired as part of *closing* a
  step — the milestone state review and memory compaction above all —
  key on the track of the step **just closed**, named explicitly by the
  close ritual, never on the pointer. The close ritual advances that
  pointer before it fires them, so at any cross-track milestone boundary
  resolve-at-invocation aims both passes at the wrong track, and a state
  reviewer reading the wrong track's plan reports nothing wrong.

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
   step's later commits — as does any documentation the amendment makes
   stale: for amendment commits, this rule wins over rule 6's
   same-commit staleness sweep, and the two rules otherwise collide with
   no stated winner. The entry lands alone only when the amendment
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
   **When I ask for something to be removed, it is removed.** A smaller
   version of it, a rewritten version, a version moved elsewhere: none of
   those is compliance, and each costs a round to detect. If you believe
   the removal is a mistake, say so in one sentence and do it anyway —
   or ask, before acting, which of the two I meant.

   **You hand nothing over unverified by yourself.** Before asking me to
   test, every check that applies to what you changed passes:

   {{STATIC_CHECKS}}

   Two families belong on that list whatever the stack. **Governance
   well-formedness:** your instantiated tooling under `.claude/skills/`
   and `.claude/agents/`, and `.claude/settings.json` — their frontmatter
   and JSON must parse. A malformed skill does not fail, it silently
   never loads; and the settings file is the enforcement mechanism
   itself, so malforming it after step `001`'s one-time probe fails
   exactly as quietly. Those two parse checks are cheap and exact, and
   they are the whole of what this rule requires. Checking further —
   that a command, path or agent a file names actually resolves — is a
   *should*: worth doing where it is exact (an agent name against
   `.claude/agents/`, a path against the tree), and worth refusing where
   it is not. Scanning prose for backticked tokens and asserting each one
   resolves has been built and regretted: it is a false-positive machine
   that grows worse as the repository does, and once mandated by a rule
   it cannot be deleted without amending the rule.
   **Prose lint over the governance documents**, configured to them as
   they already are — `SPECIFICATIONS.md` is
   read-only under rule 1, so the lint bends to it and never the reverse,
   and excluding a document from a rule is a logged decision, not a quiet
   config line. And prove what each enforcement mechanism actually does
   in your version — one probe per mechanism, **run at the step that
   introduces that mechanism**: settings keys, permission patterns and
   the guard hook being reached at all at step `001`; an agent's
   `tools:` frontmatter, and whether `CLAUDE.md` reaches a subagent's
   context at all, at step `002` — that one costs one exchange with the
   first agent you spawn ("quote rule 9's opening line") and every
   reviewer agent's boundary rests on it; `.claude/rules/` loading at
   the step that first adopts a rules file, if any. The probes are
   independent, and one passing says nothing about another; pinning them
   all to the first step means probing mechanisms that do not exist yet,
   which reports a pass for nothing.
   Assume nothing here, including from this prompt. A mechanism that
   turns out to enforce nothing is a guard on paper, and the failure
   announces nothing, so probe at least: whether a skill's frontmatter
   restricts anything at all; which spelling of a file-path rule the
   file tools actually match; whether the settings keys you set are
   honoured; whether the hook is reached. **The values you measure do
   not live in this prompt or in `CLAUDE.md`** — they go in the
   `.claude/docs/` file this step writes, each with the version it was
   taken on, the method, and the re-measure recipe. Standing
   instructions have no staleness discipline: a version-stamped fact
   restated there outlives its version in silence, which is the same
   failure one layer up. Whatever the probe finds, what binds is what
   you keep.
   These checks live behind **documented commands in
   the repository** — two questions, kept apart because each answer must
   mean something: a *check* ("is what is committed here well-formed?" —
   syntax, lint and formatting over the whole working tree, untracked
   files included and gitignored paths excluded, with one standing
   exception this prompt decides now:
   everything under `.claude/spec-work/` is excluded from the harness —
   the exclusion keys on the path, not on tracked status — because
   rule 1 makes that directory no session's reading material) and
   a *test* ("is the implementation right?" — fixtures and expectations
   proving the behaviour **this repository itself ships**, the cases
   that must fail included). Three limits keep that honest: a
   third-party tool is never retested — that shellcheck reports SC2086
   is its maintainers' problem, not this repository's; a must-warn case
   is required only where the implementation already defines a warning
   tier, never a reason to invent one; and where the repository ships
   no behaviour of its own yet, a *test* command that says so is the
   correct state, not a gap to fill. One observable, since "untracked
   files included" is where hook runners quietly disagree: a lint error
   in a file that exists but has never been added to the index must
   still fail *check*. Runners that enumerate from git (`pre-commit
   run --all-files` among them) see only what git already knows about,
   so the entry point passes the file list explicitly — tracked plus
   untracked-but-not-ignored, which is one command substitution
   (`git ls-files --cached --others --exclude-standard`). Never
   `git add --intent-to-add`: it writes to the index as a side effect of
   a *check*, turning `?? file` into ` A file` in `git status
   --porcelain` — the output the handover and approve rituals read for
   their clean-tree preconditions — and letting the next `git commit -a`
   sweep that file into an unrelated commit. That glue is one line, not
   a bespoke runner. Then a *verify* entry point
   running both. **The mechanism behind those commands is configured,
   not written** — rule 11 applied to the harness itself. Use what I
   already use: {{HOUSE_TOOLING}}. Where I have no preference, take the
   standard tool of the ecosystem; where nothing standard fits, the
   runner, installer or test driver you write is a decision logged with
   the alternatives you rejected and put to me *before* it is built.
   Whatever the mechanism: documented, kept green, and runnable by me
   too. A fast form
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

   **`CLAUDE.md` is loaded on every run, so it stays small** — under 220
   lines, treated as a hard budget that yields to exactly one thing:
   rule 9's boundary enumeration is carried whole, and the trimming
   happens elsewhere. **It is written with headroom** — around 180 lines
   when you first hand it over, not 219. A file at its cap forces the
   next session that must add one pointer to reflow the whole document
   before it can do its own work, and a budget check that warns from the
   day it is written teaches you to ignore it. When the budget binds,
   things leave in this order, and the order is not yours to reshuffle:
   first anything context-specific that a read-trigger can reach
   (`.claude/docs/`), then the temporary tooling-templates block once
   its directory is gone, then per-track detail that the track's own
   plan already carries. Rule 9's enumeration never leaves, and neither
   does the current-step pointer. If the rules still cannot be restated
   inside the headroom after that, that is a finding to raise with me,
   not a file to pack — and one legitimate outcome of raising it is a
   budget of this project's own, logged as a deviation with what makes
   it necessary. A repository whose boundary enumeration is long, or
   which has many source-of-truth directories to name, has a higher
   floor than these numbers assume; what must not happen is the floor
   being met by deleting something with nowhere else to go. It holds only what applies always —
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
   and are not, and the failure announces nothing. If it does not load,
   the fallback is a `.claude/docs/` file with its read-trigger in
   `CLAUDE.md`; a nested `CLAUDE.md` only where this repository has no
   single-`CLAUDE.md` invariant to break. Claude Code's **auto memory is already disabled**
   for this repository
   (`.claude/settings.json`, committed during the specification phase)
   and stays disabled: it is machine-local and unversioned — a second
   memory outside git, outside review, outside these rules — and
   everything it would hold belongs in `.claude/docs/` or `DECISIONS.md`
   instead. Confirm in step `001` that your version honours the key, on
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
   skills (`orient`, `resume-step`, `handover-step`, `approve-step`),
   five agents
   (`step-reviewer`, `optimize-memory`, `state-reviewer`,
   `code-reviewer`, `test-reviewer`), and one hook, `bash_guard.py` —
   the Bash permission guard step `001` instantiates, whose own module
   docstring carries its doctrine. Instantiate only the ones that fit
   this project, adapted: fill every placeholder with this repository's
   real commands and paths — including the governance set (`{{PLAN}}`,
   `{{DECISIONS}}`, `{{SPEC}}`, `{{STEP_ID}}`), which each template
   resolves to the files and identifier form that actually govern the
   work it performs. A template arrives with those as placeholders on
   purpose: a leftover one is visible, while a plausible wrong filename
   is not. A placeholder whose referent does not exist yet at
   instantiation — the state reviewer's architecture vocabulary and
   inspection commands, in a repository where nothing is built — is
   seeded from the specification's own vocabulary and kept current under
   rule 6 as the system materializes; "fill every placeholder with real
   commands and paths" is otherwise unsatisfiable for anything
   instantiated up front. Where a template's own enumeration of a routine is narrower
   than the rule it claims to execute, the rule wins and the
   enumeration is rewritten to match. Each adoption logged. **What
   waits is decided by the certainty of the trigger, not by whether the
   trigger has fired yet:** a ritual whose moment is a certainty of this
   plan — the milestone close is the standing example, and it needs both
   a state review and a memory compaction — is instantiated up front,
   because tooling created during the event it exists to handle arrives
   too late and gets improvised instead. Only a *conditional* trigger
   justifies waiting: an agent that reviews code, or tests, in a
   repository that has neither yet. Once none remains un-instantiated
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
   adopt. The permission baseline is not in that latitude: step `001`
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
   closing commit receives an annotated tag `step-NNN`, whose message
   carries the step identifier and title, the approval date, and a short
   paragraph of notable outcomes — fixed here rather than left to the
   close ritual, because that ritual is instantiated at step `002` and
   would otherwise anchor on whatever shape the first two closes
   improvised. The same
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
   commit locally; pushing to any remote happens only when I ask for it,
   with one standing exception: **at a step close, attempt the push** —
   that is when I want the commit and its tag published and when I forget
   to say so, and the permission gate is there to put the question to me.
   It stays an exception to be cited, never a pattern to extend: nowhere
   else do you attempt a gated act because something downstream might
   catch it.

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
   settings baseline of step `001` also enforces mechanically. The
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

11. **Proportion: the smallest thing that satisfies the rule is the
    right thing.** Every other rule here rewards thoroughness — nothing
    handed over unverified, every artifact covered, every decision
    logged — and nothing in them ever asks for less. This one does, and
    it applies to your own output before it applies to anything else:
    - **The boring standard tool beats yours.** Before writing a runner,
      an installer, a discovery library or a test driver, ask whether
      the ecosystem already ships one. That question costs a sentence;
      skipping it has cost six hundred lines.
    - **Build at the moment of need, not in anticipation of it.** A
      check family for a file type the repository does not contain, an
      abstraction over one case, a warning tier nothing needs: each is
      scaffolding that must be maintained and eventually deleted.
    - **Deletion is a legitimate outcome of a review, and of a step.**
      When you review, or when a reviewer reports to you, "this could be
      removed" and "this could be replaced by something standard" rank
      beside defects. A review round that only ever adds is how a small
      job becomes a large one.
    - **A clean review is not evidence that the work was worth doing.**
      Reviewers judge conformance to the plan; whether the plan's output
      earns its size is my judgement, and yours before mine. If the
      answer to "what would be lost by deleting this?" is nothing, say
      so before I do.

## Your first task — this session, no implementation yet

Produce four files, then stop for my review:

1. **`PLAN.md`** — the implementation plan, derived from the
   specification:
   - {{ORDERING}}. Where that order allows, put the cheap steps first:
     {{CHEAP_FIRST}}.
   - **The repository foundation comes first, in four gated steps**,
     before any project code. They are separate steps because each is
     separately testable and because you must not build them all before
     I have seen any of them: a foundation delivered whole arrives with
     everything already written, and my first correction then costs the
     lot. Ordered by dependency — the tooling of `002` cites the
     boundary that `001` enforces, all of it runs under the harness of
     `000`, and `003` puts that same harness on the forge.
     **These four are one milestone, and it is drawn by what a working
     repository needs, not by cost class.** CI is the first step that
     leaves this machine, which is a reason for it to come *last within
     the foundation* — never a reason to move it out into a later
     milestone grouped by cost. I do not consider a project bootstrapped
     until its CI has run green.
     - **`000` — the harness, local only.** A `.gitignore` written with
       rule 5 in mind ({{IGNORE_ITEMS}}; `.claude/reviews/`, which the
       reviewer templates assume is ignored — an untracked report
       otherwise blocks every clean-tree precondition downstream;
       `CLAUDE.local.md`); pinned base dependencies installable through
       one documented setup command; the check/test/verify harness of
       rule 2, built on the tools named there rather than on anything of
       your own; **`check` in both of rule 2's scopes from the start** —
       the whole-tree gate as the default, and the narrowed
       what-changed form the development loop runs between gates, since
       every step after this one uses it — as **one entry point taking
       a scope, never a second recipe**: two recipes hold two lists of
       checks and will eventually differ in *what* they look for, not
       only in how much they look at; the same harness wired into the
       commit hooks, so the local runners never diverge; and the lint
       covering the
       governance documents themselves (`SPECIFICATIONS.md`, `PLAN.md`,
       the rest), since in this repository documents are load-bearing.
       Its test: a fresh clone, the setup command, the check command,
       one commit — all green. **The CI workflow is deliberately not in
       this step** but in `003`: nothing local can exercise a workflow,
       and a tagged step must not carry an artifact its own gate never
       ran.
     - **`001` — the permission and hook baseline**, proposed for my
       review as a whole. Two layers, and the guard decides the shape of
       the settings rather than the other way round.
       **The guard first:** instantiate
       `.claude/spec-work/handoff/assets/bash_guard.py` as
       `.claude/hooks/bash_guard.py` (executable), read its module
       docstring in full, and edit only its `REGISTRY`. That docstring
       is the doctrine for this deliverable — how to choose between
       *rules* and *grants* per tool, what must land in
       `.claude/settings.json`, what the guard cannot see, and the rule
       that its `GIT` ground rules are the same in every project and are
       added to, never weakened. Inventory what this project actually
       runs — the harness, the container and cloud tooling, the
       language runtimes, anything a `justfile` or `Makefile` shells
       out to — and give each tool in the registry the acts rule 9
       gates for *this* project. Every rule you add gets a `CASES`
       entry: `--selftest` fails on a rule no case reaches, which is
       what keeps the intent executable rather than remembered.
       **Then the settings**, per the docstring's pairing: one broad
       allow per registry tool, no `ask` rule for anything the guard
       gates (a matching `ask` prompts even where the guard says allow,
       so it cancels every carve-out), no prefix rule restating a guard
       decision — a prefix is strictly weaker and gives you two sources
       of truth — and, as the **one deliberate exception to that**, a
       short `deny` backstop for the acts that cannot be undone: a hook
       fails open, and a prefix rule that binds without it is worth more
       than the duplication costs. Keep it short enough that the
       exception stays visible as one. Keep settings' `ask` tier for tools the guard has
       no registry entry for — `gh`, `curl`, whatever this project
       reaches for outside it. **`git push` is not one of them**: it is
       gated in the guard's ground rules, and restating it as a prefix
       rule is the two-sources-of-truth case above, the weaker of which
       misses `git -C dir push`. What holds for a push wherever it is
       expressed is the *tier*: it asks and is never denied — a denied
       pattern cannot be approved in the very exchange rule 9 relies
       on. `deny` stays reserved for what has no authorised use at all,
       each named in the proposal.
       Auto memory is already off — keep it off.
       **A hook fails open**, so it is gated twice in this same step,
       and the two gates ask different questions.
       `bash_guard.py --liveness` goes in the pre-commit lint: the file
       is executable, the registry builds, every rule and grant is
       well-formed, a payload still comes back as a verdict — no
       behaviour cases, so a lint stays a lint, and the silent deaths
       (a syntax error from an edit, a lost `+x`, a rename) fail the
       commit. `bash_guard.py --selftest` goes in the *test* entry
       point: liveness, then every case, then coverage — a rule or
       grant no case reaches fails it. A guard that stops working must
       fail a gate, not fail quietly. And say plainly, in the proposal, what a dead guard
       would leave open — a broad allow plus a dead hook is a wider
       surface than a narrow allow list ever was, and the `deny`
       backstop exists exactly there.
       **Then measure, and write down what you measured.** Rule 2's
       probes for this step's mechanisms run here; their results land
       in a `.claude/docs/` file — every claim a measurement with the
       version it was taken on, the method, and a short re-measure
       recipe to re-run after a Claude Code update — plus a liveness
       check the session rituals of `002` can run: one command that
       must run silently, one the guard *grants*, and one it must
       **refuse, naming the rule that read it**. That third probe is
       the only one that says the hook is reached at all: if it merely
       prompts, the hook is not wired and the deny backstop is all that
       is left, while the guard's own `--selftest` and `--liveness`
       would still pass — they answer whether the file is correct, not
       whether anything calls it. For the same reason the governance
       family checks that the hook path in the settings resolves: a
       path naming a file that is not there leaves valid JSON, a
       settings file that loads, a green lint, and a guard that never
       runs. Report in the
       step summary what each mechanism actually did, including the
       ones that turned out to enforce nothing. Name the permission
       mode you expect me to work in — it is a committed setting
       (`permissions.defaultMode`), not only a per-session choice, and
       it decides how much the rest has to carry: under `default` an
       unmatched command still prompts, while under `auto` or
       `bypassPermissions` nothing prompts by itself and the guard's
       asks are the only gate left — so **whether a hook `ask` still
       prompts in that mode is one of this step's probes**, recorded
       like the rest: the close ritual attempts its push in reliance on
       it, and a gate that has stopped gating says nothing about it.
       Set the mode rather than working
       around it — `acceptEdits` is what removes the need for a blanket
       `Edit(/**)` allowance — and let it decide whether the
       mode-disabling keys belong in the baseline at all. Its test: my
       review of the proposal, the
       probe results, and `--selftest` green.
     - **`002` — the workflow tooling**, instantiated from
       `.claude/spec-work/handoff/assets/` per rule 3: `orient`,
       `resume-step`, `handover-step`, `approve-step`, the
       `step-reviewer` agent, and the agents whose trigger is a
       certainty of this plan (a milestone close needs its state review
       and its memory compaction to exist before it arrives, not to be
       improvised at the boundary). A recovery ritual created during the
       crisis it is needed for is too late. Propose the conditionally
       triggered rest only when their trigger exists — and an
       instantiated file must never name a skill or agent you did not
       adopt: trim the reference or adopt it, because a dangling name is
       a ritual that silently skips a step. One carve-out: a name that
       sits on `CLAUDE.md`'s not-yet-adopted list is not dangling — it
       is the documented fallback the milestone ritual relies on. Its
       test: I invoke each ritual and see it do what it claims —
       note that a new skill or agent may only be picked up at session
       start, so say whether a restart is part of the test.
     - **`003` — the same harness on the forge**, and the step that
       finishes the bootstrap. The workflow **reuses `000`'s entry
       points** rather than restating a single check — CI and the local
       runners must never be able to disagree about what "green" means
       — splits check and test into separate jobs once both exist,
       caches the toolchain, and keeps a way of proving a fresh setup
       still works, which may ride a scheduled job the specification
       already requires rather than becoming a second scheduled workflow
       of its own. Ask me which forge the repository will live on if the
       specification does not settle it. This is the one foundation step
       nothing local can exercise, so **its gate is a real run**: name
       the forge, the remote and my authorisation of the first push as
       external prerequisites needed *at bootstrap* — not late, which is
       where a cost-ordered plan would put them — and treat the workflow
       as unverified until I authorise that push and the run comes back
       green. Its test: I authorise the push and watch the run.
     Nothing here is exempt from the small-step rule. If one of the
     four is still too big for a single test — or cut in the wrong
     place for this project — say so, and split it further in the plan
     you present; the cold review below is invited to find exactly that.
     And the four foundation entries carry this prompt's per-step
     prescriptions **in full** — the permission classifier and its
     traps, the probe duties, the CI reuse rule and its prerequisites,
     the instantiation list — as their deliverables and test content:
     this prompt is consumed once at bootstrap, and a session resuming
     onto the plan must find that detail in the plan, not remember it.
   - Steps carry three-digit identifiers per rule 6 — `000` to `003`,
     the foundation, onward — grouped under milestones or feature
     headings when the plan is big enough that grouping helps. The
     milestone close is what triggers rule 3's compaction and state
     review, and what makes those two agents' adoption certain at step
     `002`, so a plan you judge too small to group says so in the
     open-questions section rather than omitting the grouping silently.
     Steps must be small
     enough that I can test each one alone. For every step:
     **objective**, **spec sections implemented**, **deliverables**,
     **how I test it** — stating, when the test crosses rule 9's
     boundary, that it does, what it costs, and how I clean up
     afterwards — and **status** (`pending` / `in progress` /
     `awaiting test` / `done`).
     **An approved step keeps none of that.** On approval its entry is
     replaced, not annotated — the plan text described intentions the
     step itself has since changed, and it sits in a file every session
     reads at start. What is left is the heading and one bullet:

         ### <step id> — <step title> — `done`

         - **Outcome (approved YYYY-MM-DD, tag `<step id>`):** what now
           exists and what it decided, in a few lines, citing the
           decision entries it rests on. Detail in git history between
           tags `<previous step tag>` and `<step id>`.

     Carry it into `CLAUDE.md`'s plan conventions **as one line, not as
     this block** — a closed step keeps its heading marked `done` and
     one outcome bullet with the approval date, the tag, what now
     exists, and the tag range for the detail. That is enough to act on,
     which is what the early closes need: `/approve-step` is
     instantiated at step `002`, so the first two closes happen without
     it, and the first compacted entry is what every later close
     imitates.
   - Include the spec's non-code deliverables as steps in their own
     right: {{NONCODE}}.
   - **The plan accounts for the whole specification**: every section
     appears in at least one step, or in a short explicit list of what
     this pass leaves out with the reason — {{EXCLUSIONS}} give you most
     of that list. An orphaned section is how a requirement gets lost.
     **Open facts are accounted for one by one**, each naming the step
     that settles it: they are the items the specification itself
     ordered resolved during implementation, so a section-level
     "verified along the way" leaves them owned by nobody — and the
     ones that go missing are the facts a section mentions in prose
     rather than lists (a size or cost "to be measured at
     implementation" is an open fact, whatever it is called where it
     appears).
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
   it will emerge, a section headed exactly **`Current state`** (that
   wording — your tooling templates reference the section by name)
   **holding a closed list of item kinds and nothing else**: the
   current and next step, live world-state, open obligations, the
   pointers into `.claude/docs/`. What a closed step *produced* is not
   one of them — its outcome belongs in its plan entry and its tag, a
   durable fact in `.claude/docs/`, an invariant in the decision log —
   so the close ritual deletes that paragraph rather than demoting it.
   Say so here: without the closed list, each close adds one reasonable
   paragraph and the section becomes a changelog, which has been
   measured at 131 lines. And the session-start
   routine — including the standing instruction that a session resumed
   after an interruption, or told the work was interrupted, runs
   `/resume-step` before touching anything, never trusting the
   transcript, and — until step `002` has instantiated that skill —
   applies rule 3's re-orientation routine directly instead: the
   pointer to a not-yet-existing command must not strand the
   interruptions most likely to happen early, the ones during the
   foundation steps themselves. It also carries the plan-step entry
   shape — the open form in full, and the compacted-on-approval form as
   a single rule rather than a block, since the ritual that performs a
   close carries the detail and `CLAUDE.md` only has to state the
   invariant for the closes that happen before that ritual exists — and
   the
   boundary-crossing-cost rule from the plan instructions above: later
   sessions extend the plan and close its steps from `CLAUDE.md` alone,
   and the bootstrap cold review sources those conventions from there,
   so they must actually be present.
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
   points to — and it lands **with headroom, around 180 lines, not at
   the 220-line cap**, so the next session that must add a pointer adds
   it instead of reflowing the file first. Two things the restatement
   must not do, both observed: rule 9's enumeration is carried whole
   **including the qualifiers that bound its free side** — "installing
   pinned dependencies is free, fetching what is not pinned is not" is
   one statement, and keeping half of it widens the boundary; and **no
   sentence may cite a clause the file does not contain** — a
   restatement that drops a clause and keeps the sentence referring to
   it leaves a rule that cannot be read at all. Write it so that a
   fresh session with no memory of this conversation behaves exactly as
   this one.
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
agent files come later, in step `002`) that reads only `SPECIFICATIONS.md`
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
  excluded with reason, verified section by section, not trusted; and
  **every open fact mapped to the step that settles it, item by item**
  — a section-level pointer ("verified across the later steps") is not
  a mapping, and the items that slip are the ones a section mentions in
  passing rather than lists;
- **ordering** — dependencies respected, the cheap steps genuinely
  first, and no step depending on a capability a later step delivers
  (the classic: something goes live before its day-two operations
  exist);
- **granularity** — each step testable by me alone, boundary-crossing
  tests naming their cost and cleanup. **No step is exempt**, the
  foundation steps included: "this step is too big to judge in one
  gate" is one of the most valuable findings this review can return,
  and a plan that declares any step's breadth beyond question has
  disarmed its own reviewer;
- **proportion** — deliverables that exceed what their step's objective
  requires, anything the plan proposes to build that a standard tool of
  the ecosystem already provides, anything scheduled ahead of the need
  for it. "Delete this" and "use the boring existing tool" are findings
  of the same rank as a coverage gap;
- **prerequisites** — the external list complete, each with the step
  that first needs it;
- **consistency** — no dangling references between steps;
- **premises** — any factual claim in the plan the specification does
  not state is flagged for verification, never trusted: training
  knowledge goes stale.

Triage its findings — accept, reject with reason, or genuinely my
call — **apply and commit the accepted ones**, then present the triage
together with the corrected plan for discussion, rejected findings and
their reasons included. Step `000` begins only after I approve the plan.
````

## Tooling assets

The ten templates beside this file (`handoff-assets/`) are copied verbatim
to `.claude/spec-work/handoff/assets/` when the prompt is written — the
*implementer* instantiates and adapts them, not the spec session, because
the real adaptation (the harness commands' names, which tools the guard's
registry must carry) only exists once the foundation steps design the
harness and its permission baseline. One
exception has a
channel: when a cold review round finds a defect in a copied template
itself — generic, nothing project-specific in the fix — correct the local
copy during triage, and record it in the upstream findings file (phase 7,
step 6) so the template is fixed at its source too. Each markdown template
states its target path and placeholders in a header comment.

`bash_guard.py` is the one that is not a markdown template: it is working
code, copied executable, and it explains itself in its module docstring —
target path, the engine/registry split, how to choose between *rules* and
*grants*, what must land in `.claude/settings.json`, what it cannot see,
and how it stays honest. It carries no `{{SLOT}}`: everything
project-specific goes in its `REGISTRY` section, and everything above that
banner is meant to travel between projects unchanged. Two of its standing
properties outlive instantiation and belong in the project's own rules
when step `001` adopts it: its `GIT` entry is ground rules — added to for
a stated project reason, never weakened to get past a prompt — and after
the operator's one-pass review of the initial registry, **every later rule
change is theirs to approve**, with a reported misbehaviour fixed only
together with a `CASES` entry reproducing the exact command they gave.

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
the project and read there, when they are instantiated, by a session that has no access to
the skill and that rule 1 forbids from going hunting through
`.claude/spec-work/`. Every template header therefore states its
placeholders' meaning inline, however much that repeats. Pointing at
`PROMPT.md` instead is no better — the prompt is consumed once at
bootstrap, while the templates are read later — so the only correct
target for a template's own explanation is the template.

| Template            | Becomes                                | Adoption default                              |
| ------------------- | -------------------------------------- | --------------------------------------------- |
| `orient.md`         | `.claude/skills/orient/SKILL.md`       | step 002 — session-start ritual               |
| `resume-step.md`    | `.claude/skills/resume-step/SKILL.md`  | step 002 — post-interruption verification     |
| `handover-step.md`  | `.claude/skills/handover-step/SKILL.md`| step 002 — pre-test handover ritual           |
| `approve-step.md`   | `.claude/skills/approve-step/SKILL.md` | step 002 — post-approval close ritual         |
| `step-reviewer.md`  | `.claude/agents/step-reviewer.md`      | step 002 — runs before every handover         |
| `optimize-memory.md`| `.claude/agents/optimize-memory.md`    | step 002 where the plan has milestones        |
| `state-reviewer.md` | `.claude/agents/state-reviewer.md`     | step 002 where the plan has milestones        |
| `code-reviewer.md`  | `.claude/agents/code-reviewer.md`      | conditional — when there is code to review    |
| `test-reviewer.md`  | `.claude/agents/test-reviewer.md`      | conditional — when there is a suite to review |
| `bash_guard.py`     | `.claude/hooks/bash_guard.py`          | step 001 — the Bash permission guard          |

The defaults split on **trigger certainty, not on trigger arrival**. A
milestone close is a certainty the moment the plan groups steps under
milestones, and it needs two passes — the state review and the memory
compaction — so both agents are instantiated with the rituals rather than
at the boundary they serve; deferring them only guarantees that the first
milestone close improvises what it cannot find. `code-reviewer` and
`test-reviewer` are the genuinely conditional pair: each reviews something
the repository may never contain, and an agent reviewing code that does
not exist is unreviewed weight. `bash_guard.py` lands a step earlier than
the rest because the baseline it belongs to is step `001`'s whole subject.

Shared conventions the templates carry, worth preserving at instantiation:
skills carry `name` and `description` and nothing else — an `allowed-tools`
list restricts nothing (probed live under Claude Code 2.1.231: with a
read-only ritual active, a `Write` and a plain `ls` both succeeded), so it
reads like enforcement while enforcing nothing, and `disallowed-tools` is
worse, binding for the whole turn that invoked the skill without ever
prompting, which strands the rest of that turn with no way to write. A
skill's read-only discipline is therefore prose ("report and stop"), and
anything that must actually bind goes in `.claude/settings.json` or a hook
— where, on the same version, file-edit rules match `Edit(path)` and a
`Write(path)` rule never fires. Agents are the exception: their `tools:`
frontmatter does bind, and the templates keep it. Re-probe all of this
at instantiation rather than trusting this paragraph — it describes one
version, and the failure mode of every item here is silence.
Further: reviewer agents are read-only except for their own
report under the untracked `.claude/reviews/`; review reports **become a
plan of decisions for the user's approval — nothing is fixed straight from
a report**; `handover-step` (pre-test) and `approve-step` (post-approval)
are different moments and never merge; `approve-step`'s hard precondition
is the user's explicit approval in the exchange, never inference.

**No agent template pins a `model:`, and that is a rule, not an
omission.** The milestone passes — the state review and the memory
compaction — must not run on the model that wrote the work they judge,
and *that requirement is a relation*: no fixed value can state it, since
a pinned `fable` becomes same-model the day implementation moves to
`fable`. So the constraint lives where a relation can be evaluated — in
the ritual that spawns them, which passes the override at invocation —
and each of those two agents says in its body that the absence is
deliberate, because an agent without `model:` inherits the invoking
session's, which is exactly the outcome to avoid. Everything else here
buys a **cold context**, which any model gives, and may run on the
session's own. This was learned the expensive way: an earlier version
pinned `fable` on the two milestone passes but stated the reason as "the
strongest model available" — unmeasurable, so the implementing session
read the stated criterion, could not apply it, substituted one it could
(match the session's model), and pinned the implementing model on the
very passes that exist to be independent of it. State the criterion, not
a value that happens to satisfy it today.
