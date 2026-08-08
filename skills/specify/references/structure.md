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
