---
type: "ProjectCollection"
title: "Cardputer examples"
description: "Collection of standalone Cardputer ADV hardware-test examples; repository-level rights unresolved."
status: draft
issue: "https://github.com/ozand/adv/issues/49"
object_profile: "Hardware test example collection"
sources:
  - resource: "https://github.com/konsumer/cardputer-examples/blob/6a648e32ad54457946ff7eb5a3b55a0dfaaa6cd2/README.md"
    revision: "6a648e32ad54457946ff7eb5a3b55a0dfaaa6cd2"
evidence:
  - claim: "Existing report describes standalone Cardputer ADV hardware-test examples and a PlatformIO project."
    source: "https://github.com/konsumer/cardputer-examples/blob/6a648e32ad54457946ff7eb5a3b55a0dfaaa6cd2/README.md"
    revision: "6a648e32ad54457946ff7eb5a3b55a0dfaaa6cd2"
    method: "source-reported"
    locator: "README.md project description"
applicability:
  target: "Cardputer ADV example collection"
  state: "unknown"
  reason: "No build or physical-device verification; individual examples may differ."
rights:
  state: "unknown"
  reason: "No root LICENSE at the pinned revision; asset and dependency terms are not established."
---

# Cardputer examples — Issue #49 comparison profile

## Comparable dimensions
- **Role:** Collection of standalone hardware-test examples, not one end-user product (source-reported by the pinned README project description).
- **Documented prerequisites:** Existing report identifies a PlatformIO project; exact per-example prerequisites remain **unknown**.
- **Build/runtime/device result:** **unknown**; no build or device test was performed.
- **Rights:** Root repository license absent at approved revision; code, assets and dependencies are not cleared for reuse.

## Identity and safety

Approved repository revision: `6a648e32ad54457946ff7eb5a3b55a0dfaaa6cd2`. This profile cites and paraphrases the existing public report; it reproduces no source code, screenshots, assets, or raw captures. Rights remain an explicit release limitation.

See the [bounded comparison report](../reports/issue49-cardputer-comparison.md) and [existing Launcher source report](../reports/2026-10-07_launcher-cardputer-projects.md).

## Comparability

Compare this examples collection with other firmware/example projects only on documented project role and source-reported scope. It is not directly comparable to the CalcPuter/Cardulator calculator applications.
