# D01 — Host stack and repository decision proposal

**Status:** Proposal for owner decision; not implementation authorization. Issue [#68](https://github.com/ozand/adv/issues/68). Decision records: [ADR-015](../adr/ADR-015-deviceops-host-stack-and-repository-boundary.md) (host language), [ADR-016](../adr/ADR-016-deviceops-single-executor-and-local-ipc.md) (shared executor/IPC), and [ADR-017](../adr/ADR-017-deviceops-runtime-repository-boundary.md) (repository boundary). Inputs: [architecture](ARCHITECTURE.md), [contracts](CONTRACTS.md), [roadmap](ROADMAP.md), Issues [#37](https://github.com/ozand/adv/issues/37) and [#38](https://github.com/ozand/adv/issues/38).

## Recommendation

Recommendation: Python 3.11+ host core, Windows 11 x64 first qualification target. Process lifecycle and real local IPC are proposed separately in ADR-016; repository location and publication boundary are separate in ADR-017. SQLite/storage details remain an open D02/D04 implementation decision, not selected here. MCP/CLI must share the one executor if both are enabled; stdio-only independent frontend processes are insufficient. No listener, runtime repository creation or implementation is authorized.

This recommendation is **theory**, not a measured compatibility result. Python reuse has a concrete source basis: PR #82 candidate `196d2f915e0fa2424b707f3fd30d873050a3b022` contains a standard-library protocol validator plus fake-serial tests. That does not make the CLI a service or prove Windows packaging/serial behavior.

## Stack comparison

| Candidate | Reuse / MCP / serial | Windows and packaging | Cost / risk | Disposition |
|---|---|---|---|---|
| Python 3.11+ | Existing ADV CLI/tests; pyserial; official MCP Python SDK | Windows support and single-folder packaging require prototype qualification; straightforward script/test workflow | Dynamic typing; distribution and migrations need ownership | Recommended for reuse-first MVP |
| TypeScript / Node | Official MCP TypeScript SDK; serialport bindings | SDK metadata requires Node >=18; serialport 13 requires Node >=20 and native binding packaging qualification | Native dependencies and larger deployment footprint | Viable alternative; no reuse advantage in current repo |
| Rust | Strong static typing and single-binary potential; serial/MCP crates need pinned review | Potentially good Windows artifact, but cross-build/signing/install workflow unverified | Rewrite existing Python protocol behavior; more initial integration work | Do not infer host language from firmware preference |

Registry metadata snapshot checked 2026-10-12 (**reported**): pyserial 3.5, SHA256 `c4451db6ba391ca6ca299fb3ec7bae67a5c55dde170964c7a14ceefec02f2cf0`; MCP Python SDK 2.3.0, SHA256 `dd0c44c089d16453e8ae31a3877a0054d7a2314caaa81f5e0541b9b1734b237`; pytest 8.4.2, SHA256 `872f880de3fc3a5bdc88a11b39c9710c3497a547cfa9320bc3c5e62fbf272e79`; each is registry artifact metadata, not a selected runtime pin. MCP TypeScript SDK 1.32.1 and serialport 13.0.0 metadata report MIT, with npm integrity hashes `sha512-2DdE+SJDtzLEEWzY1ZjY7Q+VcPhcV1KisD3zI4u0XZyktsjHum1mwbMI+JaulUBi2OZk+KJAi2uPXzxichPkdw==` and `sha512-PHpnTd8isMGPfFTZNCzOZp9m4mAJSNWle9Jxu6BPTcWq7YXl5qN7tp8Sgn0h+WIGcD6JFz5QDgixC2s4VW7vzg==`. None is a chosen dependency; primary-source review, Windows qualification and complete transitive-license/security audit remain outstanding.

## Runtime constraints to carry forward

- One persistent executor owns the serial/session and job lifecycle; CLI and MCP reach that same process through authenticated local IPC. See Proposed ADR-016; the concrete IPC mechanism remains open pending Windows qualification.
- Storage must persist bounded operations without replaying uncertain effects; the exact store/schema remains open for D02/D04.
- No TCP/HTTP listener, remote tunnel, browser bridge, or network service in the local MVP.
- No arbitrary serial/shell command. Use named capabilities, current ADR-006/009 compatibility, explicit effects, and no implicit SD/audio/run/flash operations.
- Initial OS qualification target recommendation: Windows 11 x64; other OSes are not claimed until tested.
- `adv` is proposed to remain documentation/coordination only (ADR-017); the owner must approve the destination and exact path allowlist separately.

## Issue #68 acceptance coverage

1. **Stack, dependencies, licenses, versions/SHA, OS, rationale — partial.** Language/OS recommendation and registry metadata are documented; no SHA-locked package selection, primary-source qualification, or complete transitive license audit is claimed.
2. **Owner acceptance / ADR status — unmet.** ADR-015/016/017 remain Proposed; owner must accept/reject or revise them.
3. **Implementation location and path allowlist — proposed, not accepted.** ADR-017 keeps runtime outside `adv`, but no destination repository identity or exact future runtime allowlist exists yet.
4. **#37/#38 inputs — reviewed, not completed/transferred.** Their constraints are cited here; #37's stage-A evidence dependency and #38's scenario evidence/comparison criteria remain upstream work. These issues stay open.
5. **Future source-task gates — documented.** Fake-only prototype and separately authorized hardware gates are stated; this does not clear a source issue to start before owner acceptance.

## Gates before implementation

No runtime code, dependency installation, repository creation, serial/USB, firmware, audio, flash, or network endpoint under this issue. After owner acceptance, open/activate the separately scoped implementation issue in the approved runtime repository; pin toolchain/dependencies there; build fake-only lifecycle and parity tests first. Hardware access remains a separate owner authorization and profile qualification. ADR-015 stays Proposed until explicit owner acceptance.
