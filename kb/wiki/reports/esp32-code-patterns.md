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

## Active probing: bounded connection result

Marauder's [connection-check helper](https://github.com/justcallmekoko/esp32marauder/blob/b2b9f92382eb60b39b8741be3b567e416cdbe672/esp32_marauder/WiFiScan.cpp#L11378-L11390) sets a timeout, calls a connection API, stops the client on either branch and returns a Boolean. Its [caller](https://github.com/justcallmekoko/esp32marauder/blob/b2b9f92382eb60b39b8741be3b567e416cdbe672/esp32_marauder/WiFiScan.cpp#L11631-L11664) records positive results. This is `code-inspected` error/result handling, not proof of reachability or an operational scanning recipe.

## Credential-related request state

The [Marauder request-state concept](../concepts/operations/wifi-credential-dataflow.md) describes a [request callback](https://github.com/justcallmekoko/esp32marauder/blob/b2b9f92382eb60b39b8741be3b567e416cdbe672/esp32_marauder/EvilPortal.cpp#L120-L140) and [conditional output branch](https://github.com/justcallmekoko/esp32marauder/blob/b2b9f92382eb60b39b8741be3b567e416cdbe672/esp32_marauder/EvilPortal.cpp#L399-L424). Configuration and error handling beyond those cited branches remain unknown. No actual credential, request payload, deployment steps, or successful capture is documented.

## Control/emulation: HID report submission

A [Cardputer HID example](https://github.com/destillegast/m5cardputer-hid-tools/blob/6224edb227827e9755cd4e6635102e677e50d632/src/regular_keyboard.cpp#L10-L42) reads keyboard state and invokes report submission and release methods. This is a `code-inspected` call path, not proof of host acceptance or device operation. Setup, error handling and supported hardware outside the linked slice are unknown. The [ontology validation note](https://github.com/ozand/adv/blob/8abc8b6f9965d1e68a927674ddb131460f1ad0df/docs/research/issue-99-ontology-validation.md) records the source context and rights uncertainty.

## Parameter extraction and data exfiltration

**Unresolved:** the original [bounded ontology sample](https://github.com/ozand/adv/blob/8abc8b6f9965d1e68a927674ddb131460f1ad0df/docs/research/issue-99-ontology-validation.md) did not establish distinct implementation patterns for either category. A request-state assignment or generic file transfer alone is not evidence of a separate exfiltration pattern. No API, configuration, error handling, or concrete source-backed implementation is claimed for these two categories. They remain research gaps, not proof of absence in the corpus; Issue #107 remains open until its full scope is resolved.

## Evidence and safety boundary

Links point to pinned upstream revisions; local original repositories remain outside the KB. Published content is bounded factual synthesis, not copied source, captured data, operational steps or a claim of rights clearance. Missing error handling, configuration and target applicability must not be filled from names or labels. Related: [WiFi synthesis](protocols/wifi.md) and [Issue #107](https://github.com/ozand/adv/issues/107).
