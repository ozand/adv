# Proposed Cardputer consumer-validation contract

**Status:** Proposed under Issue #47 and ADR-012; not adopted or implemented. No migration, enforcement, repair, QMD refresh, or device/runtime operation authorized.

## Scope and compatibility

Compose local consumer policy with universal `kb-bootstrap`; do not replace it or claim current corpus conformance. Universal validation requires nonempty extensible `type`; `title` remains universally optional. ADR-010 recommends `title` for adv canonical cards, but this proposal creates no mandatory title rule or retroactive legacy migration. Optional `object_profile` remains distinct from `type`.

Framework source reference pin: `73277fdb3e54184901f67268bc676a562b0a677a`. Installed `kb-bootstrap` v0.4.0 receipt is associated with source commit `db18df399ee2e7e236b4df6699b5d4892fc9c04e`; matching version text does not prove binary/source identity.

## Report layers

A future report distinguishes:

| Layer | Reports | Does not establish |
|---|---|---|
| Universal structural/profile | Named framework invocation/version and supported OKF profile | Local policy, truth, privacy, rights, device behavior |
| Repository graph | Dead links, orphans, evidence links | Semantic correctness or publication permission |
| QMD declaration/configuration | Declared configuration only | Runtime registration, freshness, retrieval, embeddings, truth |
| Cardputer consumer policy | Proposed ADR-010/011 checks | Source truth or device verification |

Until ADR-012 is accepted and checks are implemented, report consumer policy **not implemented**, never PASS. A failure in one layer does not redefine another; prior validation does not retroactively pass future policy.

## Proposed deterministic fixture contract

These are expected outcomes for future fixtures, not implemented tests. Fixture PASS means only rule behavior, never factual truth.

| ID | Input | Expected local outcome | Universal result/notes |
|---|---|---|---|
| F01 | Nonempty extensible `type`, valid claim/source evidence, explicit applicability | PASS | Universal profile PASS |
| F02 | Missing or empty `type` | FAIL | Universal profile FAIL |
| F03 | Unknown but nonempty `type` | PASS | Extensibility preserved |
| F04 | Adv card lacks `title` | PASS; recommendation warning only | Not universal failure; no legacy migration |
| F05 | Optional `object_profile` omitted | PASS | Distinct from `type` |
| F06 | Claim lacks valid source-evidence relation | FAIL | Does not imply factual falsity |
| F07 | Applicability `unknown`, `not-applicable`, `unsupported` distinguished | PASS | No coercion among states |
| F08 | Status promoted from structural PASS, QMD presence, or unreviewed claim | FAIL | No auto-promotion |
| F09 | Disposition has receipt, disposition, canonical target, denominator accounting | PASS | Per accepted ADR-011 |
| F10 | Eligible unresolved/unassessed artifact omitted from frozen denominator | FAIL | Retrieval/indexing alone earns no assessment credit |
| F11 | External public source citation URL | PASS | External citations allowed |
| F12 | Canonical target traversal/outside approved wiki/root, private source path, dangling target | FAIL | Does not ban external citations |
| F13 | QMD declaration represented as freshness/retrieval/truth proof | FAIL | Declaration-only scope |
| F14 | Hardware-verified claim lacks required device evidence | FAIL | No device validation performed |

## Link and evidence boundaries

External public source citations are valid. Canonical target links must resolve within approved wiki/root scope; reject traversal, private/local source paths, and dangling targets. These constraints do not prove truth, rights, privacy, or publication eligibility. Preserve ADR-010/011 provenance and evidence labels.

## Safety and non-actions

- Proposal only; no validator/fixture implementation, automatic repair, rewrite, migration, backfill, or status/evidence promotion.
- No live source requests/cloning, private inventory, QMD registration/update/embed/search, device or hardware operation.
- Structural PASS proves neither factual correctness, applicability, privacy, rights, publication eligibility, freshness, retrieval, nor device behavior.
- No current corpus content is claimed to pass proposed policy.
- ADR-012 acceptance is required before implementation or enforcement. Migration or framework upgrade requires separate authorization.
