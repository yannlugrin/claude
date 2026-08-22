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
memory. **Five are exempt by construction**, and raising them as
findings against a finalized specification is the mistake this sentence
otherwise invites: `{{BOUNDARY}}`, `{{CODE_REVIEW}}` and `{{TEST_GATE}}`
are policy calls, `{{REFERENCES}}` and
`{{HOUSE_TOOLING}}` are the user's own context. None has a source in the
specification, all five are asked for in the batch, and not finding
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
   job. **YAML is present from step `000` in the default stack, and the
   slot must name it**: the hook runner's own configuration is the
   first artifact of any class this repository gets, with CI's workflow
   following at `003`. The one family guaranteed to exist from step one
   is the one an expected-instance list drawn from the product's own
   languages reliably omits. Fill the slot as a short bulleted list (it stands alone in the
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
     machinery around someone else's executable. **That pin is half a
     mechanism, and the other half is what bumps it** — not more
     coverage, the rest of the same decision. A version a human reads
     (`pre-commit==4.4.0`) may be bumped by a human. A digest a human
     cannot read — an action SHA, an image digest, a lock file — takes
     its automated bump (whatever the forge offers: Dependabot,
     Renovate) in the step that takes the pin, or the pin is not taken:
     an unbumped digest fails more quietly than the floating tag it
     replaced, turning a dependency that silently stays current into
     one that silently rots while looking more deliberate. Where the
     forge offers no bot, the pin still names its bump trigger, logged
     at the pin — the two halves land together either way. *Ships*
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

   One family is standing whatever the stack, and the slot names it:
   **Python, for `bash_guard.py`** — the repository ships it from step
   `001` on, whichever language the entrypoints and tooling turn out to
   be, so a slot written around the entrypoint language leaves the most
   load-bearing file in the tree covered only by the catch-all above.
   A second family is standing for a different reason: **repository
   hygiene and secret detection**, present from step `000`. It is not
   indexed on an artifact class — trailing whitespace, missing final
   newlines, mixed line endings, merge-conflict markers, accidental
   large files, case collisions, broken symlinks, shebang-and-executable
   disagreement, and above all a committed key or credential are
   file-type-agnostic and apply from the first commit. Say so in the
   slot, and say that **the never-ahead rule does not reach it**: that
   rule governs per-artifact-class families, and an implementer holding
   it beside rule 11's build-at-the-moment-of-need has a
   doctrine-shaped reason to defer the one family that has nothing to
   wait for. This is the boring standard tool by construction — the
   stock hook collection of whichever runner `{{HOUSE_TOOLING}}` names,
   pinned in one place, no code written — so rule 11 argues for it
   rather than against. One split the slot decides rather than leaves
   open: the **fixers** (whitespace, final newline, line endings)
   belong to the commit hook, while *check* asserts rather than
   repairs. A hook that rewrites the working tree as a side effect of
   answering "is what is committed here well-formed?" is the
   `git add --intent-to-add` prohibition of rule 2 one step milder, and
   the rituals that read `git status --porcelain` for a clean tree are
   downstream of both. **The fixers carry the vendored file's exemption
   with them**, for the same reason the Python family carries it: a
   vendored file is never reflowed, and a whitespace or final-newline
   fixer reflows it exactly as a formatter would. Excluding it from the
   linters and leaving it inside the fixers protects nothing.

   Back to the guard's own family:
   carry its own exemptions forward with it as known configuration
   items of step `001`, and there are two, not one: a **lint-width**
   exemption **and** a **formatter exclusion** — a vendored file is
   never reflowed, and where the runner passes filenames explicitly
   (`pre-commit` does), the formatter needs its `force-exclude` wrinkle
   on top. The docstring names the rules and the path; a slot that says
   "width exemption" leaves the format run to reflow the file on its
   first pass.
5. `{{IGNORE_ITEMS}}` — what this stack and project leak into the working
   tree that must never be committed (credential files, local environment
   files, tool caches). The fixed text already carries the three that
   hold in every project: `CLAUDE.local.md`, `.claude/reviews/` and
   `.claude/worktrees/`.
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
    decision to ship comes back to the user before the amendment.
    **Say which clause wins where both apply, and it is the escalation
    list**: a specification that pre-commits a response fixes what will
    happen, not who watches it land, so a pre-committed branch that
    changes a tier, a limitation or a documented capability still comes
    back. Unstated, this is the collision two reasonable implementers
    resolve in opposite directions, on the project's most consequential
    items. Name the ones that always come back — the ones whose
    unfavourable outcome carries a tier or ship consequence — rather
    than leaving the criterion to be applied item by item. Also state where the
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

    **Naming a task runner obliges its companion invariant, and the
    prompt carries it: no recipe ever performs an act the boundary
    gates.** A `PreToolUse` guard judges the command it is given — it
    sees `just release` or `make publish`, never the `docker push`
    inside the recipe — and no permission rule reaches inside one
    either, so a gated act behind a recipe name bypasses the gate
    unseen. The alternative, gating the runner itself, prompts on
    every `just check` and destroys the development loop the boundary's
    free side exists to protect. Gated acts live in CI, or in a command
    the user invokes directly. This holds for any runner that turns a
    name into commands (`make`, `npm run`, `task`), not only for
    `just`, and the step that builds the permission baseline records it
    as a rule of that baseline.
14. `{{CODE_REVIEW}}` — **how much review the code itself gets, and a
    policy call like the boundary; ask it in the batch.** Two questions
    in one: is a cold code review a *standing* gate on every
    code-bearing step, or spawned on request when the implementer
    judges it worth it — and where it is standing, which **foci** does
    it carry? Recommend standing wherever the project ships code that
    runs in somebody else's environment, and read the foci off the
    specification's own risk statements rather than inventing them:
    permission-path code wants security, anything with a stated latency
    budget wants performance, and code quality is the one that travels.
    The answer decides four places at once — rule 2's text, step
    `002`'s adoption list, the `handover-step` sequence that carries
    the gate past bootstrap, and whether `code-reviewer` and
    `test-reviewer` are conditional adoptions at all — which is why it
    belongs in the batch rather than in the implementer's latitude.
    Ask the test half separately: a suite-bearing step is not the same
    trigger as a code-bearing one, and a project may want the first
    without the second — unless `{{TEST_GATE}}` below is answered on,
    which settles that half rather than leaving it open. Measured: a run that left this to the
    implementer had the operator volunteer it after the batch was
    ruled, and it then took four review rounds to integrate — one to
    find it had no carrier past bootstrap, two more to stop the
    test-review clause reading as a deferral. Asked up front it is one
    decision; asked late it is a rewrite of the four places above.
15. `{{TEST_GATE}}` — **whether a step's behaviour is pinned by its cases
    before it is implemented, and on which steps; a policy call like the
    boundary, asked in the batch.** Where the gate is on, a gated step's
    cases are written, committed and approved *before* its implementation
    exists, so that step has two gates rather than one. Where it is off,
    nothing else in the template changes and the slot renders empty.

    **Scope by contract, not by how well specified the step is.** The
    criterion is whether the step creates something later work depends
    on — an API, a CLI surface, a file format, an output stream, a wire
    shape. Where it does, the gate earns its place whether or not the
    specification fixes that contract, and it earns most where the
    specification deliberately left it open. Where it does not — packaging,
    a README, a measurement pass — cases are ceremony however well
    specified the step is, and **a gate that gets rubber-stamped teaches
    the next one to be**. Propose the criterion and the classification it
    produces together: the plan then carries the answer per step, so "is
    this step gated?" is settled once at planning time instead of becoming
    a question at the start of every step.

    **A case has two possible sources, and they are not the same act.**
    *Transcribed* — the specification fixes the behaviour and the case
    restates it, citing the section. *Decided* — the specification left it
    open and the case **is** the decision, fixing the surface before
    anything is built on it. The second is not the lesser case; it is the
    reason to run a gate on a project whose specification does not define
    everything. The alternative to a decided case is not the absence of a
    decision — it is a decision made silently by the implementation and
    met at handover as a fait accompli, where the user must overrule a
    defence rather than choose between options. So a decided case takes
    the route any decision takes: within latitude, logged under rule 4;
    the user's call, asked before the gate closes. **A case that decides
    is not a defect. A case that decides while presenting itself as
    required is.**

    **Approved cases are frozen, and the freeze names an act rather than
    an operation.** Changing or deleting an approved case retracts what
    the user approved, and comes back to them as a change; **adding** a
    case during implementation is free, since it retracts nothing. But
    narrowing, contradicting or carving an exception out of an approved
    case **is a change whatever operation performs it** — a new case
    reading "…except with this flag" has amended an approved one without
    editing it, and without this sentence the addition allowance is a
    documented bypass. Freezing is not detachable from the gate: without
    it, tests-first degrades into writing the tests twice, and the
    contract the gate fixed is renegotiated by whatever the implementation
    found convenient.

    The transcribed/decided fork governs those additions too, and settles
    three questions with one distinction. Apply it at both moments:

    |                  | decides nothing              | decides something         |
    | ---------------- | ---------------------------- | ------------------------- |
    | Approval         | autonomous                   | logged, or asked          |
    | Reviewed against | the specification            | its declaration and the log |
    | Red before green | no — a regression case is green by nature | yes, as at the gate |

    **The gate's test is the red run, not the reading of the case file.**
    Say so in rule 2 where the gate lands, because the gate otherwise
    contradicts that rule's strongest sentence — what the user tests is
    behaviour, never a document. At the gate the check half is green (the
    cases are code and are held to it) while the test half is **red**,
    failing on the new cases and on nothing else, its output quoted in the
    handover with each failure traced to the assertion it comes from: an
    import error, a fixture typo and a suite that never ran are all red,
    and none of them is a case.

    **The handover names what the cases pin, what they deliberately leave
    open, and what is not covered.** That reads like coverage honesty and
    is in fact the main safeguard against this gate's own failure mode,
    **over-specification by test**: a case written before the code can pin
    an exact error string, an internal call order or one plausible data
    shape among several, and frozen, those become requirements nobody
    chose and the freeze makes them expensive to undo.

    **A gated step needs a fifth status, and the plan's vocabulary gains
    it.** `awaiting test` names the state where the user owes the step a
    test; at the gate the user owes an approval of the cases instead, and
    reusing one name for both is the confusion this slot otherwise ships.
    Two costs, and the second is a trap: a session resuming mid-step
    cannot tell from the plan whether the cases or the implementation are
    on the table, and `approve-step` — whose precondition is a step in
    `awaiting test` — would close, compact and tag a step that has no
    implementation, on the strength of an approval that was only ever
    about its cases. So add **`awaiting case approval`**. The gated
    lifecycle is `pending` → `in progress` (cases) → `awaiting case
    approval` → `in progress` (implementation) → `awaiting test` →
    `done`, and the transition worth stating is the one that looks
    backwards: **approving the cases returns the step to `in progress`**,
    it does not advance it.

    **Answering this slot constrains `{{CODE_REVIEW}}`'s test half — they
    are one policy area, and belong in the batch together.** A gate
    freezes cases, and freezing unreviewed cases is worse than no gate: it
    makes a wrong contract immutable. So a gate obliges a cold review of
    the cases *at* the gate on every gated step, and `test-reviewer` stops
    being a conditional adoption. Presented separately, the batch will
    happily return "gate on, test review on request", which is the failure
    mode wearing the shape of an answer.

    Three consequences to carry, none of them visible at the moment the
    slot is answered:
    - **The gate commits a tree whose test half fails.** The known-good
      state is the tagged commit, not every commit, so a red mid-step
      commit breaks no invariant — but a project that pushes per commit,
      or whose CI runs on every push to a step's branch, turns the gate
      into a red CI run. Say where the red commit is allowed to live.
    - **The user approved one suite and will be handed another.** The
      implementation handover owes a diff against the approved set — what
      was added, and under which of the two headings — and the review at
      that handover is told to read it. That is where
      contradiction-by-addition is caught, or nowhere.
    - **A case that settles an open fact is that channel firing.** Where
      the specification ordered a fact settled during implementation and a
      gated step's case settles it, the case pins it, the user approves,
      and the amendment lands under rule 1 in the same commit. Say so, or
      two mechanisms resolve the same question at different moments with
      no rule for which goes first.

    The answer reaches rule 2's text, the plan's status vocabulary and
    per-step fields, three of the four rituals (`handover-step`'s
    sequence, `approve-step`'s precondition, `resume-step`'s
    mismatch rule), `test-reviewer`'s brief and `description`, and step
    `002`'s adoption list. Recommend the gate
    wherever the plan has contract-bearing steps at all. Its cost is a
    round-trip per gated step, paid by the user — but on the steps where
    the specification is least complete that is not new cost: those
    questions were going to be asked anyway, later, against code that had
    already answered them. Measured: one project adopted the gate
    mid-implementation, after a suite written *after* its code encoded the
    code's behaviour rather than the contract — the runner merged the
    output streams, so every assertion about which stream carried what
    passed either way, and only the operator's eye caught it. A case
    written from the specification first would have had to name the
    channel.

## Monorepo and multi-track projects

The template assumes one specification, one plan, one decision log, one
step-number namespace. That holds for most projects and should not be
abandoned lightly — but a monorepo breaks it, and the usual trigger is a
specification already split into a root document plus one per component
(`structure.md`, "Multi-document specifications"). When it applies, the
shape is **tracks**: the root track owns repository-wide work — its
charter is drawn below — and each component directory owns one track.

**Enumerate the tracks from what the repository ships, never from the
documents that happen to exist.** The split is what suggests tracks, but
it is not what defines them: a component the root document specifies
directly has no document of its own, and deriving the track list from the
document list makes it invisible — the very component that is shared or
foundational, and whose decisions the most people will later go looking
for. Walk the specification's deliverables instead; each one that owns —
or, on this reading, should own — a directory gets a track, and each one
that has no per-component document yet gets the pointer document
`structure.md` mandates (a finding against the specification, raised
under rule 1 before the plans are written, not a gap to route around).

Three rules govern the assignments, and the batch carries them:

- **Ownership follows artifacts, not blast radius.** The question is
  where a deliverable's files live, not how far its changes ripple. CI is
  root-owned because `.github/workflows/` is a root directory — not
  because a rebuild reaches every component; a component whose changes
  reach every other one is a component with many cross-track dependency
  edges, which is what those edges are for. Left unstated, this is
  decided by whichever criterion the session reaches for first, and
  "ripples widely" is the one that reads as most responsible.
- **The root track's charter is closed**: the foundation and harness, CI,
  shared documentation, and files at the repository root. Widening it —
  putting a shippable component on the root track — is a decision with a
  reason, logged, never a line transcribed into the track map. Measured:
  a bootstrap prompt added "the builder image" to that enumeration in
  passing, the implementing session transcribed it, and neither the plan
  nor the log carried a word of why; the reasoning had to be constructed
  after the fact, under challenge, by the session that had inherited it —
  which is late, since by then the operator has to overrule a defence
  rather than choose between options.
- **A milestone in the root plan named after a single deliverable is a
  track wearing a disguise.** It is the visible-on-sight tell, and it
  belongs in the batch as a check on the assignment the prompt proposes.

What changes, rule by rule — nothing else does:

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
  ("needs `step-sc-002` done"), never from a global sequence. **What a
  step's position used to guarantee, an edge must now state** — and the
  first of those is the foundation: every component track's first step
  names the foundation's last step as a dependency, or the whole track
  becomes startable as soon as the harness skeleton exists, before the
  permission baseline meant to be gating its work. Inside one plan, "the
  foundation comes first, before any project code" is enforced by
  ordering; split across plans it is enforced by nothing unless written.
  The failure is quiet in the worst way — the plans stay consistent,
  every reference resolves, and the only symptom is that the rule the
  plans state (position never sequences, only dependency lines do) has
  become true of a step nobody meant it to be true of. Watch for it
  wherever a step moves out of the root plan into a track: it arrives
  carrying only the dependencies that were worth writing down back when
  its position said the rest. One
  consequence must be restated rather than inherited: the template's
  "`git diff` between two tags is exactly one step's change" holds only
  where one namespace is one sequence. With tracks interleaved in a
  single history, a step's change is the range from the **previous
  `step-*` tag of any track** — the same tag rule 3's re-orientation
  finds — never from that track's own previous tag, which sweeps in
  every other track's steps that landed between the two. The compacted
  plan entry's `<previous step tag>` means that tag as well.
- **The first task** produces one plan and one log per track, plus the
  single `CLAUDE.md` and root `README.md`; the plans *together* must
  account for every section of every specification document. **The track
  map is its own logged decision**, not a clause of the entry adopting
  the workflow — the first task's item 2 states what that entry
  contains. The prompt proposes the map; the implementer re-derives it
  against the three rules above and logs what it concluded. A map transcribed without that entry is
  unanswerable later — the question "why is this here?" has no reader, and
  the session that inherited the answer no longer exists.
- **Every deliverable has an owning track as well as a location.** The
  location rule is the template's own, in the per-step shape; what
  tracks add is that a track's directory fixes it for the ordinary case,
  so only what lands *outside* the active track's directory has to name
  its path.
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
  reviewer reading the wrong track's plan reports nothing wrong. **That
  exception needs a carrier past bootstrap**, since the prompt is
  consumed once: name it in the list of what `CLAUDE.md` must hold and
  in the step `002` plan entry's content, not only here — stated only
  in the prompt, it survives just where the concise restatement happens
  to keep it, which is the one place nothing checks.

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
   same-commit staleness sweep — stated because the two rules would
   otherwise collide with no winner. The entry lands alone only when the amendment
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
   and what I should observe, (c) you waiting. **What I test is the
   system's behaviour, never a document.** "Read the record and confirm
   it is right" is not a test: it moves the step's verification onto my
   reading of prose you wrote, which is the one thing my gate exists to
   be independent of. A file appears in the test instructions only when
   the file *is* the deliverable — an operator document, a contract,
   something under `docs/` — never when it is your own memory under
   `.claude/docs/` (rule 3). Where a step's real product is a
   measurement, the test is re-running the measurement.
   You do not begin the next step until I explicitly say so.
   Fixes I request belong to the current
   step, not a new one. Never batch several steps because they look small.
   **When I ask for something to be removed, it is removed.** A smaller
   version of it, a rewritten version, a version moved elsewhere: none of
   those is compliance, and each costs a round to detect. If you believe
   the removal is a mistake, say so in one sentence and do it anyway —
   or ask, before acting, which of the two I meant.

   {{TEST_GATE}}

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
   they are the whole of what this rule requires. A small custom check is
   **sanctioned** here, and **the sanction covers the check's existence,
   never its size or its shape** — rule 2's put-it-to-me-before-it-is-built
   gate is not waived by it, so anything reaching past the parse question
   goes to me before it is written. Measured: a project read this
   paragraph as blanket pre-approval and shipped a hundred and seventy
   lines with an eighteen-case suite, against a plan line capping it at
   "a few".
   **Measure the ecosystem rather than inheriting this paragraph's
   answer.** `claude plugin validate --strict <dir>` is the tool to try
   first; on Claude Code 2.1.238 it flagged a missing `description` and
   passed silently — "Validation passed", exit zero — on both cases that
   matter here: a `name` disagreeing with the path the loader reads it
   from, and frontmatter that does not parse, which it skips without a
   word. The check earns its place on that measurement, and a version
   that closes the gap retires it, so re-measure before believing either
   half. Checking further —
   that a command, path or agent a file names actually resolves — is a
   *should*: worth doing where it is exact (an agent name against
   `.claude/agents/`, a path against the tree), and worth refusing where
   it is not. Scanning prose for backticked tokens and asserting each one
   resolves has been built and regretted: it is a false-positive machine
   that grows worse as the repository does, and once mandated by a rule
   it cannot be deleted without amending the rule.
   One more is exact enough to be worth doing, on the same *should*
   footing as its neighbours above and never as a new requirement —
   the sentence before this one is why, and it applies here too — once
   the repository has several `.claude/docs/` files: **a `§N` pointer
   checked against the target document's headings.** A citation naming the section *title*
   is checked exactly; a bare number can only be checked for existence,
   which is why the title is worth requiring in the one class where a
   pointer is followed by a session that will not re-read the target —
   the instantiated skills and agents. Measured: an off-by-one section
   pointer shipped in four ritual files on the day they were written,
   the numbering having shifted in the same commit. Two scope rules keep
   it honest: read-only documents stay outside it — a check that can go
   red inside a file nobody may edit is a check nobody can turn green —
   and it recognises one citation shape rather than parsing prose, which
   is the regretted machine above wearing a different hat.
   **Prose lint over the governance documents**, configured to them as
   they already are — `SPECIFICATIONS.md` is
   read-only under rule 1, so the lint bends to it and never the reverse,
   and excluding a document from a rule is a logged decision, not a quiet
   config line. A bend made for the specification is **scoped to that
   file**: the same finding raised anywhere else is fixed, not
   accommodated, and a rule relaxed globally to spare one read-only
   document quietly stops binding on every document that could have
   been corrected. And prove what each enforcement mechanism actually does
   in your version — one probe per mechanism, **run at the step that
   introduces that mechanism**: settings keys, permission patterns and
   the guard hook being reached at all at step `001`; an agent's
   `tools:` frontmatter, and whether `CLAUDE.md` reaches a subagent's
   context at all, at step `002` — one exchange with the first agent
   that step spawns ("quote rule 9's opening line" — never the
   bootstrap cold reviewer, whose context must stay confined to the
   specification and your four files), and every reviewer agent's
   boundary rests on it. Its pre-committed unfavorable branch: if
   `CLAUDE.md` does not reach a subagent's context, each agent's body
   carries the gated set inlined — a logged decision naming the
   single-source-of-truth cost — never a citation to a rule the agent
   cannot read; `.claude/rules/` loading at
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
   files included and gitignored paths excluded, with the standing
   exceptions this prompt decides now — keyed on the path, not on
   tracked status:
   everything under `.claude/spec-work/`, because
   rule 1 makes that directory no session's reading material, and —
   where `{{REFERENCES}}` filled it — everything under `.claude/refs/`,
   because it is the user's supplied material, read-only under rule 3
   and owned elsewhere, not this repository's product to lint. Without
   that second exclusion a lint finding inside a reference has no legal
   resolution: the file cannot be edited, and the bend-the-config
   escape beside it is written for the specification alone. Drop the
   clause where the project has no references, rather than naming a
   directory that will not exist) and
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
   running both, **check before test**. **The mechanism behind those commands is configured,
   not written** — rule 11 applied to the harness itself. Use what I
   already use: {{HOUSE_TOOLING}}. Where I have no preference, take the
   standard tool of the ecosystem; where nothing standard fits, the
   runner, installer or test driver you write is a decision logged with
   the alternatives you rejected and put to me *before* it is built.
   Whatever the mechanism: documented, kept green, and runnable by me
   too. **A check that runs on the real tree ahead of every test run
   does not also need a test suite.** *Verify* runs *check* first, so
   everything in that half is executed against the repository itself on
   every invocation; a suite re-proving it afterwards is a regression
   harness for scaffolding, and it arrives with the fixture roots, root
   arguments and deliberately-malformed trees that exist only to feed
   it. Test what the project ships, not what watches over it. A fast form
   of *check* narrowed to what changed is legitimate mid-step; the commit
   that receives a `step-NNN` tag runs the full one — that commit is the
   state every later session treats as known-good. {{CODE_REVIEW}}
   My gate exists to
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
   lines, treated as a hard budget that yields to the **whole-carry
   blocks** and nothing else: rule 9's boundary enumeration always, plus
   any further block this prompt marks as carried whole — safety text a
   project adds for its own reasons is safety text on the same footing.
   They are carried entire and the trimming happens elsewhere. Say how
   many there are rather than writing "exactly one thing": a project
   that adds a second leaves that sentence contradicting its own rules,
   and the agent that compacts this file reads it. **It is written with headroom** — around 180 lines
   when you first hand it over, not 219. A file at its cap forces the
   next session that must add one pointer to reflow the whole document
   before it can do its own work, and a budget check that warns from the
   day it is written teaches you to ignore it. **The headroom belongs to
   the number, not to those two numbers**: every budget this project ever
   holds — the baseline, one derived at the first task, one re-derived
   later because a doctrine change added lines — lands with room left
   against itself. A budget re-derived to exactly the length of the file
   that prompted the re-derivation has recorded that file rather than
   budgeted it, and the next session pays the compaction the
   re-derivation declined. When the budget binds,
   things leave in this order, and the order is not yours to reshuffle:
   first anything context-specific that a read-trigger can reach
   (`.claude/docs/`), then the temporary tooling-templates block once
   its directory is gone, then per-step detail the plan already
   carries — and, where the repository has tracks, per-track detail its
   own plan carries. No whole-carry block ever leaves, and neither
   does the current-step pointer. If the rules still cannot be restated
   inside the headroom after that, that is a finding to raise with me,
   not a file to pack — and one legitimate outcome of raising it is a
   budget of this project's own, logged as a deviation with what makes
   it necessary. A repository whose boundary enumeration is long, or
   which has many source-of-truth directories to name, or which carries
   a track map, has a higher floor than these numbers assume — so where
   you can already see that at the first task, **derive the budget then
   and log it** rather than landing over the cap and deviating
   afterwards: the numbers here are a single-track baseline, and a
   budget first met by breaching it teaches the next session that the
   budget is decorative. What must not happen is the floor being met by
   deleting something with nowhere else to go. It holds only what applies always —
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
   **A `.claude/docs/` file is a conditional segment of `CLAUDE.md`** —
   loaded at its trigger instead of on every run, and held to the same
   test: what a future session needs in order to *act*, and cannot get
   faster from a rule, a docstring or a command it can run. Two things
   are therefore never in one. **Justification** — why a decision was
   taken is `DECISIONS.md`, why a rule exists is the rule; a memory file
   that argues its own contents spends a future session's context on a
   debate that session is not having. **Duplication** — a second copy of
   what `CLAUDE.md`, the specification, the plan or a docstring already
   says is a copy that goes stale in silence, because nothing checks it
   against its original. And none of it is written for me: it is your
   memory, not a report, and no gate of mine is satisfied by reading one
   (rule 2).
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
   never edited into my document.
   **Read-only also means it does not flow the other way**: what you
   take from a reference is its shape, never its text. Shape is a
   decision you could have reached yourself — two parallel jobs, a
   cache keyed on the file that decides its contents; text is the
   sentence explaining the decision, whatever its subject. That
   boundary is invisible while writing, because prose read an hour ago
   comes back as fluent recall, so it is not a matter of judgement but
   a step: **read the reference, close it, write the artifact without
   it open, and before committing compare the two — any sentence they
   share is text and comes out.** Shape survives paraphrase; text is
   what you would have had to quote. This matters beyond style: a
   reference is someone else's material, and step `003` may well have
   ruled it stripped from what the repository publishes — prose
   surviving in a shipped file defeats that ruling silently.
   {{REFERENCES}}
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
   instantiation — **a general rule, not one file's exemption** — is
   seeded from the specification's own vocabulary and kept current under
   rule 6 as the system materializes. The standing examples: the state
   reviewer's architecture vocabulary and inspection commands, and
   `resume-step`'s world-state checks, both in a repository where
   nothing is built yet. "Fill every placeholder with real
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
   justifies waiting, and `{{CODE_REVIEW}}` decides whether the review
   pair has one: where that slot leaves the review on request, an agent
   that reviews code, or tests, in a repository that has neither yet is
   the standing example of waiting; where it makes the review a standing
   gate, both are certainties like the rituals and wait for nothing. Once none remains un-instantiated
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
   placeholders in anything committed. **This rule gets a mechanism,
   not only your care:** key and credential detection runs in the
   commit hooks from step `000`, with the repository-hygiene family of
   rule 2. A must with nothing enforcing it is the guard on paper that
   step `001` warns about — and this is the one rule here whose breach
   cannot be undone by noticing it afterwards, since a committed secret
   is a rotated secret.

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
   Where no remote exists yet, say so in the close summary instead of
   attempting anything.
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
   it in that exchange, never on your own initiative — with rule 6's
   step-close push attempt as the one standing exception, named here
   because this enumeration is carried whole into `CLAUDE.md`, and a
   faithful carry that omits it lands two rules that contradict each
   other — a boundary the
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
      **This applies to things that are separable.** Before deferring
      half of a mechanism, ask what the shipped half does alone: if it
      is worse than what preceded it, the two halves are one decision
      and both land now. Deferring the half with the worse failure mode
      is not proportion, and it arrives wearing this rule's words.
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

Produce four files and have them cold-reviewed as this section's closing
paragraphs order; only then stop for my review. (This first task is
deliberately one ungated unit, unlike the foundation it plans: its
output is text a correction rewrites cheaply, and its cold review is
rule 2's self-verification before handover — the session has no harness
yet — not a step gate.)

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
       `.claude/worktrees/`, which the specification phase already
       ignores and which stays ignored — an isolated worktree
       materializes inside the repository, and a commit made while one
       exists swallows the checkout, which has happened; you are
       rewriting this file, so carry forward what is in it rather than
       replacing it from this list;
       `CLAUDE.local.md`); pinned base dependencies installable through
       one documented setup command; the check/test/verify harness of
       rule 2, built on the tools named there rather than on anything of
       your own — the harness *skeleton* and entry points, carrying at
       `000` only the families whose artifacts already exist (the
       governance documents and whatever else this step itself lands):
       the rest join with their first artifact, per rule 2's
       never-ahead rule, so this step's green gate says nothing about
       files that are not there;
       **`check` in both of rule 2's scopes from the start** —
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
       docstring in full, and edit only its `REGISTRY` and `CASES`
       blocks — the two named together because they are the pair the
       docstring obliges and they do not sit together in the file.
       That docstring
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
       allow per *rule- or grant-bearing* tool — never for the shell
       wrapper layer, because a broad allow on a command-runner is a
       broad allow on everything it runs the moment the guard is dead,
       and never for a tool registered deny-everything, whose broad
       allow buys nothing while the guard lives and is pure liability
       when it dies — no `ask` rule for anything the guard
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
       expressed is the *tier* — and the tier splits on
       recoverability. The **ordinary** push asks and is never denied:
       a denied pattern cannot be approved in the very exchange rule 9
       relies on, and that push is the one rule 6's close ritual
       attempts. The **unrecoverable spellings** — force, mirror and
       ref deletion, however written — are denied, which is not an
       exception to that claim but its boundary: the guard's own `GIT`
       ground rules already deny them, and a doctrine asserting that
       every push merely asks would be weakening ground rules it
       forbids weakening two paragraphs earlier. State the split, or
       the unscoped sentence collides with the guard shipped beside
       it. `deny` stays reserved for what has no authorised use at all,
       each named in the proposal.
       **And the boundary protects its own files:** native file-tool
       rules at the **ask** tier gating edits to
       `.claude/settings.json` and `.claude/hooks/`, landed inside this
       same proposal. Ask, not deny: a deny would end the guard's own
       maintenance channel, and the baseline's own evolution, with no
       unlock path. Under a mode that auto-accepts file edits, one
       silent, well-formed settings edit that drops the push gate turns
       the close ritual's standing push attempt into an unprompted
       publish — and the governance family's parse and hook-path checks
       catch malformation, never a well-formed loosening.
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
       probes for this step's mechanisms run here — and settings and
       hook changes may be picked up only at session start, so a probe
       run in the session that made the edit can report a false "not
       enforced": the probe method includes the restart, and the
       recorded re-measure recipe says so. Their results land
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
       runs.
       **That record is rule 3's memory and carries the three fields
       only.** Why a probe was worth running, what rule 9 gates, what
       the guard's own docstring explains: each already has a home, and
       a restatement here is the duplication rule 3 forbids — measured,
       a record written as a proof reached eight hundred lines and was
       cut to two hundred with nothing lost. And **I test the
       mechanisms, not the record**: the liveness triple is this step's
       manual test, per rule 2.
       Report in the
       step summary what each mechanism actually did, including the
       ones that turned out to enforce nothing. Name the permission
       mode you expect me to work in — it is a committed setting, not
       only a per-session choice, and it decides how much the rest has
       to carry. (`permissions.defaultMode` is the key at the time of
       writing: illustration, verified by the same probe as the mode
       list. A settings key is a version-stamped fact exactly as a mode
       name is, and this paragraph renounces asserting those two
       sentences later.) **This prompt names
       no modes and asserts no mode behavior — deliberately**: the
       mode set and what each mode does to an unmatched command are
       properties of the installed version (illustration only, to be
       re-derived from the running version: modes exist that prompt,
       that auto-approve, and that judge by classifier and can deny
       outright — three different answers to what backs the guard's
       silence), so take the list from the running version and **probe
       the mode you propose**: what an unmatched command does under
       it, and **whether a hook `ask` still prompts** — recorded
       like the rest: the close ritual attempts its push in reliance on
       it, and a gate that has stopped gating says nothing about it.
       Set the mode rather than working
       around it — if, for illustration, a mode auto-accepts file
       edits, that is what removes
       the need for a blanket
       `Edit(/**)` allowance — and let it decide whether the
       mode-disabling keys belong in the baseline at all. A mid-step
       session restart is expected here — the probes are trustworthy
       only after one — so the step's test instructions say where the
       restart falls. Its test: my
       review of the proposal, the
       probe results, and `--selftest` green.
     - **`002` — the workflow tooling**, instantiated from
       `.claude/spec-work/handoff/assets/` per rule 3: `orient`,
       `resume-step`, `handover-step`, `approve-step`, the
       `step-reviewer` agent, and the agents whose trigger is a
       certainty of this plan (a milestone close needs its state review
       and its memory compaction to exist before it arrives, not to be
       improvised at the boundary — and the certainty rests on the
       foundation milestone this prompt itself declares, never on a
       later grouping the plan is still free to decline). A recovery ritual created during the
       crisis it is needed for is too late. Propose the conditionally
       triggered rest only when their trigger exists — and an
       instantiated file must never name a skill or agent you did not
       adopt: trim the reference or adopt it, because a dangling name is
       a ritual that silently skips a step. One carve-out: a name that
       sits on `CLAUDE.md`'s not-yet-adopted list is not dangling — it
       is the documented fallback the milestone ritual relies on. Its
       test: I invoke each ritual and see it do what it claims — real
       invocations for the session-start, resume and handover rituals,
       while the close ritual proves itself at this very step's close
       (its trigger is any step approval, and `002`'s is the first
       after it exists); and for the agents whose only true trigger
       arrives with the milestone close, a smoke test (spawn, report
       shape, the model-override plumbing), their real proof deferred
       to that close with the step's test instructions saying so. A
       test that waits on a trigger the step cannot fire is not a test.
       Note that a new skill or agent may only be picked up at session
       start, so say whether a restart is part of the test.
     - **`003` — the same harness on the forge**, and the step that
       finishes the bootstrap. The workflow **reuses `000`'s entry
       points** rather than restating a single check — CI and the local
       runners must never be able to disagree about what "green" means
       — splits check and test into separate jobs once both exist,
       caches the toolchain, and keeps a way of proving a fresh setup
       still works — riding a scheduled workflow the specification
       already requires, where it requires one, rather than becoming a
       second; where it requires none, this rides the CI triggers that
       already exist, and a scheduled workflow of its own is built only
       if a real need appears, as a logged decision. Naming a schedule
       the specification never asked for invents a requirement, and
       sets the first task's two reviewers up to contradict each other.
       Ask me which forge the repository will live on if the
       specification does not settle it.
       **The workflow's own third-party steps are pinned by digest, and
       the pin brings its bump bot into this same step** — the general
       rule is in the check-family clause above, and this is where it
       bites: a forge's actions are published behind mutable major
       tags, so what CI ran is recorded by no diff in the repository,
       and a SHA that nothing bumps rots instead. Take both halves or
       neither. **A bump bot is also a CI producer**, which is the
       third part of the same mechanism: it opens pull requests and
       force-pushes their branches as it rebases them, so superseded
       runs stop being a hypothetical the moment it exists, and the
       workflow bounds them — queued runs per ref collapse to the
       latest, **except on the branch whose green run is the record
       that an approved step passed**, which is never cancelled. That
       split is the part to state; a bound that cancels the step-close
       run destroys the evidence rule 6 closes on, which is worse than
       no bound at all. State it as behaviour and take the spelling
       from the forge you run (GitHub's `concurrency:` key at the time
       of writing — illustration, like every version-stamped fact
       here). And note *why* it lands now rather than earlier: without
       the bot, a single-operator repository whose pushes are approved
       steps supersedes almost nothing, and a bound written ahead of
       the bot is rule 11's anticipation. The bot is what dates the
       need. This is the one foundation step
       nothing local can exercise, so **its gate is a real run**: name
       the forge, the remote and my authorisation of the first push as
       external prerequisites needed *at bootstrap* — not late, which is
       where a cost-ordered plan would put them — and treat the workflow
       as unverified until I authorise that push and the run comes back
       green. One deliverable is a decision, not an artifact: what of
       `.claude/` goes public with the repository, decided before the
       first push it becomes irreversible at, logged and put to me.
       **Two directories, ruled separately, because they are not the
       same question.** `.claude/spec-work/` is the specification
       phase's history, its review reports and any template still
       sitting in it — nobody's reading material under rule 1, so
       publishing it is a choice about transparency. `.claude/refs/` is
       *my* supplied material, whose authority lives elsewhere: some of
       it may be nobody's business outside this machine, and some of it
       is the project's own yardstick that later steps still consume,
       which a blanket strip would delete out from under them. A single
       ruling covering both reliably gets one of them wrong.
       Its test: I authorise the push and watch the run.
     Nothing here is exempt from the small-step rule. If one of the
     four is still too big for a single test — or cut in the wrong
     place for this project — say so, and split it further in the plan
     you present; the cold review below is invited to find exactly that.
     And the four foundation entries carry this prompt's per-step
     prescriptions **in full** — the guard instantiation and its
     registry discipline, the settings-tier traps (`ask` cancels every
     carve-out, the deny backstop, the push tier), the mode probing,
     the probe duties and their restart caveat, the baseline's
     self-protection rules, the CI reuse rule and its prerequisites,
     the publish-or-strip decision, the instantiation list — as their
     deliverables and test content:
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
     **how I test it** — an observation about the system's behaviour,
     never the reading of a document (rule 2), and stating, when the
     test crosses rule 9's boundary, that it does, what it costs, and
     how I clean up afterwards — and **status** (`pending` / `in progress` /
     `awaiting test` / `done`, plus `awaiting case approval` where
     `{{TEST_GATE}}` puts a gate on the plan).
     Where `{{TEST_GATE}}` puts a gate on this plan, each entry also says
     **whether the step is gated**, decided against that slot's contract
     criterion. State the criterion once in the plan's reading
     conventions and the answer per step in the entry: a step whose entry
     is silent still has an answer, and a criterion re-applied at the
     start of each step is the per-step question the gate was scoped to
     avoid.
     **Deliverables say where their files land** wherever the
     specification does not already fix it: a path no plan states is a
     path a later session invents at the moment it needs one, and two
     sessions invent differently. Naming the directory once per
     deliverable is enough — the files inside it need no enumeration.
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
   entry recording the adoption of this workflow. Where the repository
   has tracks, a second entry records the **track map** — every component
   considered, every deliverable the root track owns and why it is
   root-owned. The map this prompt proposes is a proposal: re-derive it
   from what the repository ships, and log what you concluded, including
   where you agreed with me. An assignment nobody wrote down is an
   assignment nobody can answer for later.
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
   shape and the tag-message shape — both fixed in rule 6 precisely so
   the early closes do not improvise them, and both needing a carrier
   here for two reasons that outlast each other: the first closes
   happen before step `002` instantiates any ritual, and that ritual,
   once it exists, **cites** these shapes rather than transcribing
   them, so something has to be what it cites. `CLAUDE.md` is that
   carrier — the open plan-entry form in full, the
   compacted-on-approval form and the tag-message shape stated
   completely enough to be pointed at — or the `.claude/docs/` file it
   points at, should the budget later evict them there, in which case
   the citation moves with them. And
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
   points to — and it lands **with headroom against the budget rule 3
   states**, not at its cap, so the next session that must add a pointer
   adds it instead of reflowing the file first. Do not restate the
   numbers here: rule 3 carries them and a project may derive its own,
   and a second copy is the drift U-050 already removed from the
   compaction agent. Two things the restatement
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
- **layout and ownership** — every deliverable has a location the plan
  states, and nothing the repository ships is left without one. Where the
  plan has tracks, every deliverable has an owning track too, and any the
  root track owns that is not a root-level or shared artifact carries the
  reason. This lens exists because the others cannot see its failure: a
  component with no directory and no owner passes coverage (its sections
  are mapped), ordering, granularity and consistency untouched, and
  surfaces only when someone builds it or, later, comes looking for its
  decisions;
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

Tell the reviewer which layer it is judging, or one of those lenses
fires on decisions I have already made. The foundation steps, the
harness, the tooling and the permission baseline are **prescribed by
this prompt**, and the reviewer cannot see that — so **premises** runs
over the project plan rather than the workflow layer, and **coverage**
maps the specification's sections. Every other lens keeps the whole
plan, **proportion included**: rule 11's founding measurement — six
hundred lines of bespoke runner where a standard tool already
existed — was itself a foundation-step failure, so a carve-out sparing
the foundation from proportion would spare it from the lens its own
evidence produced. A proportion finding against a prescribed step is
one the operator rejects in a sentence; not receiving it costs more.
Granularity above all, since "this step is too big
to judge in one gate" is a finding this review is explicitly invited to
return about the foundation itself.

One check the cold reviewer is structurally barred from — it may not
read this prompt — runs beside it: spawn a **second subagent,
deliberately not cold**, that reads this prompt in full — the ground
rules and the "Your first task" section — plus **all four files** you
have just written: the plan, `DECISIONS.md`, the `CLAUDE.md` and the
`README.md`. It reports
every kind of loss: every prescription the plan dropped or weakened —
the four foundation entries above all, but also the consumed-once
rest: the non-code-deliverable step contents, the
milestone-grouping-or-say-so requirement, the boundary-crossing cost
statements — and every ground rule `CLAUDE.md`'s restatement dropped,
weakened, or left citing a clause the file does not contain (item 3's
two observed failure modes included): `CLAUDE.md` is the rules' sole
carrier after this session, and the cold reviewer is structurally
barred from checking it — and item 4's prescriptions in `README.md`
(descriptive only, the For-reviewers frame two standing rituals read),
checked the same way; and item 2's in `DECISIONS.md`, which the cold
reviewer does not read either — a thin file at bootstrap, but its entry
format is the one every later entry copies, so a defect there is
inherited rather than noticed. It judges
transcription fidelity, nothing else — this prompt is consumed once,
and a dropped clause in the plan is invisible later, not wrong. Its
findings join the same triage.

Triage all findings — accept, reject with reason, or genuinely my
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
step 7) so the template is fixed at its source too. Each markdown template
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

**In a multi-track repository a governance placeholder is never
instantiated as one literal path**, and how it does resolve depends on who
reads the file. An **agent** starts from a fresh context holding only a
step id, so it carries a table: one row per track naming that track's
plan, log and specification, with the standing note that a component track
reads the root specification too. A **skill** executes in the invoking
session, which has just read the track map, so it says the plan, the log
and the specification mean the active track's and points at that map — a
second, third and fourth copy of the table would be drift surface bought
for nothing, and the map is what the copies would be copying. Either way
the active track comes from the track map and the `Current state` pointer,
or from the step id the invocation carries — and in the two milestone
passes, from the track named at spawn, per the close-ritual exception
above. Say this in the template headers rather than only here: "resolves
to the active track at invocation" is a property the instantiating session
has to turn into text, and the natural way to satisfy a single-valued
placeholder is to pick one path, which is exactly the silent failure the
placeholders exist to prevent.

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
`test-reviewer` are the pair whose default `{{CODE_REVIEW}}` decides:
where that slot makes the review a standing gate they are certainties
like the rituals, adopted at `002` and carried by `handover-step`;
where it leaves the review on request they are genuinely conditional,
since each then reviews something the repository may never contain and
an agent reviewing code that does not exist is unreviewed weight. The
table's "conditional" is the on-request default, not a fixed property —
and the two halves answer separately, since a suite is a later
certainty than code in most plans. Where `{{TEST_GATE}}` puts a gate on
the plan, `test-reviewer` stops being conditional whatever that test half
would otherwise have said: the gate freezes cases, and cases frozen
without a cold review are a wrong contract made immutable. `handover-step`
is then run twice on a gated step, which its own template carries. `bash_guard.py` lands a step earlier than
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
frontmatter does bind, and the templates keep it — **but what it binds is
which tools exist, not what they can do.** An agent listing `Bash` can
write files however carefully the rest of the list is drawn, so a
reviewer's read-only discipline rests on its prose and not on its
frontmatter; only `tools: Read` alone makes writing mechanically
impossible, and then the agent needs another route to whatever `Bash`
was fetching. Stated because the true half invites the wrong conclusion:
a list that visibly omits `Write` and `Edit` reads as a sandbox, and one
project's probe had to establish the difference before its reviewers'
boundary could be described honestly. Re-probe all of this
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
