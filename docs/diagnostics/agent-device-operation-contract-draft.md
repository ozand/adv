---
type: research-draft
title: Agent-device capability-operation contract proposal
issue: https://github.com/ozand/adv/issues/37
status: draft
---

# Agent-device capability-operation contract proposal

**Status: draft / theory only.** This document proposes review questions and candidate semantics. It is not an accepted contract, public API, protocol, ABI, security scheme, architecture selection, implementation authorization, or device-operation permission. No transport is selected; MCP is not the goal.

## 1. Purpose, evidence, and non-goals

The proposal addresses how a future agent-facing operation might declare bounded inputs/outputs, effects, authority, prerequisites, and uncertain outcomes. It is informed by Issue #36's reviewed inventory at main commit `1f1868a9d2192f5d3f28f850306541e3f51fbc43`, whose six README-derived candidates are **source-documented only**. They are examples for analysis, not requirements, verified capabilities of this Cardputer, or evidence of demand. Issue #35 context is the bounded findings handoff ([output](https://github.com/ozand/adv/blob/e07c2fb30960b32f82b7ddfa75df12a1b4a72479/kb/research/2026-10-08_cardputer-agent-usage/output.md), [synthesis](https://github.com/ozand/adv/blob/e07c2fb30960b32f82b7ddfa75df12a1b4a72479/kb/research/2026-10-08_cardputer-agent-usage/synthesis.md)); it reports author claims, not adoption evidence.

Evidence labels used below:

- **Source-contract tested:** a project contract and passing source-level/fake-transport tests; not hardware/runtime verification.
- **Source-documented:** an upstream source describes an implementation or intended behavior; not independently observed.
- **Device-verified:** requires an authorized observation tied to exact installed firmware and device; none is supplied by this proposal.
- **Unknown:** evidence is absent, incomplete, or not tied to target identity/version.

Out of scope: changing ADR-006, publishing an API, implementing host/device services, granting shell or arbitrary storage/GPIO access, selecting an architecture or authentication design, and operating or flashing a device.

## 2. Candidate operation descriptor (proposal)

A future operation description could specify the following, with each value bounded and reviewable:

| Field | Proposal / unresolved point |
|---|---|
| Identity | Stable operation ID and descriptor version; exact naming/compatibility policy is unresolved. |
| Inputs | Typed schema, allowed values, maximum sizes, normalization, required vs optional fields; reject unknown fields by default. |
| Outputs | Typed schema, maximum bytes/items, redaction/minimization, truncation marker; no raw log/key pass-through. |
| Target and prerequisites | Device/session identity evidence, required connection/state, firmware compatibility evidence; absent evidence remains `unknown`. |
| Effects | Multi-axis declaration: cached vs fresh I/O; volatile state vs persistent storage; physical output vs external-target state. Read-only is not a sufficient label. |
| Authority | Minimum principal/scope required; explicit allowlist and target binding; an adapter cannot widen authority. Identity/authentication design remains unresolved. |
| Human approval | If required, bind approval to the exact operation, arguments/artifact, target, scope and expiry. Agent annotations alone do not confer authority. |
| Limits | Explicit input/output caps, time/resource bounds, concurrency/lease rules, cancellation semantics and stop conditions. Actual values require per-operation evidence/review. |
| Result lifecycle | Preserve the distinctions in §3; never convert timeout/cancellation into proof of no effect or successful completion. |
| Retry/reconciliation | Declare idempotency and replay behavior. No automatic retry of an operation with uncertain outcome unless a separately reviewed idempotency/reconciliation mechanism proves safety. |
| Audit/data retention | Record only minimal operation ID, target binding, outcome and evidence needed for accountability; retention and privacy policy remain undecided. |
| Recovery | State whether rollback exists, who owns it, and what evidence confirms it. Cancellation is not rollback. |

These are draft fields, not a normative schema or accepted security mechanism. Capabilities without explicit bounded inputs/effects/authority should remain unavailable rather than inheriting broad permissions.

## 3. Lifecycle, uncertainty, cancellation, and retry

A future transport-neutral result model should distinguish, at minimum:

1. request parsed and validated;
2. authority/confirmation checked;
3. transmission attempted;
4. complete transport write observed;
5. device acknowledgement received;
6. operation reported executed/completed;
7. result independently verified, if such verification exists.

These are not interchangeable success states. A partial write, lost acknowledgement, timeout, reboot, disconnect or cancellation can leave an effect uncertain. Report `unknown`/`inconclusive` when completion cannot be established; do not infer failure, success, or rollback. If cancellation is requested, report cancellation request/acknowledgement separately from operation state. Retry must not silently repeat a possibly non-idempotent operation.

**ADR-006 compatibility boundary:** the accepted source contract remains exactly `status`, `sd_test`, `run <ID>`, and `result <ID>`. It defines fixed v1/v2 envelopes and bounds, one RAM-retained result, duplicate-ID cache behavior, reset loss, read-only `result`, and opt-in one-shot SD behavior. Its accepted contract is not device/runtime authorization or hardware PASS. This proposal does not change or reinterpret that contract.

The owner-accepted RAM-only diagnostic run record is lost on reset. After reset or uncertain loss, its old outcome is `UNKNOWN`; do not automatically rerun the diagnostic. A future boot/session identifier could help bind operation identity, but is only a proposal and not part of the current ADR-006 ABI.

## 4. Effects, permissions, and safety boundaries

Effects should be described by operation-specific dimensions, not a single `read_only=true` flag. Examples of distinct dimensions include: cached report versus fresh sensor I/O; volatile sensor initialization versus persistent NVS/storage writes; physical RF/audio output versus an external service/device state change. A supposedly observational operation can still initialize hardware, emit RF/audio, or disclose private state.

Authority should be least-privilege and target-bound. Human confirmation, when required, should present the exact operation and target and must not be synthesized from an agent-provided annotation. Potential server-side single-writer/lease and allowlist mechanisms are candidate requirements for later design, not accepted architecture. MCP/tool annotations can describe intent but are not enforcement.

Do not permit arbitrary shell, arbitrary file or memory access, bulk storage reads, unrestricted GPIO, or silent persistent configuration changes. Distinguish the existing owner-approved, bounded 64-KiB SD diagnostic write in Issue #2/ADR-006 from any proposed whole-SD/file/resource read: the latter would require separate privacy, authority, retention and recovery review. This proposal authorizes neither.

## 5. Transport invariants; no architecture choice

A future host adapter, device-side service, or hybrid may have different prerequisites and trust boundaries, but none may expand the operation's declared authority, remove a required confirmation, change effect semantics, or conceal uncertain outcomes. Any adapter must preserve bounds and report transport/application/device/verification stages separately.

This document does not rank or choose host-side CLI/MCP, device network MCP, or hybrid. Authentication, identity, secure-channel, deployment and recovery details are unresolved decisions for owner/security review before any implementation. A transport label does not itself make an operation safe or authorized.

## 6. Illustrative capability mappings (maximum three; not approved operations)

| Issue #36 source-documented candidate | Illustrative contract questions only | Evidence / authority caveat |
|---|---|---|
| Notification display — [ntfy README](https://github.com/forshaws/cardputer-ntfy/blob/dba7143b0290b106bd6b6ae2c8f7b93d36bce48c/README.md), commit `dba7143b0290b106bd6b6ae2c8f7b93d36bce48c` | Bound topic identity, message size, retained history and sensitive-content handling; distinguish fetch from local display/storage. | README-reported only; topic authorization, privacy and SD retention are unknown. Not verified on target. |
| Explicit broker action — [WesTek MQTT README](https://github.com/w35m17h/cardputer-mqtt/blob/48930a30d7d787d695b95fd2b2e62c7b7bb61465/README.md), commit `48930a30d7d787d695b95fd2b2e62c7b7bb61465` | Bind allowed topic, payload, target and confirmation; distinguish message publish from broker/device acknowledgement and actual external effect. | README-reported only; this can change external state. No permission model or device execution was verified. |
| Physical coding-agent approval/status surface — [Claude Buddy Cardputer fork README](https://github.com/y88huang/claude-desktop-buddy-cardputer/blob/257d3d84435c11a98e9dc376257acffda2a633cb/README.md), commit `257d3d84435c11a98e9dc376257acffda2a633cb` | Bind any approval to exact pending action/target/scope and expiration; distinguish displayed prompt from authenticated/accepted decision. | README-reported BLE/developer-mode behavior only; security, accidental input and installed runtime are unknown. No approval was sent. |

Examples do not establish that these capabilities exist on this project's installed device, are safe, or are desired. The general diagnostic commands are not counted as new examples; they remain governed by ADR-006.

## 7. Unresolved owner/security decisions

- Which principal owns operation authority, how identity is established, and how revocation works?
- Which operations require human approval, and what exact operation/target/effect must be shown?
- What bounds and concurrency/lease behavior are justified by evidence for each operation?
- How should lost acknowledgement, reset, timeout, cancellation and partial writes be represented and reconciled?
- Which data may be retained or displayed, for how long, and under what privacy controls?
- What recovery is possible for each persistent/external effect, and who may authorize it?
- Which hardware owner review and independent security review are required before accepting any public contract?

No choices are made here. A chosen public contract or trust-boundary change requires a separate accepted ADR before implementation. Hardware-owner and independent-review records must be added only after those reviews actually occur.

## 8. Issue #37 acceptance traceability

| Acceptance criterion | Draft evidence / status |
|---|---|
| Bounded operation input/output, effects/authority, timeout/errors/uncertainty, retry/idempotency | §§2–4 give proposed fields and semantics; per-operation numeric limits and actual schemas remain unresolved. |
| Preserve ADR-006 four commands; differences unresolved | §3 lists the unchanged four commands and explicitly excludes changes. |
| Transport-neutral; transport cannot broaden authority or hide uncertainty | §5 states invariants; no transport selected. |
| Traceable to Stage A; unsupported assumptions and owner/security questions marked | §1 and §6 cite pinned #36 evidence; §7 lists unresolved decisions; all examples source-documented only. |
| Hardware-owner coordination and independent review recorded; proposal clearly labeled | Hardware-owner read-only review of exact draft commit `a8d64246bd8df0061b816851c1672f70f0014e4d` returned PASS as draft-only proposal on 2026-10-08; no API/security approval or major blocker was conveyed. Independent content/structure review also returned PASS on that same draft. These reviews do not constitute owner acceptance, security approval, or an accepted contract. The current post-receipt candidate must be re-reviewed before treating this criterion as final for the updated commit. |
| Future public contract/trust-boundary implementation gated on accepted ADR and authorization | §§1, 7 state separate accepted ADR/authorization gate. |
| No API/code/firmware/device/QMD mutation | Drafting-only scope; verify at review/delivery. |

## References

- [Issue #37](https://github.com/ozand/adv/issues/37)
- [Issue #36 Stage A inventory](https://github.com/ozand/adv/tree/1f1868a9d2192f5d3f28f850306541e3f51fbc43/kb/research/2026-10-08_cardputer-capability-inventory)
- [ADR-006](https://github.com/ozand/adv/blob/1f1868a9d2192f5d3f28f850306541e3f51fbc43/docs/adr/ADR-006-hardware-diagnostic-serial-json.md)
