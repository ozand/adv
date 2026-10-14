---
type: "Project"
title: "CalcPuter"
description: "C++ calculator described for Cardputer; upstream claims only."
status: draft
issue: "https://github.com/ozand/adv/issues/49"
object_profile: "Calculator"
sources:
  - resource: "https://github.com/advascript/calcputer/blob/d70d88d707f9fd289d096c4295b61159963c9b47/README.md"
    revision: "d70d88d707f9fd289d096c4295b61159963c9b47"
evidence:
  - claim: "README describes a C++ calculator with mathematical functions, formulas, fraction entry, and help."
    source: "https://github.com/advascript/calcputer/blob/d70d88d707f9fd289d096c4295b61159963c9b47/README.md"
    revision: "d70d88d707f9fd289d096c4295b61159963c9b47"
    method: "source-reported"
    locator: "README.md calculator feature description"
  - claim: "README lists PlatformIO and Arduino IDE setup and the M5Cardputer library."
    source: "https://github.com/advascript/calcputer/blob/d70d88d707f9fd289d096c4295b61159963c9b47/README.md"
    revision: "d70d88d707f9fd289d096c4295b61159963c9b47"
    method: "source-reported"
    locator: "README.md setup instructions"
applicability:
  target: "M5Stack Cardputer"
  state: "unknown"
  reason: "Upstream documentation is not a successful build or device verification."
rights:
  state: "unknown"
  reason: "Existing root MIT evidence does not clear bundled components or assets."
---

# CalcPuter — Issue #49 comparison profile

## Comparable dimensions
- **Role:** C++ calculator (source-reported).
- **Documented features:** Mathematical functions, formulas, fraction entry, and help are described in the existing pinned profile.
- **Prerequisites:** PlatformIO and Arduino IDE setup are documented; no build was run here.
- **Applicability:** Actual Cardputer model/build result remains **unknown**.
- **Rights:** Existing profile notes MIT root license evidence; bundled components/assets are not cleared.

## Identity

Approved repository revision: `d70d88d707f9fd289d096c4295b61159963c9b47`. This comparison profile is distinct from Cardulator, despite both being calculator-oriented.

See the [bounded comparison report](../reports/issue49-cardputer-comparison.md) and existing [CalcPuter profile](../entities/calculator-calcputer.md).

## Comparability

Compare with Cardulator only as calculator-oriented projects, using documented feature descriptions and cited source reports. Differences in detail are not evidence that an undocumented feature is absent; build and device behavior remain unknown.
