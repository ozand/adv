---
type: "Concept"
title: "WiFi receive-side AP discovery records"
description: "A pinned-source example of building and displaying AP records from received management frames."
issue: "https://github.com/ozand/adv/issues/100"
sources:
  - resource: "https://github.com/justcallmekoko/esp32marauder"
    revision: "b2b9f92382eb60b39b8741be3b567e416cdbe672"
evidence:
  - claim: "The AP scan path initializes a promiscuous callback and channel selection; callback code reads received management-frame metadata."
    source: "https://github.com/justcallmekoko/esp32marauder/blob/b2b9f92382eb60b39b8741be3b567e416cdbe672/esp32_marauder/WiFiScan.cpp"
    revision: "b2b9f92382eb60b39b8741be3b567e416cdbe672"
    method: "code-inspected"
    locator: "RunAPScan, lines 4331–4368; apSnifferCallbackFull, lines 7406–7424"
---

# WiFi receive-side AP discovery records

## Bounded example

At the pinned Marauder revision, [`RunAPScan`](https://github.com/justcallmekoko/esp32marauder/blob/b2b9f92382eb60b39b8741be3b567e416cdbe672/esp32_marauder/WiFiScan.cpp#L4331-L4368) configures the `apSnifferCallbackFull` path and channel selection. The [callback](https://github.com/justcallmekoko/esp32marauder/blob/b2b9f92382eb60b39b8741be3b567e416cdbe672/esp32_marauder/WiFiScan.cpp#L7406-L7424) receives packet metadata, obtains an address from the frame payload, and branches on management-frame type. This documents a source-level receive/discovery structure, not an observed scan result or a claim about all AP fields.

## Relation and unknowns

| Relation | Evidence and status |
|---|---|
| Device/component | Target device and radio variant: `unknown`. |
| Firmware/source | Marauder at the pinned revision; code-inspected structure, not Cardputer compatibility. |
| Operation | Receive-side AP discovery/recording path; static code only. |
| Setup | Runtime configuration, permissions, and radio prerequisites: `unknown`. |
| Data/output | Frame metadata is read; complete record schema, persistence, and retention: `unknown`. |
| Scenario | Editorial source-pattern description only; no live network or device observation. |

## Limits

This source slice does not establish which security protocols or generations can be negotiated, successful operation on a named device, or a separate active-probe procedure. Absence of an active scan API in this cited slice is not a whole-firmware negative finding.

## Related
- [Issue #100 WiFi synthesis](../../reports/protocols/wifi.md)
- [Passive monitoring receive path](wifi-passive-monitoring.md)
