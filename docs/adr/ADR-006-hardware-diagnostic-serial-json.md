# ADR-006: Expose hardware diagnostic status through bounded serial JSON

**Status**: Proposed
**Date**: 2026-10-07
**Authors**: Repository owner and coding assistant (candidate)
**Supersedes**: None
**Related**: ADR-001; Issue #2

## Context

The Issue #2 diagnostic sketch has local display status but no bounded machine-readable interface. The owner authorized a narrow serial interface with `status` and `sd_test` commands and JSON telemetry. The existing SD operation is opt-in and one-shot; repeated requests must not retry its filesystem writes. This proposal records the interface rationale; it does not claim owner acceptance of every protocol detail or authorize device access.

### Problem statement

Expose readiness and the retained SD-test outcome to a host without adding arbitrary device commands or repeat SD mutations.

### Prior art

The existing physical `S` key invokes the bounded SD test. The serial command will share that one-shot operation rather than introduce a second SD path.

## Decision

Provide exactly two newline-terminated ASCII commands, `status` and `sd_test`, with fixed-schema bounded JSON v1 responses. `status` reports cached values and never accesses SD. `sd_test` and physical `S` share one one-shot gate; subsequent requests return the retained outcome.

### What this IS

- A fixed 64-byte command-line limit; malformed, unknown, and overlong lines are rejected after consuming through newline.
- Bounded JSON fields for firmware build label, board/IMU readiness, and SD state, stage, fixed reason enum, verified bytes, and cleanup result. Command errors use the same envelope and a fixed error reason, including `not_ready` without starting or latching an SD test.
- An opt-in operation only; no automatic SD access during boot.

### What this IS NOT

- A shell, arbitrary command/file access, raw log/key transport, or device-identity endpoint.
- A hardware validation claim or permission to connect, run SD tests, install, or flash.

### Success criteria

The two commands return bounded valid JSON; status does not call SD; malformed/overlong commands cause no SD operation; serial and key invocation share a one-shot guard; all terminal SD paths retain a state and fixed reason without raw device text.

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
