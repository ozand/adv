---
type: "Concept"
title: "SD initialization frequency retry sequence"
description: "A board-specific SD initialization control flow observed in a CardputerADV example."
status: draft
issue: "https://github.com/ozand/adv/issues/50"
object_profile: "Board-specific peripheral initialization example"
sources:
  - resource: "https://github.com/konsumer/cardputer-examples/blob/6a648e32ad54457946ff7eb5a3b55a0dfaaa6cd2/src/sd/main.cpp"
    revision: "6a648e32ad54457946ff7eb5a3b55a0dfaaa6cd2"
evidence:
  - claim: "The inspected function drives GPIO 5 high, delays, initializes SPI, tries SD.begin at 25 MHz, then ends, delays, and retries at 16 MHz if the first attempt fails."
    source: "https://github.com/konsumer/cardputer-examples/blob/6a648e32ad54457946ff7eb5a3b55a0dfaaa6cd2/src/sd/main.cpp"
    revision: "6a648e32ad54457946ff7eb5a3b55a0dfaaa6cd2"
    method: "code-inspected"
    locator: "lines 11-27"
applicability:
  target: "The specific CardputerADV example and its stated shared-bus configuration"
  state: "unknown"
  reason: "No board, peripheral, or SD initialization was run or independently validated."
rights:
  state: "unknown"
  reason: "No established root LICENSE at the pinned revision; code, assets, and dependencies are not cleared for reuse. This card contains original prose only."
---

# SD initialization frequency retry sequence

## Problem
A peripheral initialization routine may include an alternate configuration attempt after its first attempt fails.

## Observed mechanism
In the pinned `src/sd/main.cpp`, `beginSDCard()` sets GPIO 5 to output/high, waits 2 ms, initializes SPI, and calls `SD.begin` at 25 MHz. If that call fails, the function calls `SD.end()`, waits 10 ms, and retries at 16 MHz. This is a description of source control flow only. The nearby “known-good” comment is not independent reliability evidence.

## When it may help
Treat this only as an example of explicit fallback sequencing to investigate for a board/peripheral combination. Re-derive pin ownership, shared-bus behavior, chip-select wiring, supported clock rates, and library failure/reinitialization semantics for the actual target.

## Trade-offs and limits
The source does not prove that either attempt succeeds, that the fallback is reliable, or that its delays/frequencies suit another board. The source repository has no established root license at this revision, so implementation reuse is not cleared. The example's later create/read/delete test-file operations are outside this pattern and were not run; do not use them on user media without explicit authorization.

## Evidence and provenance
Evidence is `code-inspected` at the exact revision and line locator above; no build, source execution, SD access, or device test was performed. Source identity and revision are immutable in the cited URL.

## Rights and transfer boundary
Original synthesis only; no code, screenshots, or assets copied. Rights for this repository's code, assets, and dependencies remain unknown. This is not legal clearance.

## Related
- [Issue #50 proposal and exact source scope](https://github.com/ozand/adv/issues/50#issuecomment-6159929423)
- [Cardputer examples project profile](../entities/cardputer-examples.md)
