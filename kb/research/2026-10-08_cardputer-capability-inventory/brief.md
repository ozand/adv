---
type: research-brief
title: Cardputer capability inventory beyond the fixed diagnostic interface
date: 2026-10-08
issue: https://github.com/ozand/adv/issues/36
status: draft
---

# Cardputer capability inventory — research brief

## Scope and method

A bounded source-document study for Issue #36. Inventory candidate capabilities beyond the four-command source contract in ADR-006; exclude those diagnostics from new capability rows. Distinguish project-reported behavior, source-documented interface/implementation, and actual installed-device verification. Only exact, pinned local source documents already present in the approved corpus and accepted project contracts are eligible. Maximum eight candidate rows; no quota is implied. Stop at eight or when sources are insufficient. No catalog-wide enumeration, code execution, device operation, network access, clone, QMD, API publication, or architecture choice.

For each candidate record its source/revision/path, interface, effects, prerequisites, risks, authority/permission level, use-case relevance, evidence class, uncertainties, and whether human/device verification is required. If a field lacks evidence, say unknown; do not infer support from a generic MCU or board label. See [candidate inventory](summary.md).

## Evidence classes

- **Verified (source contract/test only):** a bounded source-level behavior supported by an accepted contract or passing source-contract tests. This does not imply runtime or hardware verification.
- **Source-documented:** an upstream README or other pinned document reports an implementation or intended behavior. Attribution remains explicit; it is not independently observed.
- **Unknown:** source is absent, ambiguous, incomplete, or not tied to the claimed board/revision/installed state.
- **Device-verified:** reserved for an explicit, permitted, timestamped observation tied to exact device/firmware. None is established by this research brief.

## Exclusions and gates

Issue #2 / ADR-006 already own `status`, `sd_test`, `run <ID>`, and `result <ID>`, including their fixed bounds, RAM retention, one-shot SD behavior, and source-contract test evidence. They are cross-referenced, not counted as new capability rows or hardware PASS claims. No shell, arbitrary file/memory access, bulk storage reads, unrestricted GPIO, device/network MCP, installation, or firmware modification is authorized. Issue #35 usage findings are optional scenario context only and do not establish capability or adoption.

## Bounded sampling record

Sampling/provenance record (session timestamps; no monotonic duration measured): six local README documents were inspected at 2026-10-08 13:01:36.132–13:02:22.907. All six repositories were already included in the Issue #35 scout; three of the six also overlapped the lead's separately opened pages (AIFlow, Cardputer LLM, Claude Buddy) at the same canonical repository revisions. The other three documents were MQTT, ntfy, and SSH client. Thus this inventory has six source rows, zero new repository sources beyond #35, and does not add three independent sources to the #35 corpus. Deduplicate source counts by canonical repository URL + full revision + document path, not by page or study count. Brief and summary were first written at 13:15:42.186 and 13:16:34.653; the research commit completed at 13:21:22.669. Times are local session transcript timestamps; no monotonic end-to-end duration is claimed. No new upstream source pages, network research, clones, code, QMD, or device operations were used. GitHub Issue/governance metadata and the pinned project roadmap/ADR were read for scope and boundaries, not counted as capability sources. No claim of actual adoption or installed-device behavior.

## Publication and review

This is a draft evidence artifact, not canonical wiki synthesis or a public API/architecture decision. Preserve citations and source identity; do not copy whole README/code excerpts. Apply privacy, relevance, provenance, and rights review to any source capture before publication. Independent review is required before claiming Issue #36 complete.
