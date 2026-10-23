---
name: kb-wiki-builder
description: "Use this skill when documenting Cardputer hardware/module capabilities, firmware operations, or data-flow scenarios in the canonical wiki. It guides evidence-backed synthesis in both directions: module capability to operation/data, and desired data to required setup."
---

# KB Wiki Builder

Create concise, evidence-backed knowledge pages from reviewed sources. Follow the [capability research workflow](../../../docs/capability-research-workflow.md) for the capability-to-scenario and desired-data-to-setup chains.

## Process

1. **Identify scope and sources.** Read the governing issue and accepted [ADR-007](../../../docs/adr/ADR-007-publish-reviewed-research-captures-exclude-local-source-originals.md) and [ADR-010](../../../docs/adr/ADR-010-define-extensible-knowledge-evidence-contract.md). Keep original repositories, account data, private captures, and bulky sources in ignored `sources/`. Never publish them.
2. **Trace both directions.** For each question, map `device → module/component → firmware/tool and version → operation → input/output data → scenario`. Work forward from a claimed capability and backward from desired data/setup. Do not infer a missing edge.
3. **Record relations, not broad labels.** For each supported relation, record named device/module, firmware/tool version or `unknown`, operation, setup/prerequisites, data direction/format/destination/limits, scenario, source locator/revision, evidence class, and gaps. Use a small table or linked bullets; do not introduce a new schema.
4. **Qualify every claim.** Distinguish `source-reported`, `code-inspected`, `device-observed`, and `device-verified` per accepted ADR-010. Cite the exact source/revision. A successful build or README claim is not device verification. Mark inaccessible or unverified details `unknown`; use `unsupported` only when evidence establishes absence of support.
5. **Draft canonical wiki content.** Preserve the repository's OKF `type` and existing page conventions. Keep evidence attached to each claim. Separate raw/research evidence from canonical synthesis.
6. **Review before publication.** Check source identity, revision, claim accuracy, privacy, relevance, and rights under ADR-007. Store only bounded reviewed captures in `kb/raw/` or `kb/research/`; keep source originals in `sources/`. QMD indexing is optional and does not authorize publication.
7. **Validate and report.** Run the documented structural validator when applicable. Report factual review, structural validation, and QMD state as separate outcomes; do not claim one proves another.

## Guardrails

- A chip or component name alone does not prove wiring, pinout, driver support, firmware integration, electrical compatibility, or operation.
- Preserve conflicting evidence and limitations; do not upgrade owner-reported leads or inaccessible product pages into source-verified claims.
- Do not perform hardware operations, flashing, source execution, dependency setup, or QMD mutation unless separately authorized.
- If evidence is missing, document the gap and next evidence needed instead of inventing a compatibility path.
