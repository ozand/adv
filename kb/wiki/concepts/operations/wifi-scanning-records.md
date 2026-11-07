---
type: "Concept"
title: "WiFi receive-side AP discovery records"
description: "A pinned-source example of building and displaying AP records from received management frames."
issue: "https://github.com/ozand/adv/issues/100"
sources:
  - resource: "https://github.com/runaque/adv_wardriver"
    revision: "ed08a787ecf0090cb174f9d55216033db5dce58a"
  - resource: "https://github.com/justcallmekoko/esp32marauder"
    revision: "b2b9f92382eb60b39b8741be3b567e416cdbe672"
evidence:
  - claim: "The ADV Wardriver README reports 2.4 GHz scans and GPS-fix-dependent SD logging, and names Cardputer ADV, Cap LoRa-1262 and microSD as hardware; original Cardputer is stated to be unsupported."
    source: "https://github.com/runaque/adv_wardriver/blob/ed08a787ecf0090cb174f9d55216033db5dce58a/README.md"
    revision: "ed08a787ecf0090cb174f9d55216033db5dce58a"
    method: "source-reported"
    locator: "README lines 8–9, 25–34, 42–50, 167–170"
  - claim: "The AP scan path initializes a promiscuous callback and channel selection; callback code reads received management-frame metadata."
    source: "https://github.com/justcallmekoko/esp32marauder/blob/b2b9f92382eb60b39b8741be3b567e416cdbe672/esp32_marauder/WiFiScan.cpp"
    revision: "b2b9f92382eb60b39b8741be3b567e416cdbe672"
    method: "code-inspected"
    locator: "RunAPScan, lines 4331–4368; apSnifferCallbackFull metadata/classification, lines 7406–7424; AP record update/construction, lines 7471–7497 and 7548–7597; queued display line, 7538–7541"
---

# WiFi receive-side AP discovery records

## Bounded example

At the pinned Marauder revision, [`RunAPScan`](https://github.com/justcallmekoko/esp32marauder/blob/b2b9f92382eb60b39b8741be3b567e416cdbe672/esp32_marauder/WiFiScan.cpp#L4331-L4368) configures the `apSnifferCallbackFull` path and channel selection. The [callback](https://github.com/justcallmekoko/esp32marauder/blob/b2b9f92382eb60b39b8741be3b567e416cdbe672/esp32_marauder/WiFiScan.cpp#L7406-L7424) receives packet metadata, obtains an address from the frame payload, and branches on management-frame type. Its beacon branch updates an existing AP record or constructs one with selected fields ([record handling](https://github.com/justcallmekoko/esp32marauder/blob/b2b9f92382eb60b39b8741be3b567e416cdbe672/esp32_marauder/WiFiScan.cpp#L7471-L7497), [construction and metadata assignment](https://github.com/justcallmekoko/esp32marauder/blob/b2b9f92382eb60b39b8741be3b567e416cdbe672/esp32_marauder/WiFiScan.cpp#L7548-L7597)); the callback also queues a display line in a conditional UI path ([display queue](https://github.com/justcallmekoko/esp32marauder/blob/b2b9f92382eb60b39b8741be3b567e416cdbe672/esp32_marauder/WiFiScan.cpp#L7538-L7541)). This documents a source-level receive/discovery and selected-record presentation structure, not an observed scan result or a claim about all AP fields.

## Cardputer ADV example (source-reported)

The pinned [ADV Wardriver README](https://github.com/runaque/adv_wardriver/blob/ed08a787ecf0090cb174f9d55216033db5dce58a/README.md#L25-L50) describes scanning 2.4 GHz access points and recording them to microSD with GNSS coordinates in WiGLE CSV format. It lists a Cardputer ADV, Cap LoRa-1262 and microSD, and explicitly says the original Cardputer is not supported. The README says an access point is logged only after a GPS fix and once per session ([logging rules](https://github.com/runaque/adv_wardriver/blob/ed08a787ecf0090cb174f9d55216033db5dce58a/README.md#L167-L170)). These are the author's reported features and requirements, not independently verified hardware behavior or compatibility. Location-tagged network records can be sensitive; handle their storage and sharing accordingly.

## Relation and unknowns

| Relation | Evidence and status |
|---|---|
| Device/component | Marauder target device and radio variant: `unknown`; ADV Wardriver's declared hardware is a separate README-reported example above. |
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
