# Proposed source-to-knowledge disposition contract

**Status:** Proposed under Issue #46/ADR-011; not adopted. No backfill/current-corpus claim is authorized.

## Purpose and boundaries

Extend Issue #5 accounting; do not create a second catalog, source inventory, clone manifest, or QMD index. Keep catalog listing rows, normalized repository candidates, source revisions, document artifacts, canonical targets, and indexed documents distinct but linkable. Preserve aliases/forks. Apply ADR-010 claim/source evidence semantics and ADR-007/004 publication boundaries. No private corpus/QMD state was inspected; no source acquisition, cloning, indexing, migration, or implementation is authorized.

## Accounting unit and identity

Primary unit: a source-artifact record = canonical source/repository identity + exact revision when known + document/path locator. Different revisions are distinct artifacts. A frozen snapshot declares source set, provenance, eligibility, and deduplication. Historical counts/index hits do not establish current completeness.

## Acquisition versus disposition

`retrieved` and `indexed` are separate acquisition/retrieval flags, not disposition states. Retrieved/indexed artifacts can remain unassessed; indexing does not prove study. First determine eligibility for the frozen snapshot. Explicitly excluded records are outside the eligible denominator and require an exclusion reason; they are not a disposition state. Every eligible artifact has exactly one current primary disposition:

| State | Meaning | Required evidence |
|---|---|---|
| `not-assessed` | No substantive assessment | Optional queue reason; not a negative finding |
| `studied` | Bounded source scope substantively reviewed | Receipt records scope/date/reviewer, claims or no-claims outcome, limitations and relevant review decisions |
| `synthesized` | Source claim represented in canonical knowledge | Assessment receipt plus at least one explicit target relation and claim/source provenance |
| `deferred` | Assessment intentionally postponed | Reason; optional revisit trigger/date |
| `unresolved` | Eligible artifact identity/revision/access/rights/assessment outcome remains unknown | Required reason; included in denominator and disposition partition; no assessment coverage credit |

A `studied` state requires an assessment receipt; opening/indexing is insufficient. Review with no reusable claims remains `studied`, not `synthesized`. Synthesis does not prove truth, completeness, applicability, or device verification. Targets are zero-to-many per artifact; multiple artifacts may support a target. Do not infer reciprocal links. Reassessment appends dated history and requires a new receipt; coverage counts current state only. No automatic promotion from QMD, stable status, links, or validator success.

## Coverage denominator and arithmetic

Each report declares a frozen snapshot, eligibility/deduplication rules, unit, explicit exclusions, and unresolved count. `N` is the number of distinct eligible source-artifact records (source identity + revision + document locator), not catalog rows, repository candidates, clone folders, Markdown documents, or QMD hits. An artifact known to be eligible but lacking assessment/access evidence is `unresolved`, included in `N`, and earns no assessment/synthesis credit. A listing/candidate whose identity or eligibility cannot be resolved is reported outside `N` as unresolved scope; the report must mark coverage partial/unknown rather than imply complete catalog coverage.

Eligible artifacts partition exactly once by current disposition:

`N = not_assessed + studied + synthesized + deferred + unresolved_eligible`.

Explicitly excluded records and unresolved listing/candidate identities are reported separately from this eligible-artifact partition. Never mix units or snapshots. Report counts, numerator, denominator, exclusions, unresolved scope and snapshot reference together.

- Assessment coverage = (`studied` + `synthesized`) / `N`.
- Synthesis coverage = `synthesized` / `N`.
- Target-linked synthesized-artifact coverage = eligible `synthesized` artifacts with at least one target relation / `N`; by definition this equals synthesis coverage because synthesized requires a target link. Report distinct-target count separately as a descriptive count, not as artifact coverage.
- If `N = 0`, ratios are not-applicable, not 0%.
- Unresolved eligible artifacts stay in `N` with zero assessment/synthesis credit; unresolved identities outside the artifact unit are separately reported as unresolved scope and make catalog-wide coverage partial/unknown.

## Worked examples (specification arithmetic only)

Example A: a frozen set has 12 eligible artifacts: 2 `not-assessed`, 3 `studied`, 2 `synthesized`, 3 `deferred`, and 2 `unresolved`. Separately report one unresolved listing identity and two explicitly excluded records outside `N`. Assessment coverage is (3+2)/12 = 41.7%; synthesis coverage is 2/12 = 16.7%. Because each synthesized artifact requires at least one target link, target-linked synthesized-artifact coverage is also 2/12 = 16.7%. If those two artifacts link to the same canonical target, report one distinct target separately; do not use target count as an artifact-coverage numerator. These are illustrative values, not current corpus facts.

Example B: an artifact that is retrieved and indexed but has no assessment receipt remains `not-assessed`; it enters `N` only if the declared eligibility rule includes it and counts in neither study nor synthesis numerator.

Example C: one synthesized artifact linked to two targets counts once in synthesis and target-linked artifact coverage; report the two distinct targets separately. Two synthesized artifacts supporting one target count as two artifacts in both coverage numerators and one distinct target. These examples are not executable tests, audited manifest rows, or evidence that any source was actually reviewed.

## Relationship to Issue #5 and adoption boundary

Extend existing Issue #5 catalog/candidate/manifest/QMD identities; do not duplicate them. Historical Issue #5 totals are historical receipts, not current counts. No private manifest or local corpus was inspected.

This finite contract is proposed for owner review; ADR-011 acceptance is required before adoption/backfill. No serialization, manifest change, companion-file choice, live scan, cloning, source acquisition, QMD/index operation, or migration is authorized by this proposal.
