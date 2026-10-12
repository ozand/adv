# ADR-018: Bind DeviceOps authorization grants to principals, targets, operations, and effects

**Status**: Proposed
**Date**: 2026-10-12
**Authors**: Coding assistant (draft for owner review)
**Issue**: [#70](https://github.com/ozand/adv/issues/70)
**Supersedes**: None
**Related**: ADR-006 (bounded diagnostic serial JSON); ADR-009 (bounded opt-in audio diagnostics); ADR-014 (DeviceOps service-centered agent infrastructure); Issues #66, #68, #69

## Context

DeviceOps is proposed as a shared operation service for ESP32 management. Issue #70 scopes a server-side policy module, principal/target binding, permission issuance/revocation, effect classification, replay controls, and fake security fixtures. The service may expose several transports; none should independently grant authority. PR #82's `docs/deviceops/SECURITY.md` describes proposed trust boundaries and grants but explicitly leaves cryptographic/storage details to D03. Its `CONTRACTS.md` distinguishes transport, acknowledgement, execution, verification, and physical evidence.

ADR-006 and ADR-009 establish that bounded diagnostic source contracts do not themselves authorize device access, runtime tests, installation, or flashing. ADR-014 is proposed and distinguishes owner-confirmed direction from detailed architecture still requiring decision. This ADR therefore proposes a security contract only; it does not choose a grant signature format, credential store, host runtime, cryptographic identity mechanism, or enforcement implementation.

Threat assumptions: agent inputs, logs, device text, artifact paths, and transport annotations may be adversarial or stale. The trusted issuer and policy implementation are separate from the model requesting an operation. A process with full OS-administrator rights or an independent process with physical USB access can bypass a host service unless separately controlled by the operating system or hardware. These are design assumptions and residual risks, not claims of an existing implementation.

## Decision

**Proposed:** Every effectful DeviceOps operation must be authorized by a trusted issuer-controlled grant (or equivalent trusted policy decision) bound to the authenticated principal, an explicit target binding and accepted identity strength, the named operation plus normalized arguments or immutable plan digest, relevant artifact digest, policy revision, expiry, and a finite use/time/effect budget. The grant may authorize only enumerated effects. The model, client-provided `approved` fields, tool annotations, logs, firmware markers, and transport locators cannot issue or broaden a grant.

The service must reject absent, expired, revoked, replayed, or mismatched authority before external I/O, and revalidate it immediately before dispatch from a queue. Consumption and operation acceptance must be atomic with respect to the grant's replay/use budget. A changed principal, target/session binding, operation arguments, plan, artifact, adapter, or material precondition requires a newly authorized decision. An ambiguous device rebinding blocks effectful I/O.

Authorization distinguishes cached reads from fresh I/O, reset/control-line effects, volatile state, persistent storage, physical audio/RF effects, external network effects, and disclosure of sensitive data. Revocation prevents new dispatch; it does not assert that an already-started physical operation was cancelled or rolled back. Each operation must preserve transmission/acknowledgement/effect uncertainty and follow its documented safe-point or quarantine behavior.

This decision is a proposed contract, **not** an implementation, grant wire format, signature algorithm, identity attestation scheme, OS sandbox, or guarantee against a fully privileged host administrator or a competing process with USB access. It grants no device, network, installation, credential, or deployment permission.

## Consequences

### What gets easier

- Multiple frontends can share one explicit authority model without treating a transport or agent instruction as approval.
- Review and fake tests can reason about target substitution, queued revocation, replay, bounded effects, and uncertain outcomes.

### What gets harder

- Each operation needs normalized inputs, explicit effect declarations, target/identity evidence, budgets, and a well-defined dispatch boundary.
- Atomic grant consumption, revalidation, revocation, and non-rollback uncertainty require careful transactional and executor lifecycle design.
- Device binding and OS-level enforcement cannot be inferred from port names or firmware claims; deployments must state their residual bypass risks.

### What does not change

- ADR-006/009 firmware command contracts and their separate operation permissions remain unchanged.
- No new device identity primitive, credentials, remote endpoint, runtime code, or physical-device authority is created by this proposal.
- DeviceOps direction remains governed by ADR-014's proposed status and D01/D02 decisions remain separate.

## Alternatives Considered

### Treat frontend or model approval flags as authority

Rejected: untrusted inputs can self-assert approval, and multiple transports would create inconsistent enforcement points.

### Grant broad authority to a device or session

Rejected: it does not constrain operation, artifact, plan, principal, expiry, or effects and is vulnerable to confused-deputy and replay behavior.

### Rely on VID/PID, port path, or firmware marker as cryptographic identity

Rejected: these are observations with limited evidence strength and do not establish a unique, authenticated physical target.

### Claim the local service prevents a privileged host or competing USB process from acting

Rejected: absent OS/hardware enforcement, the service cannot control those bypass paths. Document them as residual risks instead of overclaiming.

## Test Contract

| Claim | Test | Current evidence |
|---|---|---|
| Missing, expired, revoked, mismatched principal/target/artifact/plan authority denies before I/O | Fake-policy negative tests: absent/expired/revoked/wrong-principal/wrong-target/wrong-digest | Not implemented; Issue #70 acceptance criteria |
| Grant use/budget cannot be replayed by concurrent dispatch | Fake transactional store/clock test racing duplicate consumption | Not implemented |
| Queued work revalidates revocation and exact target/plan before dispatch | Fake queue test: revoke or mutate binding after enqueue; assert zero transport calls | Not implemented |
| Untrusted approval fields, annotations, logs, and firmware markers cannot create authority | Confused-deputy/injected-log fixture; assert deny before fake transport | Not implemented |
| Effect classes and identity strength are explicit and ambiguous rebinding blocks I/O | Contract/schema tests for cached/fresh/reset/storage/audio/RF/network/disclosure and ambiguous session | Not implemented; D02/#69 dependencies may refine vocabulary |
| Revocation does not falsely claim an in-flight operation was cancelled or rolled back | In-flight fake write/revocation test asserts explicit uncertain/partial state and no blind retry | Not implemented |
| OS-admin and competing USB process are stated as residual threat assumptions | Threat-model review against actual chosen deployment boundary | Proposal text only; OS/runtime target unresolved in D01/#68 |

## References

- [Issue #70](https://github.com/ozand/adv/issues/70)
- [Epic #66](https://github.com/ozand/adv/issues/66)
- [D01 architecture decision #68](https://github.com/ozand/adv/issues/68)
- [D02 contracts #69](https://github.com/ozand/adv/issues/69)
- [DeviceOps security proposal](../deviceops/SECURITY.md)
- [DeviceOps contracts proposal](../deviceops/CONTRACTS.md)
- [ADR-006](ADR-006-hardware-diagnostic-serial-json.md)
- [ADR-009](ADR-009-bounded-opt-in-audio-diagnostics.md)
- [ADR-014](ADR-014-deviceops-service-centered-agent-infrastructure.md)
