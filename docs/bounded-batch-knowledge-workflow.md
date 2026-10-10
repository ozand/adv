# Bounded batch knowledge workflow (Accepted)

**Status:** Accepted under Issue #48 / ADR-013. This document defines a finite workflow contract; it does not authorize source acquisition, corpus migration, QMD operations, or automatic publication.

## Purpose and boundaries

Make batch research/synthesis reproducible and independently reviewable while keeping source identity, claim evidence, disposition, consumer conformance, retrieval state, and publication permission separate. Apply accepted ADR-007/010/011/012; do not redefine their fields or infer truth from retrieval/status/validation.

## Batch record

The minimal machine-readable example/checker subset is: batch/Issue identity, base and candidate SHA, owner/objective/writer, frozen input IDs/source/revision/locator/hash and eligibility, one result per eligible input, three validation-layer statuses with explicit `required` flags, declared precondition/reason for every NOT APPLICABLE layer, aggregate gate, exact-SHA read-only review declaration, durable sanitized Issue receipt pointer, and explicit release-decision field. The checker does not authenticate identities or approval. Unknown input eligibility must remain unresolved and cannot receive studied/synthesized credit until represented as a newly frozen, resolved input record.

For each batch, retain these fields in its Issue/PR record or an explicitly scoped companion artifact. [`batch-record.example.json`](batch-record.example.json) is a machine-readable synthetic example; the read-only checker validates its structure only.

| Field | Required meaning |
|---|---|
| `batch_id` | Stable human-readable identifier scoped to the governing Issue |
| `issue` | Open governing Issue URL and acceptance criteria |
| `owner` | Decision/release owner and one candidate writer |
| `objective` | Bounded outcome and explicit non-goals |
| `base` | Full consumer-repository commit on which the candidate is based |
| `inputs` | Per artifact: canonical source/repository identity, locator, immutable revision/hash when available, representation, provenance |
| `eligibility` | Eligible, excluded-with-reason, or unresolved eligibility; use ADR-011 artifact unit and frozen snapshot |
| `exclusions` | Unique artifact IDs and explicit reason, outside N |
| `limits` | Time/size/attempt limits, stop conditions, unresolved scope |
| `candidate` | Full candidate commit and content hashes for reviewed outputs |
| `results` | Per-artifact disposition/receipt/target relations under ADR-010/011 |
| `validation` | Separate universal, consumer-policy, and optional retrieval results with command/tool/version, input snapshot, exit, limitations |
| `reviewers` | Read-only review roles, exact candidate SHA, findings, verdict |
| `release` | Owner release decision and sanitized durable Issue/PR receipt linking snapshots, candidate/reviewed/delivered identities and risks |

Do not place private absolute paths, credentials, raw logs, source payloads, or sensitive corpus contents in public records. A source locator/hash is not proof of rights or truth.

## Single-writer lifecycle and exact review

1. **Scope and freeze:** confirm the open Issue, objective, exclusions, limits, and stop conditions. Freeze base commit and source-artifact snapshot identities. Moving/unavailable source identity remains unresolved; do not silently substitute it.
2. **One writer:** one writer owns the candidate tree/branch. Parallel contributors may inspect immutable inputs read-only and return findings, but do not edit that candidate. The writer serializes and integrates changes explicitly.
3. **Record results:** each eligible artifact has exactly one disposition per ADR-011. The `(source, revision, locator)` tuple is its accounting identity within a frozen snapshot and must not be duplicated under multiple IDs. `studied` requires a receipt with scope/date/reviewer/claims-or-no-claims outcome/limitations. `synthesized` additionally requires an internal `kb/wiki/` target path and explicit claim/source provenance relations. Public source URLs belong in evidence provenance, never in canonical target links. `deferred` and `unresolved` require reasons. `excluded` is not a disposition and remains outside the eligible results partition. Unknown eligibility cannot receive assessment credit until captured as a new frozen, resolved input. These are structural declarations; checker PASS does not verify evidence truth.
4. **Separate validation layers:** report (a) universal `kb-bootstrap`, (b) repository consumer policy, and (c) retrieval/index only if separately authorized and run. `NOT RUN` is never PASS. Structural/profile checks do not establish local policy, truth, rights/privacy, retrieval freshness, or device behavior.
5. **Independent exact-content review:** reviewers are read-only and record the exact candidate commit and relevant content hashes. A changed candidate invalidates review for changed bytes; review the new exact SHA. A branch name alone is not review identity.
6. **Deterministic gate:** each layer declares `required: true|false`. A required layer yields PASS/FAIL/PARTIAL/NOT RUN; an unrequired layer must be NOT APPLICABLE with a concrete precondition and reason. FAIL blocks release. PARTIAL names unresolved scope and cannot silently become PASS. All layers NOT APPLICABLE means `NOT CHECKED`, not PASS, and cannot authorize release. Overall status cannot hide a layer or unresolved input eligibility.
7. **Release receipt:** after owner decision, record batch ID, Issue/PR, base/source snapshot, candidate/reviewed/delivered commits, file hashes as needed, separate layer results, release decision, and residual risks. Keep it sanitized and durable in the governing Issue/PR; terminal logs alone are not durable evidence.

No step implies automatic publication, evidence/status promotion, reciprocal-link generation, repair, migration, QMD mutation, or source acquisition.

## Worked synthetic example (specification only)

This example illustrates fields and arithmetic only. It is not an actual source review, corpus inventory, or executed workflow test.

```text
batch_id: issue48-example-01
issue: https://github.com/ozand/adv/issues/48
base: 1e7bc44f0ff00d8504ad929898e43f3127e27f9c
inputs:
  - id: artifact-a
    source: https://github.com/example/public-docs
    revision: aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
    locator: README.md#feature-a
    eligibility: eligible
  - id: artifact-b
    source: https://github.com/example/public-docs
    revision: bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb
    locator: docs/feature-b.md
    eligibility: eligible
  - id: artifact-x
    source: https://github.com/example/third-party
    revision: cccccccccccccccccccccccccccccccccccccccc
    locator: LICENSE
    eligibility: excluded
    reason: outside declared rights scope
snapshot: frozen; distinct source+revision+locator IDs
N: 2
partition: not_assessed=0, studied=1, synthesized=0, deferred=0, unresolved_eligible=1
assessment coverage: 1/2
synthesis coverage: 0/2
unresolved scope: none
```

The partition is `N=0+1+0+0+1=2`. If complete assessment is required, the gate is PARTIAL because an eligible artifact is unresolved. The excluded artifact is visible separately and outside N. If a listing's artifact eligibility is unknown, report it outside N and mark catalog scope PARTIAL/unknown; do not claim complete catalog coverage. Its result cannot be `studied` or `synthesized`; resolve identity/eligibility under a new frozen input record before assessment. If N=0, ratios are NOT APPLICABLE, not zero percent. The checker enforces that every eligible input has one result and that layer outcomes agree with the aggregate gate; it does not compute these coverage ratios.

A sanitized receipt can summarize the separate checks, for example:

```text
universal: PASS | owner=kb-bootstrap | source pin=73277fdb... | exit=0
consumer: PARTIAL | owner=adv | candidate=<exact SHA> | exit=1
retrieval: NOT RUN | reason=not required/authorized
review: PASS | reviewer role=<role> | exact candidate=<full SHA>
release: NOT AUTHORIZED | reason=consumer layer partial
```

These placeholders are not execution evidence. Never claim binary/source identity without verifying the module import path/version. A planned fixture or worked example is not an executed test.

## Owner acceptance and implementation boundary

Owner acceptance is recorded on [Issue #48](https://github.com/ozand/adv/issues/48#issuecomment-6091040472) for the exact ADR/workflow revision described in ADR-013. This workflow is Accepted under ADR-013. Acceptance authorizes a separate implementation increment for minimal templates, read-only aggregate checks, and synthetic fixtures only. It does not establish current-corpus conformance, authorize live source acquisition/QMD operations/migration, or grant publication permission.

## Verification status

- Example manifest/result arithmetic is specification-only; no source artifacts were retrieved or assessed.
- The local read-only structural receipt checker is implemented; it requires explicit applicability for every layer, rejects NOT APPLICABLE without a concrete precondition/reason, and does not permit a PASS gate when all layers are unrequired. Unknown-eligibility artifacts cannot be assessed under that unresolved record; scope remains PARTIAL.
- The checker requires PARTIAL for eligible `not_assessed`, `deferred`, or `unresolved` dispositions and rejects non-string reasons and malformed input IDs. It rejects duplicate source-artifact tuples, validates lexical internal `kb/wiki/` targets, and parses governing Issue URLs without network access. It does not verify target existence or whether receipts, preconditions, provenance, or hashes correspond to source bytes. Reviewer/release identity and sanitization are not authenticated.
- No QMD runtime state, private corpus, or device/hardware state was inspected.
- Contract acceptance does not assert operational performance or production readiness.
