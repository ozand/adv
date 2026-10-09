# Diagnostic scripts

Reusable, bounded Cardputer-Adv diagnostics:

- [`adv_serial_rx.ps1`](adv_serial_rx.ps1) — passive serial receive only; DTR/RTS
  disabled; bounded duration and byte count; serial content is suppressed.
- [`adv_launcher_probe.py`](adv_launcher_probe.py) — bounded Launcher information
  requests restricted to source-reviewed `help`, `version`, `whoami`, and
  `partitions`; prints only validated fields; no raw serial output.
- [`adv_diagnostic_cli.py`](adv_diagnostic_cli.py) — explicit `status` / `sd_test`
  and `run` / `result` client for the ADV hardware-check JSON protocol; sanitized
  output, bounded I/O, no automatic retry. `sd_test` writes up to 64 KiB to the
  reserved test path. Proposed Issue #43 builds add explicit `mic_test`,
  `mic_result`, `tone_test`, and `tone_result`; these require the exact audio
  proposal build marker; the detailed source/API contract is accepted in ADR-009, but runtime remains separately unauthorized.
  Audio commands are never part of `run`; no device/runtime audio test is authorized.

See [Issue #2 diagnostic report](../docs/diagnostics/ISSUE-2-CARDPUTER-ADV.md) for
observations, safety boundaries, source citations, and untested hardware areas.
These scripts do not certify hardware functionality. Do not add raw serial captures,
credentials, or local tool environments to Git.
