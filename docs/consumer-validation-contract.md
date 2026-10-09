# Proposed Cardputer consumer-validation contract

**Status:** Accepted contract under ADR-012. Acceptance authorizes the bounded consumer-check implementation described here; it does not claim implementation or current-corpus conformance, nor authorize migration, repair, QMD operations, framework upgrade, or device/runtime operation.

## Scope and compatibility

Compose local consumer policy with universal `kb-bootstrap`; do not replace it or claim current corpus conformance. Universal validation requires nonempty extensible `type`; `title` remains universally optional. ADR-010 recommends `title` for adv canonical cards, but this proposal creates no mandatory title rule or retroactive legacy migration. Optional `object_profile` remains distinct from `type`.

The repository owner accepted ADR-012 and this contract as published at merge `5cc32431e10b32a40fbde6b160524e369ab58277`; the coordinating session relayed the exact response “принят” on 2026-10-09. Accepted artifacts: ADR blob `3d7597e99c1d18288e6a9500b4f1c011fa259f6d`; contract blob `2f6797672107891e16ca4d0ff698be328214d679`. See [acceptance record](https://github.com/ozand/adv/issues/47#issuecomment-6086379078). This records relayed decision provenance; it is not a separate claim of GitHub verification of the human statement. Implementation starts only after this acceptance-record increment is reviewed and published.

Framework source reference pin: `73277fdb3e54184901f67268bc676a562b0a677a`. Installed `kb-bootstrap` v0.4.0 receipt is associated with source commit `db18df399ee2e7e236b4df6699b5d4892fc9c04e`; matching version text does not prove binary/source identity.

## Report layers

The composed report distinguishes:

| Layer | Reports | Does not establish |
|---|---|---|
| Universal structural/profile | Named framework invocation/version and supported OKF profile | Local policy, truth, privacy, rights, device behavior |
| Repository graph | Dead links, orphans, evidence links | Semantic correctness or publication permission |
| QMD declaration/configuration | Declared configuration only | Runtime registration, freshness, retrieval, embeddings, truth |
| Cardputer consumer policy | Accepted ADR-010/011 checks | Source truth or device verification |

ADR-012 is accepted, but checks remain **not implemented** until separately delivered. Report consumer policy **not implemented**, never PASS. A failure in one layer does not redefine another; prior validation does not retroactively pass future policy.

## Deterministic fixture contract

The following are implementation acceptance cases, not evidence that tests have already run. Fixture PASS means rule behavior only, never factual truth.

| ID | Input | Expected local outcome | Universal result/notes |
|---|---|---|---|
| F01 | Nonempty extensible `type`, valid claim/source evidence, explicit applicability | PASS | Universal profile PASS |
| F02 | Missing or empty `type` | FAIL | Universal profile FAIL |
| F03 | Unknown but nonempty `type` | PASS | Extensibility preserved |
| F04 | Selected new/revised adv card lacks recommended `title` | Recommendation not met; report warning, not universal or proposal-wide conformance PASS | Legacy records outside selected scope are NOT CHECKED, not failures; no retroactive migration |
| F05 | Optional `object_profile` omitted | PASS | Distinct from `type` |
| F06 | Claim lacks valid source-evidence relation | FAIL | Does not imply factual falsity |
| F07 | Applicability `unknown`, `not-applicable`, `unsupported` distinguished | PASS | No coercion among states |
| F08 | Status promoted from structural PASS, QMD presence, or unreviewed claim | FAIL | No auto-promotion |
| F09a | Five distinct eligible IDs partitioned as not_assessed=0, studied=1, synthesized=2, deferred=0, unresolved_eligible=2; disposition rows link to valid receipts/targets | PASS; assessment coverage (studied+synthesized)/N = 3/5 (60%); synthesis/target-linked = 2/5 (40%) | Unresolved earns zero assessment credit; count each ID once |
| F09b | Add 2 excluded IDs with explicit reasons | PASS; excluded IDs are outside eligible N=5 | Eligible counts and ratios remain unchanged; never silently omit eligible items |
| F10a | Eligible unresolved artifact omitted from frozen denominator or counted as assessed | FAIL | Retrieval/indexing alone earns no assessment credit |
| F10b | Five eligible IDs retain known partition above; one unknown listing is confirmed not an artifact | PARTIAL scope/completeness only; eligible assessment remains 3/5 (60%), synthesis 2/5 (40%) | The unknown listing remains outside N; N=0 yields NOT APPLICABLE, not 0/0 |
| F11 | External public source citation URL | PASS | External citations allowed |
| F12 | Canonical target traversal/outside approved wiki/root, private source path, dangling target | FAIL | Does not ban external citations |
| F13 | QMD declaration represented as freshness/retrieval/truth proof | FAIL | Declaration-only scope |
| F14 | Hardware-verified claim lacks required device evidence | FAIL | No device validation performed |
| F15 | Claim cites exact source revision and document locator mapped to the claim | PASS | Provenance relation is present; does not establish truth |
| F16 | Claim requires provenance but source revision or locator is missing/mismatched | FAIL | Do not invent a locator or pin |

## Link and evidence boundaries

External public source citations are valid. Canonical target links must resolve within approved wiki/root scope; reject traversal, private/local source paths, and dangling targets. These constraints do not prove truth, rights, privacy, or publication eligibility. Preserve ADR-010/011 provenance and evidence labels.

## Safety and non-actions

- Acceptance authorizes implementation of read-only consumer checks and deterministic fixtures only; no automatic repair, rewrite, migration, backfill, or status/evidence promotion.
- No live source requests/cloning, private inventory, QMD registration/update/embed/search, device or hardware operation.
- Structural PASS proves neither factual correctness, applicability, privacy, rights, publication eligibility, freshness, retrieval, nor device behavior.
- No current corpus content is claimed to pass the accepted policy.
- ADR-012 acceptance is recorded; implementation must stay within this contract. Migration or framework upgrade requires separate authorization.
