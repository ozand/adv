# ADR-021: Define a bounded draft status-operation contract

**Status:** Accepted — owner receipt recorded in [Issue #69](https://github.com/ozand/adv/issues/69#issuecomment-6134297908); runtime implementation remains partial
**Date:** 2026-10-12
**Authors:** Repository owner and coding assistant
**Issue:** [#69](https://github.com/ozand/adv/issues/69)
**Supersedes:** None
**Related:** ADR-006, ADR-009, ADR-014, ADR-019

## Context

**Vocabulary:** `deviceops.request.v0` / `deviceops.result.v0` are accepted revision labels for this bounded internal contract slice, not a stable/public API version.

D02/#69 asks for versioned transport-neutral operation/result schemas, finite limits, deterministic fake-only conformance, and preservation of ADR-006/009 firmware wire contracts. PR #85's proposal describes these semantics but leaves schema fields and bounds open and contains no executable validator or fixture suite. Its Issue #69 source receipt records the missing work and explicitly distinguishes proposals from tested behavior.

Owner-approved D01 direction is recorded in [Issue #68 owner receipt](https://github.com/ozand/adv/issues/68#issuecomment-6130478169): Windows-first Python, one persistent executor with authenticated named-pipe IPC, local SQLite, and private `ozand/deviceops`. This does not itself accept a public operation format, trust/grant mechanism, or device behavior. Runtime source work belongs in the separate private repository and only in its scoped paths.

ADR-006 defines the bounded firmware `status` and retained-result behavior; ADR-009 keeps audio opt-in. A host request format must not imply new firmware commands, identity attestation, physical PASS, or permission to perform I/O. The numeric choices below are accepted finite host-contract bounds, not measured service-capacity guarantees or stable deployment defaults.

## Decision

The owner accepted this versioned, closed-object **status-profile-only** host request/receipt contract with canonical serialization and explicit evidence/outcome fields, as recorded in the receipt linked above. Acceptance is limited to the `diagnostic_start` / `STATUS` shape, JSON Schema Draft 2020-12, the finite candidate bounds below, and `NOT_TESTED|INCONCLUSIVE` physical outcomes. It does not complete Issue #69, establish a stable public API or production enforcement, or authorize device/network effects. The pure validator rejects malformed inputs without I/O and does not authorize an operation.

### Accepted schema and contract bounds

The accepted contract revision is documented in this ADR and published in private [`ozand/deviceops`](https://github.com/ozand/deviceops) through [PR #4](https://github.com/ozand/deviceops/pull/4): reviewed source HEAD `9508eb15c230f16faea118fccdc8bf9fe23cf87c`, merged to runtime `main` as `f4275ceade282d2162a10edcd95f56beb299f570` on base `ca86cbd6ef5cd6814f776974ee340a8bdbdaec8e`. The PR comparison against that base contains seven added contract/schema/test files under `deviceops/contracts/` and `tests/contracts/`; the merge commit itself retained existing main history. Exact contract files are `deviceops/contracts/request.schema.json`, `deviceops/contracts/result.schema.json`, and `deviceops/contracts/models.py`. Independent published-main verification is recorded at [Issue #81 comment 6145600160](https://github.com/ozand/adv/issues/81#issuecomment-6145600160): it verified the seven published blobs and ran 95 contract / 196 full repository tests on Windows 11 x64 / CPython 3.13.3. That receipt used the then-installed MCP SDK 1.29.0, so it does not qualify the later SDK dependency lock, host integration, adapter, or hardware. The private request/result shape is restricted to `diagnostic_start` with profile `STATUS`; other named operations have no schema/receipt in this slice.

Accepted request fields: `schema_version`, `request_id`, `target_id`, `operation`, `profile`, `arguments`, `observed_at`, `adapter_version`, optional-valued `firmware_marker`, and optional-valued `session_generation`. The accepted result shape includes a required `profile: STATUS`; in this profile `physical_result` is restricted to `NOT_TESTED|INCONCLUSIVE`, because status reads do not independently establish physical PASS/FAIL. A future physical-measurement profile requires a separately reviewed evidence contract. The broader candidate operation names are `device_list`, `device_inspect`, `device_connect`, `diagnostic_start`, `operation_get`, and `report_get`; only `diagnostic_start` may have the `STATUS` profile, and `arguments` is empty in this slice. Unknown fields, duplicate JSON keys, unsupported versions, malformed UTF-8, invalid enums, non-finite numbers, and over-limit encoded input reject before enqueue.

Accepted contract bounds: request JSON ≤4096 UTF-8 bytes; result receipt JSON ≤1024 UTF-8 bytes; identifiers ≤128 characters; reason codes ≤64 characters; queue depth ≤32; retained jobs ≤128; event history ≤64 entries per job. The owner accepted these as finite contract bounds, not measured service-capacity guarantees or authorization to operate hardware. Queue, retention, and event limits are contract candidates for later enforcement; they are not implemented by this schema validator. Host bounds do not change firmware frame limits. Further TTL, pagination, and operation-specific bounds remain unresolved and must be added before those surfaces are accepted.

The result contract separates `operation_id` and a strictly typed state (`accepted|running|succeeded|failed|inconclusive|cancelled`) from stage, transmission (`not_attempted|partial|complete|unknown`), device acknowledgement (`not_received|received|unknown`), effect certainty (`none|known_partial|known_completed|unknown`), verification (`not_attempted|passed|failed|inconclusive`), optional stable reason, provenance, and the status-profile physical result (`NOT_TESTED|INCONCLUSIVE`). `succeeded` alone cannot claim a physical PASS. Evidence includes adapter version, firmware marker as informational compatibility evidence, observation time, identity level, evidence level, and `cached|fresh|synthetic` source.

Deduplication scope is principal + target + request ID; identical canonical operation payload returns the same host job, changed payload under that scoped key conflicts, and a different target is a separate key. This does not promise exactly-once device execution. Host `operation_id` is never a firmware run ID. Cached evidence is not silently upgraded to fresh after reset/session-generation change. A late/unmatched response, cache replay after reset, stale session, or firmware-marker mismatch cannot be counted as current status success; uncertain effect remains `inconclusive` and does not trigger automatic mutating retry.

### What this IS

- An owner-accepted, versioned, status-only host request/result format and finite initial bounds.
- A pure, offline validator and synthetic conformance cases in the private runtime repository.
- A gate for subsequent operation profiles to add their own accepted schemas and effects.

### What this IS NOT

- An accepted stable public API, production enforcement guarantee, or public data format.
- A grant/token/signature/authentication design or a decision about detailed principal identity.
- A firmware ABI change, device attestation, hardware qualification, or authorization for serial/USB/network access.
- A command to implement mutating run, SD, audio, deployment, config, GPIO, arbitrary shell/serial, or raw-data export.

### Success criteria

1. The exact versioned request/result schemas and bounds are explicit and closed.
2. A pure validator rejects malformed, unknown, duplicate-key, and one-over-bound inputs without any backend call.
3. Synthetic fixtures distinguish status success from physical verification and cover scoped deduplication, reset/cache replay, session mismatch, firmware mismatch, late ACK/result, and unknown effect.
4. ADR-006/009 wire shapes and limits remain unchanged; all unexecuted/unsupported profiles remain clearly gated.

## Consequences

### What gets easier

Core, adapter, and frontend contributors can implement against a small, testable candidate shape while preserving a narrow no-device fake-only path.

### What gets harder

The numeric limits may need revision from resource measurements. Closed schemas require explicit version changes for added fields. Separate identity, effect, and evidence dimensions add implementation and migration work; the test suite cannot establish physical device truth.

### What does not change

D01 architecture direction, accepted ADR-006/009 firmware contracts, private repository boundary, and prohibition on unauthorized device/network effects remain unchanged.

## Alternatives Considered

### Keep only prose and defer all concrete bounds

Rejected because Issue #69 requires validator-ready finite boundaries and reproducible negative cases. The owner accepted the bounded status-only slice; expansion into additional operations remains separately reviewed.

### Adopt a stable public API immediately

Rejected because the owner accepted only the bounded internal status-contract decision, not a stable public API, client compatibility commitments, or production enforcement.

### Include all diagnostic, SD, and audio operations in the first schema

Rejected because those effects require distinct compatibility, authorization, and physical evidence. A status-only slice provides an inspectable parser contract without accidentally enabling them.

## Test Contract

| Claim in Decision | Test | Currently |
|---|---|---|
| Closed status request schema rejects malformed, duplicate, unknown, and over-bound data | `tests/contracts/test_models.py`; Draft 2020-12 schema checks | Historical pre-publication candidate run at `3a35c941e12415877bc56bb193ef73657ee62e6a` reported 57 contract / 158 full tests; this is not the merged source head. The merged source HEAD `9508eb15c230f16faea118fccdc8bf9fe23cf87c` has 95 contract / 196 full tests, and the independent published-main rerun at `f4275ceade282d2162a10edcd95f56beb299f570` is recorded at Issue #81 comment 6145600160. No host, adapter, production, or device qualification is claimed |
| STATUS receipts reject physical PASS/FAIL and validate state/evidence/encoded size, including unknown-effect success rejection | `tests/contracts/test_models.py`; `Draft202012Validator` | Covered by the merged source HEAD `9508eb15c230f16faea118fccdc8bf9fe23cf87c` test run and published-main rerun at `f4275ceade282d2162a10edcd95f56beb299f570` (Issue #81 comment 6145600160). No device or runtime integration is claimed |
| Reset/cache, mismatch, and late-frame scenarios remain inconclusive with fixed parser-only fixtures | `tests/contracts/test_scenarios.py` fake-only cases | Covered by the merged source HEAD `9508eb15c230f16faea118fccdc8bf9fe23cf87c` test run and published-main rerun at `f4275ceade282d2162a10edcd95f56beb299f570` (Issue #81 comment 6145600160); no adapter or device evidence is claimed |
| Firmware wire contracts remain unchanged | Review exact changed paths and compare ADR-006/009/source paths | This increment changes only `deviceops/contracts/` and `tests/contracts/` in the private runtime repository; no firmware or ADV-006/009 source path changed |

## Rollback

The accepted candidate remains narrowly scoped and has no stable external clients or persisted production format. Revising its contract requires a reviewed, versioned ADR change; do not silently alter the accepted shapes. Any future persisted/client-visible format migration requires an explicit compatibility plan. No production runtime rollback was performed.

## References

- [Issue #69](https://github.com/ozand/adv/issues/69)
- [D02 proposal and source/owner receipts](https://github.com/ozand/adv/issues/69#issuecomment-6130446464)
- [D01 owner acceptance](https://github.com/ozand/adv/issues/68#issuecomment-6130478169)
- [ADR-006](ADR-006-hardware-diagnostic-serial-json.md)
- [ADR-009](ADR-009-bounded-opt-in-audio-diagnostics.md)
- [ADR-014](ADR-014-deviceops-service-centered-agent-infrastructure.md)
- [ADR-019](ADR-019-deviceops-operation-contract-proposals-remain-non-normative-until-reviewed.md)
- [DeviceOps contract proposal](../deviceops/proposals/D02-contract-proposal.md)
