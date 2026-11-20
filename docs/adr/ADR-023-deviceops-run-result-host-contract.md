# ADR-023: Separate finite ADV run/result from the accepted STATUS operation

**Status**: Proposed — owner acceptance required before runtime implementation
**Date**: 2026-10-20
**Authors**: DeviceOps adapter lane
**Supersedes**: None
**Related**: ADR-006 (ADV serial protocol), ADR-009 (opt-in audio), ADR-021 (accepted STATUS-only host contract), Issue #72

## Context

Issue #72 asks DeviceOps to support the already-defined ADV `run <ID>` / `result <ID>` protocol. Published private runtime PR #18 at `0c0dacc60ceb26b8671503787f8e46cd5e012bb1` and adapter PR #14 at `762c22ce28f329eb3011725b60db9091336e56e0` expose a STATUS-only adapter (`status\n`). Accepted ADR-021 intentionally accepts only `diagnostic_start` / `STATUS`; its request/result shape must not be silently broadened. The pinned host parser is ADV `7e096a15705570282e8ccc1721c24d842f969609:scripts/adv_diagnostic_cli.py`, SHA-256 `f7afb6489ae736b365612dfc7d9152174e41465ef3856be06559c0d0aed11b1d`.

ADR-006 source contract: run IDs are 1–12 uppercase ASCII alphanumeric; one volatile result slot exists; exact-ID run repeats return cached result, other IDs are rejected while occupied; reset loses the slot; `result <ID>` is read-only. No device execution or physical behavior was inspected for this proposal.

### Problem statement

Define whether and how the host can represent one finite firmware run and its separate result lookup without changing STATUS semantics or replaying a run after uncertain transmission.

### Prior art

ADR-006 already defines the firmware wire commands and cache; this proposal adds only a host-facing contract boundary. ADR-021 defines a different STATUS-only host profile and is not a precedent for broadening its schema.

## Decision

**Proposed recommendation:** define run and result as a separate host operation profile, distinct from `diagnostic_start` / `STATUS`; preserve the existing ADV wire format exactly.

### What this IS

- A bounded, distinct host-level run operation with a host-generated operation ID and a separate read-only result query referencing that host operation ID. The exact request/result representation and enum mapping remain explicit owner decisions below; ADR-021 types are not implicitly widened.
- A firmware run ID is adapter-generated, 1–12 uppercase ASCII alphanumeric, recorded as provenance, and bound to the active transport/session generation. It is never accepted as the host operation ID or as authorization input.
- The adapter issues at most one `run <ID>` frame per accepted host run. A complete host write is not a device acknowledgement. Partial/failed write, timeout, lost acknowledgement, reset/session loss, malformed or mismatched response yields an inconclusive outcome and never automatically retries run.
- The separate result operation references a prior host operation ID, resolves its bound firmware ID/session mapping, and issues only bounded read-only `result <ID>`; it cannot submit/replay run. Busy slot, wrong/unknown ID, unavailable mapping, empty slot after reset or unavailable result yields explicit non-success/inconclusive status; never fabricate a result or physical PASS.
- Mapping lifetime is scoped to the known transport session/generation. After process restart, transport reopen or firmware reset without a verifiable same-session cache, mapping is unavailable and must not authorize run replay or fabricated receipt. Durable mapping policy is an unresolved owner decision; proposed initial behavior is fail closed rather than persisting a claim of device-slot continuity.
- Existing principal/target/request dedup still applies to host operations; it does not extend firmware volatile result lifetime or promise exactly-once device execution.

### What this IS NOT

- A change to firmware, ADR-006 command/frame semantics, or ADR-021 STATUS schema/meaning.
- Permission for real serial/COM/USB access, automatic `sd_test`, audio, reset, flash, service, or hardware testing.
- A claim that software result states establish physical PASS, persistent storage across reboot, or exactly-once device execution.

### Explicit owner decisions required before implementation

This ADR recommends the separate profile above but does not accept or enact it. The owner must choose each item (or reject the profile):

| Decision | Recommendation in this proposal | Owner disposition |
|---|---|---|
| Host request/result shape | New operation-specific closed request/result profile, separate from ADR-021 `diagnostic_start` / `STATUS`; do not introduce a generic version-negotiation framework | OPEN |
| Result-query binding | `result` request references the host `operation_id`; server resolves the stored mapping; clients never submit raw firmware ID | OPEN |
| Receipt semantics | Reuse existing transmission / ACK / effect-certainty / verification axes and add bounded firmware-ID/session provenance only if accepted schema permits; otherwise hold fields in internal evidence, no new enum values presumed | OPEN |
| Mapping lifetime | Process/session-generation scoped initially; after restart/reopen/reset, unavailable mapping is blocked/inconclusive unless continuity is independently established | OPEN |
| Firmware-slot semantics | Mirror ADR-006 same-ID cache, busy-other-ID, reset-loses-result; no automatic resubmission after uncertain `run` | OPEN |

Implementation cannot start until owner disposition resolves the shape and receipt-field question; schema/enum expansion may require a subsequent ADR-021 amendment or a further superseding decision. ADR-006 and ADR-021 remain unchanged by this Proposed ADR.

### Success criteria

- STATUS-only requests retain byte/schema/behavior compatibility.
- `run` emits no more than one firmware run command even across host timeout/duplicate/restart; uncertain dispatch never auto-replays.
- `result` emits only a result query and cannot cause a run.
- Firmware ID validation, busy/cache/reset semantics, bounds, reason mapping and unsupported-marker denial are deterministic and fake-tested before any hardware qualification.
- Invalid, stale or unsupported session/model/capability inputs reject before a mutating run write.

## Alternatives Considered

### Extend `diagnostic_start` / `STATUS`

Rejected: this would change the owner-accepted ADR-021 meaning and could make a read-only STATUS request imply a mutating run.

### Keep D05 permanently STATUS-only and defer run/result

Safe fallback if the owner declines a new host profile. It avoids a schema extension but leaves Issue #72's accepted run/result criteria unimplemented.

### Submit raw firmware IDs as host operation IDs

Rejected: firmware IDs are short, volatile and reset-scoped; they are not unique host job identity, authorization, or durable dedup keys.

## Consequences

### What gets easier

The existing STATUS contract remains stable while run/result can be reasoned about with explicit write-once and uncertainty semantics.

### What gets harder

A separate profile needs schema/version review, ID/session mapping, result-query lifetime rules, reason mapping, and tests for duplicate, busy, reset and uncertain-write cases. Firmware cache is volatile, so host persistence cannot manufacture a result after reset.

### What does not change

ADR-006 firmware commands remain authoritative; ADR-021 STATUS remains read-only and unchanged; ADR-009 audio remains separate opt-in. No device access is authorized by this proposal.

## Test Contract

| Claim | Test scenario | Currently |
|---|---|---|
| Firmware ID is bounded uppercase ASCII and invalid IDs reject before run write | fake request/adapter tests | not yet written |
| Accepted run writes at most one command; uncertainty never retries | fake transcript + partial-write/timeout/lost-ACK tests | not yet written |
| Result query is read-only and references host operation/session mapping | fake transcript asserts only `result <ID>` and binding | not yet written |
| Restart/reset without known session continuity cannot replay or fabricate result | fake lost-mapping/reset scenario | not yet written |
| Busy/cache/reset and unsupported marker map conservatively | stateful fake firmware slot and marker matrix | not yet written |
| Existing STATUS bytes/schema remain unchanged | existing STATUS adapter/composition regression suite | existing tests; exact future candidate must rerun |

## Rollback

Before implementation/publication, withdraw this Proposed ADR without changing ADR-006 or ADR-021. After owner acceptance and client use, any reversal must preserve the separate STATUS profile and version/deprecate the run/result profile explicitly; never reinterpret prior STATUS requests.

## References

- Issue #72: https://github.com/ozand/adv/issues/72
- Pre-edit research: https://github.com/ozand/adv/issues/72#issuecomment-6281172324
- Accepted ADR-006 and ADR-009; accepted ADR-021
- Pinned ADV parser source/hash recorded in Context
