# ADR-004: Keep operational lessons in an ignored project-local store

**Status**: Accepted
**Date**: 2026-10-07
**Accepted**: 2026-10-07 by repository owner in this session
**Authors**: Repository owner and coding assistant
**Supersedes**: None
**Related**: ADR-001, ADR-002, ADR-003; Issue #7

## Context

The public repository separates reviewed source captures (`kb/research/`), canonical knowledge (`kb/wiki/`), durable architectural decisions (`docs/adr/`), and reusable procedures (`.agents/skills/`). Reusable facts from local diagnostics need to persist between sessions without publishing raw captures, private host paths, identifiers, or device data.

Issue #7 requested a separate project-local lessons mechanism. The owner explicitly accepted storing operational lessons in an ignored `local-lessons/` directory, without automatic synchronization/publication or a new search dependency. This ADR records that decision and its boundaries. Owner acceptance came after PR #9 was opened; the accepted status is therefore a follow-up to, not part of, the original reviewed PR head.

## Decision

Store reusable operational lessons in `local-lessons/` at the repository root and add that path to `.gitignore`. Do not track lesson entries or indexes in Git. Only human-reviewed, sanitized summaries suitable for public knowledge may be separately synthesized into `kb/research/` or `kb/wiki/` through their existing review processes; they are not automatically copied or published from local lessons.

Each lesson is Markdown with YAML frontmatter: unique ID, title, category, evidence label, created/updated dates, provenance, verification context, and review status. Labels (`verified`, `measured`, `reported`, `theory`, `hypothesis`) describe evidence type/status and are not an ordinal confidence scale. Their operational definitions and manual review gate are maintained in the tracked `docs/local-lessons-workflow.md`, available on clean clones; tentative theory/hypothesis must never be presented as verified guidance. A starter README and capture template are provided there for manual copying into the ignored local store; no schema enforcement is claimed. A small `local-lessons/index.md` provides local search. No new search dependency or QMD collection is introduced. Relevant diagnostic tasks should consult the index before repeating operations. The repository owner is accountable for maintenance; authors update entries and index, and a second reviewer checks evidence, privacy, duplication, and staleness before operational reuse.

Lessons must contain no raw device logs, full serial/MAC identifiers, credentials, personal data, private network details, or binary/source dumps. `.gitignore` prevents ordinary accidental inclusion, not deliberate force-staging; inspect staged paths before every commit/push. Lessons are distinct from ADR rationale, public research evidence, canonical wiki synthesis, and executable skill procedures.

## Consequences

### What gets easier

- Local lessons can preserve reusable diagnostics without mixing them into the public evidence corpus.
- A local index enables lookup between sessions without adding a runtime dependency.

### What gets harder

- Lessons are not synchronized across clones; maintainers must back them up locally.
- Manual search/review can become stale; public promotion requires a separate review and is never automatic.

### What does not change

- `kb/research/` and `kb/wiki/` remain governed by their public evidence/synthesis review processes.
- Raw evidence remains local; this decision does not authorize publishing it.

## Alternatives Considered

### `kb/wiki/`

Rejected because local operational observations may be sensitive and lack public review.

### `kb/research/`

Rejected because it is public, trackable evidence, not private operational memory.

### `.search/`

Rejected because it is raw/ephemeral evidence without a durable lesson/index contract.

### New QMD collection/dependency

Rejected because the owner explicitly chose not to introduce a search dependency; manual local text search is sufficient initially.

## Test Contract

| Claim | Check | Current evidence |
|---|---|---|
| Local lessons are ignored and absent from tracked tree | `git check-ignore -v local-lessons/<file>`; `git ls-files local-lessons` | Passing: rule covers `/local-lessons/`; candidate contains no lesson files. Deliberate force-staging still requires staged-path review. |
| Public KB collections stay distinct | Inspect QMD declarations and ignore rule | Passing by inspection: no QMD declarations changed; ignore is limited to `/local-lessons/`. |
| Lesson metadata has evidence/provenance/context | Parse local lesson frontmatter and inspect fields | LL-0001 local sample parsed with PyYAML; includes verified label, provenance, dates, and version/context review. Sample remains local-only. |
| Privacy exclusions are observed | Human review of sanitized local lesson | Manual review only; not machine-enforced. |
| Lessons are searchable without a new dependency | Inspect tracked workflow and local index starter | Passing by inspection: workflow uses manual local text search; no dependency/QMD collection added. |

## References

- [Issue #7](https://github.com/ozand/adv/issues/7)
- [AGENTS.md](../../AGENTS.md)
- [KB index](../../kb/index.md)
- [Local lessons workflow](../local-lessons-workflow.md)
