# ADR-015: Implement the DeviceOps host core in Python

**Status:** Proposed — requires owner review and acceptance before implementation.
**Date:** 2026-10-12.
**Issue:** [#68](https://github.com/ozand/adv/issues/68); [Epic #66](https://github.com/ozand/adv/issues/66).
**Supersedes:** None.
**Related:** ADR-014, ADR-016, ADR-017.

## Context

ADR-014 establishes a proposed host service/core but leaves implementation language open. Issue #68 asks for a bounded comparison of Rust, Python and TypeScript, including reuse and maintenance. This ADR selects only a proposed host language/runtime; process lifecycle, IPC, storage and repository location are separate decisions.

Evidence: **verified** — PR #82 candidate `196d2f915e0fa2424b707f3fd30d873050a3b022` contains a Python ADV diagnostic CLI and fake-serial tests; serial import is optional and protocol parsing uses standard-library modules. **reported** — the DeviceOps roadmap requires a single-writer executor and CLI/MCP parity. Existing Python source supports reuse, but does not prove a service implementation or production readiness.

### Problem statement

Recommend a host language that can reuse existing protocol logic without treating firmware language preference as a host constraint.

### Prior art

The Python client and fake-serial tests at the candidate SHA above are the directly relevant reuse point. Candidate registry metadata observed 2026-10-12: pyserial 3.5 BSD-3-Clause; MCP Python SDK 2.3.0 MIT (Python >=3.10); pytest 8.4.2 MIT (Python >=3.9); TypeScript MCP SDK 1.32.1 MIT (Node >=18); serialport 13.0.0 MIT (Node >=20). Metadata does not establish Windows compatibility, package quality, full transitive-license compliance or security; versions are not selected or pinned.

## Decision

### What this IS

Recommend Python 3.11+ for the DeviceOps host core, with Windows 11 x64 as the first qualification target. The language choice is based on existing Python protocol code and remains a proposal pending owner acceptance. For a prototype, prefer the standard library and shortlist pyserial, the official MCP Python SDK and pytest; verify exact versions, primary sources, platform compatibility and all transitive licenses before pinning.

### What this IS NOT

This ADR does not decide executor process lifecycle, IPC, storage, code repository, packaging design, or authority/security enforcement. It does not accept a dependency version, authorize installation, or approve runtime/device/network activity. It does not change ADR-006/009 firmware contracts.

### Success criteria

A later fake-only prototype reuses or faithfully ports the existing protocol tests; clean Windows qualification and dependency/license review pass before device access. Owner accepts or rejects this proposal explicitly.

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
- **No language decision:** preserves flexibility, but prevents a coherent prototype plan. Owner may reject the recommendation and keep the choice open.

## Test Contract

| Claim | Test | Currently |
|---|---|---|
| Existing protocol behavior is reusable | fake-serial regression suite at pinned source revision | tests exist at candidate SHA; not rerun here |
| Proposed runtime is viable on Windows | clean Windows 11 install and fake-only smoke test | not yet written |
| Dependencies are acceptable | pinned lock + transitive license inventory and security review | not yet written |

## Rollback

Before owner acceptance, reject the proposal without runtime changes. After acceptance, a host-language switch requires a superseding ADR; existing firmware contracts remain unchanged.

## References

Issue [#68](https://github.com/ozand/adv/issues/68), PR #82 candidate SHA above, ADR-014, DeviceOps architecture/requirements, and package metadata sources (PyPI/npm records checked 2026-10-12).
