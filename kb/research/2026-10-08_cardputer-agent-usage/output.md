---
type: ResearchHandoff
title: "Issue #35 bounded Cardputer and agent-device findings handoff"
description: "Evidence-qualified, source-linked findings for later capability planning."
created: "2026-10-08"
issue: "https://github.com/ozand/adv/issues/35"
status: draft
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
tags: [cardputer, esp32, agents, research, handoff]
---

# Issue #35 findings handoff

**Status:** bounded research findings; no implementation or owner acceptance implied.

## Findings

- Project-authored examples describe several distinct patterns: a desktop agent/editor with device terminal access (AIFlow); a physical status and permission surface for a desktop agent (Claude Desktop Buddy fork); external-compute chat using Cardputer as a serial UI (cardputer_llm); broker-mediated state/control (MQTT); notifications (ntfy); and remote terminal access (SSH client).
- Official M5Stack documentation supports device-capability context only. Its stated application areas are not evidence of user behavior.
- These examples support keeping approval/status, console access, notifications, general control, and remote shell as separate research scenarios. They do not establish demand or validate an architecture.

## Evidence-qualified opportunity ordering

1. **Agent/device status and approval scenarios** — most directly aligned to the Issue #35 question, supported by README reports for Claude Buddy and AIFlow. Still self-reported, with no independent usage, reliability, safety, or usability evidence.
2. **Notification and control as distinct scenarios** — MQTT and ntfy README reports describe different interaction classes; neither demonstrates deployed reliability or user preference.
3. **Remote terminal and external-compute chat as boundary cases** — reports add alternatives but also explicit caveats (plaintext SSH credential storage; external inference and author-reported slowness).

This is relevance-based, not demand ranking. Evidence is insufficient to prioritize by adoption, popularity, satisfaction, or market size.

## Limits and follow-up evidence gaps

No user interviews, adoption telemetry, independent runtime/device tests, comparative task studies, or security reviews were performed. Sample is seven source records: one vendor product page and six project README reports, of which three README records were opened publicly and three inspected by a separate local-clone scout. See `brief.md`, `raw/README.md`, and `synthesis.md` for method/provenance. Source code, binaries, and credentials were not copied or executed; no QMD or hardware action occurred.

## Recommendation boundary

Use these patterns to formulate later capability questions only. Before architecture or implementation decisions, gather independent user/task evidence and assess authorization, failure handling, credential handling, supported interfaces, and recovery. This handoff does not select MCP, host/device/hybrid architecture, grant shell/GPIO access, or authorize roadmap stage E implementation.
