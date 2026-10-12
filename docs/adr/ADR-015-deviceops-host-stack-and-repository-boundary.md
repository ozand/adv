# ADR-015: Implement DeviceOps as a Python host service in a separate runtime repository

**Status:** Proposed — requires owner review and acceptance before implementation.
**Date:** 2026-10-12.
**Issue:** [#68](https://github.com/ozand/adv/issues/68); [Epic #66](https://github.com/ozand/adv/issues/66).
**Supersedes:** None.
**Related:** ADR-006, ADR-009, ADR-014.

## Context

ADR-014 establishes a host service/core as the proposed center, but leaves implementation language, first OS, IPC, storage and runtime repository open. Issue #68 asks for a bounded comparison and explicit implementation boundary. This is a documentation decision only; owner acceptance is pending.

Evidence: **verified** — PR #82 candidate `196d2f915e0fa2424b707f3fd30d873050a3b022` contains a Python ADV diagnostic CLI and fake-serial tests; its serial import is optional, and protocol parsing uses Python standard-library modules. **reported** — project roadmap requests a persistent single-writer executor and CLI/MCP parity. These facts support reuse feasibility, not a persistent service implementation or production readiness.

### Problem statement

Propose a host stack and repository boundary for owner decision: reuse existing protocol logic in a small local MVP without making `adv` a runtime or binary distribution repository.

### Prior art

The existing ADV CLI and fake-serial tests at candidate revision `196d2f915e0fa2424b707f3fd30d873050a3b022` provide a Python reuse point. Registry metadata checked 2026-10-12: pyserial 3.5 (BSD-3-Clause); MCP Python SDK 2.3.0 (MIT, Python >=3.10); pytest 8.4.2 (MIT, Python >=3.9); TypeScript MCP SDK 1.32.1 (MIT, Node >=18); serialport 13.0.0 (MIT, Node >=20). These are candidates, not approved dependencies or lockfile pins. Registry metadata does not establish Windows compatibility, packaging quality, full transitive license compliance, or security.

## Decision

### What this IS

Recommend a **Python 3.11+ host core**, with **Windows 11 x64 as the first qualification target**, one long-lived executor process, local SQLite persistence and named-operation CLI/MCP frontends. Use pyserial as the serial-adapter candidate. MCP is an optional frontend, not the core API. The initial IPC recommendation is stdio for agent-launched use; a local named-pipe transport is deferred until multi-client lifecycle needs are demonstrated. The core exposes typed in-process operations; clients must not open serial independently.

Place runtime code, packaging, lockfiles, binaries and runtime tests in a **new, separately owner-approved DeviceOps runtime repository**, not in `adv`. Do not create that repository as part of this proposal. In `adv`, allow only reviewed architecture/decision documentation and coordination artifacts. Existing `scripts/adv_diagnostic_cli.py` and its tests are candidates for protocol/validation reuse, not a ready service. A later implementation must use an explicitly reviewed path allowlist; this proposal does not authorize moving files.

For a future prototype, shortlist Python standard library for core/SQLite, pyserial 3.5 (BSD-3-Clause), official MCP Python SDK 2.3.0 (MIT; Python >=3.10), and pytest 8.4.2 (MIT; Python >=3.9). These versions are **reported registry metadata observed 2026-10-12**, not a selection, lockfile or full transitive-license audit. Revalidate primary project sources, security notices, Windows support and transitive licenses before pinning versions in the runtime repository. No network listener, device-side MCP, browser bridge, tunnel, flashing library, or OTA dependency in the first MVP.

### What this IS NOT

This is not owner acceptance of the detailed design, authorization to create a repository, install packages, operate USB/COM, run firmware, deploy, or expose a network service. It does not change ADR-006/009 wire contracts or implement grants/security policy. It does not assert that Python, SQLite, Windows packaging, or any SDK has passed qualification.

### Success criteria

Owner accepts or rejects this proposal explicitly; a later issue names the runtime repository and exact allowed paths; a fake-only prototype proves one executor owner across CLI/MCP, persistence across restart, and zero physical I/O in offline tests; Windows packaging and dependency/license checks pass before hardware qualification.

## Consequences

### What gets easier

Reuse of the existing host validator and tests; one process owns transport and job state; SQLite enables inspectable local persistence without a separate service.

### What gets harder

Python distribution/upgrade and SQLite migration/backup become product responsibilities. A process boundary, stdio lifecycle and single-instance enforcement require design and tests. Windows COM behavior and packaging still require dedicated qualification; Python's dynamic typing requires explicit schemas and validation.

### What does not change

The `adv` repository remains documentation/knowledge, not runtime distribution. Fake tests precede device tests. Device access, USB/COM, audio, flashing, network exposure and dependency installation remain separately gated. Timeouts and uncertain effects never imply safe retry.

## Alternatives Considered

- **TypeScript/Node:** strong MCP ecosystem and mature serial bindings, but Node >=20 is required by the checked serialport release and native bindings complicate packaging; no repository evidence justifies that cost over reuse of existing Python protocol tests.
- **Rust:** attractive for a static binary and stronger compile-time guarantees, but requires a protocol/client rewrite and separate serial/MCP ecosystem qualification; firmware-language preference is not sufficient evidence for host choice.
- **Python without a service process:** simpler initially, but independent CLI/MCP invocations cannot reliably own one serial session and durable job lifecycle.
- **Keep runtime in `adv`:** rejected because it conflicts with the repository's published knowledge-only boundary and would couple binary/runtime release to knowledge publication.
- **Do nothing:** retains split host operations and leaves the DeviceOps MVP untestable; acceptable if the owner rejects the service direction, in which case no runtime repo is created.

## Test Contract

| Claim | Test | Currently |
|---|---|---|
| CLI and MCP share one executor | fake parity and single-writer tests | not yet written |
| State survives restart without replaying uncertain work | SQLite crash/restart fixtures | not yet written |
| Windows distribution works without device access | clean-VM install/uninstall smoke test | not yet written |
| Dependencies/licenses are bounded and reproducible | lockfile + license inventory CI | not yet written |
| Offline suite performs no physical I/O | fake transport and zero-device-call assertion | not yet written |

## Rollback

Before implementation, reject or replace the proposal without runtime migration. After acceptance, changing language, repository boundary, IPC or persistence requires a superseding ADR; existing firmware contracts remain unaffected.

## References

Issues [#37](https://github.com/ozand/adv/issues/37), [#38](https://github.com/ozand/adv/issues/38), [#68](https://github.com/ozand/adv/issues/68); PR #82 candidate SHA above; PyPI `pyserial` and `mcp`, npm `@modelcontextprotocol/sdk` and `serialport` metadata checked 2026-10-12; ADR-014 and DeviceOps architecture/requirements.
