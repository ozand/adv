# ADR-019: Keep D02 operation contracts non-normative until reviewed

**Status:** Proposed
**Date:** 2026-10-12
**Authors:** Repository owner and coding assistant
**Issue:** [#69](https://github.com/ozand/adv/issues/69)
**Supersedes:** None
**Related:** ADR-006, ADR-009, ADR-014

## Context

D02 needs to clarify host operation semantics, identifiers, bounds, results, and fake-only conformance cases while D01 architecture and security decisions remain under review. Accepted ADR-006/009 already define bounded firmware source contracts, but do not define a stable host DeviceOps API. Publishing a draft as though it were normative could cause adapters or clients to depend on unreviewed schemas, numbers, or enforcement assumptions.

This proposed decision is grounded in the Issue #69 task and the bounded source/document review recorded in [the Issue #69 research comment](https://github.com/ozand/adv/issues/69#issuecomment-6129685648). No runtime behavior or API implementation was tested.

## Decision

Until D01 and the relevant owner/security review accept D02, operation schemas, reason enums, catalog names, and bounds are proposals only. They MUST be marked non-normative and MUST NOT be presented as a stable API, implemented enforcement, or authorization to access devices, serial, network, firmware, or deployment.

The D02 draft may specify deterministic fake-only validation cases and acceptance criteria. It does not change ADR-006/009 wire contracts or select an implementation repository, runtime, schema dialect, dependency, or trust model. Acceptance of the host contract requires an explicit ADR decision and exact-candidate review before implementation relying on the contract begins.

## Consequences

### What gets easier

D02 can make progress on reviewable semantics and test expectations without pretending architecture or enforcement decisions are settled.

### What gets harder

Implementers cannot treat draft names, schemas, or numeric bounds as stable; follow-on work may need revision after D01 and owner/security review.

### What does not change

Existing accepted firmware contracts remain in force. This ADR does not authorize hardware, serial, network, package installation, deployment, or physical testing.

## Alternatives Considered

### Publish D02 as normative immediately

Rejected because schema/version, numeric limits, trust model, and implementation boundary are not yet accepted.

### Defer all D02 drafting until D01 is complete

Rejected for this proposal because the roadmap permits parallel draft work; acceptance remains gated on D01.

## Test Contract

| Claim in Decision | Test | Currently |
|---|---|---|
| Proposal artifacts are labeled non-normative and gated on D01/review | Read-only review of `docs/deviceops/proposals/D02-contract-proposal.md` and this ADR | not yet independently reviewed |
| Draft fixture plan does not claim validator/runtime execution | Review text and verify no runtime implementation/test artifacts are included in this change | not yet independently reviewed |
| ADR-006/009 wire contracts are unchanged | Diff scope check: only proposal/ADR/research/index paths; no firmware/host implementation paths | not yet independently reviewed |

## References

- [Issue #69](https://github.com/ozand/adv/issues/69)
- [D02 proposal](../deviceops/proposals/D02-contract-proposal.md)
- [D02 research record](https://github.com/ozand/adv/issues/69#issuecomment-6129685648)
- [ADR-006](ADR-006-hardware-diagnostic-serial-json.md)
- [ADR-009](ADR-009-bounded-opt-in-audio-diagnostics.md)
- [ADR-014](ADR-014-deviceops-service-centered-agent-infrastructure.md)
