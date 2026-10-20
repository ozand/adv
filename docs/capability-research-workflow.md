# Hardware capability and operation research workflow

Issue: [#111](https://github.com/ozand/adv/issues/111)

This guide documents a module or device without turning a product claim into a compatibility claim. Use the repository's general research workflow as well when that guide is available in the working revision. Keep the original source under ignored `sources/`; publish only a bounded, reviewed synthesis. Follow accepted [ADR-010](adr/ADR-010-define-extensible-knowledge-evidence-contract.md) for claim-level evidence and [ADR-007](adr/ADR-007-publish-reviewed-research-captures-exclude-local-source-originals.md) for publication boundaries. This guide adds no schema or API.

## Trace the chain in both directions

For each candidate, record the supported links and gaps in this chain:

`device → module/component → firmware/tool and version → operation → input/output data → scenario`

- **Capability to scenario:** start with an evidenced module/component; identify the firmware/tool and version that exposes it, the operation, data direction/format/destination, prerequisites and limits, then a bounded scenario.
- **Desired data to setup:** start with the data needed and the intended scenario; trace backward to the operation, required firmware/tool/version, module/component, device, setup and permissions. Mark missing links `unknown`; do not invent a feasible path.
- A component/chip name alone does not establish wiring, pinout, driver support, firmware integration, electrical compatibility or a working operation.
- A missing report is not evidence of unsupported behavior. Use `unsupported` only when qualifying evidence explicitly establishes lack of support. Keep link direction explicit (e.g. controls, receives, emits, depends on); do not represent a multi-step chain as an unlabeled graph edge.

## Relation record

Use a small Markdown table or linked bullets; keep evidence attached to each claim/relation, not as one grade for the whole page.

| Field | Record |
|---|---|
| Device and module/component | Exact named target and relationship; variant/revision or `unknown` |
| Firmware/tool | Name, version/commit and configuration; `unknown` if not evidenced |
| Operation | Observable operation, not a broad feature label |
| Setup | Connections, prerequisites, permissions and dependencies; unknown pinout stays unknown |
| Data | Input/output, transmit/receive direction, format, destination and limits |
| Scenario | Intended bounded use and relevant constraints |
| Evidence | Claim-level class and source locator/revision or observation record |
| Gaps | Unverified links, conflicts, access failures and next evidence needed |

Preserve the existing OKF `type` and source/evidence practices. Distinguish `source-reported`, `code-inspected`, `device-observed`, and `device-verified` as defined by ADR-010. Cite a pinned source revision where available. `device-verified` requires a documented, claim-bounded test on the exact device/configuration; a source statement or successful compile is not device verification.

## Bounded example: HS.ADV v0.1

This example is illustrative, not a compatibility finding. The owner supplied the public [HS.ADV v0.1 product-listing reference](https://ozon.by/product/modul-rasshirenie-dlya-cardputer-adv-hs-adv-v0-1-5184589234), whose accessible content could not be verified here (HTTP 403). The owner-described Cardputer ADV/module association and CC1101, nRF24, optional PN532 names are therefore **owner-reported leads**, not independently inspected listing claims or confirmed component contents. This example shows how to preserve that distinction; the exact contents, variants, and relationships remain unknown pending accessible primary evidence.

| Link | Current evidence/status |
|---|---|
| Cardputer ADV → HS.ADV v0.1 | Owner-reported association with public listing; listing content inaccessible in this review |
| Module → CC1101 / nRF24 / optional PN532 | Owner-reported names only; not independently verified as listing claims or board contents |
| Components → pinout/electrical interface | `unknown`; no schematic or pin map verified |
| Firmware/tool/version → drivers and operations | `unknown`; no pinned firmware source verified |
| Operation → input/output data and scenario | `unknown`; no code or hardware test evidence |

Two example queries show how to use the workflow without inventing a capability:

1. **Capability → scenario:** “What operation and data can HS.ADV v0.1 provide?” Start at the module row, then follow component → firmware/tool → operation → data. The chain stops at the inaccessible product-page details; no operation or output can currently be attributed to this module.
2. **Desired data → setup:** “What setup would be needed to receive and decode an NFC response?” Trace scenario → expected data/direction → operation → firmware/tool → component → device. For this module, each implementation edge remains unknown, so the workflow yields no pinout or setup recommendation.

Do not infer component presence, wiring, supported bands, firmware integration, compatibility, behavior, or a "first/official" status from owner-reported leads or an inaccessible page. Replace unknowns only with claims supported by cited public source revisions, code inspection, or qualifying device tests; preserve disagreements and limitations.

## Builder integration (future)

When reviewed evidence is ready for canonical synthesis, follow an approved wiki-building process and preserve claim-level evidence. No builder skill adoption is part of this Issue; the untracked primary-workspace draft is not assumed to be approved or available on clean clones.

## Review checklist

- [ ] Both capability→scenario and desired-data→setup paths are represented; unresolved edges remain explicit.
- [ ] Each factual edge has a source locator/revision and evidence class; access failures and owner-provided leads are labeled.
- [ ] Source claims are not phrased as code support, compatibility, or device verification.
- [ ] Privacy, relevance, provenance and rights are reviewed before any capture is tracked under `kb/raw/` or `kb/research/`.
- [ ] Originals remain in ignored `sources/`; QMD indexing does not grant publication permission.

This issue does not authorize hardware operation, flashing, QMD changes, or source execution.
