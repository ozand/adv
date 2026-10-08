---
type: ResearchReport
title: "Reported Cardputer and agent-device interface examples"
description: "Bounded, source-linked examples from project README claims and official product documentation; not adoption research."
created: "2026-10-08"
issue: "https://github.com/ozand/adv/issues/35"
status: draft
sources:
  - resource: "https://docs.m5stack.com/en/core/Cardputer"
    revision: "Product page accessed 2026-10-08; no immutable revision identifier"
  - resource: "https://github.com/m5stack/aiflow"
    revision: "930edd59329568bc8c8f5db5d591abc51548afa2"
    document: "README.md"
    blob: "38b8ea6663fc1cc3bf42a4d99316e2d654d9bd0b"
  - resource: "https://github.com/layer812/cardputer_llm"
    revision: "f7a839d1221a3ac2b65a6d32036b937d5884ea7d"
    document: "README.md"
    blob: "552d322f2d0cf8a181585f259bdfa30eb522d351"
  - resource: "https://github.com/y88huang/claude-desktop-buddy-cardputer"
    revision: "257d3d84435c11a98e9dc376257acffda2a633cb"
    document: "README.md"
    blob: "d8183c021ab40496f7177e870bc5c871c0636fc0"
  - resource: "https://github.com/w35m17h/cardputer-mqtt"
    revision: "48930a30d7d787d695b95fd2b2e62c7b7bb61465"
    document: "README.md"
    blob: "2644f76e46075c827c6737926feee2e79f9fb330"
  - resource: "https://github.com/forshaws/cardputer-ntfy"
    revision: "dba7143b0290b106bd6b6ae2c8f7b93d36bce48c"
    document: "README.md"
    blob: "bbdee3c6614a199e73181e0283788abab2d5c9fa"
  - resource: "https://github.com/sub0pt1mal/interactivesetup-m5cardputer-sshclient"
    revision: "944336fb415fa607660cbf3a3f86f635ef8eb788"
    document: "readme.md"
    blob: "b7ef414fb6e15479adcfcc8fd4a6e12983f67ff9"
tags: [cardputer, esp32, agents, interfaces, research]
---

# Reported Cardputer and agent-device interface examples

## Executive summary

The bounded sample contains several distinct interface patterns: a desktop coding environment paired with a device terminal; a physical approval/status surface for a desktop coding agent; a handheld chat terminal whose inference runs on an external Raspberry Pi; and broker-based control, notification, or SSH interfaces. These are examples reported by project authors, not evidence of adoption or user demand. The official M5Stack page documents device capabilities and intended application areas, not observed use.

The evidence supports treating approval/status, device-console, notification, and remote-control interfaces as separate capability hypotheses. It does not support choosing an architecture, declaring a priority by demand, or concluding that a particular interface is widely used.

## Device context (official product documentation)

M5Stack describes Cardputer as an ESP32-S3-based, keyboard-and-screen device with microphone, speaker, IR emitter, Grove expansion, and microSD storage. The product page lists rapid prototyping, industrial control, smart-home control, data acquisition, embedded education, and IoT as application areas. These are vendor-stated capabilities and intended applications, not independent usage observations.

Source: [M5Stack Cardputer product page](https://docs.m5stack.com/en/core/Cardputer), accessed 2026-10-08. Mutable web page; no immutable revision identifier was captured.

## Reported project examples

### Desktop development and device console

AIFlow's README describes an Electron/React desktop editor with chat using the Claude Agent SDK and a terminal connecting to devices over WebSocket or Web Serial. This presents a developer workflow that brings agent chat/editor and device console into one desktop application. Evidence is a project README claim; it does not establish actual deployment, reliability, or user adoption.

Source: [AIFlow](https://github.com/m5stack/aiflow), pinned revision [`930edd59329568bc8c8f5db5d591abc51548afa2`](https://github.com/m5stack/aiflow/commit/930edd59329568bc8c8f5db5d591abc51548afa2), README blob `38b8ea6663fc1cc3bf42a4d99316e2d654d9bd0b`.

### Physical agent approval and status surface

Claude Desktop Buddy Cardputer fork README reports a BLE-connected Cardputer ADV interface for Claude desktop developer mode. It describes visible activity/transcript/status, Y/N permission approval, and audio/LED feedback. The README states the BLE API requires developer mode and is intended for makers/developers, not an officially supported product feature. This is a project-reported proof-of-concept pattern, not validation of security suitability, accessibility, usability, or supported operation.

Source: [Claude Desktop Buddy Cardputer fork](https://github.com/y88huang/claude-desktop-buddy-cardputer), pinned revision [`257d3d84435c11a98e9dc376257acffda2a633cb`](https://github.com/y88huang/claude-desktop-buddy-cardputer/commit/257d3d84435c11a98e9dc376257acffda2a633cb), README blob `d8183c021ab40496f7177e870bc5c871c0636fc0`.

### Handheld chat with external inference

The cardputer_llm README describes the Cardputer as a serial terminal connected to a Raspberry Pi Zero 2 W running Ollama and a small model. The model runs on the external Pi, not on the Cardputer; the author warns that inference is slow. This is evidence for a split device/UI plus external compute example, not on-device LLM capability or measured performance.

Source: [cardputer_llm](https://github.com/layer812/cardputer_llm), pinned revision [`f7a839d1221a3ac2b65a6d32036b937d5884ea7d`](https://github.com/layer812/cardputer_llm/commit/f7a839d1221a3ac2b65a6d32036b937d5884ea7d), README blob `552d322f2d0cf8a181585f259bdfa30eb522d351`.

### Broker control and notifications

The cardputer-mqtt README reports an MQTT dashboard with subscribed state, topic toggles/macros, profiles, and SD-backed configuration. This differs from approval UI by providing general broker-mediated control/state patterns; it implies scope and authorization questions and is not evidence of safe or deployed operation.

Source: [cardputer-mqtt](https://github.com/w35m17h/cardputer-mqtt), pinned revision [`48930a30d7d787d695b95fd2b2e62c7b7bb61465`](https://github.com/w35m17h/cardputer-mqtt/commit/48930a30d7d787d695b95fd2b2e62c7b7bb61465), README blob `2644f76e46075c827c6737926feee2e79f9fb330`.

The cardputer-ntfy README reports a pager-style notification client with topic configuration and locally persisted/cycling alert text. Its stated role is narrower and more notification-oriented than MQTT control. A README example mentions server leak alerts; this report intentionally does not reproduce operational payload details. This is author-reported capability, not an evaluated alerting system.

Source: [cardputer-ntfy](https://github.com/forshaws/cardputer-ntfy), pinned revision [`dba7143b0290b106bd6b6ae2c8f7b93d36bce48c`](https://github.com/forshaws/cardputer-ntfy/commit/dba7143b0290b106bd6b6ae2c8f7b93d36bce48c), README blob `bbdee3c6614a199e73181e0283788abab2d5c9fa`.

### Remote terminal

The Cardputer SSH fork README describes a handheld remote SSH terminal. It explicitly warns that Wi-Fi/SSH credentials are saved in plaintext; it also labels WireGuard as work-in-progress/failed and says the fork is low maintenance. These are material limitations, so this is risk/negative evidence rather than a recommendation. No credential values or network details are included.

Source: [interactive SSH Cardputer fork](https://github.com/sub0pt1mal/interactivesetup-m5cardputer-sshclient), pinned revision [`944336fb415fa607660cbf3a3f86f635ef8eb788`](https://github.com/sub0pt1mal/interactivesetup-m5cardputer-sshclient/commit/944336fb415fa607660cbf3a3f86f635ef8eb788), actual document path `readme.md`, blob `b7ef414fb6e15479adcfcc8fd4a6e12983f67ff9`.

## Opportunity ordering (evidence relevance, not demand)

1. **Agent status/approval interaction and desktop-device bridge.** Highest direct relevance to the agent/device interface question: one README describes approval/status on a physical Cardputer, another describes desktop agent chat with device terminal connectivity. Evidence remains self-reported, one project per pattern, with no independent usage validation. Any future work needs separate review of authorization, failure modes, and supported API status.
2. **Notification versus general control as distinct interface contracts.** MQTT and ntfy examples suggest different roles: interactive state/action versus alert presentation. This distinction can inform later scenario discovery, but source claims do not establish which is wanted or safer.
3. **Remote terminal and external-compute chat as alternative interaction/deployment patterns.** SSH example has explicit credential-storage and maintenance risks; external LLM example shifts inference off-device and reports slow performance. These are useful boundary cases, not recommendations.

This ordering is based only on match to Issue #35's research question and evidence specificity. There is insufficient evidence to rank demand, adoption, popularity, market size, or user preference.

## Evidence strength and limitations

- **Official product capability/intended-use evidence:** one M5Stack product page; authoritative for vendor-published specifications and intended use, not actual use.
- **Project-reported implementation/use-case evidence:** six pinned README records (AIFlow, cardputer_llm, Claude Buddy fork, MQTT dashboard, ntfy pager, SSH client). These document what project authors say their projects provide. No usage telemetry, interviews, adoption counts, independent product tests, or runtime/device validation were gathered.
- **Sampling:** four public browser pages opened (M5Stack Cardputer product page and three GitHub README pages); six README records inspected by a separate local-clone scout. Three repo URL+revision+document identities overlap exactly, leaving seven distinct source records total. Combined source cap 8 respected; 45-minute cap not exhausted. The three scout-only README sources were not opened in the browser session. The scout reports local clone HEADs, not current remote status.
- **Rights/privacy:** this synthesis paraphrases bounded claims and links to pinned sources; it does not reproduce full READMEs, binaries, credentials, or private operational data. The SSH security warning is retained at a high level; ntfy's operational example payload is omitted. Repository licenses were not assessed for this study; do not reuse source code/assets based on this report.
- **Confidence:** high that these statements occur in the cited project documents as inspected/reported; low regarding operational performance or external validity; no basis for adoption/demand conclusions.

## Research method and provenance

Issue #35 bounded research, 2026-10-08. The local scout inspected only README documents in six existing local clones and returned exact commit and document blob identifiers. Three repository README pages were also opened in an explicitly created Surf window; GitHub current HEAD lookups matched those scout pins for those three repositories. The official product page was read in the same dedicated window and has no immutable revision. No local QMD collections/index were available, and QMD was not run. No source code was executed, no hardware was operated, and no device/network/GPIO control was attempted. Research stopped after the assigned seven-source sample; no additional web pages were opened.
