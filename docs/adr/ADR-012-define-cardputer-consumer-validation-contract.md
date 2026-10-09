# ADR-012: Define a Cardputer consumer-validation contract

**Status**: Proposed
**Date**: 2026-10-09
**Issue**: #47
**Authors**: Repository owner and coding assistant
**Supersedes**: None
**Related**: ADR-010 (knowledge/evidence), ADR-011 (disposition/coverage); Issue #47

## Context

Issue #47 proposes deterministic Cardputer-specific consumer checks composed with, not substituted for, universal OKF validation. ADR-010/011 are accepted finite contracts; they do not authorize migration or establish corpus conformance. The universal profile requires nonempty extensible `type`; `title` is universally optional and only recommended for adv cards by ADR-010. No new mandatory title rule or retroactive legacy migration is established here.

Evidence: ADR-010, accepted ADR-011 contract blob `c285422dc12371e4c4a23ef27482bce0758bd848`, Issue #47, and framework documentation. Framework source reference pin `73277fdb3e54184901f67268bc676a562b0a677a` is distinct from the installed v0.4.0 binary receipt associated with source commit `db18df399ee2e7e236b4df6699b5d4892fc9c04e`; equal version labels do not prove byte identity. No new inventory, private-source inspection, runtime/device test, or framework installation was performed.

### Problem statement

Define a bounded proposal for Cardputer consumer checks/reports that separates universal structure from local policy without implying truth, privacy, publication permission, or index freshness.

### Prior art

`kb-bootstrap` documents universal OKF, provenance/freshness, graph-integrity, and QMD-declaration checks as separate reports. ADR-010/011 define accepted metadata/evidence/disposition semantics; structural PASS does not prove factual truth or that the corpus satisfies every local policy.

## Decision

Propose `docs/consumer-validation-contract.md` as a read-only, separately labelled consumer-validation contract. Preserve universal `kb-bootstrap` results as a separate layer; consumer checks must not replace or reinterpret them. Define proposed deterministic policy and fixture expectations from accepted ADR-010/011, without implementing validators or fixtures. Existing records remain governed by accepted universal/contract semantics; this proposal imposes no mandatory title or retroactive migration. No repair, status promotion, or live data/index/device operations.

**This is not** a claim that a consumer validator exists, a framework upgrade, migration plan, factual/privacy/rights oracle, index-freshness check, or permission to adopt/enforce the contract. ADR-012 itself must be accepted before enforcement implementation.

### Proposed output layers and compatibility

A future composed report distinguishes:

1. **Universal structural/profile:** result from named `kb-bootstrap` invocation/version; supported universal profile claims only.
2. **Repository graph:** separate dead-link/orphan/evidence-link results.
3. **QMD declaration/configuration:** declared configuration only; no runtime registration, refresh, retrieval, embeddings, freshness, or truth claim.
4. **Cardputer consumer policy:** proposed checks from ADR-010/011; until ADR-012 is accepted and checks are implemented, report **not implemented**, never PASS.
5. **Recommendation state:** for an explicitly selected new/revised adv card, report whether ADR-010's title recommendation is met; absent legacy records outside the selected scope are `NOT CHECKED`, not failures. No universal title requirement is introduced.
6. **Provenance state:** for a selected claim, report whether its cited source revision and document locator are present and mapped to that claim. Missing required provenance is a local policy failure, not a factual-falsity finding.

Do not collapse layers into one undifferentiated PASS. A failure in one layer does not redefine another. Record framework source pin and invoked binary version separately; do not claim byte identity without evidence. Existing validation outputs do not retroactively pass future consumer policy.

## Consequences

### What gets easier

Reviewers can distinguish universal, repository-structural, QMD-declaration, and local-policy outcomes while preserving extensible OKF fields.

### What gets harder

Reports need tool/version/layer labels; local fixtures require maintenance; lack of implemented consumer validation remains visible.

### What does not change

No existing card is migrated, rewritten, or promoted. ADR-010/011 semantics, publication boundaries, QMD safety, source locality, and device restrictions remain unchanged.

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

Because ADR-012 is Proposed and no checker/data change exists, withdraw it and remove its index row in a reviewed follow-up. If accepted/implemented later, reversal requires a new scoped decision and preservation of historical reports.

## References

- Issue #47
- ADR-010 and `docs/knowledge-model-contract.md`
- ADR-011 and `docs/source-to-knowledge-disposition-contract.md`
- `kb-bootstrap` release source commit `db18df399ee2e7e236b4df6699b5d4892fc9c04e`; framework source pin `73277fdb3e54184901f67268bc676a562b0a677a`
- Framework docs: `OKF_V0_2_CANONICAL_PROFILE.md`, `CANONICAL_PROVENANCE_FRESHNESS_PROFILE.md`
