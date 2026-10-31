---
type: "Concept"
title: "WiFi EAPOL callback and buffer structure"
description: "A bounded source-inspected example of EAPOL-related callback and buffer handling, not evidence of complete handshake capture."
issue: "https://github.com/ozand/adv/issues/100"
sources:
  - resource: "https://github.com/justcallmekoko/esp32marauder"
    revision: "b2b9f92382eb60b39b8741be3b567e416cdbe672"
evidence:
  - claim: "An EAPOL-related callback inspects received packet fields, tracks an EAPOL count, and has packet-buffer append code in the bounded inspected branch."
    source: "https://github.com/justcallmekoko/esp32marauder/blob/b2b9f92382eb60b39b8741be3b567e416cdbe672/esp32_marauder/WiFiScan.cpp"
    revision: "b2b9f92382eb60b39b8741be3b567e416cdbe672"
    method: "code-inspected"
    locator: "eapolSnifferCallback, lines 10361–10390 and 10505–10524, including EAPOL count at line 10517; EAPOL/beacon buffer append lines 10572–10573"
---

# WiFi EAPOL callback and buffer structure

## Bounded example

At the pinned Marauder revision, `eapolSnifferCallback` processes received frames, classifies EAPOL-related traffic, and increments an EAPOL counter in its data-frame path ([callback setup and frame handling](https://github.com/justcallmekoko/esp32marauder/blob/b2b9f92382eb60b39b8741be3b567e416cdbe672/esp32_marauder/WiFiScan.cpp#L10361-L10390), [EAPOL count and frame parsing](https://github.com/justcallmekoko/esp32marauder/blob/b2b9f92382eb60b39b8741be3b567e416cdbe672/esp32_marauder/WiFiScan.cpp#L10505-L10524)). A separate bounded branch appends a received frame to an internal buffer when the callback marks it as EAPOL or beacon ([append condition](https://github.com/justcallmekoko/esp32marauder/blob/b2b9f92382eb60b39b8741be3b567e416cdbe672/esp32_marauder/WiFiScan.cpp#L10572-L10574)). These are code structures only; they do not establish a completed handshake, successful capture, exported format, or runtime behavior.

## Relation and unknowns

| Relation | Evidence and status |
|---|---|
| Device/component | Radio variant and supported device: `unknown`. |
| Firmware/source | Marauder at the pinned revision; static code-inspected path. |
| Operation | EAPOL-related observation/callback processing is evidenced; complete handshake capture is not established. |
| Setup | Runtime settings, prerequisites, and environment: `unknown`. |
| Data/output | A buffer append path exists in the cited slice; schema, persistence, completeness, and export are `unknown`. |
| Scenario | No packet collection or device scenario was performed. |

## Limits

An EAPOL callback or packet buffer is not proof of a complete four-message exchange, a usable artifact, protocol-version support, or device success. No packet details, operational instructions, or capture procedure are included.

## Related
- [Issue #100 WiFi synthesis](../../reports/protocols/wifi.md)
- [Passive monitoring receive path](wifi-passive-monitoring.md)
