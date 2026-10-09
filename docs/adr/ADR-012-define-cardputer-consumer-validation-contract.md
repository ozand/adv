# ADR-012: Define a Cardputer consumer-validation contract

**Status**: Accepted — the coordinating session relayed the repository owner's exact response “принят” on 2026-10-09 for the published ADR and contract at merge `5cc32431e10b32a40fbde6b160524e369ab58277` (ADR blob `3d7597e99c1d18288e6a9500b4f1c011fa259f6d`; contract blob `2f6797672107891e16ca4d0ff698be328214d679`). The Issue #47 acceptance record is [comment-6086379078](https://github.com/ozand/adv/issues/47#issuecomment-6086379078). This records relayed decision provenance, not independent GitHub verification of the human statement.
**Date**: 2026-10-09
**Issue**: #47
**Authors**: Repository owner and coding assistant
**Supersedes**: None
**Related**: ADR-010 (knowledge/evidence), ADR-011 (disposition/coverage); Issue #47

## Context

Issue #47 requires deterministic Cardputer-specific consumer checks composed with, not substituted for, universal OKF validation. The published proposal received exact-content peer-review PASS from `f33` and `e1ff` on pre-acceptance commit `5b5ef8e4740b0b6764c22647c6ee3f17d6a80311`; this acceptance-record increment requires its own review. ADR-010/011 are accepted finite contracts; they do not authorize migration or establish corpus conformance. The universal profile requires nonempty extensible `type`; `title` is universally optional and only recommended for adv cards by ADR-010. No new mandatory title rule or retroactive legacy migration is established here.

Evidence: ADR-010, accepted ADR-011 contract blob `c285422dc12371e4c4a23ef27482bce0758bd848`, Issue #47, and framework documentation. Framework source reference pin `73277fdb3e54184901f67268bc676a562b0a677a` is distinct from the installed v0.4.0 binary receipt associated with source commit `db18df399ee2e7e236b4df6699b5d4892fc9c04e`; equal version labels do not prove byte identity. No new inventory, private-source inspection, runtime/device test, or framework installation was performed.

### Problem statement

Define a bounded proposal for Cardputer consumer checks/reports that separates universal structure from local policy without implying truth, privacy, publication permission, or index freshness.

### Prior art

`kb-bootstrap` documents universal OKF, provenance/freshness, graph-integrity, and QMD-declaration checks as separate reports. ADR-010/011 define accepted metadata/evidence/disposition semantics; structural PASS does not prove factual truth or that the corpus satisfies every local policy.

## Decision

Accept `docs/consumer-validation-contract.md` as the finite read-only Cardputer consumer-validation contract. Preserve universal `kb-bootstrap` results as a separate layer; consumer checks must not replace or reinterpret them. This recorded owner acceptance authorizes implementation of the specified consumer checks and deterministic fixtures. Existing records remain governed by accepted universal/contract semantics; no mandatory title or retroactive migration is imposed. No repair, status promotion, or live data/index/device operations.

**This is not** a claim that a consumer validator exists, a framework upgrade, migration plan, factual/privacy/rights oracle, index-freshness check, or permission to migrate, repair, promote status, refresh QMD, or operate a device. Acceptance is recorded; implementation is authorized only within the finite read-only consumer-check and fixture scope. The acceptance-record PR and independent exact-commit review remain gates before implementation starts.

### Output layers and compatibility

The composed report distinguishes:

1. **Universal structural/profile:** result from named `kb-bootstrap` invocation/version; supported universal profile claims only.
2. **Repository graph:** separate dead-link/orphan/evidence-link results.
3. **QMD declaration/configuration:** declared configuration only; no runtime registration, refresh, retrieval, embeddings, freshness, or truth claim.
4. **Cardputer consumer policy:** accepted checks from ADR-010/011; until implementation and fixtures are delivered, report **not implemented**, never PASS.
5. **Recommendation state:** for an explicitly selected new/revised adv card, report whether ADR-010's title recommendation is met; absent legacy records outside the selected scope are `NOT CHECKED`, not failures. No universal title requirement is introduced.
6. **Provenance state:** for a selected claim, report whether its cited source revision and document locator are present and mapped to that claim. Missing required provenance is a local policy failure, not a factual-falsity finding.

Do not collapse layers into one undifferentiated PASS. A failure in one layer does not redefine another. Record framework source pin and invoked binary version separately; do not claim byte identity without evidence. Existing validation outputs do not retroactively pass future consumer policy.

## Consequences

### What gets easier

Reviewers can distinguish universal, repository-structural, QMD-declaration, and local-policy outcomes while preserving extensible OKF fields.

### What gets harder

Reports need tool/version/layer labels; consumer fixtures require maintenance; implementation remains outstanding after this acceptance-record increment.

### What does not change

No existing card is migrated, rewritten, or promoted. ADR-010/011 semantics, publication boundaries, QMD safety, source locality, and device restrictions remain unchanged. The implementation remains bounded to read-only deterministic checks and fixtures.

## Alternatives Considered

- **Universal PASS implies local conformance:** rejected because the minimal profile permits extensible fields and does not enforce local policy.
- **Replace/fork universal semantics:** rejected; conflates consumer policy with OKF and risks compatibility.
- **One aggregate result:** rejected; hides which layer was checked.
- **Auto-repair/promote metadata:** rejected; validation is read-only and cannot establish truth.

## Test Contract

| Claim | Check | Current evidence |
|---|---|---|
| Universal/local checks remain distinct | Fixtures assert separate labels/sections | Not yet written |
| Required metadata/evidence checks reflect ADR-010 | Positive/negative fixtures for nonempty type, claim/source evidence, applicability, status/evidence separation, and required source revision/locator | Proposed; fixtures await acceptance |
| Recommended/optional metadata stays compatible | Selected new/revised adv title recommendation warns when unmet; out-of-scope legacy is NOT CHECKED; optional profile is not universal failure; types remain extensible | Proposed; fixtures await acceptance |
| Disposition/coverage checks reflect ADR-011 | Exact partition: not_assessed=0, studied=1, synthesized=2, deferred=0, unresolved_eligible=2; N=5; assessment (studied+synthesized)/N=3/5; synthesis/target-linked=2/5; 2 reasoned exclusions outside N; unknown non-artifact listing affects completeness only; N=0 is NOT APPLICABLE | Proposed; fixtures await acceptance |
| Link scope permits citations safely | Positive external source URL; negative canonical target outside approved wiki/root, traversal, private source path, dangling target | Proposed; fixtures await acceptance |
| QMD declaration does not imply runtime state | Output fixture labels declaration-only | Not yet written |
| Validation is read-only | Future before/after fixture tree/index comparison | Proposed; implementation awaits acceptance |

## Rollback

This accepted decision may be superseded only by a new scoped ADR and owner decision. Any reversal must preserve historical reports and must not silently rewrite past validation results.

## References

- Issue #47
- ADR-010 and `docs/knowledge-model-contract.md`
- ADR-011 and `docs/source-to-knowledge-disposition-contract.md`
- `kb-bootstrap` release source commit `db18df399ee2e7e236b4df6699b5d4892fc9c04e`; framework source pin `73277fdb3e54184901f67268bc676a562b0a677a`
- Framework docs: `OKF_V0_2_CANONICAL_PROFILE.md`, `CANONICAL_PROVENANCE_FRESHNESS_PROFILE.md`
