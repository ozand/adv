# ADR-008: Proposed communication ontology structure

**Status:** Proposed — pending owner decision and Issue #99 acceptance validation
**Date:** 2026-10-20
**Issue:** #99
**Related:** Accepted ADR-007, ADR-010; open Issue #50

## Context

The existing knowledge base organizes canonical pages under `kb/wiki/entities/`, `kb/wiki/concepts/`, and `kb/wiki/reports/`. Issue #99 requests a bounded communication ontology connecting protocols, devices/capabilities, operations, implementation patterns, and synthesis. The six-repository source-inspection sample and limitations are recorded in [the validation note](../research/issue-99-ontology-validation.md). Its bounded evidence informs candidate examples only; it does not establish complete corpus coverage or acceptance.

Issue #45's finite knowledge/evidence contract was accepted by the owner (comment 6072992191). ADR-010 permits claim/source-level `source-reported`, `code-inspected`, `device-observed`, and higher-threshold `device-verified` evidence. Applicability and editorial lifecycle are separate. ADR-007 keeps originals local-only and permits only bounded reviewed captures under its privacy, secret, relevance, provenance, and rights gates.

## Proposed decision

Organize future communication knowledge within existing canonical layers, without adding a new schema or migrating existing pages:

1. Protocol/technology entities in `kb/wiki/entities/protocols/`.
2. Device-type/capability entities in `kb/wiki/entities/devices/`.
3. Operation concepts in `kb/wiki/concepts/operations/`.
4. Domain synthesis reports in `kb/wiki/reports/protocols/`.

Use lowercase kebab-case filenames based on the protocol/device/operation name; retain the existing directory layout and do not create a parallel taxonomy root. Each proposed page type uses existing Markdown/OKF conventions: nonempty `type` is required by OKF; recommend `title` and a concise `description`; include `issue` and claim-linked `sources` when applicable. `object_profile`, `tags`, editorial `status`, evidence details, and applicability remain optional/context-specific as described by ADR-010. Do not invent ontology-wide required fields that would contradict the accepted contract. A page states its kind in prose/frontmatter and explicitly links related protocol, device/capability, operation, pattern, and report pages; links are directional references, not proof of reciprocal support. Each consequential claim cites source identity and full revision where available plus path/symbol locator. Exact controlled vocabularies, a new machine-readable relationship schema, automated enforcement, and migration are not decided here.

### Coverage targets (not findings)

The navigation proposal should provide protocol/technology entries or explicitly marked gaps for WiFi, BLE, LoRa, Sub-GHz, NFC, IR, USB, ESP-NOW, and MQTT. Candidate operation concept pages should include passive monitoring, active probing, credential capture, control/emulation, parameter extraction, and data exfiltration. These labels define topics to validate, not assertions that every category is present, supported, safe, or implemented in the sample. A protocol entry links to applicable device/capability and operation pages only where claim-level evidence supports that relation; absence or unknown applicability stays explicit. An implementation-pattern explanation links its exact source revision/path to the operation concept it illustrates and states whether the support is source-reported or code-inspected. Reports synthesize the evidenced links and list unresolved coverage, rather than filling gaps by inference.

## Evidence and scope rules

- Attach evidence to each factual claim/source, using only ADR-010 classes: `source-reported`, `code-inspected`, `device-observed`, or `device-verified`. `unknown` and `not_run` are missing-evidence/execution states, not evidence classes; inference must be identified as reasoning, not a new class.
- `device-observed` records a direct observation with device/model, software/configuration, procedure, result, provenance, limitations, and verifier context. It does not itself verify other claims. Use `device-verified` only when ADR-010's higher-threshold claim-specific requirements are met; otherwise do not label the claim device-verified. Record missing evidence as unknown and determine applicability separately under ADR-010.
- Manifest tags and repository READMEs are leads/source-reported claims, not proof of implementation. Code inspection requires an exact repository revision and file/symbol locator. Structural validation does not prove technical truth.
- Keep source clones and bulky inputs in ignored `sources/`; publish no copied repositories/code. Bounded captures may be published only under ADR-007 review. QMD is retrieval only, never evidence or publication permission.
- Operation categories are candidate organizational concepts, not assertions that each exists in every protocol or sampled project. In particular, the bounded sample did not establish `parameter extraction` or `data exfiltration` as distinct implemented capabilities.

## Alternatives considered

- A single flat taxonomy: rejected as a proposal because it obscures many-to-many links among protocols, devices, operations, and patterns.
- Treat manifest tags or a README feature list as corpus validation: rejected because they are not code inspection or device evidence.
- Add a new `hypothesis` evidence class: rejected because it would extend the accepted finite ADR-010 vocabulary. Draft/template state and explicit uncertainty remain separate from evidence.

## Acceptance gates and consequences

This proposal is not accepted architecture, implementation permission, or downstream issue authorization. Issue #99 remains open until its acceptance criteria—including bounded sample validation and explicit gaps—are reviewed. The six-source note supports initial examples but leaves coverage gaps; no claim of complete ontology validation is made. Issues #100–#107 remain independently governed and must not be activated by this proposal alone.

If accepted, the structure would guide later bounded domain issues. Each page/report still needs its own source review, evidence labels, safety framing, rights/privacy review, and documented structural validation where available. No current corpus migration, new validator, QMD mutation, source acquisition, device operation, or publication is authorized by this Proposed ADR. The six-source matrix records code-inspected structures for credential-handler routing, HID report generation, and frame processing; their safety-sensitive behavior must not be operationalized or presented as a recommendation. Later documentation must remain descriptive, source-grounded, and within applicable project safety and publication review.

## Review questions

1. Is this four-layer organization suitable while keeping exact schema/required fields open?
2. Are evidence, uncertainty, and applicability rules faithfully bounded by accepted ADR-010?
3. Which bounded sample and gaps must Issue #99 resolve before downstream ontology issues proceed?
