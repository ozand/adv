# ADR-011: Define source-to-knowledge disposition and coverage

**Status**: Accepted
**Date**: 2026-10-09
**Authors**: Repository owner and coding assistant
**Supersedes**: None
**Related**: ADR-004 (local lessons), ADR-007 (publication boundary), ADR-010 (knowledge/evidence contract); Issues #5, #45, #46

## Context

Owner acceptance of this finite disposition and coverage contract was recorded by the coordinator in [Issue #46 comment 6074262030](https://github.com/ozand/adv/issues/46#issuecomment-6074262030), based on the owner's explicit decision: “принимаю ADR-011 Проверенный PR #56 с контрактом”. The accepted proposal was published at main commit `15aed78a3dd2038ca0673c5abf3713746aa84ff2`; ADR-011 blob `75e0c2b1fdb3ddddcecef56a5f9b7dac16f9538f`, companion contract blob `bf3af6c0238ed362216199f141ea27e5e20e63ac`. Acceptance applies to that finite contract only; it does not authorize migration/backfill, QMD operations, live source acquisition, or device/runtime operations.
Issue #5 owns the local catalog/corpus accounting workflow and distinguishes catalog listing rows, normalized repository candidates, source revisions, clone outcomes, and QMD retrieval. It does not establish which source artifacts were studied, synthesized, deferred, or represented in canonical targets. Issue #46 requests a disposition/coverage contract extending that existing accounting, not a second inventory.

The public `docs/OPERATIONS.md` documents historical local-corpus accounting and cautions that historical counts/manifests are not current-state claims. Its examples include different units (listing rows, URL candidates, source revisions, Markdown documents, indexed files). They must not be added together or reused as current denominators. ADR-010 is accepted at main commit `143c2de99c7b20e1e1879ead19aec139ef57d3bd`; its evidence model keeps claim provenance and applicability distinct from retrieval and editorial status.

Evidence basis: direct inspection of Issue #5's public accounting interface, `docs/OPERATIONS.md`, accepted ADR-010/knowledge contract, and Issue #46. No private manifests, current local corpus, source clones, or QMD index were inspected. No current corpus totals are asserted.

### Problem statement

Define a deterministic, source-artifact-level disposition and coverage model that extends Issue #5 accounting while distinguishing acquisition/indexing from assessment and synthesis.

### Prior art

Issue #5 already records catalog rows/candidates, repository/source revisions, clone outcomes, and QMD retrieval. The contract proposed here links those existing identities to assessment outcomes and canonical targets; it does not replace or recreate them. ADR-007's publication boundaries and ADR-010's evidence semantics remain in force.

## Decision

Accept `docs/source-to-knowledge-disposition-contract.md` as the finite disposition/coverage contract for Issue #46. Its primary accounting unit is a **source-artifact record** identified by canonical repository/source identity plus full revision and document/path locator where available. Keep catalog listing rows, normalized repository candidates, source artifacts, canonical targets, and indexed documents as distinct linked entities; aliases/forks remain distinct or explicitly related rather than silently merged.

Treat `retrieved` and `indexed` as separate acquisition/retrieval flags, not mutually exclusive disposition states. A source can be retrieved, indexed, later studied, and/or synthesized. Each eligible artifact has exactly one current disposition: `not-assessed`, `studied`, `synthesized`, `deferred`, or `unresolved`. Explicit `excluded` records are outside the eligible set, require a reason, and are reported separately. An eligible artifact with unresolved identity/revision/access/rights/outcome remains `unresolved` within the denominator and receives no assessment credit. A `studied` record requires an assessment receipt (scope, date/reviewer, outcome and limitations); merely opening/indexing is insufficient. `synthesized` requires at least one explicit source-artifact-to-canonical-target relation. One source may support zero or many targets; multiple sources may support one target. No reciprocal target relation is inferred automatically.

Coverage uses a named, frozen set of **eligible source-artifact records**. Eligibility, deduplication and exclusions must be declared with the snapshot; counts from different units are never summed. The eligible partition is `N = not_assessed + studied + synthesized + deferred + unresolved_eligible`. Unresolved listing identities whose artifact eligibility is unknown are reported outside `N`; do not claim complete catalog coverage while that scope remains unresolved. Retrieval/index flags and target relations are orthogonal. Reassessment history is append-only; coverage counts current state only.

This ADR records the owner's acceptance of the finite contract above. Acceptance does not implement or enforce the format and does not authorize live requests, cloning, indexing, QMD updates, private source-corpus inspection, migration, or backfill.

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
| Acquisition/index flags are orthogonal to disposition | Contract fixtures combining retrieval/index flags with each disposition | Not yet implemented |
| Studied requires an assessment receipt | Contract fixture rejects studied without scope/outcome receipt | Not yet implemented |
| Synthesized requires a source-artifact-to-target relation | Contract fixture rejects synthesized with zero target links | Not yet implemented |
| Coverage arithmetic is deterministic | Worked examples partition a frozen eligible-artifact set; exclusions/unresolved separate | Specification examples reviewed; executable validator not implemented |
| Source identity preserves revision/document and relationships | Alias/fork and many-to-many contract examples | Contract-level semantics accepted; no current source/manifest audit performed |
| ADR-007/010 boundaries remain unchanged | Review data paths and evidence labels | No migration/QMD/source operations performed |

## Rollback

Any future reversal requires a superseding ADR and, if records are later adopted, a separately planned migration; do not silently reinterpret historical counts. No records are migrated by this acceptance.

## References

- [Issue #46](https://github.com/ozand/adv/issues/46)
- [Issue #5](https://github.com/ozand/adv/issues/5)
- [Issue #5 operations/accounting contract](../OPERATIONS.md)
- [Accepted ADR-010](ADR-010-define-extensible-knowledge-evidence-contract.md)
- [Accepted knowledge model contract](../knowledge-model-contract.md)
- [ADR-007 publication boundary](ADR-007-publish-reviewed-research-captures-exclude-local-source-originals.md)
