# ADR-010: Define an extensible knowledge and evidence contract

**Status**: Accepted
**Date**: 2026-10-09
**Authors**: Repository owner and coding assistant
**Supersedes**: None
**Related**: ADR-004 (local lessons), ADR-007 (publication boundary); Issues #3, #5, #45

## Context

Owner acceptance was recorded in [Issue #45 comment 6072992191](https://github.com/ozand/adv/issues/45#issuecomment-6072992191) for the finite proposal published at main commit `60172a4ac68739d5b19745f2bee503f0f46ca02a`, including the `docs/knowledge-model-contract.md` blob `fa6c098eb2d71187c2feffd8dca02428acb3a0d2`. Acceptance covers advancement of Issues #46–#51 under that contract only; it is not blanket acceptance of future ADRs, migration, QMD/index changes, or device claims.
The Cardputer KB needs consistent object classification, claim-level evidence, applicability context, and minimal metadata without implying that structure proves truth. Existing OKF uses a required nonempty `type` and permits unknown types/additional fields. Existing cards vary in source detail and distinguish upstream statements from runtime verification. ADR-007 separates reviewed public raw/research evidence from canonical wiki synthesis and ignored original sources; ADR-004 keeps operational lessons local-only.

Evidence basis: inspected published CalcPuter and Cardulator cards and current OKF profile behavior. These are examples of current document practice, not proof that every card follows one contract. The knowledge model is a proposal; no migration or schema adoption is authorized by filing this ADR. An OpenWIKI proposal was reviewed read-only at source revision `d1c7fc75a6a906da258cd94dbcb1602f98516480`; its compatibility guidance is advisory only and adds no requirement or evidence to this contract.

### Problem statement

Provide a compact, extensible contract for knowledge object profiles, evidence attached to claims, applicability/version context, and minimum card metadata while retaining existing publication and layer boundaries.

### Prior art

OKF `type` is required, nonempty, and extensible. Existing cards use `Project`, `status`, issue links, and pinned source/revision/license metadata. ADR-007 governs publication eligibility; QMD indexing is not permission. These existing fields must not be reinterpreted as evidence of device operation.

## Decision

Propose the finite contract in `docs/knowledge-model-contract.md` for review. Preserve OKF's required extensible `type`; recommend `title` for adv canonical cards, not as an OKF universal requirement. Keep optional `object_profile` separate from `type`. Record evidence per claim/source, not as a document-wide grade. Distinguish source-reported, code-inspected, device-observed, and the higher-threshold device-verified claim class; keep applicability and lifecycle separate. No existing cards or vocabularies are migrated or promoted.

**This is not** a universal object taxonomy, source disposition workflow, publication-boundary change, or authorization to migrate content, index QMD, or assert device verification. Acceptance applies only to the finite proposal identified in the Issue #45 owner decision; implementation and migration remain separately scoped.

## Consequences

### What gets easier

Readers can distinguish a project profile from its evidence and target applicability while preserving mixed-source cards.

### What gets harder

Authors must attach provenance to individual claims and explicitly mark unknown applicability; validation and review must avoid treating structural conformance as truth.

### What does not change

OKF `type`, raw/research/wiki/sources boundaries, local lessons, and current card contents remain unchanged unless separately accepted and authorized.

## Alternatives Considered

- **Replace `type` with a closed universal taxonomy** — rejected for this proposal because OKF permits extensible types and existing consumers may rely on them; migration impact is unassessed.
- **One confidence/status value per document** — rejected because a card may mix README reports, code inspection, and device observations.
- **Autopromote evidence from structure, stable status, or QMD** — rejected because none establishes factual or runtime correctness.
- **Migrate existing cards now** — rejected; Issue #45 explicitly requires separate owner acceptance before adoption/migration.

## Test Contract

| Claim | Check | Current evidence |
|---|---|---|
| Existing `type` remains valid and profiles are optional extensions | Validate representative existing cards without migration | Proposed; structural check only, not run against new contract |
| Mixed evidence stays claim/source scoped | Review a card with source and code evidence | Proposed review rule; no automated truth check |
| Unknown applicability is not treated as unsupported | Contract fixtures for missing vs explicit unsupported | Not yet written |
| Evidence/lifecycle are separate dimensions | Validate no status-to-evidence coercion | Not yet written |
| Publication/layer boundaries remain unchanged | Review paths against ADR-004/007 | Proposed; no migration or QMD action |

## Rollback

Any future reversal requires a reviewed superseding ADR. No content was migrated by this decision. Do not alter existing cards or accepted ADRs as rollback.

## References

- [Issue #45](https://github.com/ozand/adv/issues/45)
- [Proposed knowledge model contract](../knowledge-model-contract.md)
- [OKF v0.2 validator source](https://github.com/ozand/kb-bootstrap/tree/73277fdb3e54184901f67268bc676a562b0a677a)
- [CalcPuter example](https://github.com/ozand/adv/blob/ac87dcf43519303e2ce6aae86d03f0aa6f395f96/kb/wiki/entities/calculator-calcputer.md)
- [Cardulator example](https://github.com/ozand/adv/blob/ac87dcf43519303e2ce6aae86d03f0aa6f395f96/kb/wiki/entities/calculator-cardulator.md)
- ADR-004 and ADR-007
