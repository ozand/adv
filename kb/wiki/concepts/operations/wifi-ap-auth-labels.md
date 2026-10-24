---
type: "Concept"
title: "WiFi AP authentication-mode display labels"
description: "A bounded code-inspected mapping from an AP-record authmode value to a UI label, not a protocol-support claim."
issue: "https://github.com/ozand/adv/issues/100"
sources:
  - resource: "https://github.com/brucedevices/firmware"
    revision: "a59213f3ec6cd302fa32c2042b2700c9c24d991a"
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
---

# WiFi AP authentication-mode display labels

## Bounded example

At pinned revision `a59213f3ec6cd302fa32c2042b2700c9c24d991a`, `autoMode2String` maps named auth-mode cases to labels such as `WPA_PSK`, `WPA2_PSK`, and `WPA3_PSK`; unmatched values return `UNKNOWN`. These are code-inspected token-to-string mappings, not explanations of protocol semantics. The external enum definitions were not inspected.

The inspected path is: AP record → `authmode` field → `autoMode2String` → label in the `Auth mode` row. The [header](https://github.com/brucedevices/firmware/blob/a59213f3ec6cd302fa32c2042b2700c9c24d991a/src/modules/wifi/ap_info.h#L1-L6) declares the `displayAPInfo()` entry point; `fillInfo` reads and converts the field (`ap_info.cpp`, lines 74–90, 109–111), and the view displays the row (lines 119–123). This is static source structure, not a scan result, runtime observation, or evidence of successful connection or authentication.

## Relation and unknowns

| Relation | Evidence and status |
|---|---|
| Device/component | Target device and WiFi component/variant: `unknown`. |
| Firmware/source | Bruce firmware at pinned revision above; code-inspected mapping only, not a compatibility claim. |
| Setup/prerequisites | Runtime prerequisites, API contract and configuration: `unknown`. |
| Input | Auth-mode value supplied through the AP record; API population and value provenance: `unknown`. |
| Operation/output | Static converter returns a display label, including fallback `UNKNOWN`; actual displayed runtime value: `unknown`. |
| Scenario | Editorial trace of source-record field to UI label; not an observed scenario. |

## Limits

The mapping does not establish enum meanings, protocol behavior, device/security-mode support, compatibility, or runtime accuracy. No device or source execution was performed. It adds no security-coverage claim to the separate [WiFi passive monitoring receive-path concept](wifi-passive-monitoring.md).

## Related

- [Issue #100: WiFi domain ontology](https://github.com/ozand/adv/issues/100)
