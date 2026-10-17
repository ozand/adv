# Bounded adaptation of lat.md research ideas

**Status:** Accepted for the finite Issue #92 Markdown adaptation; not an architecture or schema decision.
**Issue:** [#92](https://github.com/ozand/adv/issues/92)
**Upstream identity:** [`vercel-labs/lat.md` at `4cb85d97baff4a659e9da837a9aab447509e32cd`](https://github.com/vercel-labs/lat.md/tree/4cb85d97baff4a659e9da837a9aab447509e32cd)

## Decision

Reuse only these ideas in existing Markdown workflows: record research decisions with explicit rationale and evidence; provide concise agent context rather than copying a large prompt; and demonstrate a task-to-mechanism-to-source-to-limits-to-transfer-to-evidence chain using already released KB content. Keep sources immutable and distinguish an upstream project's claims or examples from independently verified behavior.

This is original analysis, not a port of lat.md. It adds no canonical schema, API, dependency, installation, vault, graph, service, embeddings, MCP, hooks, generator, or new publication/search layer. It does not change accepted ADR-007/010/011/012/013 or current wiki/research boundaries. An architecture change would require its own decision and authorization.

## Applicable observations and limits

The pinned upstream material describes a documentation-oriented research workflow, supported language/reference behavior, external-source treatment, and a generated agent template. These are bounded observations of that pinned repository, not Cardputer KB guarantees. This adaptation keeps only practical Markdown guidance and rejects tool or architecture adoption.

Important constraints from the inspected pinned materials:

- The symbol registry does not support C++ symbols. This does not prevent ordinary file links; nor does a structural/reference check validate symbol semantics or establish source truth. Existing concept cards' pinned source URLs and locators remain the evidence anchors.
- External documentation sources are read-only and excluded from semantic search in the described project. This KB does not adopt or claim that retrieval setup.
- A configured source selection can change; a mutable ref resolves to an immutable commit pin for retrieval. A local content override may select another pin or expose dirty working-tree bytes even when the recorded HEAD matches the pin. Cite full immutable commit URLs for provenance, distinguish selected pin from actual local bytes, and never silently retarget or treat a local override as proof of source identity.
- Structural validation checks shape/references, not semantic truth, runtime behavior, hardware compatibility, or rights.
- Generated agent templates can become stale. The existing `AGENTS.md` and accepted ADRs remain authoritative; do not copy the upstream template wholesale, especially where its setup assumptions differ from this repository's offline-default guidance.
- No unmeasured speed, multilingual, or other performance claim is adopted.

## Worked mapping using existing released knowledge

**Task:** understand how an interactive REPL may accumulate multiline input.

- **Mechanism:** the AREA512 concept card describes appending lines, checking incomplete input, executing complete accumulated input, and resetting on execution/interruption.
- **Immutable source:** `area512` revision `5d0fef94f389161421b1f7559c15d8303effa7be`, [`python_repl.c` lines 23–90 and 116–179](https://github.com/engneer-hamachan/area512/blob/5d0fef94f389161421b1f7559c15d8303effa7be/components/area512/mrbgems/picoruby-area512-repl/src/python_repl.c).
- **Limits:** the existing card labels this `code-inspected`; it was not built, executed, or device-tested. Buffer bounds, memory safety, parser correctness, error recovery, and language-wide applicability are unknown. The source alone does not establish those properties.
- **Transfer conditions:** consider only where the target parser exposes incomplete-input semantics; independently define buffer/encoding limits, cancellation, error handling, and cleanup for every exit path.
- **Evidence chain:** follow the existing [canonical concept card](../../kb/wiki/concepts/incremental-multiline-repl-assembly.md) and [AREA512 project profile](../../kb/wiki/entities/area512.md). The profile's README claim remains `source-reported`, distinct from the card's `code-inspected` mechanism. Neither establishes runtime truth or clears bundled rights.

This example links existing knowledge; it does not duplicate the card, introduce new claims, or upgrade its evidence class.

## References

Pinned upstream sources inspected for this bounded adaptation:

- [`lat-workflow.md`](https://github.com/vercel-labs/lat.md/blob/4cb85d97baff4a659e9da837a9aab447509e32cd/lat.md/docs/lat-workflow.md) — capture decisions and review intent/evidence.
- [`concepts.md`](https://github.com/vercel-labs/lat.md/blob/4cb85d97baff4a659e9da837a9aab447509e32cd/lat.md/docs/concepts.md) — supported languages and the limits of references/checks.
- [`external_sources.md`](https://github.com/vercel-labs/lat.md/blob/4cb85d97baff4a659e9da837a9aab447509e32cd/lat.md/docs/external_sources.md) and [`external-sources.md`](https://github.com/vercel-labs/lat.md/blob/4cb85d97baff4a659e9da837a9aab447509e32cd/lat.md/knowledge/external-sources.md) — pin identity, read-only/retrieval boundaries, mutable commit and local override caveats.
- [README.md](https://github.com/vercel-labs/lat.md/blob/4cb85d97baff4a659e9da837a9aab447509e32cd/README.md) and [`templates/AGENTS.md`](https://github.com/vercel-labs/lat.md/blob/4cb85d97baff4a659e9da837a9aab447509e32cd/templates/AGENTS.md) — project scope and template lifecycle/staleness context.

No upstream source was executed or modified. The upstream repository is cited as research evidence only; no code, generated template, assets, or bulk source content is copied here.
