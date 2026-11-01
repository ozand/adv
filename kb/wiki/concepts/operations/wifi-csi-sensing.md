---
type: "Concept"
title: "Wi-Fi CSI capture: a bounded source example"
description: "Static source-inspected CSI callback structure, not device or sensing-accuracy evidence."
issue: "https://github.com/ozand/adv/issues/100"
sources:
  - resource: "https://github.com/mohith-das/wiview"
    revision: "00de456ba58a5bcae4978e51c3c9095809801b7c"
evidence:
  - claim: "The README describes a CSI sensing application for Cardputer-Adv."
    source: "https://github.com/mohith-das/wiview/blob/00de456ba58a5bcae4978e51c3c9095809801b7c/README.md"
    revision: "00de456ba58a5bcae4978e51c3c9095809801b7c"
    method: "source-reported"
    locator: "lines 1–9"
  - claim: "CSI initialization configures CSI, registers a callback, enables CSI and returns on errors; the callback computes an aggregate and stores a bounded I/Q snapshot."
    source: "https://github.com/mohith-das/wiview/blob/00de456ba58a5bcae4978e51c3c9095809801b7c/firmware/src/csi/csi_capture.cpp"
    revision: "00de456ba58a5bcae4978e51c3c9095809801b7c"
    method: "code-inspected"
    locator: "lines 38–69 and 74–104"
  - claim: "A reader retries a bounded snapshot copy when the sequence changes; the writer updates that sequence after copying. This inspection alone does not establish a coherent concurrent snapshot."
    source: "https://github.com/mohith-das/wiview/blob/00de456ba58a5bcae4978e51c3c9095809801b7c/firmware/src/csi/csi_capture.cpp"
    revision: "00de456ba58a5bcae4978e51c3c9095809801b7c"
    method: "code-inspected"
    locator: "callback lines 57–63; csi_latest_iq lines 140–155"
---

# Wi-Fi CSI capture: a bounded source example

The pinned [wiview README](https://github.com/mohith-das/wiview/blob/00de456ba58a5bcae4978e51c3c9095809801b7c/README.md#L1-L9) describes a Channel State Information (CSI) sensing application for Cardputer-Adv. This target and sensing behavior are upstream-reported, not independently observed.

In the same revision, [initialization](https://github.com/mohith-das/wiview/blob/00de456ba58a5bcae4978e51c3c9095809801b7c/firmware/src/csi/csi_capture.cpp#L74-L104) configures CSI, registers a receive callback and enables CSI, returning failure when those calls fail. The [callback](https://github.com/mohith-das/wiview/blob/00de456ba58a5bcae4978e51c3c9095809801b7c/firmware/src/csi/csi_capture.cpp#L38-L69) calculates an aggregate from received I/Q pairs and retains a length-limited snapshot. These are static code structures, not evidence that initialization succeeds, CSI is received, or any person is detected.

## Snapshot handoff and uncertainty

The [reader](https://github.com/mohith-das/wiview/blob/00de456ba58a5bcae4978e51c3c9095809801b7c/firmware/src/csi/csi_capture.cpp#L140-L155) copies the current snapshot and compares a sequence value before and after the copy; it retries up to three times and can report failure. The [callback](https://github.com/mohith-das/wiview/blob/00de456ba58a5bcae4978e51c3c9095809801b7c/firmware/src/csi/csi_capture.cpp#L57-L63) updates that sequence after writing the snapshot. An unchanged sequence during the reader's comparison therefore does not by itself rule out an in-progress write. This source inspection does not establish thread safety, a reproducible race, actual output corruption, or device behavior.

## Evidence and limits

| Relation | Evidence and status |
|---|---|
| Device | README names Cardputer-Adv; tested compatibility: `unknown`. |
| Operation | CSI callback and initialization paths: `code-inspected`; runtime behavior: `unknown`. |
| Input/output | Callback reads I/Q data and retains an aggregate and bounded snapshot; actual values and downstream results: `unknown`. |
| Accuracy | Presence, motion and breathing accuracy, range and environmental sensitivity: `unknown`. |
| Verification | No firmware execution or device test. |

The source is outside the report's 46 candidate rows; eligibility is unresolved and no coverage denominator follows. No operational instructions or network captures are included.

## Related

- [Partial Wi-Fi domain synthesis](../../reports/protocols/wifi.md)
- [Issue #100](https://github.com/ozand/adv/issues/100)
