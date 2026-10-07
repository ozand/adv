---
type: "Project"
title: "CalcPuter"
description: "A Cardputer calculator project described by its upstream README."
tags: [cardputer, calculator, catalog-project]
status: stable
issue: "https://github.com/ozand/adv/issues/3"
sources:
  - resource: "https://github.com/advascript/calcputer/blob/d70d88d707f9fd289d096c4295b61159963c9b47/README.md"
    revision: "d70d88d707f9fd289d096c4295b61159963c9b47"
    license_evidence: "Repository README states MIT; root LICENSE is present at this revision. Bundled components/assets not separately audited."
  - resource: "https://github.com/advascript/calcputer/blob/d70d88d707f9fd289d096c4295b61159963c9b47/LICENSE"
    revision: "d70d88d707f9fd289d096c4295b61159963c9b47"
    license: "MIT"
---

# CalcPuter

## Overview

The upstream README presents CalcPuter as a C++ calculator for M5Stack Cardputer, with expression evaluation, built-in formulas, fraction entry, and a help screen. These are README claims, not independently tested behavior.

## Key facts

- The README lists mathematical functions including trigonometry, roots, logarithms, and rounding operations.
- It documents PlatformIO and Arduino IDE setup directions and identifies the M5Cardputer library.
- The README's device/build statements do not establish compatibility with every Cardputer variant or a successful build on this revision.

## Catalog identity and licensing

- Launcher catalog listing FID: `fd254f0082bf90ccb2826f91be969f76`.
- Upstream repository: [advascript/calcputer](https://github.com/advascript/calcputer).
- The README states MIT and a root `LICENSE` file is present at the pinned revision. This does not independently establish terms for bundled dependencies or assets.

## References

- [Pinned upstream README](https://github.com/advascript/calcputer/blob/d70d88d707f9fd289d096c4295b61159963c9b47/README.md)
- [Pinned upstream LICENSE](https://github.com/advascript/calcputer/blob/d70d88d707f9fd289d096c4295b61159963c9b47/LICENSE)
