# Agent working context for Cardputer KB tasks

Use this short checklist when turning an existing KB question into bounded research or synthesis. It complements, and never overrides, the governing Issue, `AGENTS.md`, accepted ADRs, or the [bounded batch workflow](bounded-batch-knowledge-workflow.md).

## Work from evidence

1. State the user's task and the mechanism or question being answered; keep the scope and exclusions tied to the open Issue.
2. Reuse existing canonical KB records where possible. For a new source-derived statement, cite its repository, document/path, and full immutable revision. A branch, mutable commit selection, local dirty override, or search result alone is not stable provenance.
3. Separate what upstream documentation claims (`source-reported`) from what a pinned code range visibly implements (`code-inspected`) and from behavior actually observed. A structural checker validates form and links, not semantics or truth.
4. State limits, prerequisites, and transfer conditions beside the claim. Missing evidence is `unknown`, not unsupported, safe, compatible, or complete.
5. Preserve claim-level provenance and existing evidence labels; don't copy upstream code, templates, assets, or whole documents. Prefer links to already published canonical material over duplication.

## Keep repository boundaries

- Follow accepted ADR-007 for privacy, provenance, relevance, rights, and local-only source originals; ADR-010/011/012 for evidence, disposition, and validation boundaries; ADR-013 for bounded, exact-SHA review and delivery.
- `kb/research/` is reviewed evidence; `kb/wiki/` is original, provenance-linked synthesis. QMD membership is not publication permission.
- The cited symbol registry does not support C++ symbols; ordinary file links remain possible, but structural/reference checks do not validate symbol semantics. Preserve source pins/locators and unknown applicability.
- External documentation/search behavior and local override precedence are properties of the cited tool, not this KB. Do not claim retrieval or freshness without the separately authorized check.
- Treat generated agent templates as examples that can become stale. Reconcile any proposed text with current repository instructions; never replace them wholesale from an upstream template.
- No new schema, dependency, service, graph, generator, MCP, hooks, migration, source execution, device operation, or QMD mutation without a separately governed decision and authorization.

## Review handoff

Before publishing, inspect the exact staged paths; exclude `sources/`, private/local state, and unreviewed captures. Run only project-scoped checks from the isolated task root and record actual command, root, revision, result, and limits. Independent review must identify the exact candidate SHA; any content change requires review of the new SHA. Report residual rights/evidence/runtime limits without converting structural PASS into factual assurance.
