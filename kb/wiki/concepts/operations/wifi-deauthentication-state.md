---
type: "Concept"
title: "WiFi deauthentication state structure"
description: "Pinned-source examples of deauthentication-related state and received-frame classification, without operational guidance."
issue: "https://github.com/ozand/adv/issues/100"
sources:
  - resource: "https://github.com/0ct0sec/m5porkchop"
    revision: "38d7078c09205e23b65018fd486a5fd1e40ee440"
  - resource: "https://github.com/justcallmekoko/esp32marauder"
    revision: "b2b9f92382eb60b39b8741be3b567e416cdbe672"
evidence:
  - claim: "The OINK source defines bounded deauthentication-related state and schedules state transitions; this is source structure, not a claim of successful operation."
    source: "https://github.com/0ct0sec/m5porkchop/blob/38d7078c09205e23b65018fd486a5fd1e40ee440/src/modes/oink.cpp"
    revision: "38d7078c09205e23b65018fd486a5fd1e40ee440"
    method: "code-inspected"
    locator: "DeauthBurstState and timing state, lines 263–284"
  - claim: "Marauder's AP/STA callback classifies a received management frame into a deauthentication-related record path."
    source: "https://github.com/justcallmekoko/esp32marauder/blob/b2b9f92382eb60b39b8741be3b567e416cdbe672/esp32_marauder/WiFiScan.cpp"
    revision: "b2b9f92382eb60b39b8741be3b567e416cdbe672"
    method: "code-inspected"
    locator: "apSnifferCallbackFull, lines 7406–7428"
---

# WiFi deauthentication state structure

## Bounded examples

At the pinned m5porkchop revision, OINK declares [deauthentication-related state](https://github.com/0ct0sec/m5porkchop/blob/38d7078c09205e23b65018fd486a5fd1e40ee440/src/modes/oink.cpp#L263-L284), including target/client fields and scheduling metadata. At the pinned Marauder revision, one [AP/STA callback branch](https://github.com/justcallmekoko/esp32marauder/blob/b2b9f92382eb60b39b8741be3b567e416cdbe672/esp32_marauder/WiFiScan.cpp#L7406-L7428) classifies a received management frame into a deauthentication-related record path. These are two different static code observations; neither by itself proves a complete operation, successful effect, or device behavior.

## Relation and unknowns

| Relation | Evidence and status |
|---|---|
| Device/component | Exact supported board/radio and firmware-to-device mapping: `unknown`. |
| Firmware/source | Two pinned source examples; no prevalence claim. |
| Operation | State/data handling is source-inspected; full execution outcome is unknown. |
| Setup | Prerequisites, permissions, and environmental conditions: `unknown`. |
| Data/output | Complete runtime output, retention, and effect: `unknown`. |
| Scenario | No operational scenario or device observation is claimed. |

## Limits

This descriptive note does not provide attack steps, frame construction, timing instructions, or target selection. State names and received-frame classification do not establish runtime success, security impact, interoperability, or support on Cardputer hardware.

## Related
- [Issue #100 WiFi synthesis](../../reports/protocols/wifi.md)
- [Passive monitoring receive path](wifi-passive-monitoring.md)
