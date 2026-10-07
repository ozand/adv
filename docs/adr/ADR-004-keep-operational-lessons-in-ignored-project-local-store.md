# ADR-004: Keep operational lessons in an ignored project-local store

**Status**: Proposed
**Date**: 2026-10-07
**Authors**: Repository owner and coding assistant
**Supersedes**: None
**Related**: ADR-001, ADR-002, ADR-003; Issue #7

## Context

The public repository separates reviewed source captures (`kb/research/`), canonical knowledge (`kb/wiki/`), durable architectural decisions (`docs/adr/`), and reusable procedures (`.agents/skills/`). Reusable facts from local diagnostics need to persist between sessions without publishing raw captures, private host paths, identifiers, or device data.

Issue #7 requests a separate project-local lessons mechanism. This ADR records the boundary and minimum format, not the full workflow implementation. **Owner acceptance is pending; this ADR remains Proposed and is not an accepted project policy.**

## Decision (proposed)

Store reusable operational lessons in `local-lessons/` at the repository root and add that path to `.gitignore`. Do not track lesson entries or indexes in Git. Only human-reviewed, sanitized summaries suitable for public knowledge may be separately synthesized into `kb/research/` or `kb/wiki/` through their existing review processes; they are not automatically copied or published from local lessons.

Each lesson is Markdown with YAML frontmatter: unique ID, title, category, evidence label, created/updated dates, provenance, verification context, and review status. Labels (`verified`, `measured`, `reported`, `theory`, `hypothesis`) describe evidence type/status and are not an ordinal confidence scale. Their operational definitions are maintained in `local-lessons/README.md`; tentative theory/hypothesis must never be presented as verified guidance. A small `local-lessons/index.md` provides local search. No new search dependency or QMD collection is introduced. Relevant diagnostic tasks should consult the index before repeating operations. The repository owner is accountable for maintenance; authors update entries and index, and a second reviewer checks evidence, privacy, duplication, and staleness before operational reuse.

Lessons must contain no raw device logs, full serial/MAC identifiers, credentials, personal data, private network details, or binary/source dumps. `.gitignore` prevents ordinary accidental inclusion, not deliberate force-staging; inspect staged paths before every commit/push. Lessons are distinct from ADR rationale, public research evidence, canonical wiki synthesis, and executable skill procedures.

## Consequences

- Local lessons can preserve reusable diagnostics without mixing them into the public evidence corpus.
- They are not synchronized across clones; maintainers must back them up locally.
- Manual search/review can become stale; public promotion requires a separate review and is never automatic.

## Alternatives considered

- `kb/wiki/`: rejected because local operational observations may be sensitive and lack public review.
- `kb/research/`: rejected because it is public, trackable evidence, not private operational memory.
- `.search/`: rejected because it is raw/ephemeral evidence without a durable lesson/index contract.
- New QMD collection/dependency: deferred; Markdown/index are sufficient for the initial small store.

## Test contract

| Claim | Check | Candidate result |
|---|---|---|
| Local lessons are ignored and absent from tracked tree | `git check-ignore -v local-lessons/<file>`; `git ls-files local-lessons` | Candidate: ignore rule covers `local-lessons/`; no candidate lesson files tracked/staged. Ignore does not prevent deliberate force-staging. |
| Public KB collections stay distinct | Inspect QMD declarations and ignore rule | Candidate review: no QMD declarations changed; ignore rule is limited to `/local-lessons/`. |
| Lesson includes evidence label/provenance/context | Parse local sample frontmatter and inspect fields | Separate local LL-0001 frontmatter parsed successfully with PyYAML; fields include verified label, provenance, dates, and version/context review. Sample is local-only and not committed. |
| Privacy exclusions are observed | Human review of sanitized local lesson | Manual check only; not machine-enforced |
| Lessons are searchable without dependency | Inspect local index/links and tracked workflow | Candidate docs specify manual local index/text search and add no dependency/QMD collection; clean clone has tracked workflow but not local lesson entries. |

## References

- [Issue #7](https://github.com/ozand/adv/issues/7)
- [AGENTS.md](../../AGENTS.md)
- [KB index](../../kb/index.md)
