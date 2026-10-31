---
type: "Concept"
title: "WiFi portal request and state structure"
description: "A pinned-source example of HTTP request handlers and associated state, without deployment instructions."
issue: "https://github.com/ozand/adv/issues/100"
sources:
  - resource: "https://github.com/justcallmekoko/esp32marauder"
    revision: "b2b9f92382eb60b39b8741be3b567e416cdbe672"
evidence:
  - claim: "The source defines captive-endpoint handlers that return an HTML response and a separate request-state callback."
    source: "https://github.com/justcallmekoko/esp32marauder/blob/b2b9f92382eb60b39b8741be3b567e416cdbe672/esp32_marauder/EvilPortal.cpp"
    revision: "b2b9f92382eb60b39b8741be3b567e416cdbe672"
    method: "code-inspected"
    locator: "setupServer, lines 69–118; request state path, lines 120–140"
---

# WiFi portal request and state structure

## Bounded example

In the pinned source, [handlers](https://github.com/justcallmekoko/esp32marauder/blob/b2b9f92382eb60b39b8741be3b567e416cdbe672/esp32_marauder/EvilPortal.cpp#L69-L118) return an HTML response for configured endpoints and a [separate request callback](https://github.com/justcallmekoko/esp32marauder/blob/b2b9f92382eb60b39b8741be3b567e416cdbe672/esp32_marauder/EvilPortal.cpp#L120-L140) updates in-memory state when request parameters are present. This is a static request/state/output structure, not evidence that a portal was deployed, reached, or used successfully.

## Relation and unknowns

| Relation | Evidence and status |
|---|---|
| Device/component | Target device, firmware integration, and network configuration: `unknown`. |
| Operation | Handler and state code are code-inspected; runtime outcome is unknown. |
| Setup | Host configuration, DNS behavior in a live environment, user authorization, and prerequisites: `unknown`. |
| Data/output | Code retains request-derived state; complete storage and runtime outputs are not established by this bounded citation. |
| Scenario | No operational guidance or observed scenario is claimed. |

## Limits

This page intentionally does not document setup, deployment, lures, request fields, credential values, or operational use. WPAD is not established by this source slice. No completed portal or captured data is claimed.

## Related
- [Issue #100 WiFi synthesis](../../reports/protocols/wifi.md)
- [Credential-data state concept](wifi-credential-dataflow.md)
