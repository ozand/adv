---
type: ResearchBrief
title: "Issue #35 bounded Cardputer and agent-device research brief"
description: "Scope, method, provenance boundaries, and process deviations for bounded usage research."
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
tags: [cardputer, esp32, agents, research, method]
---

# Issue #35 research brief

- Issue: https://github.com/ozand/adv/issues/35 (OPEN, in progress)
- Scope: bounded evidence about reported Cardputer/ESP32 utilities and agent/device interfaces; not market sizing or implementation.
- Checkout: `ozand/adv`, clean isolated clone, main `e253cf84f6caefb61a9e82ab6a8082a9b5fab3da`.
- Local project QMD/source corpus: absent; no project QMD command or index changes. After a validator failure, one workspace-level `qmd search ... -c workspace-kb` lookup was attempted; it returned `Collection not found: workspace-kb`. This was outside the project-QMD scope and is disclosed as a process deviation. No further QMD commands were run.
- Sampling cap: 8 materially used public source pages total, 45 minutes, 60 seconds/page. Six README records were inspected by the scout in existing local clones; four public pages were opened in the dedicated Surf window. Deduplication by canonical URL + revision + document path yields seven distinct source records: official M5Stack Cardputer product documentation, plus six project README records. Three web-opened repository pages exactly match the scout's pinned revisions and README blob IDs. This is below the 8-source cap; the planned time window was not exhausted. No further pages were opened.
- Surf: CLI 2.20.0; dedicated task window 1071839057; collection began 2026-10-08 16:08:09 +03:00 and ended by 16:16:36 +03:00 (last observed collection-status time). Elapsed collection window was at most 8m27s; 45-minute cap was not exhausted. Only this new window/task tabs were used.
- Source allocation: M5Stack product page (official device capability/context); AIFlow, cardputer_llm, Claude Desktop Buddy Cardputer, MQTT dashboard, ntfy pager, and SSH client (project-authored use-case reports). Three repository records were both opened publicly and inspected in local scout clones; duplicate URL+revision+path counts once. The other three were scout local-clone evidence, not pages opened in my browser session.
- Stop criteria: stop at page/time cap or on auth/challenge/rate/transport errors. No such access error occurred; collection stopped after four browser-opened pages because the assigned source sample had been covered and no additional pages were authorized by the sample plan.
- Exclusions: no user interviews, telemetry, installations, source execution, hardware/device/network/GPIO actions, architecture selection, demand estimates, or QMD update.
- Evidence classes: official product documentation describes intended capabilities; project README statements are author-reported features/use cases. Neither class establishes independent adoption, frequency, user satisfaction, or market demand. No interviews, telemetry, independent runtime validation, or device tests were conducted.
- Provenance: full pins and README blob IDs for all six project repositories are recorded in `raw/README.md`; the three overlapping web pages match scout pins. The official product page has a canonical URL but no immutable revision identifier. Scout inspected local clone HEAD README files only and made no current-remote claim. Discovery was limited to Issue #35 scope and the assigned bounded scout sample; no search-engine queries or additional source discovery were performed.
- Deliverables: `raw/README.md` is a provenance/access-mode register with bounded paraphrases (no raw full-text capture); `synthesis.md` contains cited, confidence-qualified evidence synthesis; `output.md` is a planning handoff. The three scout-only items are explicitly labeled as local-clone evidence, not browser-opened pages. One brief file was initially written before access-plan approval; it was later corrected to document actual access, source deduplication, and this deviation. No source collection or synthesis occurred during that initial premature write.
- Publication gate: only bounded paraphrase and citations; no full README/source copy. Local original clones remain private under ignored `sources/`.
