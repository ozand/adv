# D01 — Host stack and repository decision proposal

**Status:** Proposal for owner decision; not implementation authorization. Issue [#68](https://github.com/ozand/adv/issues/68). ADR: [ADR-015](../adr/ADR-015-deviceops-host-stack-and-repository-boundary.md). Inputs: [architecture](ARCHITECTURE.md), [contracts](CONTRACTS.md), [roadmap](ROADMAP.md), Issues [#37](https://github.com/ozand/adv/issues/37) and [#38](https://github.com/ozand/adv/issues/38).

## Recommendation

Choose Python 3.11+ for a Windows 11-first, local, single-owner DeviceOps service. Use SQLite for durable jobs/evidence; expose one typed core to CLI and optional MCP frontends. Start with stdio for agent-launched use. Do not start a listener. Keep the physical transport in one core-owned broker; clients never open COM independently. Keep runtime source, manifests, locks, tests and binaries in a new runtime repository only after owner accepts its location/name. The `adv` repository remains documentation and coordination.

This recommendation is **theory**, not a measured compatibility result. Python reuse has a concrete source basis: PR #82 candidate `196d2f915e0fa2424b707f3fd30d873050a3b022` contains a standard-library protocol validator plus fake-serial tests. That does not make the CLI a service or prove Windows packaging/serial behavior.

## Stack comparison

| Candidate | Reuse / MCP / serial | Windows and packaging | Cost / risk | Disposition |
|---|---|---|---|---|
| Python 3.11+ | Existing ADV CLI/tests; pyserial; official MCP Python SDK | Windows support and single-folder packaging require prototype qualification; straightforward script/test workflow | Dynamic typing; distribution and migrations need ownership | Recommended for reuse-first MVP |
| TypeScript / Node | Official MCP TypeScript SDK; serialport bindings | SDK metadata requires Node >=18; serialport 13 requires Node >=20 and native binding packaging qualification | Native dependencies and larger deployment footprint | Viable alternative; no reuse advantage in current repo |
| Rust | Strong static typing and single-binary potential; serial/MCP crates need pinned review | Potentially good Windows artifact, but cross-build/signing/install workflow unverified | Rewrite existing Python protocol behavior; more initial integration work | Do not infer host language from firmware preference |

Metadata snapshot checked 2026-10-12: pyserial 3.5 (BSD-3-Clause); MCP Python SDK 2.3.0 (MIT, Python >=3.10); MCP TypeScript SDK 1.32.1 (MIT, Node >=18); serialport 13.0.0 (MIT, Node >=20). These are **reported registry metadata**, not selected versions, lock pins, full transitive-license audits, security reviews, or proof of compatibility. Pin exact versions in the runtime repository only after source/Windows qualification.

## Runtime shape and boundaries

- One long-lived process is the sole serial/session owner and job executor; enforce a single-instance lock and explicit busy/ownership errors.
- SQLite stores bounded operations, lifecycle events, grants/references and sanitized receipts; database files, logs, ports and real device identifiers stay outside the public `adv` checkout.
- CLI and MCP call the same core. Start with stdio MCP only if/when the selected client needs it; no TCP/HTTP listener, remote tunnel, browser bridge, or network service in MVP.
- No arbitrary serial/shell command. Use named capabilities, current ADR-006/009 compatibility, explicit effects, and no implicit SD/audio/run/flash operations.
- Initial OS qualification target: Windows 11 x64. Other OSes are not claimed until independently tested.
- Proposed `adv` allowlist for later documentation work: `docs/adr/ADR-015-deviceops-host-stack-and-repository-boundary.md`, `docs/adr/INDEX.md`, `docs/deviceops/D01-DECISION.md`. Runtime code and dependency files are excluded from this repo.

## Owner decisions still required

1. Accept/reject Python + Windows 11-first + SQLite + single local executor.
2. Accept/reject the separate runtime-repository boundary and authorize naming/creation in a separate scoped task.
3. Confirm whether stdio is sufficient for first MCP client; named pipes are deferred unless multi-client requirements demand them.
4. Approve later exact dependency versions only after a clean Windows prototype, transitive license inventory and reproducible package test.

## Gates before implementation

No runtime code, dependency installation, repository creation, serial/USB, firmware, audio, flash, or network endpoint under this issue. After owner acceptance, open/activate the separately scoped implementation issue in the approved runtime repository; pin toolchain/dependencies there; build fake-only lifecycle and parity tests first. Hardware access remains a separate owner authorization and profile qualification. ADR-015 stays Proposed until explicit owner acceptance.
