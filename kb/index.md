---
type: index
title: adv Cardputer Knowledge Base
description: Entry point for synthesized, cited Cardputer knowledge.
status: stable
---

[KB guide](README.md)

# adv Cardputer Knowledge Base

This is the entry point for synthesized knowledge about Cardputer projects. Original source materials live locally under the ignored `sources/` directory and must not be committed.

## Topics

- [Selected Launcher projects](wiki/reports/2026-10-07_launcher-cardputer-projects.md) — revision-pinned, source-linked overview of three examples.

## Workflow

1. Keep source repositories, catalog payloads, captures, binaries, and books under ignored `sources/`.
2. Check primary-source documentation and license metadata; pin code-derived claims to exact revisions.
3. Publish only concise paraphrased synthesis with provenance and links, not copied source material.
4. Check for secrets, personal data, and private network details before publication.
5. Run `kb-bootstrap validate --dir kb --project-root .` when available.
