# Issue #50 bounded source-artifact assessment receipts

**Receipt:** [Issue #50 comment 6207606025](https://github.com/ozand/adv/issues/50#issuecomment-6207606025). The independent assessor’s public receipt records the bounded review. This companion records its source pin/path/range, outcome, limitations and review decisions, and adds an explicit card-target mapping for the current candidate; the target relations are local mappings, not claims in the assessor receipt.

**Assessment date:** 2026-10-16 UTC. **Reviewer:** Pi reviewer session `01a122d6-c790-761b-9cf7-687200c76ee1` (agent/session identity; not human-authorship attestation).

## AREA512 — multiline REPL accumulation
- **Source artifact:** `https://github.com/engneer-hamachan/area512/blob/5d0fef94f389161421b1f7559c15d8303effa7be/components/area512/mrbgems/picoruby-area512-repl/src/python_repl.c`
- **Revision / locator:** `5d0fef94f389161421b1f7559c15d8303effa7be`; `lines 23-90, 116-179`.
- **Assessment outcome:** Inspected lines show newline-separated input appending, incomplete-input checking before execution, and buffer reset after execution or interruption. The proposed card describes only this bounded source mechanism.
- **Limitations:** No maximum buffer, memory-safety, parser correctness, complete cleanup, build, runtime, or device guarantee. Applicability requires incomplete-input semantics.
- **Review decisions / rights:** Exact source pin/range retained; no code/assets copied. Root MIT does not clear bundled components/assets. No legal, privacy, publication, or device clearance asserted.
- **Target relation:** `kb/wiki/concepts/incremental-multiline-repl-assembly.md` (explicit candidate mapping; relation is not asserted to be in the assessor's receipt).

## cardputer-examples — SD initialization retry sequence
- **Source artifact:** `https://github.com/konsumer/cardputer-examples/blob/6a648e32ad54457946ff7eb5a3b55a0dfaaa6cd2/src/sd/main.cpp`
- **Revision / locator:** `6a648e32ad54457946ff7eb5a3b55a0dfaaa6cd2`; `lines 11-27`.
- **Assessment outcome:** Source sets GPIO 5 high, delays 2 ms, initializes SPI, tries SD at 25 MHz, then on failure ends SD, delays 10 ms and retries at 16 MHz. Source's “known-good” comment is not independent verification.
- **Limitations:** Control-flow only; no successful initialization/reliability result. Pins, shared-bus assumptions, clock rates and library behavior are board-specific. Later file operations were outside scope and not run.
- **Review decisions / rights:** Exact pin/range retained; no code/assets copied. No root LICENSE established at this pin; implementation/assets/dependencies uncleared. No legal, privacy, publication, or device clearance asserted.
- **Target relation:** `kb/wiki/concepts/sd-initialization-frequency-retry.md` (explicit candidate mapping; relation is not asserted to be in the assessor's receipt).

## CalcPuter — expression evaluator pipeline
- **Source artifact:** `https://github.com/advascript/calcputer/blob/d70d88d707f9fd289d096c4295b61159963c9b47/src/main.cpp`
- **Revision / locator:** `d70d88d707f9fd289d096c4295b61159963c9b47`; `lines 70-100, 144-188`.
- **Assessment outcome:** Inspected tokenizer creates expression tokens and rewrites unary minus; an operator stack emits RPN under local precedence rules; a value stack evaluates and checks final stack size. Structure only, not correctness.
- **Limitations:** No grammar, math/edge-case, numeric, error, resource, test, build, runtime, or device guarantee.
- **Review decisions / rights:** Exact pin/range retained; README claims do not establish evaluator correctness; no code/assets copied. Root MIT does not clear bundled dependencies/assets. No legal, privacy, publication, or device clearance asserted.
- **Target relation:** `kb/wiki/concepts/expression-evaluator-pipeline.md` (explicit candidate mapping; relation is not asserted to be in the assessor's receipt).

## Cardulator — statement-loop cap and periodic yield calls
- **Source artifact:** `https://github.com/aroum/cardulator/blob/16e42a58bf67da0a4930ca7f257bdfd5b8c4f254/src/script_engine.cpp`
- **Revision / locator:** `16e42a58bf67da0a4930ca7f257bdfd5b8c4f254`; `lines 41-79, 1138-1145`.
- **Assessment outcome:** Inspected `runScript` counts statement-loop steps up to 10,000, makes target-specific yield/watchdog calls at loop boundaries, then reports loop-limit exhaustion.
- **Limitations:** No wall-clock bound, responsiveness, preemption, real-time, watchdog-safety, successful execution, build, or device guarantee. A statement/native call may exceed intervals; watchdog reset return is unchecked in range; arrays are left unrestored.
- **Review decisions / rights:** Exact pin/range retained; no code/assets copied. GPL-3.0 and separately named dependency terms require review before implementation reuse; assets unaudited. No legal, privacy, publication, or device clearance asserted.
- **Target relation:** `kb/wiki/concepts/cooperative-script-loop-budget.md` (explicit candidate mapping; relation is not asserted to be in the assessor's receipt).

## Scope boundary

Exactly these four bounded source-artifact assessments are recorded; this is not a census of the five-project set or whole repositories. No new source, revision, path, binary, private material, QMD state, source execution, or device operation was used. The assessor receipt and this explicit source-to-target mapping do not prove factual truth, applicability, rights clearance, or publication permission.
