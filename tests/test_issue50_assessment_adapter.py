"""Durable negative/positive coverage for the Issue #50 assessment adapter."""
from __future__ import annotations

import importlib.util
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
ADAPTER_PATH = ROOT / "docs" / "issue50" / "validate-candidate.py"
SPEC = importlib.util.spec_from_file_location("issue50_validate_candidate", ADAPTER_PATH)
assert SPEC and SPEC.loader
ADAPTER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(ADAPTER)


@pytest.mark.parametrize("field", ["outcome", "limitations", "review decisions"])
@pytest.mark.parametrize("value", ["", "   ", "\t\n"])
def test_required_assessment_fields_reject_empty_or_whitespace(field, value):
    with pytest.raises(ValueError, match="blank required assessment field"):
        ADAPTER.validate_required_receipt_fields(
            ("https://example.test/source", "a" * 40, "lines 1-2", value, "nonempty limitation", "nonempty decision", "kb/wiki/concepts/example.md")
        )


def test_actual_assessment_receipt_maps_exact_four_sources_and_targets():
    receipts, _ = ADAPTER.parse_receipt()
    assert len(receipts) == 4
    assert set(receipt["target"] for receipt in receipts.values()) == {
        "kb/wiki/concepts/incremental-multiline-repl-assembly.md",
        "kb/wiki/concepts/sd-initialization-frequency-retry.md",
        "kb/wiki/concepts/expression-evaluator-pipeline.md",
        "kb/wiki/concepts/cooperative-script-loop-budget.md",
    }
    assert all(receipt["outcome"].strip() for receipt in receipts.values())
    assert all(receipt["limitations"].strip() for receipt in receipts.values())
    assert all(receipt["review_decisions"].strip() for receipt in receipts.values())


def test_receipt_lookup_rejects_wrong_revision_or_locator():
    receipts, _ = ADAPTER.parse_receipt()
    key = next(iter(receipts))
    source, revision, locator = key
    assert (source, "0" * 40, locator) not in receipts
    assert (source, revision, "wrong locator") not in receipts
    assert receipts[key]["target"].startswith("kb/wiki/concepts/")
