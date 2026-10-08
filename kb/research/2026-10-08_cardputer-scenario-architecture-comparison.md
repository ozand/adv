---
type: ResearchReport
title: Scenario-based Cardputer access architecture comparison
created: "2026-10-08"
issue: "https://github.com/ozand/adv/issues/38"
status: draft
sources:
  - resource: "https://github.com/ozand/adv/blob/27dc0f5f5a71e615740a64e045626244f6800294/docs/diagnostics/agent-device-operation-contract-draft.md"
    revision: "27dc0f5f5a71e615740a64e045626244f6800294"
    document_blob: "20744824bac8ff0ed81fd60d3be7b374e162e754"
  - resource: "https://github.com/ozand/adv/blob/1f1868a9d2192f5d3f28f850306541e3f51fbc43/kb/research/2026-10-08_cardputer-capability-inventory/summary.md"
    revision: "1f1868a9d2192f5d3f28f850306541e3f51fbc43"
    document_blob: "4003cdd06e67a4c56ae32f457ff2fd6d4f64c173"
  - resource: "https://github.com/ozand/adv/blob/e07c2fb30960b32f82b7ddfa75df12a1b4a72479/kb/research/2026-10-08_cardputer-agent-usage/output.md"
    revision: "e07c2fb30960b32f82b7ddfa75df12a1b4a72479"
    document_blob: "97d0285d0fb9358c5107de5b3e664f3fbe25d218"
  - resource: "https://github.com/ozand/adv/blob/1f1868a9d2192f5d3f28f850306541e3f51fbc43/docs/adr/ADR-006-hardware-diagnostic-serial-json.md"
    revision: "1f1868a9d2192f5d3f28f850306541e3f51fbc43"
    document_blob: "6262db986fef9c0fc0ca89d52ee82efa496ff044"
  - resource: "https://github.com/ozand/adv/blob/1f1868a9d2192f5d3f28f850306541e3f51fbc43/docs/diagnostics/agent-device-access-roadmap.md"
    revision: "1f1868a9d2192f5d3f28f850306541e3f51fbc43"
    document_blob: "c65a748b79b3ed9710cdf10dca387421f4199cd4"
  - resource: "https://github.com/ozand/adv/blob/e07c2fb30960b32f82b7ddfa75df12a1b4a72479/kb/research/2026-10-08_cardputer-agent-usage/synthesis.md"
    revision: "e07c2fb30960b32f82b7ddfa75df12a1b4a72479"
    document_blob: "0fc0a431e7461e1e87c4d74ffa482d13c4f985bf"
tags: [cardputer, architecture, scenarios, research]
---

# Scenario-based Cardputer access architecture comparison

**Status: draft comparison; no architecture selected.** This report compares three roadmap alternatives against three bounded, source-documented scenarios. The evidence describes upstream projects and a draft contract; it does not establish behavior on this project's installed Cardputer.

## Scope and evidence labels

This comparison uses only the published roadmap, ADR-006, Stage A inventory, Stage B draft, and Issue #35 handoff at the frozen source snapshots listed above. No new source discovery, browsing, runtime test, device access, code execution, or QMD operation was performed. The Stage B contract remains a proposal, not an accepted API/ABI or implementation permission. The reviewed Stage A/Stage B documents were delivered at the cited immutable commits; the source set is not a claim that current remote main is unchanged.

- **Accepted source contract:** ADR-006's `status`, `sd_test`, `run <ID>`, `result <ID>` only; not installed-device proof.
- **Source-documented / reported:** upstream README description; not independent observation or adoption evidence.
- **Theory:** conditional architectural reasoning, not a tested property.
- **Unknown:** not established by the available sources.

## Bounded scenarios

The labels below are local comparison labels, not contract operation IDs or approved operations.

1. **Notification display (`notification-display`).** A Cardputer presents a bounded ntfy-style notification. Issue #36 and the Stage B draft cite a pinned ntfy README as a source-reported example. Topic authorization, privacy, retention and target-device behavior are unknown. Displaying a notification is not command completion or authority to act.
2. **Explicitly confirmed broker action (`confirmed-broker-action`).** An operator confirms one allowlisted MQTT-style external action. The pinned MQTT README is source-reported evidence only. A publish, broker acknowledgement, target-device acknowledgement and actual external effect are distinct stages; the implementation's permission model and actual effect are unverified. This does not imply general broker control.
3. **Agent approval/status surface (`agent-approval-surface`).** A Cardputer displays one pending Claude Buddy-style permission request and conveys a human decision bound to that exact request. The pinned README reports BLE/developer-mode behavior; it does not establish security, usability, support or installed runtime. A displayed approval is not itself authenticated authorization.

These examples are not representative usage samples or demand evidence. They do not show that an equivalent capability exists on the project's device. The coding-console example is deliberately not a scenario because it could imply arbitrary execution. ADR-006 status is retained as a reference/boundary, not an additional scenario. Coverage of the roadmap's broader goal of controlled access to device capabilities is incomplete; this three-scenario sample does not cover every device capability or owner requirement.

## Comparison method

Compare each scenario against the same three options:

- **Host-side CLI/MCP adapter** — agent interface runs on a host and would mediate a bounded device operation.
- **Device-side network MCP** — a network service on the device would expose a bounded operation.
- **Hybrid** — a host and device component divide the interface/operation path.

These are the roadmap's alternatives, not verified implementations. For each option/scenario pair, assess the same dimensions:

1. **Scenario fit and evidence:** which parts are supported by source-documented examples; what remains theory or unknown.
2. **Prerequisites/dependencies:** host, compatible transport, network/service, power and configuration needs; target support not established.
3. **Connectivity, latency, offline behavior:** qualitative dependencies only. No numerical latency, reliability, or offline claims are evidenced.
4. **Authority/effects/identity:** initiator, target binding, read/display vs external effect, operator confirmation, identity/authentication assumptions, and trust boundary. No security model is verified.
5. **Data/privacy:** message or request data crossing each boundary, possible retention/display, minimization and access unknowns.
6. **Failure and uncertainty:** distinguish request, transport, acknowledgement, reported action and independently verified effect. Timeout/disconnect does not prove non-execution or rollback.
7. **Retry/recovery/verification:** idempotency and safe retry are unknown; identify what would need to be checked and who can recover. Do not infer recovery from cancellation.

A scenario comparison table is intentionally left as an evaluation template rather than filled with unsupported architecture behavior:

| Scenario | Host-side CLI/MCP | Device-side network MCP | Hybrid |
|---|---|---|---|
| notification-display | Assess the common dimensions; host/network prerequisites and offline behavior unknown. | Assess the common dimensions; device service, identity and network behavior unknown. | Assess the common dimensions; component boundary and recovery behavior unknown. |
| confirmed-broker-action | Assess authority, target binding, consent and external-effect evidence; all implementation-specific behavior unknown. | Same criteria; service authentication and effect confirmation unknown. | Same criteria; split authority and partial-failure recovery unknown. |
| agent-approval-surface | Assess request binding and host integration; no implementation behavior established by the example. | Assess BLE/device network exposure and authorization; not established or equivalent. | Assess split approval path and uncertainty; no end-to-end validation exists. |

The table deliberately does not score or rank options. If later evidence cannot populate a cell, retain `unknown` rather than infer a winner.

## Cross-cutting authority and coverage

- Status observation, notification display, approval of an agent action and external MQTT control are distinct effects. They must not be conflated as one “agent-device” permission.
- The approval example is a human decision surface, not proof of identity or authorization enforcement. The broker example may affect external state; notification display does not imply such authority.
- None of the three scenarios establishes the operator's broader requirement for access to the maximum set of safely controllable device capabilities. This comparison sample has deliberately incomplete capability coverage.
- No option is treated as permitting shell, arbitrary code execution, deployment, firmware changes, network control, GPIO, arbitrary storage access, or other effects beyond an individually bounded scenario. The roadmap excludes unrestricted shell/GPIO and requires separate authorization for device operation.
- Host, device, and hybrid options all need explicit authority/effect boundaries; a transport name or MCP annotation does not prove enforcement.

## Tradeoffs and unresolved decisions

The available documents establish only that the roadmap considers host-side, device-side network, and hybrid approaches; they do not establish comparative latency, availability, offline support, authentication, privacy, reliability, recovery, or implementation suitability. Reported project examples illustrate interaction patterns but are not implementations of this repository's candidate architecture. There is insufficient evidence to recommend or select any option.

Questions left open for owner/security decision include: who is the trusted principal; how targets are bound; whether notification content may be stored; how a broker action's external effect is confirmed; how a physical approval is bound to the exact pending request; how timeouts and partial failures are reconciled; and what recovery is safe. Any future public contract or trust-boundary implementation requires a separate accepted ADR and authorization. This comparison itself does not publish an API or select a contract.

## Coordination and review status

The coordinator reports that the hardware lead reviewed the Issue #38 comparison plan and returned bounded-method approval with finite corrections; an independent method review also passed. These were plan reviews, not review of this report's final content. The #37 draft records prior hardware-owner and independent review for an earlier contract-draft commit, but explicitly requires review of the exact delivered draft before treating its own criterion as final. No owner acceptance, security approval or architecture decision is claimed. Independent review of this exact comparison artifact remains required before delivery.

## Method and limitations

- Snapshot: repository main at `27dc0f5f5a71e615740a64e045626244f6800294`; its parent is `e07c2fb30960b32f82b7ddfa75df12a1b4a72479`.
- Evidence: pinned Issue #35 handoff/synthesis, Stage A inventory, Stage B draft, ADR-006, and roadmap. No external sources or new operational research were added.
- Issue #35 consists of one mutable vendor product page plus six pinned project README records. README statements are author-reported; no interviews, adoption telemetry, installed-device tests, or comparative runtime measurements exist.
- Stage A's six inventory rows are source-documented only. Stage B has three illustrative mappings; neither defines accepted operation IDs or implementation semantics.
- The bounded document review started after the coordinator's writer authorization at 2026-10-08 14:19:04 +03:00 and ended at 14:31:00 +03:00 (reported execution window, not continuous stopwatch time); elapsed wall-clock window was 11m56s, below the 45-minute cap. Inputs were only the frozen published documents listed above.
- The report's conditional architecture observations are theory, not observed properties. Latency, offline behavior, identity, authorization, installed support and recovery remain unknown.
- No implementation, API publication, code/firmware/network change, hardware/device operation, or QMD/index mutation occurred.
- Process deviation: the initial report was written with one 105-line write call, contrary to the workspace chunked-write guardrail. This is disclosed, not treated as compliant; the single-file draft remains uncommitted pending review.
