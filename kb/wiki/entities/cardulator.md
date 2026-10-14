---
type: "Project"
title: "Cardulator"
description: "Scientific calculator and REPL described for Cardputer ADV and T-Deck Pro; unverified."
status: draft
issue: "https://github.com/ozand/adv/issues/49"
object_profile: "Calculator / REPL"
sources:
  - resource: "https://github.com/aroum/cardulator/blob/16e42a58bf67da0a4930ca7f257bdfd5b8c4f254/README.md"
    revision: "16e42a58bf67da0a4930ca7f257bdfd5b8c4f254"
evidence:
  - claim: "README describes a scientific calculator and REPL with unit conversion, formula tools, scripting, and plotting."
    source: "https://github.com/aroum/cardulator/blob/16e42a58bf67da0a4930ca7f257bdfd5b8c4f254/README.md"
    revision: "16e42a58bf67da0a4930ca7f257bdfd5b8c4f254"
    method: "source-reported"
    locator: "README.md feature description"
  - claim: "README claims builds for Cardputer ADV and LilyGO T-Deck Pro and lists PlatformIO build/test commands."
    source: "https://github.com/aroum/cardulator/blob/16e42a58bf67da0a4930ca7f257bdfd5b8c4f254/README.md"
    revision: "16e42a58bf67da0a4930ca7f257bdfd5b8c4f254"
    method: "source-reported"
    locator: "README.md build instructions and target claims"
applicability:
  target: "Cardputer ADV and LilyGO T-Deck Pro"
  state: "unknown"
  reason: "README support statements are not builds or device observations; this work did not run them."
rights:
  state: "unknown"
  reason: "Existing profile notes GPL-3.0 root license, but dependency and asset terms were not fully audited."
---

# Cardulator — Issue #49 comparison profile

## Comparable dimensions
- **Role:** Scientific calculator and REPL (source-reported).
- **Documented features:** Unit conversion, formula tools, scripting, and plotting are listed in the existing pinned profile.
- **Prerequisites:** PlatformIO commands are listed; not run for this comparison.
- **Applicability:** README claims Cardputer ADV and T-Deck Pro; actual build/device result remains **unknown**.
- **Rights:** Existing profile notes GPL-3.0 root license and dependencies; all assets/dependency terms remain incompletely audited.

## Identity

Approved repository revision: `16e42a58bf67da0a4930ca7f257bdfd5b8c4f254`. Keep distinct from CalcPuter.

See the [bounded comparison report](../reports/issue49-cardputer-comparison.md) and existing [Cardulator profile](../entities/calculator-cardulator.md).

## Comparability

Compare with CalcPuter as calculator-oriented projects using only documented, cited feature descriptions. Cardulator's REPL description is source-reported; it is not a verified runtime result. Undocumented feature coverage remains unknown.
