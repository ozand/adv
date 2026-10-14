---
type: "Project"
title: "AREA512"
description: "OS/runtime platform described for Cardputer variants; source-reported only."
status: draft
issue: "https://github.com/ozand/adv/issues/49"
object_profile: "Cardputer OS / runtime platform"
sources:
  - resource: "https://github.com/engneer-hamachan/area512/blob/5d0fef94f389161421b1f7559c15d8303effa7be/README.md"
    revision: "5d0fef94f389161421b1f7559c15d8303effa7be"
evidence:
  - claim: "Upstream report describes an OS for Cardputer v1.1 and ADV based on FemtoRuby."
    source: "https://github.com/engneer-hamachan/area512/blob/5d0fef94f389161421b1f7559c15d8303effa7be/README.md"
    revision: "5d0fef94f389161421b1f7559c15d8303effa7be"
    method: "source-reported"
    locator: "README.md project description"
applicability:
  target: "Cardputer variants"
  state: "unknown"
  reason: "Launcher variants remain distinct; shared repository identity does not establish identical build or hardware applicability."
---

# AREA512 — Issue #49 comparison profile

## Comparable dimensions
- **Role:** OS/runtime platform (source-reported by the pinned README project description).
- **Documented purpose:** Upstream report describes Cardputer v1.1 and ADV variants and names FemtoRuby.
- **Toolchain/prerequisites:** Not consistently represented in the existing approved comparison evidence; **unknown**.
- **Build/runtime/device result:** **unknown**; no build or hardware test was performed.
- **Rights:** Existing report notes an MIT root license; bundled components/assets were not cleared.

## Identity and evidence limits

Approved repository revision: `5d0fef94f389161421b1f7559c15d8303effa7be`. Keep Launcher variants separate; a common repository URL does not prove they are the same artifact or compatible target. Claims are source-reported, not device-verified.

See the [bounded comparison report](../reports/issue49-cardputer-comparison.md) and existing [Launcher source report](../reports/2026-10-07_launcher-cardputer-projects.md).

## Comparability

Compare this firmware/launcher entry only with Cardputer examples and UcPlayground on documented purpose and source-reported capabilities. Do not infer build success or hardware compatibility from README claims.
