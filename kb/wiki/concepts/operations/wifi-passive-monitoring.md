---
type: "Concept"
title: "WiFi passive monitoring receive path"
description: "A bounded, source-inspected example of shared WiFi packet reception and deferred network-record processing."
issue: "https://github.com/ozand/adv/issues/100"
sources:
  - resource: "https://github.com/0ct0sec/m5porkchop"
    revision: "38d7078c09205e23b65018fd486a5fd1e40ee440"
evidence:
  - claim: "The shared recon service configures promiscuous reception and dispatches received management/data frames."
    source: "https://github.com/0ct0sec/m5porkchop/blob/38d7078c09205e23b65018fd486a5fd1e40ee440/src/core/network_recon.cpp"
    revision: "38d7078c09205e23b65018fd486a5fd1e40ee440"
    method: "code-inspected"
    locator: "lines 847-869; 587-637"
  - claim: "Selected network metadata is queued and processed later through a bounded deferred-record path."
    source: "https://github.com/0ct0sec/m5porkchop/blob/38d7078c09205e23b65018fd486a5fd1e40ee440/src/core/network_recon.cpp"
    revision: "38d7078c09205e23b65018fd486a5fd1e40ee440"
    method: "code-inspected"
    locator: "lines 131-142; 640-692; 966-979"
  - claim: "The README describes DO NO HAM as passive and OINK as active."
    source: "https://github.com/0ct0sec/m5porkchop/blob/38d7078c09205e23b65018fd486a5fd1e40ee440/README.md"
    revision: "38d7078c09205e23b65018fd486a5fd1e40ee440"
    method: "source-reported"
    locator: "lines 259-336"
---

# WiFi passive monitoring receive path

## Bounded example
At the pinned revision, the shared recon service configures promiscuous reception and registers a callback. The callback classifies received management/data frames and dispatches handling. Selected network metadata is placed in a bounded pending-record queue; deferred processing drains records during later updates. These are source structures, not observed device behavior.

The README reports DO NO HAM as passive and OINK as active. Those are mode descriptions reported by the project, not proof that the shared receive path or product as a whole has zero transmission. This page describes a receive-path pattern only; it does not document or recommend operating any mode.

## Relation and unknowns

| Relation | Evidence and status |
|---|---|
| Device/component | Target device and WiFi component identity/variant: `unknown`; no device mapping is established. |
| Firmware/source | `0ct0sec/m5porkchop` at `38d7078c09205e23b65018fd486a5fd1e40ee440`; code-inspected source pattern, not a firmware/device compatibility claim. |
| Setup/prerequisites | Runtime prerequisites and configuration: `unknown` beyond the inspected static promiscuous-receive setup and callback registration. |
| Operation | Receive path classifies management/data frames and queues selected network records for deferred processing; code-inspected at the cited source locators above. |
| Data | Receives frames; selected network metadata becomes bounded pending records. Record/output format, destination, and complete retention: `unknown`. |
| Scenario | Editorial research intent: illustrate a passive-monitoring receive-path pattern. This does not validate device behavior or any operating scenario. |

## Evidence limits
No WPA/security-generation or 802.11-variant support, device compatibility, runtime behavior, mode isolation, zero-transmission guarantee, or complete traffic retention is established. The inspected queue bounds pending network records; it does not establish retention of all received traffic. The one pinned source provides no basis for corpus prevalence. Further source evidence or device testing would be needed for those claims; none was performed here.

## Related
- [Issue #100: WiFi domain ontology](https://github.com/ozand/adv/issues/100)
- [Issue #99 ontology validation note](../../../../docs/research/issue-99-ontology-validation.md)
- [Capability research workflow](../../../../docs/capability-research-workflow.md)
