# Issue #50 pattern-card candidate plan

## Authorization and boundaries

Issue #50; coordinator-relayed owner continuation instruction recorded at [comment 6182055337](https://github.com/ozand/adv/issues/50#issuecomment-6182055337). This is recorded as coordinator interpretation authorizing local drafting/review of only the four-pattern proposal, not as literal owner words approving patterns or a GitHub-authored owner statement. Exact proposal and source scopes: [comment 6159929423](https://github.com/ozand/adv/issues/50#issuecomment-6159929423). No public release, push, PR, merge, new source inspection, code/assets copying, builds/execution/device operation, or QMD/private-corpus operation is authorized here.

## Exact candidate outputs

1. `kb/wiki/concepts/incremental-multiline-repl-assembly.md` — AREA512, `python_repl.c`, lines 23–90, 116–179, revision `5d0fef94f389161421b1f7559c15d8303effa7be`.
2. `kb/wiki/concepts/sd-initialization-frequency-retry.md` — cardputer-examples, `src/sd/main.cpp`, lines 11–27, revision `6a648e32ad54457946ff7eb5a3b55a0dfaaa6cd2`.
3. `kb/wiki/concepts/expression-evaluator-pipeline.md` — CalcPuter, `src/main.cpp`, lines 70–100, 144–188, revision `d70d88d707f9fd289d096c4295b61159963c9b47`.
4. `kb/wiki/concepts/cooperative-script-loop-budget.md` — Cardulator, `src/script_engine.cpp`, lines 41–79, 1138–1145, revision `16e42a58bf67da0a4930ca7f257bdfd5b8c4f254`.

A minimal navigation link is in `kb/index.md`; no new concept taxonomy, schema, service, or pilot was introduced. The existing Issue #49 comparison report was deliberately not edited because it states only #49 content and links to project entities; adding #50 links there would be unrelated scope. This plan remains a local task artifact and is not linked from the canonical KB graph.

All are original synthesis, not copied implementation. Each claim is marked `code-inspected`; exact repository, immutable revision, file, and line locator are included. Runtime/applicability remains unknown where untested. Cards include problem, observed mechanism, applicability, trade-offs/limits, evidence/provenance, rights/transfer boundary, and links to existing project entities and the Issue #50 proposal. Cardulator limitations explicitly exclude bounded wall-clock time, responsiveness, preemption, real-time behavior, watchdog safety, and runtime success; SD sequence is not claimed reliable. See each card for detailed caveats.

Cumulative changed-path allowlist for this local candidate: this plan, `kb/index.md`, and exactly the four concept cards above (six files total). No tests, source captures, or unrelated canonical entities/reports are modified.

## Exclusions

No UcPlayground pattern: inspection scope was only the approved Cardputer test-firmwares subtree, whose README/artifact inventory offered no inspectable source mechanism. No claim about the whole repository. No one-pattern-per-source quota. No other repositories/revisions, binaries/assets, screenshots, raw captures, source code, or third-party material are included. Rights are not cleared by root-license notes; cardputer-examples rights remain unknown and dependencies/assets are unaudited.

## Verification/review gates

- Recheck changed-path allowlist (exactly the four concept cards, this plan, and the single `kb/index.md` navigation update); ensure no `sources/` path is tracked. Run `git diff --check` and parse all front matter; validate local internal links and exact revision/line metadata.
- Run the project's documented pinned `kb-bootstrap`/consumer structural validation only if the already-published tool/runtime is available without install/upgrade or QMD mutation. Report exact framework source pin, interpreter/import path/version, universal and consumer/graph layers separately. Do not claim corpus conformance from fixtures or partial checks.
- Attempt applicable repository tests; distinguish missing test files from test failures. Do not run upstream programs or devices.
- Independent read-only reviews must inspect the exact same full candidate commit and checklist (evidence/factual restraint, schema/links, rights/privacy/publication boundary). Any byte change invalidates prior review; rerun relevant checks and reviewers.
- A local commit/candidate is not public release approval. No push, PR, merge, or publication until a separate explicit owner release decision.
