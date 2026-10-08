---
type: SourceRegister
title: "Issue #35 bounded source register"
description: "Seven source identities with access mode, revision, fidelity, relevance, and capture rights/privacy notes."
created: "2026-10-08"
issue: "https://github.com/ozand/adv/issues/35"
status: stable
sources:
  - resource: "https://docs.m5stack.com/en/core/Cardputer"
    revision: "accessed 2026-10-08; mutable page"
  - resource: "https://github.com/m5stack/aiflow"
    revision: "930edd59329568bc8c8f5db5d591abc51548afa2"
  - resource: "https://github.com/layer812/cardputer_llm"
    revision: "f7a839d1221a3ac2b65a6d32036b937d5884ea7d"
  - resource: "https://github.com/y88huang/claude-desktop-buddy-cardputer"
    revision: "257d3d84435c11a98e9dc376257acffda2a633cb"
  - resource: "https://github.com/w35m17h/cardputer-mqtt"
    revision: "48930a30d7d787d695b95fd2b2e62c7b7bb61465"
  - resource: "https://github.com/forshaws/cardputer-ntfy"
    revision: "dba7143b0290b106bd6b6ae2c8f7b93d36bce48c"
  - resource: "https://github.com/sub0pt1mal/interactivesetup-m5cardputer-sshclient"
    revision: "944336fb415fa607660cbf3a3f86f635ef8eb788"
tags: [cardputer, esp32, agents, research, sources]
---

# Source records

This directory indexes the bounded evidence reviewed for Issue #35. It does not reproduce full source documents. Three repository READMEs were opened in the dedicated Surf window; three additional README records come from a separately conducted, read-only local-clone scout. Access mode is stated per record. All project statements are author-reported, not independent adoption evidence.

## Official device page — browser opened

- URL: https://docs.m5stack.com/en/core/Cardputer
- Publisher: M5Stack
- Accessed: 2026-10-08 via Surf CLI 2.20.0, dedicated window 1071839057
- Revision: mutable page; no immutable revision identifier recorded
- Fidelity: rendered page text read; no HTML/screenshot archive. Brief relevant content paraphrased in `../synthesis.md`.
- Relevance: Cardputer capabilities/specifications and vendor-stated intended applications.
- Limitation: intended applications are not observations of actual usage.
- Review: paraphrase only; no secrets or personal data retained.

## AIFlow — browser opened and scout local clone

- URL: https://github.com/m5stack/aiflow
- Revision: `930edd59329568bc8c8f5db5d591abc51548afa2`
- Document: `README.md`; blob `38b8ea6663fc1cc3bf42a4d99316e2d654d9bd0b`
- Access: public GitHub page opened in dedicated Surf window; separate scout inspected this exact pinned README from an existing local clone. Scout says current HEAD matched the pin at its inspection; no broader current-state claim.
- Relevance: desktop editor/agent chat and device terminal pattern.
- Limitation: README feature report, not deployment or adoption measurement.
- Rights/privacy: no README text copied; source code/assets not assessed or reused.

## cardputer_llm — browser opened and scout local clone

- URL: https://github.com/layer812/cardputer_llm
- Revision: `f7a839d1221a3ac2b65a6d32036b937d5884ea7d`
- Document: `README.md`; blob `552d322f2d0cf8a181585f259bdfa30eb522d351`
- Access: public GitHub page opened in dedicated Surf window; separate scout inspected this exact pinned README from an existing local clone. Scout says current HEAD matched the pin at its inspection; no broader current-state claim.
- Relevance: Cardputer serial chat UI with model inference on external Raspberry Pi.
- Limitation: author reports slow performance; not on-device inference and not measured independently.
- Rights/privacy: no README text copied; source code/assets not assessed or reused.

## Claude Desktop Buddy Cardputer fork — browser opened and scout local clone

- URL: https://github.com/y88huang/claude-desktop-buddy-cardputer
- Revision: `257d3d84435c11a98e9dc376257acffda2a633cb`
- Document: `README.md`; blob `d8183c021ab40496f7177e870bc5c871c0636fc0`
- Access: public GitHub page opened in dedicated Surf window; separate scout inspected this exact pinned README from an existing local clone. Scout says current HEAD matched the pin at its inspection; no broader current-state claim.
- Relevance: BLE-linked physical agent status/permission affordance.
- Limitation: README describes developer-mode API and says feature is maker/developer-oriented, not officially supported; no security/usability validation.
- Rights/privacy: no README text copied; source code/assets not assessed or reused.

## MQTT dashboard — scout local clone only

- URL: https://github.com/w35m17h/cardputer-mqtt
- Revision: `48930a30d7d787d695b95fd2b2e62c7b7bb61465`
- Document: `README.md`; blob `2644f76e46075c827c6737926feee2e79f9fb330`
- Access: separate scout inspected local clone HEAD README; not opened in this browser session; no current-remote claim.
- Relevance: broker state display, topic control/macros, profile/configuration report.
- Limitation: self-report; scope/authorization risks not assessed; not evidence of safe deployment or demand.
- Rights/privacy: no text copied; no source execution; operational details excluded.

## ntfy pager — scout local clone only

- URL: https://github.com/forshaws/cardputer-ntfy
- Revision: `dba7143b0290b106bd6b6ae2c8f7b93d36bce48c`
- Document: `README.md`; blob `bbdee3c6614a199e73181e0283788abab2d5c9fa`
- Access: separate scout inspected local clone HEAD README; not opened in this browser session; no current-remote claim.
- Relevance: Cardputer notification/pager report.
- Limitation: self-report; no alert reliability or adoption evidence. Example operational payload deliberately omitted.
- Rights/privacy: no text or payload copied; no source execution.

## Interactive SSH Cardputer fork — scout local clone only

- URL: https://github.com/sub0pt1mal/interactivesetup-m5cardputer-sshclient
- Revision: `944336fb415fa607660cbf3a3f86f635ef8eb788`
- Document: actual case-sensitive path `readme.md`; blob `b7ef414fb6e15479adcfcc8fd4a6e12983f67ff9`
- Access: separate scout inspected local clone HEAD document; not opened in this browser session; no current-remote claim.
- Relevance: handheld SSH/remote terminal report.
- Limitation: README warns of plaintext credential storage, marks WireGuard WIP/failed, and describes low maintenance; negative/risk evidence, not recommendation.
- Rights/privacy: credentials/hostnames not copied; no source execution.
