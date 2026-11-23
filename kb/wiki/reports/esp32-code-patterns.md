---
type: "Report"
title: "ESP32 communication code patterns: bounded catalog"
description: "Source-pinned implementation structures and explicitly unresolved categories."
issue: "https://github.com/ozand/adv/issues/107"
---

# ESP32 communication code patterns: bounded catalog

Use this index to locate evidence-backed implementation structures, not instructions to operate them. `code-inspected` means static source inspection; it does not establish runtime behavior, Cardputer compatibility, complete operation, or corpus prevalence. Configuration and error handling are limited to the cited paths; uninspected behavior is unknown.

## Passive monitoring: shared receive and deferred records

The [m5porkchop receive path](../concepts/operations/wifi-passive-monitoring.md) registers a callback for promiscuous reception and queues selected metadata for later processing ([pinned source](https://github.com/0ct0sec/m5porkchop/blob/38d7078c09205e23b65018fd486a5fd1e40ee440/src/core/network_recon.cpp#L847-L869), [enqueue](https://github.com/0ct0sec/m5porkchop/blob/38d7078c09205e23b65018fd486a5fd1e40ee440/src/core/network_recon.cpp#L131-L142), [deferred drain](https://github.com/0ct0sec/m5porkchop/blob/38d7078c09205e23b65018fd486a5fd1e40ee440/src/core/network_recon.cpp#L640-L692)). This configuration is a receive-path structure, not proof the whole application is passive. Complete error handling and retention are unknown.

**API/configuration:** `WiFi.mode` selects station mode; `esp_wifi_set_promiscuous_rx_cb`, `esp_wifi_set_promiscuous_filter` and `esp_wifi_set_promiscuous` set the receive path; `esp_wifi_set_channel` sets its current channel. **Errors:** `enqueuePendingNetwork` returns false on a full queue; the cited setup does not check those API return values. Other failure handling is not established.

## Active probing: bounded connection result

Marauder's [connection-check helper](https://github.com/justcallmekoko/esp32marauder/blob/b2b9f92382eb60b39b8741be3b567e416cdbe672/esp32_marauder/WiFiScan.cpp#L11378-L11390) sets a timeout, calls a connection API, stops the client on either branch and returns a Boolean. Its [caller](https://github.com/justcallmekoko/esp32marauder/blob/b2b9f92382eb60b39b8741be3b567e416cdbe672/esp32_marauder/WiFiScan.cpp#L11631-L11664) records positive results. This is `code-inspected` error/result handling, not proof of reachability or an operational scanning recipe.

**API/configuration:** `checkHostPort` calls `WiFiClient::setTimeout`, `connect` and `stop`; the cited caller passes a timeout value of 100. The unit and runtime effect are not established by this slice. **Errors:** unsuccessful `connect` returns false after `stop`; detailed causes are not distinguished. Related [WiFi protocol context](../entities/protocols/wifi-80211.md); no separate probing concept relation is established here.

## Credential-related request state

The [Marauder request-state concept](../concepts/operations/wifi-credential-dataflow.md) describes a [request callback](https://github.com/justcallmekoko/esp32marauder/blob/b2b9f92382eb60b39b8741be3b567e416cdbe672/esp32_marauder/EvilPortal.cpp#L120-L140) and [conditional output branch](https://github.com/justcallmekoko/esp32marauder/blob/b2b9f92382eb60b39b8741be3b567e416cdbe672/esp32_marauder/EvilPortal.cpp#L399-L424). Configuration and error handling beyond those cited branches remain unknown. No actual credential, request payload, deployment steps, or successful capture is documented.

**API/configuration:** the inspected handler uses `server.on` and `request->send`; `EvilPortal::main` checks the selected mode and AP/HTML state before `dnsServer.processNextRequest`, `Serial.print` and `buffer_obj.append`. **Errors:** the state guard returns early; failure handling for response, DNS and output calls is not established in these slices. No request parameter names or operational setup are provided.

## Control/emulation: HID report submission

A [Cardputer HID example](https://github.com/destillegast/m5cardputer-hid-tools/blob/6224edb227827e9755cd4e6635102e677e50d632/src/regular_keyboard.cpp#L10-L42) reads keyboard state and invokes report submission and release methods. This is a `code-inspected` call path, not proof of host acceptance or device operation. Setup, error handling and supported hardware outside the linked slice are unknown. The [ontology validation note](https://github.com/ozand/adv/blob/8abc8b6f9965d1e68a927674ddb131460f1ad0df/docs/research/issue-99-ontology-validation.md) records the source context and rights uncertainty.

**API/configuration:** `M5Cardputer.Keyboard.isChange`, `isPressed` and `keysState` gate construction of a `KeyReport`; `USBHIDKeyboard::sendReport` and `releaseAll` are called. **Errors:** the cited slice does not check return values or establish host acceptance; USB initialization/configuration is outside it. No separate HID ontology entity is established by this note; the [ontology validation record](https://github.com/ozand/adv/blob/8abc8b6f9965d1e68a927674ddb131460f1ad0df/docs/research/issue-99-ontology-validation.md) links the bounded source sample.

## Parameter extraction: receive metadata and record creation

At the pinned m5porkchop revision, the [receive callback](https://github.com/0ct0sec/m5porkchop/blob/38d7078c09205e23b65018fd486a5fd1e40ee440/src/core/network_recon.cpp#L587-L626) reads packet metadata and dispatches frames. The [beacon handler](https://github.com/0ct0sec/m5porkchop/blob/38d7078c09205e23b65018fd486a5fd1e40ee440/src/core/network_recon.cpp#L298-L324) rejects short input and initializes a record with selected fields. It [queues new records](https://github.com/0ct0sec/m5porkchop/blob/38d7078c09205e23b65018fd486a5fd1e40ee440/src/core/network_recon.cpp#L417-L422); the [enqueue path](https://github.com/0ct0sec/m5porkchop/blob/38d7078c09205e23b65018fd486a5fd1e40ee440/src/core/network_recon.cpp#L131-L142) can reject a full queue. This is `code-inspected` field extraction, not proof of accurate classification, complete capture, device support or observed values. See [receive-path concept](../concepts/operations/wifi-passive-monitoring.md).

**API/configuration:** `promiscuousCallback` reads signal length and RSSI before dispatch; `processBeacon` initializes BSSID, RSSI and current-channel fields. Receive configuration is described under passive monitoring above. **Errors:** the handler returns on short input and `enqueuePendingNetwork` returns false when full; the cited caller does not check that return. Field correctness and other parser errors are not established.

## Outward data transfer is not automatically exfiltration

The same pinned project's [file response path](https://github.com/0ct0sec/m5porkchop/blob/38d7078c09205e23b65018fd486a5fd1e40ee440/src/web/xfer_server.cpp#L4090-L4126) contains input and file-open rejection branches; a [separate loop](https://github.com/0ct0sec/m5porkchop/blob/38d7078c09205e23b65018fd486a5fd1e40ee440/src/web/xfer_server.cpp#L4145-L4214) reads file data and writes to a client with stalled-transfer exits. This is a `code-inspected` outward transfer structure, not evidence of unauthorized disclosure, recipient identity, access-control correctness, successful transfer or device behavior. Configuration beyond the cited paths is unknown; no file paths, payloads, endpoint details or operating instructions are provided.

## Outbound upload: bounded egress pattern

In [Adversary's pinned upload service](https://github.com/isonimus/adversary/blob/79085dd76f45afa745f2c054eaa22df77cb3cbf2/src/modules/network/wpasec_service.cpp#L59-L113), the code checks file availability and size, connection, clock and available memory before creating a secure client and attempting a connection. A [later path](https://github.com/isonimus/adversary/blob/79085dd76f45afa745f2c054eaa22df77cb3cbf2/src/modules/network/wpasec_service.cpp#L135-L150) reopens the file and calls a stream helper. The [helper](https://github.com/isonimus/adversary/blob/79085dd76f45afa745f2c054eaa22df77cb3cbf2/src/modules/network/tls_upload.cpp#L115-L169) aborts on low memory, lost connection, read failure or incomplete write. These are `code-inspected` data-egress structures relevant to the requested exfiltration category; they do **not** establish unauthorized disclosure, malicious intent, remote acceptance, certificate correctness, actual data transfer or device behavior. No credentials, endpoint details, payloads or operating procedure are reproduced.

**API/configuration:** `SD.open`, `WiFi.isConnected`, `timeSyncedForTls`, `heapTooLowForTls`, `WiFiClientSecure`, `applyCaBundle`, `setTimeout`, `connectWithRetry` and `streamFile` appear in the cited path. **Errors:** file-open, size, connectivity, clock, memory, connect and stream failures have return branches; response acceptance and certificate correctness are not established by these slices. No separate egress ontology concept relation is established; the related [credential-state concept](../concepts/operations/wifi-credential-dataflow.md) concerns a different source and does not prove a link between these implementations.

The earlier [bounded ontology sample](https://github.com/ozand/adv/blob/8abc8b6f9965d1e68a927674ddb131460f1ad0df/docs/research/issue-99-ontology-validation.md) did not establish an exfiltration example. This subsequent source slice establishes an upload path only, not the circumstances or authorization of any disclosure. Issue #107 remains open pending full acceptance review.

## Evidence and safety boundary

Links point to pinned upstream revisions; local original repositories remain outside the KB. Published content is bounded factual synthesis, not copied source, captured data, operational steps or a claim of rights clearance. Missing error handling, configuration and target applicability must not be filled from names or labels. Related: [WiFi synthesis](protocols/wifi.md) and [Issue #107](https://github.com/ozand/adv/issues/107).
