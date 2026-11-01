---
type: "Concept"
title: "WiFi AP authentication-mode display labels"
description: "A bounded code-inspected mapping from an AP-record authmode value to a UI label, not a protocol-support claim."
issue: "https://github.com/ozand/adv/issues/100"
sources:
  - resource: "https://github.com/brucedevices/firmware"
    revision: "a59213f3ec6cd302fa32c2042b2700c9c24d991a"
  - resource: "https://github.com/0ct0sec/m5porkchop"
    revision: "38d7078c09205e23b65018fd486a5fd1e40ee440"
evidence:
  - claim: "The converter maps auth-mode tokens to display labels, with fallback UNKNOWN."
    source: "https://github.com/brucedevices/firmware/blob/a59213f3ec6cd302fa32c2042b2700c9c24d991a/src/modules/wifi/ap_info.cpp"
    revision: "a59213f3ec6cd302fa32c2042b2700c9c24d991a"
    method: "code-inspected"
    locator: "autoMode2String, lines 12–26"
  - claim: "The AP-record authmode value is converted and placed in the Auth mode display row."
    source: "https://github.com/brucedevices/firmware/blob/a59213f3ec6cd302fa32c2042b2700c9c24d991a/src/modules/wifi/ap_info.cpp"
    revision: "a59213f3ec6cd302fa32c2042b2700c9c24d991a"
    method: "code-inspected"
    locator: "fillInfo, lines 74–90 and 109–111; displayAPInfo, lines 119–123"
  - claim: "The m5porkchop Cardputer build configuration declares an ESP32-S3 target."
    source: "https://github.com/0ct0sec/m5porkchop/blob/38d7078c09205e23b65018fd486a5fd1e40ee440/platformio.ini"
    revision: "38d7078c09205e23b65018fd486a5fd1e40ee440"
    method: "code-inspected"
    locator: "lines 3–8"
  - claim: "Beacon processing assigns authmode values using RSN/vendor fields and PMF flags; this does not establish correct protocol identification or device behavior."
    source: "https://github.com/0ct0sec/m5porkchop/blob/38d7078c09205e23b65018fd486a5fd1e40ee440/src/core/network_recon.cpp"
    revision: "38d7078c09205e23b65018fd486a5fd1e40ee440"
    method: "code-inspected"
    locator: "detectPMF and processBeacon, lines 243–302 and 377–415"
---

# WiFi AP authentication-mode display labels

## Bounded example

At pinned revision `a59213f3ec6cd302fa32c2042b2700c9c24d991a`, `autoMode2String` maps named auth-mode cases to labels such as `WPA_PSK`, `WPA2_PSK`, and `WPA3_PSK`; unmatched values return `UNKNOWN`. These are code-inspected token-to-string mappings, not explanations of protocol semantics. The external enum definitions were not inspected.

The inspected path is: AP record → `authmode` field → `autoMode2String` → label in the `Auth mode` row. The [header](https://github.com/brucedevices/firmware/blob/a59213f3ec6cd302fa32c2042b2700c9c24d991a/src/modules/wifi/ap_info.h#L1-L6) declares the `displayAPInfo()` entry point; `fillInfo` reads and converts the field (`ap_info.cpp`, lines 74–90, 109–111), and the view displays the row (lines 119–123). This is static source structure, not a scan result, runtime observation, or evidence of successful connection or authentication.

## Separate beacon classification example

At pinned revision `38d7078c09205e23b65018fd486a5fd1e40ee440`, the [build configuration](https://github.com/0ct0sec/m5porkchop/blob/38d7078c09205e23b65018fd486a5fd1e40ee440/platformio.ini#L3-L8) declares an ESP32-S3 Cardputer target. Separately, its [beacon-processing code](https://github.com/0ct0sec/m5porkchop/blob/38d7078c09205e23b65018fd486a5fd1e40ee440/src/core/network_recon.cpp#L243-L302) reads PMF-related flags and [assigns authmode enum values](https://github.com/0ct0sec/m5porkchop/blob/38d7078c09205e23b65018fd486a5fd1e40ee440/src/core/network_recon.cpp#L377-L415) from RSN/vendor fields and those flags for newly detected networks. This is a distinct source example, not the producer of the Bruce UI value above. Its decisions are application heuristics: the inspected code does not establish that every assigned value correctly identifies the network's security, nor that a connection or negotiation succeeds. No runtime or device check was performed.

## Relation and unknowns

| Relation | Evidence and status |
|---|---|
| Device/component | Bruce target device and WiFi component/variant: `unknown`; the separate m5porkchop build declares Cardputer/ESP32-S3. |
| Firmware/source | Bruce firmware at pinned revision above; code-inspected mapping only, not a compatibility claim. |
| Setup/prerequisites | Runtime prerequisites, API contract and configuration: `unknown`. |
| Input | Auth-mode value supplied through the AP record; API population and value provenance: `unknown`. |
| Operation/output | Static converter returns a display label, including fallback `UNKNOWN`; actual displayed runtime value: `unknown`. |
| Scenario | Editorial trace of source-record field to UI label; not an observed scenario. |

## Limits

The mapping does not establish enum meanings, protocol behavior, device/security-mode support, compatibility, or runtime accuracy. No device or source execution was performed. It adds no security-coverage claim to the separate [WiFi passive monitoring receive-path concept](wifi-passive-monitoring.md).

## Related

- [Issue #100: WiFi domain ontology](https://github.com/ozand/adv/issues/100)
