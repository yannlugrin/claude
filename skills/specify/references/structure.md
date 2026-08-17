# Document doctrine

How a specification produced by this skill is structured and written. The
doctrine was distilled from a full spec-writing cycle that worked well; it is
the default for every project. Deviating from it — trimming sections for a
small project, adding structure for a large one — is allowed, but only as an
argued decision the user approves, logged like any other.

## Identity of the document

- A specification states **what must exist, under which constraints, and
  why**. It never prescribes implementation: no code, no file layouts, no
  task structure, no tool syntax, no module names.
- Its only reader is the implementer (an AI). Documents for any other
  audience — operator guides, contracts for externally produced artifacts,
  inventories — are **deliverables of the implementation**: the spec names
  them and states what they must cover, and does not write them.
- Written in English, in prose. Tables are reserved for two uses: field
  tables for declared data models, and decision tables for dangerous
  conditional behavior.

## The reading contract

The document opens with a `## How to read this document` section that
establishes three tiers. This preamble is the core mechanism — it tells the
implementer exactly where its freedom lives:

- **Requirements** — written as "must". Decisions already taken, not open for
  reconsideration during implementation. Where one exists because of a
  trade-off, the reasoning is given **so it can be evaluated rather than
  merely obeyed**.
- **Recommended defaults** — written as "should". Starting points the
  implementation may deviate from with reason. Ranges, thresholds and tool
  choices usually live here.
- **Constraints of the environment** — facts about providers, tools,
  protocols or products. Not decisions: stated, with the reason they matter,
  because discovering them mid-implementation is expensive. Facts are
  researched before being stated, never assumed.

The preamble also states the document's silent-failure principle: where the
document says something must **not** happen, it is usually because the
failure is silent — corrupted or lost state rather than a visible error.

## Canonical spine

Numbered sections, in this order. The middle sections are per-domain and vary
with the project; the frame around them does not.

1. **Goal** — what the platform or product is, for whom, in one screen. Ends
   with the sharpest scope statements ("it does X; it never does Y").
2. **Environment and context** — provider, existing systems, scale, budget
   class; the researched facts the design rests on.
3. **Core model** — the foundational decisions serialized with their
   reasoning: architecture pattern, main components, what talks to what. A
   reader must find here the *why* of every structural choice.
4. *Per-domain requirement sections* — data model (field tables with
   per-field purpose), lifecycle and operations, monitoring, security and
   access, backup and restore… whatever the project needs. Cross-cutting
   concerns get their own sections rather than being scattered.
5. **Future Considerations** (penultimate) — not required now, but **must not
   be architecturally precluded**. Each item argues why deferring is safe:
   what adopting it later costs compared to adopting it now. An item whose
   later adoption would be expensive is not a future consideration — it is a
   present decision in disguise.
6. **Non-Goals** (last) — conscious renunciations, each with its reason and
   its blast radius ("X is an accepted single point of failure; while it is
   down, A and B stop and C continues"). This section is what makes accepted
   risks a choice instead of an oversight, and it is the first defense
   against scope creep.

## Open facts

Some facts cannot be researched before implementation. Not because nobody
looked, but because the answer lives in the artifact itself: whether a
product's interface behaves as documented, what a tool actually writes
where, whether a mechanism the design rests on exists at all in the
version that ships. Search, vendor documentation and the user's own
knowledge all end at "not known yet", and the specification must not
guess — a guessed fact reads exactly like a researched one.

Write these as **open facts**: a list, one lettered item each, in the
section holding the domain's facts. An item states three things.

- **The question, in observable terms** — what would be looked at to
  settle it, not a topic ("whether the server's stop command answers on
  a non-interactive pipe", not "console behavior").
- **What rests on it** — the requirement, tier or mechanism that changes
  if the answer is unfavourable. This is what makes the item load-bearing
  rather than curiosity.
- **The pre-committed response** — what the implementation does under
  each outcome, decided *now*, by the user, with the reasoning. Up to
  and including "under this combination the deliverable must not ship",
  and including the honest degraded case ("ships with a documented
  limitation, whose blind spot is stated plainly").

The device earns its place by moving the arbitration forward. Without it,
the implementer meets the fact mid-step and either guesses or returns
with a question nobody has ruled on — at the point where the cost of
either is highest. With it, the discovery is expected and the response
is already the user's decision.

Two rules keep it honest. An item with no pre-committed response is not
an open fact, it is a gap with a label on it. And an item whose
unfavourable outcome nobody has costed is a blocking risk in disguise —
cost it, or settle the fact before the document is finalized.

Resolutions run through the implementation's spec-amendment channel:
the specification is amended so its facts stay true, and the
user-facing consequence lands in the deliverable documentation. How much
of that the implementer may do alone is decided at handoff
(`handoff.md`, `{{OPEN_FACTS}}`), not here.

## Multi-document specifications

The default is one document. A monorepo is the case that breaks it:
several deliverables sharing conventions, where per-deliverable sections
grow with every addition while the conventions stay stable, and where
the implementer works inside one component's directory at a time. The
split is a structure deviation like any other — argued, approved,
logged — and it works like this:

- The **root document** keeps the goal, the environment facts, the core
  model and the shared conventions, plus one section stating what every
  per-component document must cover.
- Each **per-component document** lives in that component's directory,
  named identically (`<component>/SPECIFICATIONS.md`). It inherits the
  root's reading contract unchanged and may never weaken a root "must".
- A component with nothing of its own still gets the file, as a pointer
  to the root section that specifies it — the layout stays uniform, and
  a missing file never has to be interpreted.
- **The component list is the list of things the repository ships**, and
  the section defining the per-component document says so in those terms.
  Naming the class after the interesting majority — *per-game*,
  *per-service*, *per-plugin* — silently excludes every shipped
  deliverable that is not one, and the excluded one is typically the
  shared or foundational component everything else builds on. Measured: a
  repository of game images plus the builder image they all build from
  titled its section "Per-game specifications"; the builder, specified in
  a root section, got no document — and therefore no directory and no
  owner — a gap nothing downstream could see, because the handoff derives
  its component list from the documents that exist. The finalization
  consistency sweep checks the class name against the full deliverable
  list, and a deliverable outside the name is either given a document or
  given a written reason.
- **Cross-references need one convention, stated in each per-component
  preamble:** `§N` is local, `root §N` points at the root document. The
  consistency pass then covers every document, and every reference in
  every direction must resolve.

Everything downstream inherits the split — review context blocks name
all the documents, and the implementation handoff grows tracks
(`handoff.md`, "Monorepo and multi-track projects"). Weigh that before
choosing it for a project that does not need it.

## Numbering and cross-references

- Sections are numbered (`## 7. Game Instances`, `### 7.2 Configuration`) and
  referenced as `§7.2` wherever one section depends on another.
- Numbers are stable: once external reviews have started, new content takes
  the next free number or a new subsection; renumbering is a last resort and
  requires a full cross-reference sweep in the same edit.
- Every edit round ends with a check that all references resolve and that
  terminology stays uniform (one name per concept, everywhere).

## Writing rules

- **Reasoning is part of the requirement.** Every non-obvious must carries
  its why; every rejection explains the failure mechanism, not just the
  verdict. This is what lets a reviewer attack the reasoning instead of
  guessing at it.
- **Hunt silent failures.** The most valuable passages are concrete failure
  narratives: what sequence of ordinary events leads to lost state without an
  error. Where behavior branches dangerously, use a decision table and make
  the safe branch fail loudly rather than proceed plausibly.
- **Precision proportional to risk.** Stay high-altitude where any competent
  choice works; be intransigent and specific exactly where a wrong guess is
  expensive or silent. Uniform precision is a smell — it buries the vital
  detail among trivia.
- **Honest scope edges.** Known blind spots and scope-of-protection limits
  are stated in place ("this mechanism cannot alert on its own death"). The
  document prefers admitting a limit over implying coverage it does not
  have.
- **Compact, never lossy.** Compression is welcome at finalization; the floor
  is comprehension — nothing is removed that a requirement needs in order to
  be understood.
