# ADR-013: Define a bounded batch knowledge workflow

**Status**: Accepted
**Acceptance date**: 2026-10-09
**Date**: 2026-10-09
**Issue**: #48
**Authors**: Repository owner and coding assistant
**Supersedes**: None
**Related**: ADR-007, ADR-010, ADR-011, ADR-012

## Context

This decision responds to [Issue #48](https://github.com/ozand/adv/issues/48). Its companion [workflow contract](../bounded-batch-knowledge-workflow.md) contains the normative field definitions and worked example.

Issue #48 requests a bounded workflow for batch knowledge work: immutable input identity, structured outputs, single-writer coordination, independent exact-content review, deterministic gates, and a durable sanitized delivery receipt. Accepted ADR-010/011/012 define evidence, disposition, and consumer-validation boundaries; they do not implement batch orchestration or authorize source acquisition, migration, QMD operations, or publication.

Owner acceptance provenance: the coordinator relayed the owner's explicit decision, “подтверждаю,” accepting the exact reviewed ADR/workflow candidate `9a2324d95917e3e03288beefa3eba60caca40ff8`; that candidate was published in PR #62 merge commit `b74b6ef839244299114e1f2f9791622e49dbe009`. The relay and decision scope are recorded in [Issue #48](https://github.com/ozand/adv/issues/48#issuecomment-6090976967). Acceptance covers this finite workflow contract, not automatic publication, current-corpus conformance, or source/device/QMD operations.

Evidence basis: open Issue #48 and accepted contracts. No private corpus, manifests, source clones, or QMD index was inspected. The worked example is synthetic only; no current batch inventory or corpus completeness claim is made.

### Problem statement

Define a reproducible, reviewable batch-work contract that keeps source identity, content decisions, retrieval state, and publication/release evidence separate.

### Prior art

Issue #5 owns acquisition/catalog identities. ADR-010 scopes evidence to claims; ADR-011 defines artifact-level disposition and frozen eligible denominators; ADR-012 defines consumer checks. ADR-007 governs publication eligibility. This workflow composes those contracts without replacing their owners or semantics.

## Decision

Accept `docs/bounded-batch-knowledge-workflow.md` as a finite, tool-independent workflow contract. The companion document is the normative workflow detail; this ADR records its rationale and boundaries. Each batch declares an immutable input snapshot and base revision; one writer produces candidate outputs; read-only reviewers assess exact candidate hashes; deterministic gates report separate validation layers; release evidence is recorded in a sanitized Issue/PR receipt. Gate results do not auto-publish or promote evidence.

**This is not** an implementation, queue engine, new taxonomy, dependency, serialization mandate, source-fetch permission, current-corpus assertion, QMD update, migration, or automatic publication policy. Implementation is separately scoped to minimal templates, read-only aggregate checks, and synthetic fixtures.

## Consequences

This ADR and its companion workflow are **Accepted** as the finite contract. Acceptance authorizes a separately scoped implementation of minimum templates, a read-only aggregate receipt check, and synthetic fixtures; it does not authorize automatic release, live source acquisition, QMD mutation, corpus migration, or device operations. Operational release permission remains an explicit human decision. The checker validates declared record consistency, not approval authenticity, reviewer identity, or source integrity.

### What gets easier

Batch results become reproducible from explicit inputs and candidate hashes; reviewers can distinguish source, consumer, and retrieval evidence and identify exactly what was released.

### What gets harder

Producers must freeze input identity, preserve receipts, keep a single writer, and maintain exact revision relationships. Review is invalidated by content changes; partial scope remains visible.

### What does not change

Issue #5 remains the acquisition/accounting owner. ADR-007/010/011/012 semantics and publication boundaries remain unchanged. No current source/corpus is fetched, migrated, indexed, or published by this decision.

## Alternatives Considered

- **Parallel writable agents on one candidate:** rejected because races and conflicting edits make reviewed content identity ambiguous.
- **Aggregate PASS from any successful validator:** rejected because universal structure, local policy, and retrieval establish different claims.
- **Autopublish on all checks passing:** rejected because publication/rights/privacy review and owner release authority remain separate.
- **New queue service, dependency, or repository-wide delegation policy:** rejected; Issue #48 asks for a bounded knowledge workflow, not broader orchestration infrastructure.
- **Infer batch identity from moving source paths or QMD:** rejected; neither freezes bytes or revision.

## Test Contract

| Claim | Check | Current evidence |
|---|---|---|
| Inputs and exclusions are reproducible | Synthetic JSON record includes base, candidate, source locator/revision/hash, and eligibility/exclusion | Checker fixture validates field shapes; no live inputs examined |
| One writer and read-only reviewers are explicit | Companion workflow states the role and exact-candidate SHA rule; checker rejects mismatched review SHA | Contract and synthetic structural tests; human role/identity is not authenticated |
| Validation layers cannot mask each other | Checker enforces aggregate consistency across declared source/content/retrieval layers | Eight synthetic tests; no live validation performed |
| Coverage accounting follows ADR-011 | Companion example shows N=2 partition and partial result; checker requires one result per eligible input | Arithmetic is illustrative; checker does not recompute disposition coverage ratios |
| Delivery receipt is sanitized and durable | Checker requires a canonical Issue/comment URL, matching Issue, retention statement, and sanitized flag | Synthetic structural test; human sanitation/retention is not independently proven |

## Rollback

Supersede this accepted decision through a reviewed follow-up ADR; retain historical batch receipts and do not rewrite prior gate results.

## References

- [Issue #48](https://github.com/ozand/adv/issues/48)
- [ADR-007 publication boundary](ADR-007-publish-reviewed-research-captures-exclude-local-source-originals.md)
- [ADR-010 knowledge/evidence contract](ADR-010-define-extensible-knowledge-evidence-contract.md)
- [ADR-011 source disposition/coverage](ADR-011-define-source-disposition-and-coverage.md)
- [ADR-012 consumer-validation contract](ADR-012-define-cardputer-consumer-validation-contract.md)
- [Accepted bounded-batch workflow](../bounded-batch-knowledge-workflow.md)
- [Synthetic batch record example](../batch-record.example.json)
- [Issue #5 operations/accounting contract](../OPERATIONS.md)
