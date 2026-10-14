# Issue #49 comparison plan

## Scope and approval
Issue #49; approved five-project set and exclusions are recorded at https://github.com/ozand/adv/issues/49#issuecomment-6094176320. This plan is limited to comparison normalization, not ordinary layout/curation owned by Issue #3. No new source acquisition, QMD operations, raw capture publication, device tests, or release approval.

## Existing evidence only
Use the revision-pinned Launcher report for AREA512, Cardputer examples, and UcPlayground, plus the existing CalcPuter and Cardulator entity profiles. Preserve their exact project identities, repository revisions, source locators, evidence classes, and license limitations. Do not copy upstream code or raw source passages.

## Outputs
1. Approved set manifest and exclusions are recorded before content work in Issue comment https://github.com/ozand/adv/issues/49#issuecomment-6094176320; a read-only JSON mirror is under this folder.
2. Five comparable claim-centered profiles, retaining evidence links and applicable/unknown/N/A states with reasons. Existing calculator profiles may only be extended with comparison fields; no layout redesign.
3. Qualitative comparative report grounded only in existing public evidence. Compare project role and documented scope, not rankings or unsupported runtime performance.

## Criteria and evidence
- Common dimensions: project role, upstream-documented purpose, target applicability, evidence type/pin/locator, documented prerequisites/toolchain, license evidence/limitations.
- Mark undocumented criteria `unknown`; use `N/A` only where genuinely inapplicable and explain why. Unknown is not unsupported.
- Keep source-reported claims separate from code-inspected/device-observed; no builds or device tests are planned.
- Preserve AREA512 Launcher variants as distinct catalog variants despite common repository URL; UcPlayground collection is not one product binary.
- `cardputer-examples` has no root LICENSE at the pinned revision; assets/dependencies rights remain unknown. No reuse of its code/assets.
- Root licenses on AREA512/UcPlayground/CalcPuter/Cardulator do not clear bundled assets/dependencies.

## Verification and release boundary
Check exact set equality (5 IDs), pins/locators, claim-to-source links, unknown/N/A reasons, preserved identities, evidence-backed narrative, privacy/provenance/rights, consumer-validator fixtures, and pinned `kb-bootstrap validate-core` where supported. Validation proves structure/links, not truth or device behavior. No public publication/merge until separate explicit release approval and rights/privacy gates are satisfied.

## Verification note
The pinned `kb-bootstrap` 0.4.0 validate-core was run read-only against the final `kb` tree: canonical profile/provenance checks report zero errors and graph integrity reports zero dead links. It reports five existing repository orphans and does not validate factual truth, legal rights, actual device/runtime behavior, or publication readiness. The full repository pytest suite passed (172 tests); the focused consumer-validator suite passed (19 tests). Ruff passed on the changed validator and its tests; whole-repository Ruff reports three unrelated pre-existing findings in `scripts/adv_diagnostic_cli.py` and hardware contract tests.
