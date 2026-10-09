# ADR-011: Define source-to-knowledge disposition and coverage

**Status**: Proposed
**Date**: 2026-10-09
**Authors**: Repository owner and coding assistant
**Supersedes**: None
**Related**: ADR-004 (local lessons), ADR-007 (publication boundary), ADR-010 (knowledge/evidence contract); Issues #5, #45, #46

## Context

Issue #5 owns the local catalog/corpus accounting workflow and distinguishes catalog listing rows, normalized repository candidates, source revisions, clone outcomes, and QMD retrieval. It does not establish which source artifacts were studied, synthesized, deferred, or represented in canonical targets. Issue #46 requests a disposition/coverage contract extending that existing accounting, not a second inventory.

The public `docs/OPERATIONS.md` documents historical local-corpus accounting and cautions that historical counts/manifests are not current-state claims. Its examples include different units (listing rows, URL candidates, source revisions, Markdown documents, indexed files). They must not be added together or reused as current denominators. ADR-010 is accepted at main commit `143c2de99c7b20e1e1879ead19aec139ef57d3bd`; its evidence model keeps claim provenance and applicability distinct from retrieval and editorial status.

Evidence basis: direct inspection of Issue #5's public accounting interface, `docs/OPERATIONS.md`, accepted ADR-010/knowledge contract, and Issue #46. No private manifests, current local corpus, source clones, or QMD index were inspected. No current corpus totals are asserted.

### Problem statement

Define a deterministic, source-artifact-level disposition and coverage model that extends Issue #5 accounting while distinguishing acquisition/indexing from assessment and synthesis.

### Prior art

Issue #5 already records catalog rows/candidates, repository/source revisions, clone outcomes, and QMD retrieval. The contract proposed here links those existing identities to assessment outcomes and canonical targets; it does not replace or recreate them. ADR-007's publication boundaries and ADR-010's evidence semantics remain in force.

## Decision

Propose `docs/source-to-knowledge-disposition-contract.md` as the finite disposition/coverage contract. Its primary accounting unit is a **source-artifact record** identified by canonical repository/source identity plus full revision and document/path locator where available. Keep catalog listing rows, normalized repository candidates, source artifacts, canonical targets, and indexed documents as distinct linked entities; aliases/forks remain distinct or explicitly related rather than silently merged.

Treat `retrieved` and `indexed` as separate acquisition/retrieval flags, not mutually exclusive disposition states. A source can be retrieved, indexed, later studied, and/or synthesized. Disposition records the assessment outcome: `not-assessed`, `studied`, `synthesized`, `deferred`, `excluded`, or `unresolved`. A `studied` record requires an assessment receipt (scope, date/reviewer, outcome and limitations); merely opening/indexing is insufficient. `synthesized` requires at least one explicit source-artifact-to-canonical-target relation. One source may support zero or many targets; multiple sources may support one target. No reciprocal target relation is inferred automatically.

Coverage uses a named, frozen set of **eligible source-artifact records**. Eligibility, deduplication and exclusions must be declared with the snapshot; counts from different units are never summed. Each eligible artifact has exactly one current primary disposition for partition arithmetic; retrieval/index flags and target relations are orthogonal. Reassessment history is append-only; coverage counts current state only.

This ADR proposes a format only. It does not adopt, implement, backfill, or enforce the format and does not authorize live requests, cloning, indexing, QMD updates, source-corpus inspection, or migration. Owner acceptance of this ADR is required before adoption/backfill.

## Consequences

### What gets easier

A bounded report can distinguish acquisition from substantive assessment/synthesis, while retaining source identity, one-to-many source/target relationships, and auditable coverage arithmetic.

### What gets harder

Producers must define a stable snapshot and eligibility rule, retain assessment receipts, resolve artifact identities/revisions, and maintain target relations and disposition history. Unresolved and excluded items remain visible rather than disappearing.

### What does not change

Issue #5 remains the source for catalog/corpus acquisition and QMD workflow. ADR-010 evidence semantics, ADR-007 publication boundaries, `sources/` local-only storage, and current content remain unchanged. No current coverage totals are established.

## Alternatives Considered

- **Treat retrieved/indexed as studied:** rejected because retrieval does not prove substantive review or claim assessment.
- **One source-to-one canonical target:** rejected because sources may support multiple targets and targets may synthesize multiple sources.
- **Count catalog rows, repositories, documents, and QMD hits in one denominator:** rejected because they are different units and create misleading coverage.
- **Infer “studied” or “synthesized” from QMD, stable status, or links:** rejected because none proves assessment or semantic support.
- **Create a second inventory:** rejected because Issue #5 already owns acquisition/accounting identities.
- **Automatically generate reciprocal links or dispositions:** rejected because relationships and status cannot be inferred safely from retrieval metadata alone.

## Test Contract

| Claim | Check | Current evidence |
|---|---|---|
| Acquisition/index flags are orthogonal to disposition | Fixtures for retrieved/indexed combined with each disposition | Not yet written |
| Studied requires an assessment receipt | Fixture rejects studied without scope/outcome receipt | Not yet written |
| Synthesized requires a source-artifact-to-target relation | Fixture rejects synthesized with zero target links | Not yet written |
| Coverage counts are deterministic and non-overlapping | Worked examples partition one frozen eligible-artifact set; exclusions/unresolved separate | Worked examples present; executable validator not written |
| Source identity preserves revision/document and relationships | Review alias/fork and many-to-many examples | Contract examples; no source/manifest audit performed |
| ADR-007/010 boundaries remain unchanged | Review data paths and evidence labels | No migration/QMD/source operations performed |

## Rollback

Because this ADR is Proposed and no records are migrated, withdraw the proposal and remove its index row in a reviewed follow-up. If later accepted and adopted, reversal requires a superseding ADR and separately planned record migration; do not silently reinterpret historical counts.

## References

- [Issue #46](https://github.com/ozand/adv/issues/46)
- [Issue #5](https://github.com/ozand/adv/issues/5)
- [Issue #5 operations/accounting contract](../OPERATIONS.md)
- [Accepted ADR-010](ADR-010-define-extensible-knowledge-evidence-contract.md)
- [Accepted knowledge model contract](../knowledge-model-contract.md)
- [ADR-007 publication boundary](ADR-007-publish-reviewed-research-captures-exclude-local-source-originals.md)
