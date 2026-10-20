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

- A bounded host request for one firmware `run <ID>` and a separate read-only `result <ID>` query.
- A core-generated `operation_id` remains the authoritative host job identity. A firmware run ID is a separate adapter-generated 1–12 character `[A-Z0-9]` value, recorded in provenance and scoped to the active transport/session generation. Never derive it from, or accept it as, a client-supplied operation ID.
- The adapter sends at most one `run <ID>` frame per accepted host operation. A full write is not an acknowledgement. Partial/failed write, timeout, lost acknowledgement, reset/session loss, malformed or mismatched response yields `INCONCLUSIVE`; never automatically retry `run`.
- `result <ID>` is a separate bounded, read-only query against the retained firmware slot. It must not implicitly submit/replay a run. A busy slot, wrong/unknown ID, empty slot after reset, or unavailable result maps to an explicit bounded outcome without inventing a physical PASS.
- Same accepted host request follows existing principal/target/request dedup rules. Firmware result-cache reuse is only valid when the same firmware session/generation is known; reset invalidates that evidence.

### What this IS NOT

- A change to firmware, ADR-006 command/frame semantics, or ADR-021 STATUS schema/meaning.
- Permission for real serial/COM/USB access, automatic `sd_test`, audio, reset, flash, service, or hardware testing.
- A claim that software result states establish physical PASS, persistent storage across reboot, or exactly-once device execution.

### Proposed request/result contract questions for owner disposition

Before implementation, the owner must select the concrete representation: either a separately versioned request/result schema/profile or a new operation-specific closed shape. Required distinctions are one `run` request with accepted host ID/target/session binding, one read-only `result` query referencing the host operation, and a result that preserves transmission, acknowledgement, effect certainty, verification, firmware run ID and session-generation provenance. This ADR does not modify ADR-021's accepted types or prescribe unreviewed enum values.

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
| Accepted run writes exactly one command; uncertainty never retries | partial write, timeout, lost ACK, duplicate/reopen fake tests | not yet written |
| Result query is read-only and bound to host operation/session mapping | transcript asserts only `result <ID>` and binding | not yet written |
| Busy/cache/reset and unsupported marker map conservatively | stateful fake firmware slot and marker matrix | not yet written |
| Existing STATUS bytes/schema remain unchanged | existing STATUS adapter/composition regression suite | existing tests; exact future candidate must rerun |

## Rollback

Before implementation/publication, withdraw this Proposed ADR without changing ADR-006 or ADR-021. After owner acceptance and client use, any reversal must preserve the separate STATUS profile and version/deprecate the run/result profile explicitly; never reinterpret prior STATUS requests.

## References

- Issue #72: https://github.com/ozand/adv/issues/72
- Pre-edit research: https://github.com/ozand/adv/issues/72#issuecomment-6281172324
- Accepted ADR-006 and ADR-009; accepted ADR-021
- Pinned ADV parser source/hash recorded in Context
