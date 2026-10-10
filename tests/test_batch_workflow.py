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
            {"id": "b", "source": "synthetic source", "revision": "synthetic revision", "locator": "b.md", "eligibility": "eligible"},
            {"id": "c", "source": "synthetic source", "revision": "synthetic revision", "locator": "c.md", "eligibility": "eligible"},
            {"id": "d", "source": "synthetic source", "revision": "synthetic revision", "locator": "d.md", "eligibility": "eligible"},
            {"id": "e", "source": "synthetic source", "revision": "synthetic revision", "locator": "e.md", "eligibility": "eligible"},
            {"id": "x", "source": "synthetic source", "revision": "synthetic revision", "locator": "x.md", "eligibility": "excluded", "reason": "synthetic exclusion"},
        ],
        "results": [
            {"input_id": "a", "disposition": "studied", "assessment": {"scope": "synthetic scope", "date": "2026-01-01", "reviewer": "fixture", "outcome": "claims reviewed", "limitations": "synthetic"}},
            {"input_id": "b", "disposition": "deferred", "reason": "synthetic defer"},
            {"input_id": "c", "disposition": "synthesized", "assessment": {"scope": "synthetic scope", "date": "2026-01-01", "reviewer": "fixture", "outcome": "claim represented", "limitations": "synthetic"}, "targets": ["kb/wiki/entities/example.md"], "claim_provenance": [{"source": "synthetic source", "revision": "synthetic revision", "locator": "c.md#claim"}]},
            {"input_id": "d", "disposition": "unresolved", "reason": "synthetic access outcome unresolved"},
            {"input_id": "e", "disposition": "not_assessed"},
        ],
        "validation": {
            "source": {"status": "PASS", "required": True},
            "content": {"status": "PASS", "required": True},
            "retrieval": {"status": "NOT APPLICABLE", "required": False, "precondition": "No retrieval requested", "reason": "Outside batch scope"},
        },
        "gate": "PARTIAL",
        "review": {
            "candidate_sha": "2" * 40,
            "reviewer": "independent-reviewer",
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
    record = valid_record()
    record["results"] = record["results"][:1]
    for input_id in ("b", "c", "d", "e"):
        record["inputs"] = [row for row in record["inputs"] if row["id"] != input_id]
    record["gate"] = "PASS"
    assert MODULE.validate(record) == []


def test_all_contract_dispositions_have_minimal_valid_evidence():
    assert MODULE.validate(valid_record()) == []


def test_candidate_sha_change_invalidates_review_and_gate_does_not_mask_partial():
    record = valid_record()
    record["candidate_sha"] = "3" * 40
    record["validation"]["content"]["status"] = "PARTIAL"
    record["gate"] = "PASS"
    errors = MODULE.validate(record)
    assert any("does not match" in error for error in errors)
    assert any("gate must be PARTIAL" in error for error in errors)


def test_all_dispositions_require_their_contract_evidence():
    record = valid_record()
    results = record["results"]
    results[1].pop("reason")
    results[2].pop("targets")
    results[2].pop("claim_provenance")
    results[3].pop("reason")
    errors = MODULE.validate(record)
    assert any("deferred disposition requires a reason" in error for error in errors)
    assert any("synthesized disposition requires target relations" in error for error in errors)
    assert any("synthesized disposition requires claim/source provenance" in error for error in errors)
    assert any("unresolved disposition requires a reason" in error for error in errors)


def test_duplicate_artifact_ids_and_double_ownership_fail():
    record = valid_record()
    record["inputs"].append({"id": "a", "eligibility": "eligible"})
    record["results"].append({"input_id": "a", "disposition": "studied"})
    errors = MODULE.validate(record)
    assert any("duplicate input id" in error for error in errors)
    assert any("duplicate result ownership" in error for error in errors)


def test_unresolved_eligibility_cannot_be_assessed_without_new_resolved_record():
    record = valid_record()
    record["inputs"].append({"id": "unknown", "source": "synthetic", "revision": "unknown", "locator": "?", "eligibility": "unresolved", "reason": "identity not frozen"})
    record["results"].append({"input_id": "unknown", "disposition": "studied", "assessment": {"scope": "synthetic", "date": "2026-01-01", "reviewer": "fixture", "outcome": "claim reviewed", "limitations": "synthetic"}})
    errors = MODULE.validate(record)
    assert any("cannot receive assessed disposition" in error for error in errors)


def test_unresolved_eligibility_requires_a_result_and_reason():
    record = valid_record()
    record["inputs"].append({"id": "unknown", "source": "synthetic", "revision": "unknown", "locator": "?", "eligibility": "unresolved", "reason": "identity not frozen"})
    record["results"].append({"input_id": "unknown", "disposition": "unresolved", "reason": "identity unresolved"})
    record["gate"] = "PARTIAL"
    assert MODULE.validate(record) == []
    record["results"].pop()
    assert any("remain visible as unresolved" in error for error in MODULE.validate(record))
    record["results"].append({"input_id": "unknown", "disposition": "unresolved", "reason": "identity unresolved"})
    record["gate"] = "PASS"
    assert any("gate must be PARTIAL" in error for error in MODULE.validate(record))


def test_eligible_missing_result_and_unresolved_coverage_fail_closed():
    record = valid_record()
    record["inputs"].append({"id": "b", "source": "synthetic", "revision": "unknown", "locator": "b.md", "eligibility": "eligible"})
    record["results"] = [record["results"][0]]
    errors = MODULE.validate(record)
    assert any("eligible input missing result" in error for error in errors)


def test_not_applicable_requires_declared_exclusion_precondition():
    record = valid_record()
    record["validation"]["retrieval"] = {"status": "NOT APPLICABLE", "required": False}
    assert any("precondition" in error for error in MODULE.validate(record))
    record["validation"]["retrieval"] = {
        "status": "NOT APPLICABLE", "required": False,
        "precondition": "Batch has no retrieval/index objective",
        "reason": "No retrieval operation is in scope",
    }
    record["gate"] = "PARTIAL"
    assert MODULE.validate(record) == []
    record["validation"]["retrieval"]["precondition"] = ""
    assert any("precondition" in error for error in MODULE.validate(record))


def test_eligible_unresolved_result_forces_partial_gate():
    record = valid_record()
    record["results"][0] = {"input_id": "a", "disposition": "unresolved", "reason": "synthetic access unresolved"}
    record["gate"] = "PASS"
    assert any("gate must be PARTIAL" in error for error in MODULE.validate(record))


def test_all_layers_not_applicable_cannot_be_a_pass_or_authorize_release():
    record = valid_record()
    for name in ("source", "content", "retrieval"):
        record["validation"][name] = {
            "status": "NOT APPLICABLE", "required": False,
            "precondition": f"Synthetic exclusion for {name}", "reason": "Not required",
        }
    record["gate"] = "PASS"
    assert any("NOT CHECKED" in error for error in MODULE.validate(record))
    record["gate"] = "NOT CHECKED"
    record["release"] = {"authorized": True, "decision_ref": "https://github.com/example/repo/issues/1#issuecomment-123"}
    errors = MODULE.validate(record)
    assert any("no validation layer is required" in error for error in errors)


def test_required_layer_cannot_be_not_applicable():
    record = valid_record()
    record["validation"]["content"] = {
        "status": "NOT APPLICABLE", "required": True,
        "precondition": "Claimed exclusion", "reason": "Synthetic",
    }
    record["gate"] = "PARTIAL"
    assert any("required=false" in error for error in MODULE.validate(record))


def test_unrun_required_layer_is_not_pass():
    record = valid_record()
    record["validation"]["retrieval"]["status"] = "NOT RUN"
    record["validation"]["retrieval"]["required"] = True
    record["validation"]["retrieval"].pop("precondition")
    record["validation"]["retrieval"]["reason"] = "synthetic unrun layer"
    record["gate"] = "PARTIAL"
    assert MODULE.validate(record) == []
    record["gate"] = "PASS"
    assert any("gate must be PARTIAL" in error for error in MODULE.validate(record))


def test_excluded_input_stays_outside_results_partition():
    record = valid_record()
    record["results"].append({"input_id": "x", "disposition": "not_assessed"})
    assert any("excluded input must remain outside results" in error for error in MODULE.validate(record))


def test_receipt_must_belong_to_governing_issue():
    record = valid_record()
    record["receipt"]["url"] = "https://github.com/another/repo/issues/99#issuecomment-123"
    assert any("receipt URL must belong" in error for error in MODULE.validate(record))


def test_duplicate_reviewer_identity_is_rejected():
    record = valid_record()
    record["review"]["reviewer"] = record["writer"]
    errors = MODULE.validate(record)
    assert any("reviewer identity must differ" in error for error in errors)


def test_malformed_result_id_is_reported_without_type_error():
    record = valid_record()
    record["results"][0]["input_id"] = ["not", "hashable"]
    errors = MODULE.validate(record)
    assert any("input_id must be a declared non-empty string" in error for error in errors)


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
