# Local operational lessons workflow

This document describes the optional private, ignored local store accepted by [ADR-004](adr/ADR-004-keep-operational-lessons-in-ignored-project-local-store.md). This is local operational guidance, not authorization to publish lesson contents. The store does not exist in a clean clone. Create `local-lessons/` locally when needed; never commit or publish its contents.

## Where knowledge belongs

- `local-lessons/`: sanitized, reusable, context-bound operational observations kept only on the local machine.
- `kb/research/`: reviewed public source captures/evidence; not canonical conclusions.
- `kb/wiki/`: public, provenance-linked synthesis.
- `docs/adr/`: durable architecture/public-contract rationale.
- `.agents/skills/`: repeatable executable agent procedures.
- `.search/` and `sources/`: ignored raw/ephemeral evidence or bulky/private inputs, not durable lesson indexes.

Do not duplicate a public KB conclusion or a skill; link/refer to it where useful. Lessons are not automatically promoted. Public promotion requires a separate privacy, provenance, relevance, and publication review.

## Capture and evidence labels

Search the local index and public KB for duplicates before capture. Use one `LL-NNNN-short-title.md` per lesson, with frontmatter fields: `id`, `title`, `category`, `evidence`, `created`, `updated`, `provenance`, `verification_context`, `review_status`, and `reviewed_for`. A generic template and index stub are provided below so a clean clone can initialize its local store. There is no schema validator; metadata, privacy, and links require manual review.

Labels describe evidence type/status and are not an ordinal confidence scale:

- `verified`: directly reproduced in the stated context.
- `measured`: a measurement with method and context.
- `reported`: attributed but not independently reproduced.
- `theory`: reasoned but unverified.
- `hypothesis`: an open question to test.

Never present theory/hypothesis as established or actionable fact. Preserve the label and provenance when reusing; do not silently upgrade evidence. Include symptom, finding, bounded safe procedure, limitations, and follow-up appropriate to the evidence. State tool/version/environment and date or explicitly say not independently verified.

## Privacy, search, review, lifecycle

Never record credentials, raw logs/captures, full serial/MAC identifiers, personal data, private network details, or binary/source dumps. Keep raw material in suitable ignored local evidence paths. `.gitignore` prevents ordinary accidental inclusion but not force-staging; inspect staged paths explicitly before commits/pushes and ensure no `local-lessons/` path is tracked.

Use the manually maintained local `index.md` to search by symptom/tool/device. The repository owner is accountable for maintenance; authors update entries/index. A second reviewer should check provenance, evidence label, privacy, duplication, links, and staleness before operational reuse. Recheck `reviewed_for` when source versions or context change. Mark stale/retired lessons with a reason and replacement link where applicable; retain provenance. Local text search is sufficient; this workflow adds no search dependency or QMD collection.

## Initialize a local store

From the repository root, create the ignored directory manually (`mkdir local-lessons` or platform equivalent). Create `local-lessons/README.md` and `local-lessons/index.md` by copying the generic starter contents below. Add lesson files only locally. Do not force-add or otherwise track files from this directory. No script, network access, or dependency is needed.

### `local-lessons/README.md` starter

```markdown
# Local operational lessons

Private local store; ignored by Git and not synchronized. Follow the tracked workflow at `docs/local-lessons-workflow.md`.

Use the lesson template there. Search `index.md` and public KB for duplicates before capture. Keep raw evidence elsewhere under appropriate ignored paths; never include secrets, raw logs, full device identifiers, personal data, private network details, or dumps. Owner is accountable for maintenance; authors update entries/index and a second reviewer checks evidence, privacy, duplicates, links, and staleness before operational reuse. Preserve evidence labels; do not silently upgrade them.
```

### `local-lessons/index.md` starter

```markdown
# Local lessons index (private; ignored)

Search by symptom, tool, or device before repeating diagnostics; also check public KB for duplicates. Owner is accountable; authors update this index when adding/changing/retiring entries. Record stale/retired status and reason; preserve provenance. See `../docs/local-lessons-workflow.md` for the template and review process.

| ID | Lesson | Evidence | Reviewed for | Status |
|---|---|---|---|---|
```

### Lesson file template

Copy this into `local-lessons/LL-NNNN-short-title.md` and replace every placeholder. `reviewed_for` identifies tested version/context after review; until then use `not reviewed` and `review_status: needs-review`.

```markdown
---
id: LL-NNNN
title: "Short descriptive title"
category: tooling-or-diagnostic
evidence: reported
created: YYYY-MM-DD
updated: YYYY-MM-DD
provenance:
  - "Issue, source URL, or sanitized observation source"
verification_context: "Tool/version/environment/date, or not independently verified"
review_status: needs-review
reviewed_for: "not reviewed"
---

## Symptom

[What prompted this lesson?]

## Finding

[What was observed? Preserve the evidence label; separate fact from inference.]

## Safe procedure

[Bounded steps, or state that no procedure is established.]

## Limitations and follow-up

[Context where this may not apply; what remains uncertain.]
```

Before reuse, a human reviewer checks metadata presence, provenance/context clarity, privacy exclusions, claim-label alignment, and local index/links. This is a manual gate, not machine-enforced validation. The optional ignored store is absent from clean clones by design; no local lesson is synchronized or implied to exist.
