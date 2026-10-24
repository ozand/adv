---
type: "Report"
title: "Partial WiFi domain synthesis from bounded source patterns"
description: "A partial, claim-scoped synthesis of selected WiFi source patterns and unresolved coverage."
issue: "https://github.com/ozand/adv/issues/100"
sources:
  - resource: "https://github.com/justcallmekoko/esp32marauder"
    revision: "b2b9f92382eb60b39b8741be3b567e416cdbe672"
  - resource: "https://github.com/brucedevices/firmware"
    revision: "a59213f3ec6cd302fa32c2042b2700c9c24d991a"
  - resource: "https://github.com/0ct0sec/m5porkchop"
    revision: "38d7078c09205e23b65018fd486a5fd1e40ee440"
---

# Partial WiFi domain synthesis

## Scope and evidence

This is a bounded partial synthesis, not completion of Issue #100 or corpus coverage. Claims below are source-reported or static `code-inspected`; no code ran, no network/device was used, and no device behavior was observed. Pins are immutable. This batch consolidates the provided inspection artifacts and published Issue #99 validation note; it adds no upstream inspection.

| Source artifact | Inspected scope and evidence | Rights / limits |
|---|---|---|
| [`justcallmekoko/esp32marauder`](https://github.com/justcallmekoko/esp32marauder/tree/b2b9f92382eb60b39b8741be3b567e416cdbe672) at `b2b9f92382eb60b39b8741be3b567e416cdbe672` | Static `code-inspected`: [`WiFiScan.cpp`](https://github.com/justcallmekoko/esp32marauder/blob/b2b9f92382eb60b39b8741be3b567e416cdbe672/esp32_marauder/WiFiScan.cpp) L3876-L3945, L4331-L4369, L4984-L5210, L7406-L7599, L10361-L10575, L11378-L11390, L11631-L11664; [`BeaconFrame.cpp`](https://github.com/justcallmekoko/esp32marauder/blob/b2b9f92382eb60b39b8741be3b567e416cdbe672/esp32_marauder/BeaconFrame.cpp) L3-L15; [`EvilPortal.cpp`](https://github.com/justcallmekoko/esp32marauder/blob/b2b9f92382eb60b39b8741be3b567e416cdbe672/esp32_marauder/EvilPortal.cpp) L69-L141, L399-L424. | Artifact reports root MIT metadata; not legal clearance. No source excerpt/assets copied. |
| [`brucedevices/firmware`](https://github.com/brucedevices/firmware/tree/a59213f3ec6cd302fa32c2042b2700c9c24d991a) at `a59213f3ec6cd302fa32c2042b2700c9c24d991a` | Static `code-inspected` label/dataflow only: [`ap_info.h`](https://github.com/brucedevices/firmware/blob/a59213f3ec6cd302fa32c2042b2700c9c24d991a/src/modules/wifi/ap_info.h) L1-L6 and [`ap_info.cpp`](https://github.com/brucedevices/firmware/blob/a59213f3ec6cd302fa32c2042b2700c9c24d991a/src/modules/wifi/ap_info.cpp) L12-L26, L74-L90, L109-L123. | Artifact notes root AGPL metadata; not legal clearance. No source excerpt/assets copied. |
| [`0ct0sec/m5porkchop`](https://github.com/0ct0sec/m5porkchop/tree/38d7078c09205e23b65018fd486a5fd1e40ee440) at `38d7078c09205e23b65018fd486a5fd1e40ee440` | Published #99 note, WiFi reinspection: [`network_recon.cpp`](https://github.com/0ct0sec/m5porkchop/blob/38d7078c09205e23b65018fd486a5fd1e40ee440/src/core/network_recon.cpp) L131-L142, L587-L692, L847-L869, L966-L979; [README](https://github.com/0ct0sec/m5porkchop/blob/38d7078c09205e23b65018fd486a5fd1e40ee440/README.md) L259-L336 is `source-reported`. | #99 note reports root MIT metadata; not legal clearance. This is the note's bounded record, not a new inspection. |

These are three source repositories represented by the supplied evidence, not the whole six-repository #99 sample. A historical metadata cohort of 46 candidates is not an inspected or eligibility-frozen source-artifact set here; it is not a denominator and implies no coverage percentage. Do not generalize these examples to prevalence, protocol support, or other repositories.

## Eight operation targets: what the evidence does and does not show

| Issue #100 operation | Bounded pattern and evidence | Unknown / boundary |
|---|---|---|
| Scanning | Marauder separates beacon/AP-record discovery (WiFiScan.cpp L4331-L4369, L7406-L7424, L7471-L7497, L7528-L7599) from host/port checks and positive-result output (L3876-L3945, L11378-L11390, L11631-L11664); `code-inspected`. | AP discovery is not port scanning. No live targets, results, prerequisites, or device mapping. |
| Monitoring | Marauder packet/channel callback and presentation path (WiFiScan.cpp L4984-L5125); m5porkchop promiscuous receive/deferred-record path (network_recon.cpp L131-L142, L587-L692, L847-L869, L966-L979); `code-inspected`. | A receive path does not prove zero TX by a mode/product, complete traffic retention, runtime behavior, or output format. |
| Deauthentication attacks | The #99 note's historical six-source record mentions a pinned m5porkchop frame-processing path in `src/modes/oink.cpp` around deauthentication code; the note supplies no exact line locator for that detail. | This summary-level lead is not enough to claim a complete or working attack capability. No procedure, frame details, runtime, or device evidence. |
| Beacon spam | Marauder `BeaconFrame.cpp` L3-L15 shows a helper setting one computed frame-buffer field; `code-inspected`. | A helper alone does not establish complete beacon generation, repeated transmission, or a spam operation. |
| Evil portal / WPAD | Marauder `EvilPortal.cpp` L69-L141 and L399-L424 shows a request-to-state-to-later-output structure; `code-inspected`. | No WPAD evidence established. No portal deployment, parameters, observed values, or runtime behavior. |
| Credential capture | The same Marauder paths show name/password-related state later formatted to serial, buffer, and optional display; `code-inspected`. | State/output code is not proof of observed credentials or a completed capture; no credential values or request parameter names are included. Rights for that additional source remain unestablished in #99. |
| Handshake capture | Marauder `WiFiScan.cpp` L5128-L5210 and L10361-L10575 shows EAPOL-related callback/status structure, packet-buffer appends, and scan setup; `code-inspected`. | Callback presence does not prove complete handshake capture, retained/completed output, successful operation, or device behavior. |
| CSI sensing | No CSI implementation is established by these three source records. | Not assessed here; unknown, not evidence of absence or unsupported behavior. |

## Dataflow and interpretation

Concrete outputs in the reviewed records are limited to AP-record display/buffer updates and the separate port-check positive-result output (Marauder `WiFiScan.cpp` cited above); portal-related formatted output to serial, buffer, and optional display (`EvilPortal.cpp` L124-L141, L399-L424); Bruce's converted auth-mode label in an “Auth mode” UI row (`ap_info.cpp` L12-L26, L74-L90, L109-L123); and packet-buffer append structure in the handshake-related callback (`WiFiScan.cpp` L5128-L5210). Formats, full schemas, runtime values, destinations beyond those named, and retention are otherwise unknown.

Bruce maps AP-record `authmode` tokens to static labels, including a fallback, then places the result in a UI row. These label strings are not WPA/802.11 protocol semantics, negotiation, authentication, or proof of supported security modes. Reuse the existing [AP authentication-mode label concept](../../concepts/operations/wifi-ap-auth-labels.md); it is distinct from the [passive-monitoring receive-path concept](../../concepts/operations/wifi-passive-monitoring.md), whose shared receive path likewise does not establish zero transmission.

Forward trace: the source records connect selected code structures to receive, record, label, callback, or output steps only. Device identity/component, firmware-to-device relationship, runtime prerequisites/configuration, data formats and complete retention remain unknown. Backward trace from desired data to a verified device/setup also stops at those unknown edges; no prerequisite or compatibility path is inferred. Editorial scenario: a reader compares these source-level patterns and gaps. It is not an observed Cardputer scenario or usage recommendation.

## Coverage and publication limits

The evidence is sufficient to organize a partial domain around distinct activities and dataflows, but not to justify new WiFi protocol or device entities. No claim is made that all original operation targets are supported. Missing evidence remains unknown, not unsupported. Follow-up acceptance criteria remain open, including broader pinned-source coverage, protocol/security semantics, source rights/privacy review, and any separately authorized device validation.

The cited MIT/AGPL license metadata is a lead, not blanket rights clearance. This report uses original bounded paraphrase only; it contains no copied source/assets, credentials, private paths, operational captures, packet details, code excerpts, setup instructions, or execution guidance. Privacy/relevance review and rights review remain separate gates under ADR-007. Structural validation cannot approve publication rights or verify factual/runtime claims.

## Related

- [Issue #100: WiFi domain ontology](https://github.com/ozand/adv/issues/100)
- [Issue #99 bounded ontology validation note](../../../../docs/research/issue-99-ontology-validation.md)
- [Capability research workflow](../../../../docs/capability-research-workflow.md)
