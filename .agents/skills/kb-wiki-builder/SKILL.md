---
name: kb-wiki-builder
description: "Use this skill when synthesizing Cardputer projects, reusable software approaches, hardware capabilities, firmware operations, or data-flow scenarios in the canonical wiki. Reuse existing knowledge and preserve evidence; for capability questions trace both operation/data and desired-data/setup."
---

# KB Wiki Builder

Create concise, evidence-backed knowledge pages from reviewed sources. Follow the [capability research workflow](../../../docs/capability-research-workflow.md) for the capability-to-scenario and desired-data-to-setup chains.

## Process

1. **Identify scope and sources.** Read the governing issue and accepted [ADR-007](../../../docs/adr/ADR-007-publish-reviewed-research-captures-exclude-local-source-originals.md) and [ADR-010](../../../docs/adr/ADR-010-define-extensible-knowledge-evidence-contract.md). Keep original repositories, account data, private captures, and bulky sources in ignored `sources/`. Never publish them.
2. **Reuse existing knowledge.** Before drafting, check `kb/index.md` and relevant `kb/wiki/` entities, concepts, and task navigation for the same project, task, or mechanism. Use optional QMD only under [project QMD guidance](../../../docs/qmd-usage.md); an unavailable or stale index is not proof of absence. Enrich an appropriate existing page and link relevant pages when the evidence supports the relationship. If no suitable match exists, create a justified page within the governing issue; do not force unrelated links or automatic reciprocals.
3. **For capability or data-flow questions, trace both directions.** Map `device → module/component → firmware/tool and version → operation → input/output data → scenario`. Work forward from a claimed capability and backward from desired data/setup. Do not infer a missing edge; for other project or software-approach questions, trace only relevant supported relations.
4. **Record relations, not broad labels.** For each applicable supported relation, record relevant context such as device/module, firmware/tool version or `unknown`, operation, prerequisites, data direction/format/destination/limits, scenario, source locator/revision, evidence class, and gaps. Use a small table or linked bullets; do not introduce a new schema.
5. **Qualify every claim.** Distinguish `source-reported`, `code-inspected`, `device-observed`, and `device-verified` per accepted ADR-010. Cite the exact source/revision. A successful build or README claim is not device verification. Mark inaccessible or unverified details `unknown`; use `unsupported` only when evidence establishes absence of support.
6. **Draft for the reader's task.** Where useful and supported, explain the task addressed, applicability, prerequisites and limits in concise prose or a small table. Mark missing context `unknown`; do not require boilerplate or infer a working setup. Preserve OKF `type`, existing page conventions, claim-level evidence, and the separation between raw/research and canonical synthesis. Link an existing task route only when relevant and within its declared scope; propose a focused change rather than silently expanding an approved route.
7. **Review before publication.** Check source identity, revision, claim accuracy, privacy, relevance, and rights under ADR-007. Store only bounded reviewed captures in `kb/raw/` or `kb/research/`; keep source originals in `sources/`. QMD indexing is optional and does not authorize publication.
8. **Validate and report.** Run the documented structural validator when applicable. Report factual review, structural validation, and QMD state as separate outcomes; do not claim one proves another.

## Guardrails

- A chip or component name alone does not prove wiring, pinout, driver support, firmware integration, electrical compatibility, or operation.
- Preserve conflicting evidence and limitations; do not upgrade owner-reported leads or inaccessible product pages into source-verified claims.
- Do not perform hardware operations, flashing, source execution, dependency setup, or QMD mutation unless separately authorized.
- If evidence is missing, document the gap and next evidence needed instead of inventing a compatibility path.
