---
type: "Concept"
title: "Expression evaluator pipeline structure"
description: "A source-observed tokenizer, operator-stack, and value-stack evaluation pipeline."
status: draft
issue: "https://github.com/ozand/adv/issues/50"
object_profile: "Small expression-evaluation architecture"
sources:
  - resource: "https://github.com/advascript/calcputer/blob/d70d88d707f9fd289d096c4295b61159963c9b47/src/main.cpp"
    revision: "d70d88d707f9fd289d096c4295b61159963c9b47"
evidence:
  - claim: "The inspected source tokenizes expressions, emits reverse-Polish tokens using an operator stack, and evaluates them with a value stack and final stack-shape check."
    source: "https://github.com/advascript/calcputer/blob/d70d88d707f9fd289d096c4295b61159963c9b47/src/main.cpp"
    revision: "d70d88d707f9fd289d096c4295b61159963c9b47"
    method: "code-inspected"
    locator: "lines 70-100, 144-188"
applicability:
  target: "Small calculator-style expression evaluators"
  state: "unknown"
  reason: "The code structure was inspected, but grammar coverage and evaluation correctness were not tested."
rights:
  state: "review-required"
  reason: "The pinned repository has an MIT root license; bundled dependencies and assets were not separately cleared. This card reproduces no source code."
---

# Expression evaluator pipeline structure

## Problem
A calculator needs to turn a textual expression into operations that can be evaluated with explicit precedence handling.

## Observed mechanism
At the pinned CalcPuter revision, a tokenizer emits numeric, function, operator, and parenthesis tokens; its inspected logic also transforms a unary minus into a multiplication-by-negative-one token sequence. The evaluator uses an operator stack to emit reverse-Polish notation according to its local precedence/associativity condition, then evaluates that sequence with a numeric value stack and rejects a final stack size other than one. This describes visible source structure only.

## When it may help
This decomposition can be considered for a small calculator grammar: lexical analysis, precedence conversion, and evaluation are separate stages and can be independently specified and tested.

## Trade-offs and limits
Inspection does not establish grammar completeness, mathematical correctness, numeric edge-case behavior, or robust errors. Unary precedence/associativity, malformed input, decimal parsing, function arity, divide-by-zero behavior, resource bounds, and test coverage must be specified and validated independently. Do not treat this implementation as a correct parser by virtue of the pipeline shape.

## Evidence and provenance
Evidence is `code-inspected` at the exact revision and line locator above; no build, execution, or device test was performed. The existing CalcPuter README describes calculator features, but those statements are not used here as proof of evaluator correctness. Source identity and revision are immutable in the cited URL.

## Rights and transfer boundary
Original synthesis only; no upstream code or assets copied. The root MIT license does not independently clear bundled components or assets. Review applicable terms before reusing implementation.

## Related
- [Issue #50 proposal and exact source scope](https://github.com/ozand/adv/issues/50#issuecomment-6159929423)
- [CalcPuter project profile](../entities/calculator-calcputer.md)
