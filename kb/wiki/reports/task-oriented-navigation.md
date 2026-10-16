---
type: "Report"
title: "Task-oriented Cardputer knowledge navigation"
description: "Four bounded routes through reviewed project profiles and source-inspected concepts, with evidence class and transfer limits kept visible."
status: stable
issue: "https://github.com/ozand/adv/issues/51"
---

# Task-oriented Cardputer knowledge navigation

This guide offers four routes through existing knowledge-base references. It is a selection aid, not a ranking or completeness claim. “Primary” identifies the closest reference for the task; “adjacent” supplies context; “contrast” distinguishes a related but different mechanism, not a capability comparison. Project profiles use `source-reported` evidence; concept cards use pinned `code-inspected` evidence. Neither label implies a successful build or device behavior.

## Choose a route

| If your task is… | Start with (primary) | Also read (adjacent) | Contrast | Key prerequisite or evidence gap |
|---|---|---|---|---|
| Accept multiline input in an interactive REPL | [Incremental multiline REPL input assembly](../concepts/incremental-multiline-repl-assembly.md) | [AREA512 profile](../entities/area512.md) | [Expression-evaluator pipeline](../concepts/expression-evaluator-pipeline.md) — input-completeness detection is a different stage from evaluating a complete expression. | The parser must expose incomplete-input semantics. Buffer bounds, cancellation, error handling, and runtime behavior are unknown. |
| Understand a calculator expression-evaluation pipeline | [Expression evaluator pipeline](../concepts/expression-evaluator-pipeline.md) | [CalcPuter profile](../entities/calculator-calcputer.md); [Cardulator profile](../entities/calculator-cardulator.md) | [Script statement-loop budget](../concepts/cooperative-script-loop-budget.md) — statement-loop control is distinct from expression stages. | Grammar completeness, mathematical correctness, edge cases, and feature parity are unknown. |
| Understand SD initialization in the published CardputerADV example | [SD initialization frequency retry](../concepts/sd-initialization-frequency-retry.md) | [Cardputer examples profile](../entities/cardputer-examples.md) | None: the approved references do not document a comparable alternative SD-initialization implementation. | Pins, bus assumptions, frequencies, and library semantics are example-specific; successful initialization and reliability are unknown. This is explanatory, not hardware or media-operation advice. |
| Examine an interpreter statement-loop step cap and periodic yield calls | [Script statement-loop cap and yield calls](../concepts/cooperative-script-loop-budget.md) | [Cardulator profile](../entities/calculator-cardulator.md) | [Incremental multiline REPL assembly](../concepts/incremental-multiline-repl-assembly.md) — input assembly is distinct from interpreter execution. | Evidence is a statement-iteration cap and loop-boundary yield/watchdog calls only; wall-clock bounds, preemption, responsiveness, and device behavior are unknown. |

## How to interpret these routes

- Start with the concept for the inspected mechanism; use the linked project profile for source-reported project context, not as proof of the mechanism's correctness.
- A contrast marks a difference in question or mechanism. It does not show that one project has a feature another lacks, or that either approach is superior.
- “Unknown” means the cited evidence does not answer the question. It does not mean unsupported, absent, safe, compatible, or complete.
- The SD route has no contrast because the approved released references provide no comparable alternative; none is inferred.
- The routes do not expand beyond the four approved tasks and memberships recorded in [Issue #51](https://github.com/ozand/adv/issues/51#issuecomment-6208400922). No source code, assets, or duplicated canonical profile/card content is included here.

## Provenance and limits

This is original navigation synthesis over released KB pages from Issues [#49](https://github.com/ozand/adv/issues/49) and [#50](https://github.com/ozand/adv/issues/50). Follow the source pins and limitations in each linked entity or concept. No source was newly inspected for this report; no build, runtime, device, SD-media, or QMD operation was performed. Rights caveats remain those documented on the linked pages; navigation does not clear upstream code, dependencies, or assets for reuse.
