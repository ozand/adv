# D02 — proposed contracts and fixtures

**Status:** proposal for review; not a stable API, accepted schema, or enforcement implementation.

**Issue:** [#69](https://github.com/ozand/adv/issues/69) · **Epic:** [#66](https://github.com/ozand/adv/issues/66)

**Prerequisite for acceptance:** D01 / #68 decisions and owner/reviewer approval.

**Research receipt:** [Issue #69 comment](https://github.com/ozand/adv/issues/69#issuecomment-6129685648).

**Proposed decision records:** [ADR-019](../../adr/ADR-019-deviceops-operation-contract-proposals-remain-non-normative-until-reviewed.md) (process boundary) and [ADR-021](../../adr/ADR-021-deviceops-status-contract-and-bounds.md) (candidate status-only format and bounds).

**Executable candidate:** [private runtime PR #4](https://github.com/ozand/deviceops/pull/4), currently based on bootstrap `e56fd6a628a6bd7137b4adb48b8c646f7674263d`; candidate head is recorded in the Issue #69 handoff. This PR is proposed-only and does not publish a stable API.

This proposal sharpens `docs/deviceops/CONTRACTS.md` without changing firmware wire contracts, choosing an implementation stack, or authorizing hardware/network access. “MUST” below means a candidate requirement for review, not an existing runtime guarantee.

## 1. Contract layers and identity

Keep the following identifiers distinct:

| Identifier | Owner and purpose | Reuse rule |
|---|---|---|
| `request_id` | Client-generated idempotency key, scoped by authenticated principal and target | Same normalized request returns its existing operation during the advertised retention window; a different normalized request conflicts |
| `operation_id` | Host-generated durable job identity | Never sent to firmware as its short run ID |
| `firmware_run_id` | Adapter-generated 1–12 uppercase ASCII alphanumeric ID for ADR-006/009 firmware result slots | Unique within a known firmware session; reset invalidates claims of retained result; do not blindly reuse after uncertainty |
| `session_generation` | Host adapter generation for a transport session | Bookkeeping only; not a firmware boot counter or hardware attestation |

Binding/capability evidence SHOULD include its observation time, origin (`cached` or `fresh`), relevant profile/firmware claim, and confidence. An administrative `device_id` alone MUST NOT be represented as attested physical identity.

## 2. Candidate schemas and bounds

The formal JSON Schema dialect and exact fields remain subject to review. A status-only candidate is now staged as `deviceops.request.v0` and `deviceops.result.v0` in private PR #4; the `.v0` labels are draft identifiers, not accepted stable API versions. Candidate host bounds are request JSON ≤4096 UTF-8 bytes, result receipt JSON ≤1024 bytes, identifiers ≤128 characters, reason codes ≤64 characters, queue depth ≤32, retained jobs ≤128, and ≤64 events/job. These values are proposed finite test boundaries, not measured or accepted operational defaults. Firmware frame limits remain unchanged. Other operation profiles, pagination, retention TTL, plan/grant schemas, and stable error mappings remain open for later review. The wider proposal is to define versioned schemas for:

- **Binding/capability snapshot:** target reference, observed session generation, profile and firmware evidence, named capabilities, freshness and expiry.
- **Operation request:** `request_id`, target reference, capability ID/version, and operation-specific arguments validated against a closed schema. Unknown fields and unsupported versions are rejected before effects.
- **Accepted operation:** `operation_id`, request digest, target/session binding, accepted timestamp, lifecycle and event cursor.
- **Plan/grant reference:** immutable digest, exact target and capability scope, expiry, and issuer reference; the agent cannot mint its own grant.
- **Result/evidence receipt:** bounded terminal result, stages, transmission/ack/effect/verification axes, provenance, and evidence references.

Each schema MUST declare enforceable maxima for encoded request/response bytes, individual strings and collections, log page bytes, queue depth, retained jobs/events, plan/grant TTL, and client wait timeout. D02 acceptance requires each chosen maximum to have a positive boundary fixture and a one-over-limit rejection fixture. The status-only draft proposes the values above; queue/retention enforcement, result-encoding boundary, TTL, pagination and wait-timeout behavior are not yet implemented by the contract PR. Host wait deadline MUST be distinct from any device execution deadline. A host timeout does not prove that the device stopped.

Closed-object validation is the default: reject unknown keys, duplicate/ambiguous identifiers, malformed encodings, non-finite numbers, and values outside the declared limits before enqueue or I/O. Truncation is never silent; if a bounded presentation truncates, mark it and preserve the underlying operation status separately.

## 3. Lifecycle versus execution and evidence axes

Candidate logical states:

- `accepted` — durable host job accepted; not yet proof of dispatch.
- `running` — executor began the declared operation.
- `succeeded`, `failed`, `inconclusive`, `cancelled` — terminal outcomes of the declared host operation.

`queued` may be represented as a stage or non-terminal state, but the final schema must choose one representation consistently. Stages (for example `preflight`, `connecting`, `writing`, `awaiting_device`, `verifying`) MUST NOT be conflated with logical outcome.

Keep these independent evidence dimensions:

- transmission: `not_attempted | partial | complete | unknown`;
- device acknowledgement: `not_received | received | unknown`;
- effect certainty: `none | known_partial | known_completed | unknown`;
- verification: `not_attempted | passed | failed | inconclusive`;
- evidence level: `source_documented | source_tested | fake_tested | client_tested | device_observed | externally_verified` (per claim, not global).

`succeeded` means only that the declared operation postcondition is satisfied. A successful `status` read is not a board-health PASS. Physical checks use profile-defined `PASS | FAIL | NOT_TESTED | INCONCLUSIVE`; host state MUST NOT derive these values. Timeout, lost acknowledgement, partial write, reset, or late/unmatched response with uncertain effect yields `inconclusive` unless stronger evidence resolves it. Never automatically retry a potentially mutating operation solely because its host wait expired.

## 4. Request deduplication, cancellation, and late results

Deduplication key candidate: authenticated principal + target + `request_id`; compare a canonical normalized-payload digest. Identical retries within declared retention return the same host operation. Same scoped key with different digest returns conflict. Reusing a request ID for another target is a distinct key and remains subject to that target's policy. This is host request deduplication, not exactly-once device execution.

A client cancelling its wait is not the same as cancelling an operation. A cancellation request MUST produce a distinct event and may yield `cancelled` only if dispatch has not occurred or safe stop is confirmed according to the capability contract. Otherwise retain truthful in-progress/unknown effect state. Cancellation never implies rollback.

A result query is a distinct read operation. It MUST bind to the requested host `operation_id`, expected capability/result family, target and current valid session. A delayed result frame received in a status phase is a protocol mismatch, not a successful status reply and not proof that the intended result query ran. Preserve it as ambiguous evidence; do not silently drain/flush, relabel, or reuse it. Host write completion proves only that bytes were accepted by the host transport API, not that the device executed the command.

## 5. Error envelope proposal

Use stable, bounded reason codes; exclude raw upstream strings from machine instructions or command construction. Candidate families (final enum/mapping remains open): `invalid_request`, `unsupported_version`, `limit_exceeded`, `permission_denied`, `identity_ambiguous`, `unsupported_capability`, `incompatible_firmware`, `device_busy`, `session_changed`, `transport_error`, `ack_timeout`, `result_unavailable`, `request_conflict`, `plan_changed`, `artifact_untrusted`, `verification_failed`, `internal_error`.

An error envelope should identify the failed phase and whether an operation was accepted, without falsely implying that an error means no external effect. Include a safe correlation reference, not secrets, raw frames, full transport locators, or unrestricted device text.

## 6. Operation catalogue and effect declarations

MVP catalogue is intentionally narrow and must be the intersection of adapter implementation, known compatibility evidence, and policy. Candidate read/diagnostic operations: `device_list` (registry only; no port open), `device_inspect` (cached by default), `device_capabilities`, explicit `device_connect`, `diagnostic_start` for an allowlisted profile, `operation_get`, and distinct `diagnostic_result_query`. Each descriptor declares its input/output schema, target/session prerequisites, firmware compatibility evidence, effect dimensions, authority, timeout, concurrency, retention, retry, cancellation, and recovery.

A single `read_only` boolean is insufficient. Describe cached versus fresh I/O, transport open/reset behavior, volatile setup, persistent writes, physical audio/RF output, external network effects, and data disclosure. Deploy/config/log capabilities remain outside this initial fixture slice; `arbitrary_command`, shell, raw audio, bulk filesystem reads, and unrestricted GPIO are excluded.

## 7. Deterministic fixture plan (fake-only)

Fixtures use synthetic targets, IDs, frames, times and evidence. The harness MUST have no serial/network/device backend and fail closed if one is requested. No real device identifiers, raw logs, credentials, or captured frames belong in tracked fixtures.

| Fixture | Expected result | Required invariant |
|---|---|---|
| Minimum valid request and each declared maximum | Accepted by schema layer | Exact version, bounds, and canonical digest |
| Each field one over limit; unknown field; malformed enum/encoding | Rejected before job enqueue/effects | No dispatch, bounded error |
| Same principal/target/request ID and same canonical payload | Existing operation returned | No duplicate job or device send |
| Same principal + target + request ID, changed canonical payload | Conflict | No dispatch |
| Same request ID at a different target | Distinct scoped key; evaluate target policy | Never misclassify as same-key payload conflict |
| Partial write, full write/lost ACK, reset after dispatch | `inconclusive`, effect unknown as appropriate | No automatic mutating retry |
| Wrong session, stale firmware evidence, mismatched result family/ID | Reject or inconclusive | Never relabel a late frame as requested result |
| Cache replay from a prior session generation after reset/re-enumeration | `inconclusive` until current evidence is observed | Prior cached status/result cannot be relabeled as fresh/current |
| Firmware-marker mismatch or unknown marker | Reject/deny compatibility before adapter dispatch; do not probe mutating commands | Marker is informational evidence, never identity or authorization |
| Status request receives delayed terminal result frame | Protocol mismatch retained as ambiguity | Does not count as status success; does not claim result query ran |
| Cancellation before dispatch / after possible dispatch | Cancelled only for safe pre-dispatch stop; otherwise honest unresolved state | Cancel is not rollback |
| Physical check has no observation / all-zero measurement | `NOT_TESTED` or `INCONCLUSIVE` per profile | Never infer physical PASS/FAIL from host success or software completion |
| Queue, retained-job/event, TTL, and page limits at boundary and over | Boundary accepted; over-limit rejected/expired per declared rule | Resource limits explicit and deterministic |
| Host CLI-like and MCP-like fixture clients call same fake core | Equivalent normalized results and denials | No client can widen capability or erase uncertainty |

The private runtime PR contains candidate serialized request/result schemas, a pure request validator, and runnable synthetic fixtures for malformed/unknown/duplicate/oversize requests, status-vs-physical verification, cache replay after session generation change, firmware-marker mismatch, late result ambiguity, and no-backend fixture execution. At its current candidate head, these are proposed implementation evidence only; result bound/enforcement, all resource maxima, status transition enforcement, broader operation semantics, and independent review remain open. This document and the private PR do not establish a stable API or hardware evidence.

## 8. Compatibility and decision gates

Preserve accepted ADR-006/ADR-009 source contracts. Do not change firmware wire shapes or send host `operation_id` directly as firmware ID. A firmware result retained only in RAM is unavailable after reset; do not fabricate persistence. Audio remains explicitly opt-in and outside the initial MVP catalogue; no result implies audibility or physical pass.

This draft does not select a stable API, schema dialect, implementation language/runtime, persistent store, transport SDK, trust/grant design, or exact bounds. D01 and owner/security review must resolve relevant architecture and trust questions. An accepted contract or implementation gate requires an ADR update/new ADR as appropriate, exact reviewed candidate SHA, schema/fixture validation, and explicit owner decision. No hardware, serial, network, package installation, runtime, or deployment operation is authorized by this proposal.
