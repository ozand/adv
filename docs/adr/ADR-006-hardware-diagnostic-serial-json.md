# ADR-006: Expose hardware diagnostic status through bounded serial JSON

**Status**: Proposed
**Date**: 2026-10-07
**Authors**: Repository owner and coding assistant (candidate)
**Supersedes**: None
**Related**: ADR-001; Issue #2

## Context

The Issue #2 diagnostic sketch has local display status but no bounded machine-readable interface. The owner authorized a narrow serial interface with `status` and `sd_test` commands and JSON telemetry, then authorized preparing a finite `run <ID>` / `result <ID>` runner. The existing SD operation is opt-in and one-shot; repeated requests must not retry its filesystem writes. This proposal records the interface rationale; it does not claim owner acceptance of every protocol detail or authorize device access.

### Problem statement

Expose readiness, retained SD-test outcome, and finite software diagnostic results to a host without adding arbitrary device commands or repeat SD mutations.

### Prior art

The existing physical `S` key invokes the bounded SD test. The serial command will share that one-shot operation rather than introduce a second SD path.

## Decision

Provide newline-terminated ASCII commands `status`, `sd_test`, `run <ID>`, and `result <ID>`. The first two retain the fixed-schema v1-shaped response; the latter two use fixed-schema v2 responses with a 1024-byte cap. Run IDs are 1–12 uppercase ASCII letters/digits; only one volatile run record is retained. Repeating its ID returns the cached result; other IDs are rejected until reset. `status` reports cached values and never accesses SD. `sd_test` and physical `S` share one one-shot gate; subsequent requests return the retained outcome. The aggregate runner performs bounded RAM scratch and finite IMU-data checks only; physical checks remain `NOT_TESTED`, and SD is excluded.

### What this IS

- A fixed 64-byte command-line limit; malformed, unknown, and overlong lines are rejected after consuming through newline.
- Bounded JSON fields for firmware build label, board/IMU readiness, and SD state, stage, fixed reason enum, verified bytes, and cleanup result. Command errors use the same envelope and a fixed error reason, including `not_ready` without starting or latching an SD test.
- An opt-in operation only; no automatic SD access during boot.

### What this IS NOT

- A shell, arbitrary command/file access, raw log/key transport, or device-identity endpoint.
- A hardware validation claim or permission to connect, run SD tests, install, or flash.

### Success criteria

The fixed command allowlist and IDs are bounded; status does not call SD; malformed/overlong commands cause no SD operation; serial and key SD invocation share a one-shot guard; repeated run IDs do not rerun checks; result lookup is read-only; aggregate SD remains untested; all frames fit their caps and use fixed reasons without raw device text.

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

- [Issue #2](https://github.com/ozand/adv/issues/2)
- [Hardware diagnostic sketch](../../scripts/hardware_check/hardware_check.ino)
