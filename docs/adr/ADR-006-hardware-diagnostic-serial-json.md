# ADR-006: Expose hardware diagnostic status through bounded serial JSON

**Status**: Accepted
**Date**: 2026-10-07
**Authors**: Repository owner and coding assistant
**Accepted by**: Repository owner, 2026-10-07 (Issue #2 owner direction; see acceptance comment 6047336687)
**Supersedes**: None
**Related**: ADR-001; Issue #2

## Context

The Issue #2 diagnostic sketch has local display status but no bounded machine-readable interface. The owner authorized a narrow serial interface with `status` and `sd_test` commands and JSON telemetry, then authorized preparing a finite `run <ID>` / `result <ID>` runner. The existing SD operation is opt-in and one-shot; repeated requests must not retry its filesystem writes. The owner accepted the bounded four-command interface and its stated run/cache/SD scope in Issue #2. That acceptance is limited to the source contract; it does not authorize serial/device execution, installation, flashing, or claim hardware PASS.

### Problem statement

Expose readiness, retained SD-test outcome, and finite software diagnostic results to a host without adding arbitrary device commands or repeat SD mutations.

### Prior art

The existing physical `S` key invokes the bounded SD test. The serial command shares that one-shot operation rather than introducing a second SD path. The owner explicitly accepted that SD remains opt-in and that unmeasured nodes remain `NOT_TESTED`/`INCONCLUSIVE` (Issue #2 owner direction, 2026-10-07).

## Decision

Provide newline-terminated ASCII commands `status`, `sd_test`, `run <ID>`, and `result <ID>`. The `status` and `sd_test` envelopes retain the fixed-schema v1 shape; `run` and `result` use v2 frames capped at 1024 bytes. Both firmware shapes identify build `adv-diagnostic-2`; v1 describes the envelope version, not a firmware rollback. Run IDs are 1–12 uppercase ASCII letters/digits. The firmware retains one volatile result record in RAM: repeating the exact ID returns the cached result without rerunning checks; a different ID is rejected while occupied; reset loses the record. `result <ID>` only reads the retained record. `status` reports cached values and never accesses SD. `sd_test` and physical `S` share one one-shot gate; repeated requests return retained outcome. The aggregate runner performs board-identity reporting, a bounded 256-byte RAM scratch-pattern check, and eight finite IMU samples only; physical checks remain `NOT_TESTED`/`INCONCLUSIVE`, and SD is excluded unless explicitly requested separately.

### What this IS

- A fixed 64-byte command-line limit; malformed, unknown, and overlong lines are rejected after consuming through newline.
- Bounded JSON fields for firmware build label, board/IMU readiness, and SD state, stage, fixed reason enum, verified bytes, and cleanup result. Command errors use the same envelope and a fixed error reason, including `not_ready` without starting or latching an SD test.
- An opt-in operation only; no automatic SD access during boot.

### What this IS NOT

- A shell, arbitrary command/file access, raw log/key transport, or device-identity endpoint.
- A hardware validation claim or permission to connect, run SD tests, install, or flash.

### Success criteria

The fixed command allowlist and IDs are bounded; status does not call SD; malformed/overlong commands cause no SD operation; serial and key SD invocation share a one-shot guard; repeated run IDs do not rerun checks; result lookup is read-only; aggregate SD remains untested; all frames fit their caps and use fixed reasons without raw device text. Acceptance of this source contract does not authorize runtime/device operations.

## Consequences

### What gets easier

Host-side tools can consume readiness and SD outcomes without parsing display text.

### What gets harder

The wire schema must remain synchronized with the firmware state machine and be tested at parser boundaries.

### What does not change

SD remains an opt-in, bounded operation with potential filesystem side effects. Device access and installation require separate authorization.

## Alternatives Considered

### Text-only serial messages

Rejected because clients would parse presentation text whose wording is not a stable field contract.

### General command shell

Rejected because it grants broader operations than this diagnostic needs.

### Do nothing

Leaves the requested host-visible status/test interface unavailable.

## Test Contract

| Claim | Test | Current evidence |
|---|---|---|
| Command allowlist and line bounds are enforced | `test_command_allowlist_and_bounded_line` | source-contract test; passing |
| Status is read-only and SD test shares a one-shot gate | `test_status_path_is_cached_and_sd_test_is_one_shot` | source-contract test; passing |
| Output schema is fixed and bounded | `test_response_is_fixed_bounded_json_and_no_raw_echo` | source-contract test; passing |
| Terminal SD failure paths set a terminal state | `test_sd_terminal_paths_record_failure_or_result` | source-contract test; passing |

## Rollback

Remove the serial parser/response path while retaining the physical display/keyboard diagnostic. Once clients depend on v1 field names, incompatible changes require a version change or deprecation period.

## References

- [Issue #2](https://github.com/ozand/adv/issues/2), including owner acceptance comment [6047336687](https://github.com/ozand/adv/issues/2#issuecomment-6047336687)
- [Hardware diagnostic sketch](../../scripts/hardware_check/hardware_check.ino)
