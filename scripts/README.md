# Diagnostic and validation scripts

- [`consumer_validate.py`](consumer_validate.py) — read-only, deterministic Cardputer consumer-policy validator for an explicitly supplied JSON fixture/document. It reports an explicitly labelled **structural proxy**, canonical-target graph, and consumer-policy outcomes separately; the proxy is not the framework's universal validator. It does not scan repository data or perform repairs. To compose pinned universal checks, pass both `--kb-bootstrap-source` (clean checkout at ADR-012 commit `73277fdb3e54184901f67268bc676a562b0a677a`) and `--kb-python` (qualified interpreter); source revision and module import are verified before invocation. Without both options, universal output is only the limited structural proxy. See the accepted [consumer-validation contract](../docs/consumer-validation-contract.md) and `python -m pytest --confcutdir=tests -q -o addopts='' tests/test_consumer_validate.py`.

- [`batch_workflow.py`](batch_workflow.py) — read-only structural checker for an explicitly supplied batch JSON record. Run `python scripts/batch_workflow.py docs/batch-record.example.json`; it checks field shapes, unique input/result ownership, unresolved-eligibility handling, exact candidate/review SHA linkage, explicit per-layer applicability and gate consistency, and an explicit release-decision field. Exit 0 means structural consistency only: it does not authenticate human approvals, reviewer identity, source integrity, truth/rights, or publish content. See the accepted [bounded-batch workflow](../docs/bounded-batch-knowledge-workflow.md), [ADR-013](../docs/adr/ADR-013-define-bounded-batch-knowledge-workflow.md), and focused synthetic tests.

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
