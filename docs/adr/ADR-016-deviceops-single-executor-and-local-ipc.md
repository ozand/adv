# ADR-016: Route DeviceOps clients through one persistent local executor

**Status:** Proposed — requires owner review before implementation.
**Date:** 2026-10-12.
**Issue:** [#68](https://github.com/ozand/adv/issues/68).
**Supersedes:** None.
**Related:** ADR-014, ADR-015, ADR-017.

## Context

ADR-014 proposes one owner for the device session and equivalent CLI/MCP semantics. A stdio-launched MCP process cannot be shared with an independent CLI: starting a second process risks a second writer, while a single-instance lock alone makes the second client fail to reach the first. Tying executor lifetime to one client also undermines durable jobs. This flaw was identified in the independent PR #84 review of candidate `1d7500d48a73d2db9d5aedf80f312966245331a2` (**reported**).

## Decision

### What this IS

Propose one persistent local executor process as the sole serial/session owner. CLI and MCP, if both enabled, must reach the same process through authenticated local IPC; independent stdio-launched cores cannot satisfy the shared-executor requirement. Require single-instance enforcement, explicit client/process lifecycle and a named busy/error result when the executor is unavailable. Qualify Windows named pipes against other local IPC mechanisms before choosing one; named pipes remain a candidate, not a decision.

### What this IS NOT

Not an in-process-only dual frontend, not two independent serial owners, and not a TCP/HTTP listener, remote tunnel or network service. Does not authorize USB/COM use.

### Success criteria

Fake tests show CLI and MCP reach the same executor and state, a second executor cannot claim the target, clients can reconnect after restart, and no offline test opens physical serial.

## Consequences

### What gets easier

One serialization point can own device sessions and durable operation state across clients.

### What gets harder

IPC authentication, permissions, service lifecycle, crash recovery and Windows-specific packaging require implementation and tests.

### What does not change

Named operation authority and firmware contracts remain transport-independent. A process restart or lost response never implies a safe retry.

## Alternatives Considered

- **One stdio MCP process per client:** fails to provide a shared executor to the independent CLI and couples job lifetime to client lifetime.
- **In-process core per frontend:** permits duplicate session owners unless a separate broker is added.
- **Network listener:** increases attack surface without a demonstrated remote requirement for the first local MVP.

## Test Contract

| Claim | Test | Currently |
|---|---|---|
| Both frontends reach one process | IPC contract integration with fake transport | not yet written |
| Duplicate executor is rejected safely | multi-process single-instance test | not yet written |
| Restart does not replay uncertain operation | crash/restart reconciliation fixtures | not yet written |

## Rollback

Before acceptance, choose one frontend only or revise the proposal. After acceptance, changing process/IPC topology requires a superseding ADR.

## References

Issue #68, PR #84 review comment on candidate `1d7500d48a73d2db9d5aedf80f312966245331a2`, ADR-014 and DeviceOps architecture.
