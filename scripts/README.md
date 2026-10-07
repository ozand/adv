# Diagnostic scripts

Reusable, bounded Cardputer-Adv diagnostics:

- [`adv_serial_rx.ps1`](adv_serial_rx.ps1) — passive serial receive only; DTR/RTS
  disabled; bounded duration and byte count; does not save raw output.
- [`adv_launcher_probe.py`](adv_launcher_probe.py) — bounded Launcher information
  requests restricted to source-reviewed `help`, `version`, `whoami`, and
  `partitions`; no reset or persistence command.

See [Issue #2 diagnostic report](../docs/diagnostics/ISSUE-2-CARDPUTER-ADV.md) for
observations, safety boundaries, source citations, and untested hardware areas.
These scripts do not certify hardware functionality. Do not add raw serial captures,
credentials, or local tool environments to Git.
