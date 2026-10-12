# D01 — Host stack and repository decision

**Status:** Owner-approved architecture choices; no runtime/device authorization. Issue [#68](https://github.com/ozand/adv/issues/68). Decision records: [ADR-015](../adr/ADR-015-deviceops-host-stack-and-repository-boundary.md) (host language), [ADR-016](../adr/ADR-016-deviceops-single-executor-and-local-ipc.md) (shared executor/IPC), and [ADR-017](../adr/ADR-017-deviceops-runtime-repository-boundary.md) (repository boundary). Inputs: [architecture](ARCHITECTURE.md), [contracts](CONTRACTS.md), [roadmap](ROADMAP.md), Issues [#37](https://github.com/ozand/adv/issues/37) and [#38](https://github.com/ozand/adv/issues/38).

## Recommendation

Owner-approved: Python 3.11+ host core, Windows 11 x64 first; one persistent executor with authenticated Windows named-pipe IPC; SQLite local durable store; separate private runtime repo `ozand/deviceops` at `T:/Code/esp32/deviceops`. Path allowlist: `deviceops/`, `tests/`, `docs/`, root manifests/locks. ADR-015–017 record the decisions. Repository bootstrap commit `e56fd6a628a6bd7137b4adb48b8c646f7674263d` contains governance/readme/project-manifest skeleton only, not a runtime core. Architecture approval does not authorize device, USB/COM, firmware, audio, flash, network exposure, package publication or deployment.

The architecture choices are **owner-confirmed**; runtime compatibility remains to qualify. Python reuse has a concrete source basis: PR #82 candidate `196d2f915e0fa2424b707f3fd30d873050a3b022` contains a standard-library protocol validator plus fake-serial tests. That does not make the CLI a service or prove Windows packaging/serial behavior.

## Stack comparison

| Candidate | Reuse / MCP / serial | Windows and packaging | Cost / risk | Disposition |
|---|---|---|---|---|
| CPython 3.11+ (local measured runtime: 3.11.9 x64) | Existing ADV CLI/tests; pyserial; official MCP Python SDK | Windows 11 x64 approved first; packaging not yet qualified | Dynamic typing; distribution and migrations need ownership | Owner-approved minor line; exact patch/build channel follows standard support policy |
| TypeScript / Node | Official MCP TypeScript SDK; serialport bindings | SDK metadata requires Node >=18; serialport 13 requires Node >=20 and native binding packaging qualification | Native dependencies and larger deployment footprint | Viable alternative; no reuse advantage in current repo |
| Rust | Strong static typing and single-binary potential; serial/MCP crates need pinned review | Potentially good Windows artifact, but cross-build/signing/install workflow unverified | Rewrite existing Python protocol behavior; more initial integration work | Do not infer host language from firmware preference |

**reported — package registry records, checked 2026-10-12 (not primary-source qualification):**

| Candidate | Exact artifact / version | Registry SHA-256 | License metadata |
|---|---|---|---|
| pyserial | `pyserial-3.5-py2.py3-none-any.whl` | `c4451db6ba391ca6ca299fb3ec7bae67a5c55dde170964c7a14ceefec02f2cf0` | BSD |
| Python MCP SDK | `mcp-2.3.0-py3-none-any.whl` | `dd0c44c089d16453e8ae31a3877a0054d7a2314caaa81f5e0541b9b1734b2377` | MIT |
| pytest | `pytest-8.4.2-py3-none-any.whl` | `872f880de3fc3a5bdc88a11b39c9710c3497a547cfa9320bc3c5e62fbf272e79` | MIT |

Registry records: [pyserial 3.5](https://pypi.org/project/pyserial/3.5/), [MCP SDK 2.3.0](https://pypi.org/project/mcp/2.3.0/), [pytest 8.4.2](https://pypi.org/project/pytest/8.4.2/). Primary project sources for later verification: [pyserial](https://github.com/pyserial/pyserial/tree/v3.5), [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk/tree/v2.3.0), [pytest](https://github.com/pytest-dev/pytest/tree/8.4.2). Local measurement: CPython 3.11.9 x64 and standard-library SQLite 3.45.1 are available; this shows the host can run an offline bootstrap, not device or clean-install qualification. SQLite uses Python's standard-library `sqlite3`; no external SQLite package.

TypeScript comparison records: `@modelcontextprotocol/sdk@1.32.1` (MIT, npm integrity `sha512-2DdE+SJDtzLEEWzY1ZjY7Q+VcPhcV1KisD3zI4u0XZyktsjHum1mwbMI+JaulUBi2OZk+KJAi2uPXzxichPkdw==`) and `serialport@13.0.0` (MIT, npm integrity `sha512-PHpnTd8isMGPfFTZNCzOZp9m4mAJSNWle9Jxu6BPTcWq7YXl5qN7tp8Sgn0h+WIGcD6JFz5QDgixC2s4VW7vzg==`). These are versioned comparison candidates, not selected pins. Confirm source tags, Python version support, Windows behavior, wheel/sdist licensing, all transitive licenses and vulnerability status in a later governed implementation task before adopting any dependency. No packages were installed.

## Local MVP operational constraints

- Offline/fake MVP requires no device, USB/COM, network, tunnel, browser, firmware, audio, SD or flash. Untrusted PR/build work has no USB/production-secret access (SECURITY.md); hardware execution is a separate allowlisted runner/gate.
- Firmware/deployment failure recovery and recovery capability are profile-specific; unverified firmware does not trigger automatic reflash. A runtime repository/path choice does not grant hardware/recovery authorization.
- Web-chat/client acceptance starts on fake device before separately authorized remote/account/network exposure (VALIDATION G2).
- No arbitrary serial/shell command. Use named capabilities, current ADR-006/009 compatibility, explicit effects, and no implicit SD/audio/run/flash operations.
- Initial OS qualification target recommendation: Windows 11 x64; other OSes are not claimed until tested.
- `adv` is proposed to remain documentation/coordination only (ADR-017); the owner must approve the destination and exact path allowlist separately.

## Issue #68 acceptance coverage

1. **Stack, dependencies, licenses, versions/SHA, OS, rationale — architecture accepted; qualification partial.** Owner accepted Python 3.11+ / Windows 11 x64 first, persistent executor/named-pipe IPC, SQLite and private repo/path. Registry candidate metadata is documented; no SHA-locked package selection, primary-source qualification, Windows packaging validation or complete transitive-license audit is claimed.
2. **Owner acceptance / ADR status — satisfied.** Owner confirmation is recorded in Issue #68 comment [6130478169](https://github.com/ozand/adv/issues/68#issuecomment-6130478169): Python 3.11+ and Windows 11 x64 first; persistent executor with authenticated Windows named-pipe IPC; SQLite local durable state; private `ozand/deviceops` and approved path allowlist. ADR-015/016/017 are Accepted. This is architecture acceptance only.
3. **Implementation location and path allowlist — satisfied for bootstrap.** Private `ozand/deviceops`, local clone `T:/Code/esp32/deviceops`, and `/deviceops/`, `/tests/`, `/docs/`, root manifests/locks are owner-approved. Bootstrap commit `e56fd6a628a6bd7137b4adb48b8c646f7674263b` is limited to root governance/readme/manifest; runtime implementation still requires a scoped issue.
4. **#37/#38 inputs — reviewed, not completed/transferred.** #37 requires bounded transport-neutral operations, effects/authority and honest uncertainty/retry while preserving ADR-006; its stage-A evidence dependency remains. #38 requires evidence-linked concrete scenarios compared consistently across host/device/hybrid, and forbids an unsupported selection; its scenario evidence remains. These are input constraints, not completed deliverables, and both issues stay open.
5. **Future source-task gates — documented.** G0 decision/path/version gates, G1 fake-only offline conformance, G2 client integration on fake device, G3 separate connect/status authorization and G4 per-effect authorization/recovery gates are defined in VALIDATION.md; this decision record does not itself authorize implementation or hardware access.

## Qualification questions

These questions remain for runtime qualification or future design review; they do not undo owner acceptance of the four D01 choices:

1. The supported host is not Windows 11 x64, or CPython cannot be distributed through the owner's approved local deployment channel.
2. Reusing the existing Python protocol validator/tests is less valuable than a typed Rust/Node client that already exists in the intended runtime repository.
3. A persistent named-pipe server cannot be reliably supervised as the only session/job owner, or the security boundary cannot restrict clients to the intended local principal.
4. SQLite's locking, durability, migration, retention or backup behavior cannot meet the bounded job/evidence requirements without replaying uncertain device effects.
5. A different repo owner/visibility/publication lifecycle is required, or a separate `ozand/deviceops` repo would conflict with established ownership.
6. Offline CI cannot isolate untrusted PR builds from USB and production secrets while still validating the proposed core.
7. The intended web-chat/MCP client cannot use local IPC via the approved host integration, requiring a remote endpoint in the initial MVP.
8. A firmware/profile recovery path cannot be qualified independently, making the proposed staged fake-first then separately authorized hardware sequence unsafe or circular.

These are decision falsifiers, not claims that the conditions have been tested.

## Gates after architecture acceptance

This acceptance and repository bootstrap do not authorize runtime core under Issue #68, package installation, serial/USB, firmware, audio, flash, network endpoint, publication or deployment. Open/activate the separately scoped implementation issue in the approved runtime repository; qualify/pin the selected toolchain/dependencies there; build fake-only lifecycle and parity tests first. Hardware access remains separately authorized per effect and profile. ADR-015–017 are Accepted; implementation and operational qualification remain open.
