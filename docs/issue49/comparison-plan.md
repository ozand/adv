# Issue #49 comparison plan

## Scope and approval
Issue #49; approved five-project set and exclusions are recorded at https://github.com/ozand/adv/issues/49#issuecomment-6094176320. This plan is limited to comparison normalization, not ordinary layout/curation owned by Issue #3. No new source acquisition, QMD operations, raw capture publication, or device tests. The exact bounded release instruction is recorded at https://github.com/ozand/adv/issues/49#issuecomment-6158421250; PR review and merge remain pending.

## Existing evidence only
Use the revision-pinned Launcher report for AREA512, Cardputer examples, and UcPlayground, plus the existing CalcPuter and Cardulator entity profiles. Preserve their exact project identities, repository revisions, source locators, evidence classes, and license limitations. Do not copy upstream code or raw source passages.

## Outputs
1. Approved set and exclusions are recorded before content work in Issue comment https://github.com/ozand/adv/issues/49#issuecomment-6094176320; release authorization provenance and current publication state are recorded in the read-only JSON manifest in this folder.
2. Five comparable claim-centered project records, retaining evidence links and applicable/unknown/N/A states with reasons. AREA512, cardputer-examples, and UcPlayground have dedicated records in `kb/wiki/entities/`; CalcPuter and Cardulator comparison notes extend their existing canonical entity profiles without duplicate project records or identity changes.
3. Qualitative comparative report grounded only in existing public evidence. Compare project role and documented scope, not rankings or unsupported runtime performance.

## Criteria and evidence
- Common dimensions: project role, upstream-documented purpose, target applicability, evidence type/pin/locator, documented prerequisites/toolchain, license evidence/limitations.
- Mark undocumented criteria `unknown`; use `N/A` only where genuinely inapplicable and explain why. Unknown is not unsupported.
- Keep source-reported claims separate from code-inspected/device-observed; no builds or device tests are planned.
- Preserve AREA512 Launcher variants as distinct catalog variants despite common repository URL; UcPlayground collection is not one product binary.
- `cardputer-examples` has no root LICENSE at the pinned revision; assets/dependencies rights remain unknown. No reuse of its code/assets.
- Root licenses on AREA512/UcPlayground/CalcPuter/Cardulator do not clear bundled assets/dependencies.

## Verification and release boundary
Check exact set equality (5 IDs), pins/locators, claim-to-source links, unknown/N/A reasons, preserved canonical identities, evidence-backed narrative, privacy/provenance/rights, consumer-validator fixtures, and pinned `kb-bootstrap validate-core` where supported. Validation proves structure/links, not truth or device behavior. The bounded release instruction is recorded with coordinator-relayed provenance in the manifest and [Issue comment 6158421250](https://github.com/ozand/adv/issues/49#issuecomment-6158421250); PR review and merge remain pending until delivery.

## Verification note
Verification before current review correction: the pinned `kb-bootstrap` 0.4.0 validate-core reported zero canonical profile/provenance errors and zero dead links. It reports five repository orphans and does not validate factual truth, legal rights, actual device/runtime behavior, or publication delivery. The full pytest suite passed (172 tests); the focused consumer-validator suite passed (19 tests). Ruff passed on the changed validator and its tests; whole-repository Ruff reports three unrelated findings outside this Issue scope. Canonical-profile consolidation and release-status correction are in the pending PR delta and require fresh verification.
