---
type: "Concept"
title: "WiFi portal request-derived state"
description: "A code-inspected example of request-derived state and output branches, not proof of a completed credential capture."
issue: "https://github.com/ozand/adv/issues/100"
sources:
  - resource: "https://github.com/justcallmekoko/esp32marauder"
    revision: "b2b9f92382eb60b39b8741be3b567e416cdbe672"
evidence:
  - claim: "The request callback assigns parameter values into state; a later main-loop branch formats that state for serial and buffer output, with an optional display path."
    source: "https://github.com/justcallmekoko/esp32marauder/blob/b2b9f92382eb60b39b8741be3b567e416cdbe672/esp32_marauder/EvilPortal.cpp"
    revision: "b2b9f92382eb60b39b8741be3b567e416cdbe672"
    method: "code-inspected"
    locator: "request state, lines 120–140; main output branch, lines 399–424"
---

# WiFi portal request-derived state

## Bounded example

The inspected [request callback](https://github.com/justcallmekoko/esp32marauder/blob/b2b9f92382eb60b39b8741be3b567e416cdbe672/esp32_marauder/EvilPortal.cpp#L120-L140) assigns supplied values into application state. A later [code path](https://github.com/justcallmekoko/esp32marauder/blob/b2b9f92382eb60b39b8741be3b567e416cdbe672/esp32_marauder/EvilPortal.cpp#L399-L424) checks state flags and formats that state for serial output and an internal buffer, with an optional display call. This establishes a code-inspected dataflow structure, not the presence of any actual user data or a completed capture.

## Relation and unknowns

| Relation | Evidence and status |
|---|---|
| Device/component | Device, firmware mapping, and runtime environment: `unknown`. |
| Operation | Request-derived state and output path are code-inspected; no runtime event was observed. |
| Setup | Request path availability, user consent, prerequisites, and configuration: `unknown`. |
| Data/output | State-to-output branches are visible; actual values, retention, access controls, and downstream destination: `unknown`. |
| Scenario | No actual credential collection or operational scenario is claimed. |

## Limits

This note contains no request field names, payloads, credentials, setup, or deployment instructions. Handler code alone does not establish successful capture, storage duration, security impact, or Cardputer applicability. Rights for source reuse remain separate from this original-prose synthesis.

## Related
- [Portal request/state structure](wifi-evil-portal-structure.md)
- [Issue #100 WiFi synthesis](../../reports/protocols/wifi.md)
