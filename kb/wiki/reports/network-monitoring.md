---
type: "Report"
title: "Network monitoring and sensing: bounded source map"
description: "Source-pinned monitoring structures and limits across WiFi, BLE and packet records."
issue: "https://github.com/ozand/adv/issues/106"
---

# Network monitoring and sensing: bounded source map

This partial map connects existing WiFi concepts with selected additional source structures. `code-inspected` describes static source, not observed device behavior, actual captures, interoperability or corpus prevalence. No monitoring or device operation was performed.

## Choose the question, not the label

| Question | Existing evidence | Boundary |
|---|---|---|
| How might WiFi observations be collected? | [Passive receive and deferred records](../concepts/operations/wifi-passive-monitoring.md); [AP discovery records](../concepts/operations/wifi-scanning-records.md). | A receive path does not prove the whole program transmits nothing, or retains every observation. |
| Is a CSI-labelled input a motion measurement? | [CSI callback and distinct inputs](../concepts/operations/wifi-csi-sensing.md): source distinguishes CSI, RSSI and ESP-NOW paths. | Sensing accuracy, actual measurements and device support are unknown. |
| Does a packet callback produce a complete retained capture? | [EAPOL callback and buffer](../concepts/operations/wifi-eapol-observation.md) includes conditional buffering. | Successful persistence, completeness and a usable capture are not established. |

## BLE observations are not necessarily passive

In pinned [Adversary BLE scanner code](https://github.com/isonimus/adversary/blob/79085dd76f45afa745f2c054eaa22df77cb3cbf2/src/modules/ble/ble_scanner.cpp#L70-L86), the scan path explicitly selects active scanning and checks the start result. The [result callback](https://github.com/isonimus/adversary/blob/79085dd76f45afa745f2c054eaa22df77cb3cbf2/src/modules/ble/ble_scanner.cpp#L120-L155) updates a matching record or begins a new one. These are `code-inspected` structures; discovery coverage, identity stability and radio behavior on a device are unknown. A BLE scan result does not by itself establish human presence.

## Scan observations and position

The same pinned project's [wardriving manager](https://github.com/isonimus/adversary/blob/79085dd76f45afa745f2c054eaa22df77cb3cbf2/src/modules/wardriving/wardriving_manager.cpp#L323-L355) reads scan results and skips reprocessing the same scan count. Its [GPS update](https://github.com/isonimus/adversary/blob/79085dd76f45afa745f2c054eaa22df77cb3cbf2/src/modules/wardriving/wardriving_manager.cpp#L398-L407) returns when the receiver is not detected or lacks a valid fix. These `code-inspected` checks do not prove location accuracy, synchronized observations, recorded output or hardware compatibility.

## Packet-record and traffic-summary structures

Adversary's [PCAP writer](https://github.com/isonimus/adversary/blob/79085dd76f45afa745f2c054eaa22df77cb3cbf2/src/modules/pcap/pcap_writer.cpp#L110-L155) writes a global header with a supplied link type and snapshot length, checks the header write, and prepares packet metadata. Its [sniffer path](https://github.com/isonimus/adversary/blob/79085dd76f45afa745f2c054eaa22df77cb3cbf2/src/modules/sniffer/packet_sniffer.cpp#L349-L399) rejects certain invalid inputs, applies a filter and updates frame-type counters. These are separate `code-inspected` structures, not proof they are connected in every mode, that a file is complete, or that Wireshark can read it. Traffic counters are not content analysis or a guarantee of full traffic visibility.

## Remaining work

The source-reported sensing claims and static examples above do not establish passive presence-detection accuracy, PCAP interoperability or runtime behavior. The requested method/entity and operation coverage still needs review and, where needed, additional source-backed material; this is not completion of [Issue #106](https://github.com/ozand/adv/issues/106). No packet contents, identifiers, locations, or operating procedures are included.
