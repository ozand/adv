# ADR-015: Implement the DeviceOps host core in Python

**Status:** Accepted — owner confirmed the D01 language/OS choice on 2026-10-12; acceptance does not authorize runtime or device effects.
**Date:** 2026-10-12.
**Issue:** [#68](https://github.com/ozand/adv/issues/68); [Epic #66](https://github.com/ozand/adv/issues/66).
**Storage decision:** SQLite was also owner-accepted for local durable state in #68; see D01. Schema, retention and migration are separate implementation work.
**Supersedes:** None.
**Related:** ADR-014, ADR-016, ADR-017.

## Context

ADR-014 establishes a proposed host service/core but leaves implementation language open. Issue #68 asks for a bounded comparison of Rust, Python and TypeScript, including reuse and maintenance. This ADR records the owner-accepted host language/runtime choice; process lifecycle, IPC and repository location are separate decisions. SQLite storage is also accepted in Issue #68 and summarized in the D01 decision record.

Evidence: **verified** — PR #82 candidate `196d2f915e0fa2424b707f3fd30d873050a3b022` contains a Python ADV diagnostic CLI and fake-serial tests; serial import is optional and protocol parsing uses standard-library modules. **reported** — the DeviceOps roadmap requires a single-writer executor and CLI/MCP parity. Existing Python source supports reuse, but does not prove a service implementation or production readiness.

### Problem statement

Select a host language that can reuse existing protocol logic without treating firmware language preference as a host constraint.

### Prior art

The Python client and fake-serial tests at the candidate SHA above are the directly relevant reuse point. Versioned registry candidates and exact artifact digests are listed in [D01](../deviceops/D01-DECISION.md); they are reported metadata, not selected dependency pins or qualification evidence. Registry metadata does not establish Windows compatibility, package quality, full transitive-license compliance or security.

## Decision

### What this IS

Use Python 3.11+ for the DeviceOps host core, with Windows 11 x64 as the first qualification target. Owner accepted this language/OS direction on 2026-10-12. The measured host has CPython 3.11.9 x64 and standard-library SQLite 3.45.1 available; this verifies an offline interpreter/runtime is available, not a clean installer, packaging, or device compatibility. For a prototype, prefer the standard library and shortlist pyserial, the official MCP Python SDK and pytest; verify exact versions, primary sources, platform compatibility and all transitive licenses before pinning.

### What this IS NOT

This ADR does not decide executor process lifecycle, IPC, SQLite schema/retention/migrations, code repository, packaging design, or authority/security enforcement. It does not accept a dependency version, authorize installation, or approve runtime/device/network activity. It does not change ADR-006/009 firmware contracts.

### Success criteria

A later fake-only prototype reuses or faithfully ports the existing protocol tests; clean Windows qualification and dependency/license review pass before device access. Owner decision recorded in Issue #68; Windows packaging and device compatibility remain unqualified.

## Consequences

### What gets easier

The existing Python parser and fake-serial tests provide a concrete reuse path and reduce initial protocol rewrite.

### What gets harder

Python packaging, upgrades and runtime support become ongoing responsibilities; schemas require explicit validation and Windows behavior remains to be qualified.

### What does not change

Firmware language and ABI stay independent. No device access, serial, audio, flashing, networking or automatic retry is authorized by this language choice.

## Alternatives Considered

- **TypeScript/Node:** official MCP and serial libraries exist, but native serial packaging has a Node >=20 requirement in the checked serialport release and no current repository reuse advantage.
- **Rust:** strong type safety and possible static packaging, but requires rewriting current Python protocol behavior and separately qualifying serial/MCP crates; firmware-language preference is insufficient evidence.
- **No language decision:** preserves flexibility, but prevents a coherent prototype plan; not selected.

## Test Contract

| Claim | Test | Currently |
|---|---|---|
| Existing protocol behavior is reusable | fake-serial regression suite at pinned source revision | tests exist at candidate SHA; not rerun here |
| Selected runtime is viable on Windows | clean Windows 11 install and fake-only smoke test | not yet written |
| Dependencies are acceptable | pinned lock + transitive license inventory and security review | not yet written |

## Rollback

Owner acceptance recorded 2026-10-12. A host-language switch requires a superseding ADR; existing firmware contracts remain unchanged.

## References

Issue [#68](https://github.com/ozand/adv/issues/68), PR #82 candidate SHA above, ADR-014, DeviceOps architecture/requirements, and package metadata sources (PyPI/npm records checked 2026-10-12).
