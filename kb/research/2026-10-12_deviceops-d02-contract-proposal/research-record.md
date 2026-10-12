# D02 contract proposal — research record

**Issue:** [#69](https://github.com/ozand/adv/issues/69)
**Epic:** [#66](https://github.com/ozand/adv/issues/66)
**Base:** PR #82 head `196d2f915e0fa2424b707f3fd30d873050a3b022`
**Prepared:** 2026-10-12
**Status:** bounded source/document review; no external research, runtime, device, network protocol, or implementation testing.

## Scope and method

Read the project instructions and the governed D02/D01 material at the exact base above. Reviewed the existing proposed DeviceOps contracts, roadmap, validation plan, evidence references, Issue #37 draft contract, and accepted ADR-006/ADR-009. This record supports drafting D02 proposal details only; it does not establish stable schemas, API compatibility, an accepted numeric limit, or enforcement behavior.

## Findings grounded in reviewed sources

- **Reported (existing project contract):** current draft distinguishes host operation identity from firmware run IDs and treats status/result queries as distinct operations; ADV firmware semantics are bounded by ADR-006/ADR-009.
- **Reported (accepted ADR-006):** the source contract has a 64-byte command line, 1–12 uppercase alphanumeric run IDs, result RAM retention lost on reset, and separate status/result semantics.
- **Reported (accepted ADR-009):** audio operations are opt-in, aggregate-only, and physical output/input remains inconclusive without owner observation; audio runtime is separately gated.
- **Theory (design implication):** D02 proposals should encode resource bounds and lifecycle uncertainty as separately named fields, retain backward/source-compatibility boundaries, and avoid describing draft schemas as runtime enforcement.

## Limits / unresolved

Exact formal schema syntax, version negotiation, operation catalogue, fixture implementation, and numeric bounds require D02/D01 review. No runtime host code, parser, dependency, firmware, or installed device was tested. No physical or serial evidence was collected. External references were not opened in this bounded iteration.

## Reviewed source set

- `docs/deviceops/CONTRACTS.md`
- `docs/deviceops/ROADMAP.md`
- `docs/deviceops/VALIDATION.md`
- `docs/deviceops/REFERENCES.md`
- `docs/diagnostics/agent-device-operation-contract-draft.md`
- `docs/adr/ADR-006-hardware-diagnostic-serial-json.md`
- `docs/adr/ADR-009-bounded-opt-in-audio-diagnostics.md`
