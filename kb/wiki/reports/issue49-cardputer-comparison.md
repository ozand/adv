---
type: "ResearchReport"
title: "Cardputer project comparison — Issue #49"
description: "Bounded evidence-based comparison of five owner-approved Cardputer projects using existing pinned public references."
status: draft
issue: "https://github.com/ozand/adv/issues/49"
sources:
  - resource: "https://github.com/ozand/adv/blob/313e1ddb909c2487d0832b8783d03d06adc44199/kb/wiki/reports/2026-10-07_launcher-cardputer-projects.md"
    revision: "313e1ddb909c2487d0832b8783d03d06adc44199"
  - resource: "https://github.com/ozand/adv/blob/313e1ddb909c2487d0832b8783d03d06adc44199/kb/wiki/entities/calculator-calcputer.md"
    revision: "313e1ddb909c2487d0832b8783d03d06adc44199"
  - resource: "https://github.com/ozand/adv/blob/313e1ddb909c2487d0832b8783d03d06adc44199/kb/wiki/entities/calculator-cardulator.md"
    revision: "313e1ddb909c2487d0832b8783d03d06adc44199"
---

# Cardputer project comparison — Issue #49

**Delivered to `main` in PR #88.** The exact set/exclusions are recorded at [Issue #49](https://github.com/ozand/adv/issues/49#issuecomment-6094176320). The owner-authorized delivery instruction for this exact reviewed package is recorded as coordinator-relayed provenance at [Issue comment 6158421250](https://github.com/ozand/adv/issues/49#issuecomment-6158421250), not as a direct GitHub-authored owner statement. Post-merge verification confirmed the ten delivered file blobs match the reviewed PR and recorded the delivery audit at [Issue comment 6158888574](https://github.com/ozand/adv/issues/49#issuecomment-6158888574). This comparison reuses only already-published evidence references; it is not a new source inventory.

## Method and findings

The five projects fall into different categories: AREA512 is described as an OS/runtime platform; `cardputer-examples` and UcPlayground are collections of examples/test firmware; CalcPuter and Cardulator are calculator-oriented projects, with Cardulator also described as a REPL. These are not a uniform product set, so an overall feature ranking would be misleading and is not supported by available evidence.

Existing notes identify PlatformIO/Arduino setup for CalcPuter, a PlatformIO project for `cardputer-examples`, and PlatformIO commands for Cardulator. The available materials do not provide a consistent cross-project account of prerequisites or successful builds. Missing details remain `unknown`; no build was attempted. FemtoRuby is named in the AREA512 source report, but comparable toolchain detail is not available for all five.

Hardware applicability is evidence-limited. Sources report target variants or make support claims, but this work has no qualifying device observation or successful build evidence. Actual compatibility is therefore `unknown`, not unsupported. AREA512 launcher variants stay distinct despite a shared repository URL; UcPlayground remains a collection, not one firmware artifact.

## Rights and release limits

The existing report records no root LICENSE for `cardputer-examples`; rights for its code, assets, and dependencies remain unknown. Root-license evidence for other repositories does not clear each dependency or asset. This comparison paraphrases existing published descriptions and includes no upstream code, screenshots, raw captures, assets, or dependency material. A bounded owner instruction authorized public delivery of this exact five-project package; its coordinator-relayed provenance is recorded at [Issue comment 6158421250](https://github.com/ozand/adv/issues/49#issuecomment-6158421250), not as a direct GitHub-authored owner statement. PR #88 delivered the reviewed package to `main`; the post-merge audit is recorded at [Issue comment 6158888574](https://github.com/ozand/adv/issues/49#issuecomment-6158888574). The authorization grants no additional projects, claims, source acquisition, assets, or broader rights clearance. Rights to reuse excluded upstream assets/dependencies remain unknown.

## Exact set and exclusions

The exact five-entry manifest and explicit exclusions are recorded before content work in the [Issue #49 execution record](https://github.com/ozand/adv/issues/49#issuecomment-6094176320) and mirrored in `docs/issue49/approved-set.json`. The manifest also records coordinator-relayed release authorization at [comment 6158421250](https://github.com/ozand/adv/issues/49#issuecomment-6158421250); PR #88 delivered the reviewed package to `main`, with post-merge audit at [comment 6158888574](https://github.com/ozand/adv/issues/49#issuecomment-6158888574). All other Launcher rows/projects/repositories and additional variants/sources are excluded. No ranking, unsupported runtime/device claim, source acquisition, or QMD operation is authorized. The cited release authorization is limited to this exact reviewed package.

## Within-category comparison

### Firmware and examples

The existing Launcher report distinguishes AREA512 as an OS/runtime platform, `cardputer-examples` as standalone hardware-test examples, and UcPlayground as a project collection. Compare these three only on documented project role, target statements, and cited source-reported scope. The available report does not provide a common feature/build matrix, so no capability superiority or successful runtime can be concluded. See the individual [AREA512](../entities/area512.md), [Cardputer examples](../entities/cardputer-examples.md), and [UcPlayground](../entities/ucplayground-cardputer.md) profiles.

### Calculator applications

CalcPuter is documented as a calculator application; Cardulator as a scientific calculator/REPL. Existing profiles describe different feature detail and toolchain claims, not controlled parity evidence. Compare only those source-attributed descriptions; successful build, device behavior, and cross-project feature absence remain **unknown**. See the canonical [CalcPuter](../entities/calculator-calcputer.md) and [Cardulator](../entities/calculator-cardulator.md) entity profiles, extended with Issue #49 comparison notes.

## Existing source profiles

- [Selected Launcher projects](../reports/2026-10-07_launcher-cardputer-projects.md) — AREA512, examples, UcPlayground; pinned revisions and rights caveats.
- [CalcPuter](../entities/calculator-calcputer.md) and [Cardulator](../entities/calculator-cardulator.md) — existing revision-pinned canonical project profiles, extended in place with comparison notes.

The three firmware/example profiles under `../entities/` retain project distinctions, source pins and source-reported evidence. CalcPuter and Cardulator are not duplicated: their existing canonical entities carry the bounded Issue #49 comparison notes. The exact-set manifest is recorded at https://github.com/ozand/adv/issues/49#issuecomment-6094176320 and mirrored in the execution plan and `docs/issue49/approved-set.json`. Consumer-validator fixtures and pinned universal validation cover structure and links only; neither verifies truth, hardware operation, rights, nor public-release readiness.
