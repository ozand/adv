# Research workflow

Use this workflow for bounded, source-grounded research in the ADV knowledge project. It governs process, not topic selection or authority to access private material. The open Issue defines each task's scope and acceptance; this guide does not authorize QMD mutations, source retrieval, or publication by itself.

## 1. Intake and scope

- Identify the user question, intended decision or learning outcome, audience, and smallest useful deliverable.
- Verify a matching open GitHub Issue before research that changes tracked artifacts. Record included topics, exclusions, owner decisions needed, and stop conditions.
- Reuse current `kb/wiki/` records and accepted ADRs before starting duplicate research. Keep one question per bounded source set; do not turn every question into a market-research pipeline.
- If the request requires a new data boundary, source-access method, schema, dependency, or publication rule, stop for the applicable Issue/owner/ADR gate.
- For web research, define the question, source set, timebox, and stop condition before browsing. Prefer local/canonical evidence first; web search is optional, not a required pipeline.

## 2. Source hierarchy and retrieval

Prefer, in order appropriate to the question: primary project documentation; exact, immutable source revisions and manifests; standards or official platform references; then secondary analysis and community reports. A source search hit is a lead, not verification. Record canonical source identity, exact revision or dated URL, relevant file/section/line locator, access date, and why the source is relevant. If a revision or locator cannot be established, mark it unknown rather than guessing. For bounded web research, capture only the relevant public page/section and metadata needed to support the question; do not broaden the query or retain unrelated results. A page's own statement is `source-reported`; independently executed/measured behavior is `observed` and requires its own environment and result receipt. Never relabel reported claims as observed behavior.

Use Surf only when an Issue authorizes the bounded web-research action and the operator has selected the browser/window and access context. Follow the installed Surf skill's read-only navigation and capture guidance; do not open a new account, change login state, submit forms, or access private conversations as an implied part of research. If the intended browser/window or access authority is unclear, stop. Surf is optional and no Surf setup or dependency is required by this guide.

QMD is an optional, read-only retrieval aid. Before lookup, follow [Project QMD usage](qmd-usage.md): inspect the selected local runtime index and registered collections, then use only a listed collection. An index database selector is not a collection selector, and a tracked declaration does not prove runtime registration. A clean clone may lack the local index or source collections. Do not redirect to a parent/workspace index when routing is unexpected.

Stop and report when the intended index cannot be established, a collection is absent, paths are stale, vectors are zero/missing, or process success is uncertain. These observations do not authorize repair. Do not run `qmd update`, `qmd embed`, collection registration, index creation/rebuild, or global refresh without a separate scoped authorization and verified target. Do not execute, install, clone, or download source material unless the governing Issue separately authorizes that operation.

## 3. Capture and evidence classification

Keep source originals, whole repositories/books/PDFs, binaries, private captures, and bulky material in ignored local-only `sources/`. An externally obtained repository clone, if separately authorized, belongs under `sources/repo/` with a local provenance manifest recording canonical URL, exact revision, acquisition date, and any integrity hash; do not track that clone or copy it wholesale into public knowledge paths. Do not clone merely because a source is cited. A QMD result or local capture is not publication permission.

For each consequential claim, distinguish:

- **source-reported** — a source states the claim; cite the exact source and locator.
- **code-inspected** — the pinned code visibly implements the described structure; cite revision, path, and symbol/lines. This does not establish runtime behavior.
- **observed** — behavior was actually executed or measured; record exact command/environment, revision, result, and limits.
- **inference** — reasoning from evidence; label it and state assumptions and transfer limits.
- **unknown / not_run** — evidence is absent or execution did not occur; do not convert it to a negative product finding.

Separate evidence retrieval/indexing from substantive assessment. Preserve existing evidence labels and provenance; never raise confidence because a document is indexed, linked, or repeated in secondary sources.

## 4. Synthesis and publication review

Write original, concise synthesis in `kb/wiki/` with claim-level provenance and applicability/limitations. A useful, bounded public-source capture may be kept under `kb/research/<date>_<slug>/raw/` when appropriate; include only necessary excerpts/notes, source URL, access date, revision where available, and capture limitations. Screenshots are optional and only when needed to preserve relevant visual evidence; they are not required for every research task. Any capture tracked under `kb/raw/` or `kb/research/` requires privacy, secret, relevance, provenance, and rights review under accepted ADR-007/010/011. Evidence captures remain evidence; they are not canonical conclusions. Do not publish credentials, personal data, private network/device details, unredacted logs, unlicensed excerpts, source archives, or private conversations/URLs.

Before promoting a finding into canonical knowledge, check whether evidence supports each claim at the layer stated; identify contradictions, freshness, version limits, and unanswered questions. Keep primary-source observations separate from inference and community anecdote. Link to existing canonical knowledge rather than duplicating it when possible.

## 5. Review and stop conditions

Review exact changed paths and source citations; check links, provenance, privacy, rights, and that no local-only source/runtime state is included. Use only project-scoped validation authorized by the Issue. Structural or link checks do not prove technical truth. Re-review after any content change to the exact candidate revision.

Stop without repairing or broadening scope when access, provenance, rights, index routing, source revision, or owner decision is unresolved. Report the smallest blocker, what is and is not established, and a safe next step. Never claim current QMD health from historical snapshots, full coverage from a bounded sample, hardware behavior from source inspection, or publication approval from local indexing.
