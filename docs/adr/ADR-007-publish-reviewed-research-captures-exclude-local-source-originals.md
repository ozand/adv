# ADR-007: Publish reviewed research captures while excluding local source originals

**Status**: Accepted
**Date**: 2026-10-08
**Authors**: Repository owner and coding assistant
**Supersedes**: ADR-001
**Related**: ADR-002, ADR-003, ADR-005; Issues #3, #5, #24

## Context

The repository needs to distinguish publishable, reviewed research evidence from private or bulky source originals. Existing public ADR-001 establishes a standalone public knowledge repository, local-only source repositories/books, and a synthesis-oriented publication boundary. Owner direction in this task explicitly permits publishing reviewed research/raw captures while keeping original sources excluded. This supersedes ADR-001's synthesis-only capture restriction; it does not remove the standalone repository, local-source, privacy, or separate-repository boundaries. ADR-001 remains immutable under the accepted-ADR amendment rule and is represented as superseded by this decision in the index.

The current decision basis is the owner's explicit direction in this task: reviewed research/raw evidence may be publicly published, while original source material remains local-only. Earlier issue comments are historical supporting records, not a substitute for this current decision. Existing unpublished ADR drafts are not treated as published authority.

### Problem statement

Contributors need a clear rule for publishing reviewed research captures without publishing source originals or confusing evidence with canonical synthesis.

### Prior art

ADR-001 established the standalone public repository and a synthesis-focused boundary. The owner-directed `kb-bootstrap` single-layout workflow distinguishes raw evidence from canonical wiki synthesis. This ADR clarifies publication eligibility for reviewed captures while preserving that layer distinction; it does not change `kb-bootstrap` behavior or establish QMD indexing as publication authorization.

## Decision

Publish bounded, reviewed research captures as public evidence in `kb/raw/` and/or `kb/research/` only after privacy, secret, relevance, provenance, and rights review. Keep original repositories, books/PDFs, binaries, private captures, and bulky source materials in ignored local-only `sources/`. QMD indexing is a separate retrieval choice and does not determine Git tracking or publication eligibility.

### What this IS

- A publication boundary allowing reviewed, bounded, source-linked research evidence in `kb/raw/` and `kb/research/`.
- A local-only boundary for original repositories, books/PDFs, binaries, private captures, and bulky source material under `sources/`.
- A requirement to retain source identity, access date, capture limitations, and review provenance for published captures.

### What this IS NOT

- Permission to publish entire repositories, books, PDFs, binaries, unreviewed source dumps, credentials, private device/network captures, or personal data.
- A change to the standalone public repository boundary or to the distinction between raw evidence and canonical synthesis in `kb/wiki/`.
- A claim that QMD indexing, a local clone, or an existing draft ADR grants publication permission.
- A hardware/device operation or source-project modification.

### Success criteria

- Contributors can classify source originals as local-only and reviewed bounded captures as potentially publishable under the stated review gates.
- Published capture records retain provenance and distinguish evidence from canonical wiki claims.
- No source original, secret, personal data, or unreviewed capture is promoted by this decision.

## Consequences

### What gets easier

- Reviewed evidence can be shared with the synthesized knowledge it supports.
- Contributors have an explicit distinction between public capture evidence and local originals.

### What gets harder

- Each capture requires privacy, secret, relevance, provenance, and rights review before tracking.
- Reviewers must distinguish evidence-layer material from canonical synthesis and verify source attribution.

### What does not change

- The repository remains a standalone public knowledge repository.
- Original source repositories, books/PDFs, binaries, private captures, and bulky materials remain local-only in ignored `sources/`.
- `kb/wiki/` remains canonical synthesis; capture publication does not make a capture a verified canonical answer.
- No device/hardware behavior is established by this publication policy.

## Alternatives Considered

### Keep every capture local-only

This preserves a simpler publication boundary, but conflicts with the owner's current explicit direction that reviewed research/raw captures may be published.

### Publish source originals or whole repositories

Rejected because it would publish bulky upstream material and exceed the reviewed-capture scope; original sources remain local-only.

### Treat QMD indexing as the publication decision

Rejected because retrieval/index membership is independent of Git tracking, rights, privacy, and publication review.

## Test Contract

| Claim in Decision | Test | Currently |
|---|---|---|
| Reviewed captures may be published only in designated evidence layers | Review tracked-path inventory and capture provenance/privacy checklist | Policy statement; automated enforcement not yet written |
| Source originals remain excluded | Verify `sources/` ignore rules and `git ls-files sources` before publication | Existing repository checks/documented workflow; verify during implementation |
| QMD indexing does not authorize publication | Compare declared/runtime QMD collections separately from Git tracking | Documented boundary; no QMD operation performed for this ADR |
| Evidence remains distinct from canonical synthesis | Validate capture links/provenance and wiki promotion review | Workflow requirement; automated enforcement not yet written |

## Rollback

The publication rule can be superseded by a later ADR. Published capture files already merged to public history cannot be made confidential by changing policy; removal would require a separately authorized history/content remediation. Local originals remain under owner-controlled local storage and are not recovered from or deleted by this ADR.

## References

- ADR-001 (Proposed supersession of its synthesis-only capture restriction; standalone-repository and local-source boundaries are preserved)
- [Issue #3 owner decision records](https://github.com/ozand/adv/issues/3#issuecomment-6026992432)
- [Issue #5 corpus/publication boundary](https://github.com/ozand/adv/issues/5)
- [Issue #24 documentation/ADR reconciliation](https://github.com/ozand/adv/issues/24)
