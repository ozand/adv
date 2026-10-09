# Diagnostic and validation scripts

- [`consumer_validate.py`](consumer_validate.py) — read-only, deterministic Cardputer consumer-policy validator for an explicitly supplied JSON fixture/document. It reports an explicitly labelled **structural proxy**, canonical-target graph, and consumer-policy outcomes separately; the proxy is not the framework's universal validator. It does not scan repository data or perform repairs. See the accepted [consumer-validation contract](../docs/consumer-validation-contract.md) and `python -m pytest --confcutdir=tests -q -o addopts='' tests/test_consumer_validate.py`.

Reusable, bounded Cardputer-Adv diagnostics:

- [`adv_serial_rx.ps1`](adv_serial_rx.ps1) — passive serial receive only; DTR/RTS
  disabled; bounded duration and byte count; serial content is suppressed.
- [`adv_launcher_probe.py`](adv_launcher_probe.py) — bounded Launcher information
  requests restricted to source-reviewed `help`, `version`, `whoami`, and
  `partitions`; prints only validated fields; no raw serial output.
- [`adv_diagnostic_cli.py`](adv_diagnostic_cli.py) — explicit `status` / `sd_test`
  client for the ADV hardware-check JSON protocol; sanitized output, bounded I/O,
  no automatic retry. `sd_test` writes up to 64 KiB to the reserved test path.

See [Issue #2 diagnostic report](../docs/diagnostics/ISSUE-2-CARDPUTER-ADV.md) for
observations, safety boundaries, source citations, and untested hardware areas.
These scripts do not certify hardware functionality. Do not add raw serial captures,
credentials, or local tool environments to Git.
