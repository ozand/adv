# ADR-008: Proposed communication ontology structure

**Status:** Proposed — structure accepted by the owner for continued Issue #99 validation; remaining criteria are unresolved
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
3. Operation-pattern concepts in `kb/wiki/concepts/operations/` (the owner-accepted structural direction).
4. Domain synthesis reports in `kb/wiki/reports/protocols/`.

Use lowercase kebab-case filenames based on the protocol/device/operation name; retain the existing directory layout and do not create a parallel taxonomy root. Apply existing Markdown/OKF conventions without claiming an ontology-specific required-field contract:

| Proposed page type | Placement | Fields and provenance guidance |
|---|---|---|
| Protocol/technology entity | `kb/wiki/entities/protocols/<name>.md` | OKF-required nonempty `type`; adv recommends `title`. Use concise `description`; add governing `issue` when one exists and claim-linked `sources` with full revision/path locator where available. |
| Device/capability entity | `kb/wiki/entities/devices/<name>.md` | Same OKF `type` and adv `title` recommendation; describe only evidenced target/capability claims. Add `object_profile` only if useful, not as a replacement for `type`. |
| Operation-pattern concept | `kb/wiki/concepts/operations/<name>.md` | Same conventions; state whether the pattern is source-reported or code-inspected and link exact source revision/path. Keep safety-sensitive behavior descriptive, not instructional. |
| Synthesis report | `kb/wiki/reports/protocols/<name>.md` | Same conventions; summarize claim-linked evidence and explicitly list unknowns/gaps; no document-wide evidence grade. |

`title` is an adv recommendation, not an OKF universal minimum. `description` is a concise authoring recommendation, not a newly accepted validator requirement. Include `issue` only when a governing issue exists; `sources` should support consequential claims and preserve unknown revision/locator rather than inventing it. `object_profile`, `tags`, editorial `status`, evidence details, and applicability remain optional/context-specific under ADR-010. Do not infer requirements for legacy cards. A page states its kind in prose/frontmatter and explicitly links related protocol, device/capability, operation-pattern, and report pages; links are directional references, not proof of reciprocal support. Exact controlled vocabularies, a machine-readable relationship schema, automated enforcement, and migration remain undecided.

Owner decision: the structure in PR #109 was accepted as the direction for continuing Issue #99 validation ([Issue #99 comment](https://github.com/ozand/adv/issues/99#issuecomment-6282186430)). This does not mean all Issue #99 acceptance criteria are satisfied or authorize downstream Issues #100–#107.

### Coverage targets (not findings)

The navigation proposal names protocol/technology coverage targets WiFi, BLE, LoRa, Sub-GHz, NFC, IR, USB, ESP-NOW, and MQTT, and operation targets passive monitoring, active probing, credential capture, control/emulation, parameter extraction, and data exfiltration. These are topics to validate, not assertions of presence, support, safety, or implementation. The bounded sample supports only selected examples; the remaining targets must be identified as unknown/not covered rather than implied complete. A protocol entry links to applicable device/capability and operation-pattern pages only where claim-level evidence supports that relation; absence or unknown applicability stays explicit. An implementation-pattern explanation links its exact source revision/path to the operation concept it illustrates and states whether support is source-reported or code-inspected. Reports synthesize evidenced links and list unresolved coverage, rather than filling gaps by inference.

## Evidence and scope rules

| Issue #99 operation target | Existing bounded evidence | Validation disposition |
|---|---|---|
| Passive monitoring | WiFi sample: packet callback/promiscuous setup at pinned `m5porkchop` revision; code-inspected | Example supported at source-structure level only; runtime/device behavior not established. |
| Active probing | WiFi sample: deauthentication-frame construction/transmit path at the same pin; code-inspected | Example supported at source-structure level only; do not generalize to other protocols. |
| Credential capture | `evil-m5core2` sample: portal/cookie handler and route structures; source-reported + code-inspected | Structure evidenced; no execution or actual captured data observed. Rights unresolved. |
| Control/emulation | BLE/USB HID report structures and PN532 target/emulation paths in sampled pinned sources; code-inspected | Selected examples supported; not a universal capability claim. |
| Parameter extraction | No separate, cleanly established mapping in the six-source sample | Not established; remains an explicit coverage gap. Do not infer from tags or protocol labels. |
| Data exfiltration | No separate, cleanly established mapping; `m5porkchop` README mentions file transfer but implementation was not inspected | Not established; generic file/HTTP transfer is not sufficient evidence. Remains a gap. |

- Attach evidence to each factual claim/source, using only ADR-010 classes: `source-reported`, `code-inspected`, `device-observed`, or `device-verified`. `unknown` and `not_run` are missing-evidence/execution states, not evidence classes; inference must be identified as reasoning, not a new class.
- `device-observed` records a direct observation with device/model, software/configuration, procedure, result, provenance, limitations, and verifier context. It does not itself verify other claims. Use `device-verified` only when ADR-010's higher-threshold claim-specific requirements are met; otherwise do not label the claim device-verified. Record missing evidence as unknown and determine applicability separately under ADR-010.
- Manifest tags and repository READMEs are leads/source-reported claims, not proof of implementation. Code inspection requires an exact repository revision and file/symbol locator. Structural validation does not prove technical truth.
- Keep source clones and bulky inputs in ignored `sources/`; publish no copied repositories/code. Bounded captures may be published only under ADR-007 review. QMD is retrieval only, never evidence or publication permission.
- Operation categories are candidate organizational concepts, not assertions that each exists in every protocol or sampled project. In particular, the bounded sample did not establish `parameter extraction` or `data exfiltration` as distinct implemented capabilities.

## Protocol coverage disposition from the bounded sample

| Protocol target | Existing sample evidence | Disposition |
|---|---|---|
| WiFi | `m5porkchop`: packet callback/promiscuous and frame-processing structures at exact pin | Selected source-structure examples; not full WiFi coverage. |
| BLE | `meowusb-ble`: BLE keyboard setup; `evil-m5core2`: README/portal context as recorded in sample | Selected examples only; runtime/device behavior not established. |
| Sub-GHz | Flipper-derived sample: stored-preset transmit path | One narrow code-inspected path only. |
| NFC | `brucedevices/firmware`: PN532 init, target mode and MIFARE read/write structures | Selected source-structure examples; rights review needed. |
| USB | Two HID samples show USB keyboard/report structures | Selected examples only. |
| LoRa | No matching source in the six-sample matrix | Not covered by this sample; unknown, not unsupported. |
| IR | No matching source in the six-sample matrix | Not covered by this sample; unknown, not unsupported. |
| ESP-NOW | No matching source in the six-sample matrix | Not covered by this sample; unknown, not unsupported. |
| MQTT | No matching source in the six-sample matrix | Not covered by this sample; unknown, not unsupported. |

The matrix records sample coverage, not corpus-wide presence/absence. No new sources were acquired for these gaps. Exact pins and source-path observations are in the validation note.

## Alternatives considered

- A single flat taxonomy: rejected as a proposal because it obscures many-to-many links among protocols, devices, operations, and patterns.
- Treat manifest tags or a README feature list as corpus validation: rejected because they are not code inspection or device evidence.
- Add a new `hypothesis` evidence class: rejected because it would extend the accepted finite ADR-010 vocabulary. Draft/template state and explicit uncertainty remain separate from evidence.

## Acceptance gates and consequences

The owner accepted the proposed structure in PR #109 as the direction for continuing Issue #99 validation, bound to the reviewed candidate and recorded at Issue #99 comment 6282186430. This ADR remains a proposed artifact while remaining Issue #99 criteria are checked; that structural decision is not evidence that all criteria are met, nor implementation or downstream issue authorization. The six-source note supports initial examples but leaves coverage gaps; no claim of complete ontology validation is made. Issues #100–#107 remain independently governed and must not be activated by this proposal alone.

If the remaining Issue #99 criteria are later accepted, the structure can guide separately bounded domain issues. Each page/report still needs its own source review, evidence labels, safety framing, rights/privacy review, and documented structural validation where available. No current corpus migration, new validator, QMD mutation, source acquisition, device operation, or publication is authorized by this Proposed ADR. The six-source matrix records code-inspected structures for credential-handler routing, HID report generation, and frame processing; their safety-sensitive behavior must not be operationalized or presented as a recommendation. Later documentation must remain descriptive, source-grounded, and within applicable project safety and publication review.

## Review questions

1. Does the page-type field guidance clearly distinguish OKF requirements from adv recommendations?
2. Are evidence, uncertainty, and applicability rules faithfully bounded by accepted ADR-010?
3. Which documented sample gaps remain for Issue #99, and what separately authorized evidence would be needed to resolve them?
