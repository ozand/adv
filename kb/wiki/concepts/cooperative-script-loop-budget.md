---
type: "Concept"
title: "Script statement-loop step cap and periodic yield calls"
description: "A source-observed interpreter loop cap with periodic watchdog-reset and yield calls."
status: draft
issue: "https://github.com/ozand/adv/issues/50"
object_profile: "Embedded interpreter loop-control example"
sources:
  - resource: "https://github.com/aroum/cardulator/blob/16e42a58bf67da0a4930ca7f257bdfd5b8c4f254/src/script_engine.cpp"
    revision: "16e42a58bf67da0a4930ca7f257bdfd5b8c4f254"
evidence:
  - claim: "The inspected runScript statement loop caps its counter at 10,000 and makes periodic target-conditional watchdog-reset/yield calls, then records loop-limit exhaustion."
    source: "https://github.com/aroum/cardulator/blob/16e42a58bf67da0a4930ca7f257bdfd5b8c4f254/src/script_engine.cpp"
    revision: "16e42a58bf67da0a4930ca7f257bdfd5b8c4f254"
    method: "code-inspected"
    locator: "lines 41-79, 1138-1145"
applicability:
  target: "The inspected Cardulator script interpreter branches and their stated compile-time targets"
  state: "unknown"
  reason: "No compilation, runtime, watchdog, or device behavior was verified."
rights:
  state: "review-required"
  reason: "The pinned project root license is GPL-3.0; named third-party dependencies have separate terms and assets were not audited. This card reproduces no source code."
---

# Script statement-loop step cap and periodic yield calls

## Problem
An embedded script interpreter may need a loop-level stopping condition and opportunities to yield between interpreted statements.

## Observed mechanism
At the pinned Cardulator revision, `runScript` counts statement-loop iterations and uses `max_steps = 10000`. On ESP32-target branches it calls `esp_task_wdt_reset()` and `delay(1)` every 64 steps or when a sampled elapsed-time condition exceeds 15 ms; the Arduino branch calls `delay(1)` every 64 steps. Reaching the counter cap appends a “Loop limit reached” message. These are statements present in source, not verified operational guarantees.

## When it may help
This is an example to consider when designing explicit interpreter-loop budgeting and cooperative yield points. Define target-specific watchdog integration, scheduler behavior, counter semantics, and failure reporting for the actual runtime.

## Trade-offs and limits
The counter and sampled-time checks occur only at interpreter-loop boundaries. Work within a statement, expression, or native call may take arbitrarily long relative to those checks; this does not establish a wall-clock bound, responsiveness, preemption, or real-time behavior. The inspected code does not check the watchdog-reset return value. It explicitly leaves arrays unrestored. No watchdog safety or runtime success is claimed.

## Evidence and provenance
Evidence is `code-inspected` at the exact revision and line locator above; no build, execution, watchdog, or device test was performed. Source identity and revision are immutable in the cited URL.

## Rights and transfer boundary
Original synthesis only; no upstream code or assets copied. The root GPL-3.0 license and separately named dependency terms require review before any implementation reuse; assets were not audited. This card is not legal clearance.

## Related
- [Issue #50 proposal and exact source scope](https://github.com/ozand/adv/issues/50#issuecomment-6159929423)
- [Cardulator project profile](../entities/calculator-cardulator.md)
