---
type: "ResearchReport"
title: "Cardputer project comparison — Issue #49"
description: "Bounded evidence-based comparison of five owner-approved Cardputer projects using existing pinned public references."
status: draft
issue: "https://github.com/ozand/adv/issues/49"
sources:
  - resource: "https://github.com/ozand/adv/blob/main/kb/wiki/reports/2026-10-07_launcher-cardputer-projects.md"
    revision: "313e1ddb909c2487d0832b8783d03d06adc44199"
  - resource: "https://github.com/ozand/adv/blob/main/kb/wiki/entities/calculator-calcputer.md"
    revision: "313e1ddb909c2487d0832b8783d03d06adc44199"
  - resource: "https://github.com/ozand/adv/blob/main/kb/wiki/entities/calculator-cardulator.md"
    revision: "313e1ddb909c2487d0832b8783d03d06adc44199"
---

# Cardputer project comparison — Issue #49

**Draft for review; not approved for public release.** The exact set/exclusions and coordinator-relayed owner decision are recorded at [Issue #49](https://github.com/ozand/adv/issues/49#issuecomment-6094176320). This comparison reuses only already-published evidence references; it is not a new source inventory.

## Method and findings

The five projects fall into different categories: AREA512 is described as an OS/runtime platform; `cardputer-examples` and UcPlayground are collections of examples/test firmware; CalcPuter and Cardulator are calculator-oriented projects, with Cardulator also described as a REPL. These are not a uniform product set, so an overall feature ranking would be misleading and is not supported by available evidence.

Existing notes identify PlatformIO/Arduino setup for CalcPuter, a PlatformIO project for `cardputer-examples`, and PlatformIO commands for Cardulator. The available materials do not provide a consistent cross-project account of prerequisites or successful builds. Missing details remain `unknown`; no build was attempted. FemtoRuby is named in the AREA512 source report, but comparable toolchain detail is not available for all five.

Hardware applicability is evidence-limited. Sources report target variants or make support claims, but this work has no qualifying device observation or successful build evidence. Actual compatibility is therefore `unknown`, not unsupported. AREA512 launcher variants stay distinct despite a shared repository URL; UcPlayground remains a collection, not one firmware artifact.

## Rights and release limits

The existing report records no root LICENSE for `cardputer-examples`; rights for its code, assets, and dependencies remain unknown. Root-license evidence for other repositories does not clear each dependency or asset. This draft paraphrases existing published descriptions and copies no upstream code, screenshots, or raw captures. Before any public release, obtain separate explicit approval and complete privacy, provenance, and rights review. Unresolved rights remain a blocker to reuse of affected material.

## Exact set and exclusions

The exact five-entry manifest and explicit exclusions are recorded before content work in the [Issue #49 execution record](https://github.com/ozand/adv/issues/49#issuecomment-6094176320) and mirrored in `docs/issue49/approved-set.json`. All other Launcher rows/projects/repositories and additional variants/sources are excluded. No ranking, unsupported runtime/device claim, source acquisition, QMD operation, or release permission is inferred.

## Within-category comparison

### Firmware and examples

The existing Launcher report distinguishes AREA512 as an OS/runtime platform, `cardputer-examples` as standalone hardware-test examples, and UcPlayground as a project collection. Compare these three only on documented project role, target statements, and cited source-reported scope. The available report does not provide a common feature/build matrix, so no capability superiority or successful runtime can be concluded. See the individual [AREA512](../entities/area512.md), [Cardputer examples](../entities/cardputer-examples.md), and [UcPlayground](../entities/ucplayground-cardputer.md) profiles.

### Calculator applications

CalcPuter is documented as a calculator application; Cardulator as a scientific calculator/REPL. Existing profiles describe different feature detail and toolchain claims, not controlled parity evidence. Compare only those source-attributed descriptions; successful build, device behavior, and cross-project feature absence remain **unknown**. See [CalcPuter](../entities/calcputer.md) and [Cardulator](../entities/cardulator.md).

## Existing source profiles

- [Selected Launcher projects](../reports/2026-10-07_launcher-cardputer-projects.md) — AREA512, examples, UcPlayground; pinned revisions and rights caveats.
- [CalcPuter](../entities/calculator-calcputer.md) and [Cardulator](../entities/calculator-cardulator.md) — existing revision-pinned public profiles.

The five Issue #49 profiles under `../entities/` retain project distinctions, source pins and source-reported evidence. The exact-set manifest is recorded at https://github.com/ozand/adv/issues/49#issuecomment-6094176320 and mirrored in the execution plan. Consumer-validator fixtures and pinned universal validation cover structure and links only; neither verifies truth, hardware operation, rights, nor public-release readiness.
