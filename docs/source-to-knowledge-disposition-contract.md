# Proposed source-to-knowledge disposition contract

**Status:** Proposed under Issue #46/ADR-011; not adopted. No backfill/current-corpus claim is authorized.

## Purpose and boundaries

Extend Issue #5 accounting; do not create a second catalog, source inventory, clone manifest, or QMD index. Keep catalog listing rows, normalized repository candidates, source revisions, document artifacts, canonical targets, and indexed documents distinct but linkable. Preserve aliases/forks. Apply ADR-010 claim/source evidence semantics and ADR-007/004 publication boundaries. No private corpus/QMD state was inspected; no source acquisition, cloning, indexing, migration, or implementation is authorized.

## Accounting unit and identity

Primary unit: a source-artifact record = canonical source/repository identity + exact revision when known + document/path locator. Different revisions are distinct artifacts. A frozen snapshot declares source set, provenance, eligibility, and deduplication. Historical counts/index hits do not establish current completeness.

## Acquisition versus disposition

`retrieved` and `indexed` are separate acquisition/retrieval flags, not disposition states. Retrieved/indexed artifacts can remain unassessed; indexing does not prove study. Each eligible artifact has exactly one current primary disposition:

| State | Meaning | Required evidence |
|---|---|---|
| `not-assessed` | No substantive assessment | Optional queue reason; not a negative finding |
| `studied` | Bounded source scope substantively reviewed | Receipt records scope/date/reviewer, claims or no-claims outcome, limitations and relevant review decisions |
| `synthesized` | Source claim represented in canonical knowledge | Assessment receipt plus at least one explicit target relation and claim/source provenance |
| `deferred` | Assessment intentionally postponed | Reason; optional revisit trigger/date |
| `excluded` | Explicitly outside eligible set or removed from review | Required reason; report outside eligible denominator |
| `unresolved` | Identity, revision, access, rights, or disposition unknown | Required reason; report separately |

A `studied` state requires an assessment receipt; opening/indexing is insufficient. Review with no reusable claims remains `studied`, not `synthesized`. Synthesis does not prove truth, completeness, applicability, or device verification. Targets are zero-to-many per artifact; multiple artifacts may support a target. Do not infer reciprocal links. Reassessment appends dated history and requires a new receipt; coverage counts current state only. No automatic promotion from QMD, stable status, links, or validator success.

## Coverage denominator and arithmetic

Each report declares frozen snapshot, eligibility/deduplication rules, unit, exclusions, and unresolved count. `N` is the number of distinct eligible source-artifact records (source identity + revision + document locator), not catalog rows, repository candidates, clone folders, Markdown documents, or QMD hits. If eligibility/identity is undetermined, coverage is unknown.

Eligible artifacts partition once by current primary disposition:

`N = not_assessed + studied + synthesized + deferred`.

Excluded and unresolved are reported separately, not silently included in `N`. Never mix units or snapshots. Report counts, numerator, denominator, exclusions, unresolved count, and snapshot reference together.

- Assessment coverage = (`studied` + `synthesized`) / `N`.
- Synthesis coverage = `synthesized` / `N`.
- Target-linked synthesis coverage = distinct eligible synthesized artifacts with at least one target link / `N`; count artifacts, not links.
- If `N = 0`, ratios are not-applicable, not 0%.

## Worked examples (specification arithmetic only)

Example A: a frozen set has 10 eligible artifacts: 2 `not-assessed`, 3 `studied`, 2 `synthesized`, and 3 `deferred`. Separately report one unresolved identity and two excluded records. Assessment coverage is (3+2)/10 = 50%; synthesis coverage is 2/10 = 20%. If one synthesized artifact has a target link, target-linked coverage is 1/10 = 10%. These are illustrative values, not current corpus facts.

Example B: an artifact that is retrieved and indexed but has no assessment receipt remains `not-assessed`; it enters `N` only if the declared eligibility rule includes it and counts in neither study nor synthesis numerator.

Example C: one artifact linked to two targets counts once in target-linked coverage; two artifacts supporting one target count as two artifacts and one distinct target. These examples are not executable tests, audited manifest rows, or evidence that any source was actually reviewed.

## Relationship to Issue #5 and adoption boundary

Extend existing Issue #5 catalog/candidate/manifest/QMD identities; do not duplicate them. Historical Issue #5 totals are historical receipts, not current counts. No private manifest or local corpus was inspected.

This finite contract is proposed for owner review; ADR-011 acceptance is required before adoption/backfill. No serialization, manifest change, companion-file choice, live scan, cloning, source acquisition, QMD/index operation, or migration is authorized by this proposal.
