---
type: index
title: adv Cardputer Knowledge Base
description: Entry point for synthesized, cited Cardputer knowledge.
status: stable
---

[KB guide](README.md)

# adv Cardputer Knowledge Base

This is the entry point for Cardputer knowledge. Bounded research captures in `raw/` and `research/` may be publicly tracked after privacy, secret, relevance, provenance, and rights review; they are evidence, not canonical conclusions. Original repositories, books/PDFs, binaries, private captures, and bulky source materials remain local-only under ignored `sources/` and must not be committed.

## Topics

- [Reported Cardputer and agent-device interface examples](research/2026-10-08_cardputer-agent-usage/output.md) — Issue #35 bounded evidence handoff; project reports, not adoption data.

- [Selected Launcher projects](wiki/reports/2026-10-07_launcher-cardputer-projects.md) — revision-pinned, source-linked overview of three examples.
- [CalcPuter](wiki/entities/calculator-calcputer.md) — upstream-documented calculator features and source/license references.
- [Cardulator](wiki/entities/calculator-cardulator.md) — upstream-documented scientific calculator/REPL features and source/license references.

## Workflow

1. Keep original source repositories, catalog payloads, books/PDFs, binaries, private captures, and bulky materials under ignored `sources/`.
2. Check primary-source documentation and license metadata; pin code-derived claims to exact revisions.
3. Publish reviewed, bounded evidence captures under `raw/` or `research/` only after privacy, secret, relevance, provenance, and rights review. Synthesize supported claims into `wiki/` with provenance and links; captures remain evidence, not canonical synthesis.
4. Check for secrets, personal data, and private network details before publication.
5. Run `kb-bootstrap validate --dir kb --project-root .` when available.
