# Local operational lessons workflow (proposed)

This document describes an optional private, ignored local store proposed by [ADR-004](adr/ADR-004-keep-operational-lessons-in-ignored-project-local-store.md). ADR-004 is **Proposed**, pending owner acceptance; this is guidance for the candidate workflow, not an accepted publication policy. The store does not exist in a clean clone. Create `local-lessons/` locally when needed; never commit or publish its contents.

## Where knowledge belongs

- `local-lessons/`: sanitized, reusable, context-bound operational observations kept only on the local machine.
- `kb/research/`: reviewed public source captures/evidence; not canonical conclusions.
- `kb/wiki/`: public, provenance-linked synthesis.
- `docs/adr/`: durable architecture/public-contract rationale.
- `.agents/skills/`: repeatable executable agent procedures.
- `.search/` and `sources/`: ignored raw/ephemeral evidence or bulky/private inputs, not durable lesson indexes.

Do not duplicate a public KB conclusion or a skill; link/refer to it where useful. Lessons are not automatically promoted. Public promotion requires a separate privacy, provenance, relevance, and publication review.

## Capture and evidence labels

Search the local index and public KB for duplicates before capture. Use one `LL-NNNN-short-title.md` per lesson, with frontmatter fields: `id`, `title`, `category`, `evidence`, `created`, `updated`, `provenance`, `verification_context`, `review_status`, and, after review, `reviewed_for`. A starter template is in `local-lessons/README.md` when the ignored store has been created.

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

The optional ignored store is absent from clean clones by design. A new clone can read this tracked workflow and create its own local store; no local lesson is synchronized or implied to exist.
