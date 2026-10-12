# ADR-019: Keep D02 operation contracts non-normative until reviewed

**Status:** Proposed
**Date:** 2026-10-12
**Authors:** Repository owner and coding assistant
**Issue:** [#69](https://github.com/ozand/adv/issues/69)
**Supersedes:** None
**Related:** ADR-006, ADR-009, ADR-014

## Context

D02 needs to clarify host operation semantics, identifiers, bounds, results, and fake-only conformance cases. D01 choices in ADR-015–017 are accepted; ADR-006/009 define bounded firmware source contracts but not a stable host DeviceOps API. Owner acceptance of the narrow ADR-021 status-only contract does not make other operation schemas, production enforcement, or public API assumptions normative. Publishing unreviewed expansions as stable could create premature dependencies.

This proposed decision is grounded in the Issue #69 task and the bounded source/document review recorded in [the Issue #69 research comment](https://github.com/ozand/adv/issues/69#issuecomment-6129685648). A private, fake-only status-schema validator and unit suite have since been implemented and locally tested as a candidate; this is not production runtime, adapter, device, or stable API evidence.

## Decision

The owner has accepted only ADR-021's bounded `diagnostic_start` / `STATUS` contract slice. Other operation schemas, reason enums, catalog names, bounds, and enforcement remain proposals until separately reviewed and accepted. Even the accepted slice MUST NOT be presented as a stable public API, implemented production enforcement, or authorization to access devices, serial, network, firmware, or deployment.

The D02 draft may specify deterministic fake-only validation cases and acceptance criteria. It does not change ADR-006/009 wire contracts or select an implementation repository, runtime, schema dialect, dependency, or trust model. Any expansion beyond the owner-accepted ADR-021 slice requires an explicit ADR decision and exact-candidate review before implementation relies on it.

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
| The accepted ADR-021 slice is distinguished from still-proposed D02 expansions and no production/device authority is implied | Review the D02 proposal and this ADR against owner receipt #6134297908 | Candidate wording updated; exact-head documentation review pending |
| Draft distinguishes locally executed fake-only candidate tests from absent production/device enforcement | Review ADR-021 and private PR #4 evidence; confirm no hardware/runtime test is claimed | Candidate tests run locally; exact corrected-head review pending |
| ADR-006/009 wire contracts are unchanged | Diff scope check: only proposal/ADR/research/index paths; no firmware/host implementation paths | not yet independently reviewed |

## References

- [Issue #69](https://github.com/ozand/adv/issues/69)
- [D02 proposal](../deviceops/proposals/D02-contract-proposal.md)
- [D02 research record](https://github.com/ozand/adv/issues/69#issuecomment-6129685648)
- [ADR-006](ADR-006-hardware-diagnostic-serial-json.md)
- [ADR-009](ADR-009-bounded-opt-in-audio-diagnostics.md)
- [ADR-014](ADR-014-deviceops-service-centered-agent-infrastructure.md)
