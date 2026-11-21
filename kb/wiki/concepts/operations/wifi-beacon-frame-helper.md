---
type: "Concept"
title: "WiFi beacon-frame field helper"
description: "A narrow source-inspected helper that updates one beacon-buffer field, not a complete beacon-spam operation."
issue: "https://github.com/ozand/adv/issues/100"
sources:
  - resource: "https://github.com/justcallmekoko/esp32marauder"
    revision: "b2b9f92382eb60b39b8741be3b567e416cdbe672"
  - resource: "https://github.com/henriquesebastiao/saturn"
    revision: "814c2230b183d9d4557c3fd8fb2d93cdfaaff43a"
  - resource: "https://github.com/lshaf/unigeek"
    revision: "a5ad2f379e115d375d4e5978720f40c345464ed1"
evidence:
  - claim: "The helper validates a buffer/index condition and writes one channel value into a frame buffer."
    source: "https://github.com/justcallmekoko/esp32marauder/blob/b2b9f92382eb60b39b8741be3b567e416cdbe672/esp32_marauder/BeaconFrame.cpp"
    revision: "b2b9f92382eb60b39b8741be3b567e416cdbe672"
    method: "code-inspected"
    locator: "setBeaconFrameChannel, lines 3–15"
  - claim: "A list-processing path updates a frame buffer and calls a transmit API."
    source: "https://github.com/henriquesebastiao/saturn/blob/814c2230b183d9d4557c3fd8fb2d93cdfaaff43a/src/beacon.h"
    revision: "814c2230b183d9d4557c3fd8fb2d93cdfaaff43a"
    method: "code-inspected"
    locator: "lines 229–286"
  - claim: "A screen selects inputs and calls a separate beacon helper."
    source: "https://github.com/lshaf/unigeek/blob/a5ad2f379e115d375d4e5978720f40c345464ed1/firmware/src/screens/wifi/WifiBeaconSpamScreen.cpp"
    revision: "a5ad2f379e115d375d4e5978720f40c345464ed1"
    method: "code-inspected"
    locator: "lines 115–162"
---

# WiFi beacon-frame field helper

## Bounded example

The pinned source contains [`setBeaconFrameChannel`](https://github.com/justcallmekoko/esp32marauder/blob/b2b9f92382eb60b39b8741be3b567e416cdbe672/esp32_marauder/BeaconFrame.cpp#L3-L15), which computes an index, checks the buffer and index bounds, and updates one channel field. This is a small frame-buffer helper, not evidence that it creates complete beacon frames, transmits them, or repeats transmission.

## Other bounded source structures

In [Saturn's source](https://github.com/henriquesebastiao/saturn/blob/814c2230b183d9d4557c3fd8fb2d93cdfaaff43a/src/beacon.h#L229-L286), a list-processing path updates a frame buffer and calls a transmit API. By contrast, a [UniGeek screen](https://github.com/lshaf/unigeek/blob/a5ad2f379e115d375d4e5978720f40c345464ed1/firmware/src/screens/wifi/WifiBeaconSpamScreen.cpp#L115-L162) selects inputs and calls a separate helper. Both observations are `code-inspected`; the latter link alone does not inspect the helper's behavior. Neither call site proves actual transmission, correct frames, effective operation or device compatibility.

## Relation and unknowns

| Relation | Evidence and status |
|---|---|
| Device/component | Device and radio compatibility: `unknown`. |
| Firmware/source | Marauder at pinned revision; one helper is code-inspected. |
| Operation | One buffer-field update only; complete generation/transmission operation is not established here. |
| Setup/data/output | Runtime setup, frame completeness, output destination, and retention: `unknown`. |
| Scenario | No live or device scenario observed. |

## Limits

Do not generalize this helper to beacon-spam capability, protocol conformance, repeated transmission, or Cardputer support. The exact wider implementation and behavior were not inspected for this note.

## Related
- [Issue #100 WiFi synthesis](../../reports/protocols/wifi.md)
