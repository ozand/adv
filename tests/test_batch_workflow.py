import importlib.util
from pathlib import Path

SCRIPT = Path(__file__).parents[1] / "scripts" / "batch_workflow.py"
SPEC = importlib.util.spec_from_file_location("batch_workflow", SCRIPT)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


def valid_record():
    return {
        "batch_id": "synthetic-1",
        "issue": "https://github.com/example/repo/issues/1",
        "base": "1" * 40,
        "candidate_sha": "2" * 40,
        "owner": "owner-role",
        "objective": "synthetic validation fixture",
        "writer": "writer-role",
        "inputs": [
            {"id": "a", "source": "synthetic source", "revision": "synthetic revision", "locator": "a.md", "eligibility": "eligible", "sha256": "a" * 64},
            {"id": "x", "source": "synthetic source", "revision": "synthetic revision", "locator": "x.md", "eligibility": "excluded", "reason": "synthetic exclusion"},
        ],
        "results": [{"input_id": "a", "disposition": "studied"}],
        "validation": {
            "source": {"status": "PASS"},
            "content": {"status": "PASS"},
            "retrieval": {"status": "NOT APPLICABLE"},
        },
        "gate": "PASS",
        "review": {
            "candidate_sha": "2" * 40,
            "reviewer": "review-role",
            "reviewer_role": "review-role",
            "mode": "read-only",
            "status": "PASS",
        },
        "receipt": {
            "url": "https://github.com/example/repo/issues/1#issuecomment-123",
            "issue": "https://github.com/example/repo/issues/1",
            "retention": "durable in issue record",
            "sanitized": True,
        },
        "release": {"authorized": False},
    }


def test_minimal_valid_synthetic_record_passes_structural_check():
    assert MODULE.validate(valid_record()) == []


def test_candidate_sha_change_invalidates_review_and_gate_does_not_mask_partial():
    record = valid_record()
    record["candidate_sha"] = "3" * 40
    record["validation"]["content"]["status"] = "PARTIAL"
    record["gate"] = "PASS"
    errors = MODULE.validate(record)
    assert any("does not match" in error for error in errors)
    assert any("gate must be PARTIAL" in error for error in errors)


def test_duplicate_artifact_ids_and_double_ownership_fail():
    record = valid_record()
    record["inputs"].append({"id": "a", "eligibility": "eligible"})
    record["results"].append({"input_id": "a", "disposition": "studied"})
    errors = MODULE.validate(record)
    assert any("duplicate input id" in error for error in errors)
    assert any("duplicate result ownership" in error for error in errors)


def test_eligible_missing_result_and_unresolved_coverage_fail_closed():
    record = valid_record()
    record["inputs"].append({"id": "b", "source": "synthetic", "revision": "unknown", "locator": "b.md", "eligibility": "eligible"})
    errors = MODULE.validate(record)
    assert any("eligible input missing result" in error for error in errors)


def test_unrun_required_layer_is_not_pass():
    record = valid_record()
    record["validation"]["retrieval"]["status"] = "NOT RUN"
    record["validation"]["retrieval"]["reason"] = "synthetic unrun layer"
    record["gate"] = "PARTIAL"
    assert MODULE.validate(record) == []
    record["gate"] = "PASS"
    assert any("gate must be PARTIAL" in error for error in MODULE.validate(record))


def test_explicit_release_decision_reference_and_sanitized_receipt_required():
    record = valid_record()
    record["release"] = {"authorized": True}
    record["receipt"]["sanitized"] = False
    errors = MODULE.validate(record)
    assert any("decision_ref" in error for error in errors)
    assert any("sanitized" in error for error in errors)


def test_release_requires_all_gates_and_review_to_pass():
    record = valid_record()
    record["release"] = {"authorized": True, "decision_ref": "https://github.com/example/repo/issues/1#issuecomment-9"}
    record["validation"]["content"]["status"] = "PARTIAL"
    record["gate"] = "PARTIAL"
    errors = MODULE.validate(record)
    assert any("aggregate gate" in error for error in errors)


def test_invalid_hash_or_unknown_layer_is_rejected():
    record = valid_record()
    record["inputs"][0]["sha256"] = "not-a-hash"
    record["validation"]["mystery"] = {"status": "PASS"}
    errors = MODULE.validate(record)
    assert any("sha256" in error for error in errors)
    assert any("exactly source, content, retrieval" in error for error in errors)
