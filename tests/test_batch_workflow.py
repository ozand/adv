import importlib.util
import json
import subprocess
import sys
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
            {"id": "a", "source": "https://example.test/source", "revision": "synthetic revision", "locator": "a.md", "eligibility": "eligible", "sha256": "a" * 64},
            {"id": "b", "source": "synthetic source", "revision": "synthetic revision", "locator": "b.md", "eligibility": "eligible"},
            {"id": "c", "source": "https://example.test/source", "revision": "synthetic revision", "locator": "c.md", "eligibility": "eligible"},
            {"id": "d", "source": "synthetic source", "revision": "synthetic revision", "locator": "d.md", "eligibility": "eligible"},
            {"id": "e", "source": "synthetic source", "revision": "synthetic revision", "locator": "e.md", "eligibility": "eligible"},
            {"id": "x", "source": "synthetic source", "revision": "synthetic revision", "locator": "x.md", "eligibility": "excluded", "reason": "synthetic exclusion"},
        ],
        "results": [
            {"input_id": "a", "disposition": "studied", "assessment": {"scope": "synthetic scope", "date": "2026-01-01", "reviewer": "fixture", "outcome": "claims reviewed", "limitations": "synthetic"}},
            {"input_id": "b", "disposition": "deferred", "reason": "synthetic defer"},
            {"input_id": "c", "disposition": "synthesized", "assessment": {"scope": "synthetic scope", "date": "2026-01-01", "reviewer": "fixture", "outcome": "claim represented", "limitations": "synthetic"}, "targets": ["kb/wiki/entities/example.md"], "claim_provenance": [{"source": "https://example.test/source", "revision": "synthetic revision", "locator": "c.md#claim", "claim": "synthetic claim"}]},

            {"input_id": "d", "disposition": "unresolved", "reason": "synthetic access outcome unresolved"},
            {"input_id": "e", "disposition": "not_assessed"},
        ],
        "validation": {
            "source": {"status": "PASS", "required": True, "command": "synthetic command", "tool": "synthetic tool", "version": "1", "input_snapshot": "synthetic snapshot", "exit_code": 0, "limitations": "synthetic only"},
            "content": {"status": "PASS", "required": True, "command": "synthetic command", "tool": "synthetic tool", "version": "1", "input_snapshot": "synthetic snapshot", "exit_code": 0, "limitations": "synthetic only"},
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


def test_pr_receipt_pointer_is_allowed_for_same_repository():
    record = valid_record()
    record["receipt"]["url"] = "https://github.com/example/repo/pull/77#issuecomment-8"
    assert MODULE.validate(record) == []


def test_actual_github_discussion_anchor_is_allowed():
    record = valid_record()
    record["receipt"]["url"] = "https://github.com/example/repo/pull/77#discussion_r123"
    assert MODULE.validate(record) == []


def test_receipt_issue_url_rejects_owner_delimiter():
    record = valid_record()
    record["issue"] = "https://github.com/acme?x/repo/issues/1"
    record["receipt"]["issue"] = record["issue"]
    record["receipt"]["url"] = record["issue"] + "#issuecomment-1"
    assert any("canonical GitHub Issue" in error for error in MODULE.validate(record))


def test_malformed_enum_types_return_structural_errors():
    cases = [
        ("inputs", 0, "eligibility", []),
        ("inputs", 0, "eligibility", {}),
        ("inputs", 0, "eligibility", None),
        ("results", 0, "disposition", []),
        ("results", 0, "disposition", {}),
        ("results", 0, "disposition", None),
        ("validation", "source", "status", []),
        ("validation", "source", "status", {}),
        ("validation", "source", "status", None),
        ("review", None, "status", []),
        ("review", None, "status", {}),
        ("review", None, "status", None),
    ]
    for section, index, field, value in cases:
        record = valid_record()
        if index is None:
            record[section][field] = value
        else:
            record[section][index][field] = value
        assert MODULE.validate(record), (section, field, value)


def test_duplicate_github_repo_source_identity_is_rejected():
    record = valid_record()
    record["inputs"][1].update(source="https://github.com/Example/Repo.git", revision="r1", locator="README.md")
    record["inputs"][2].update(source="https://github.com/example/repo", revision="r1", locator="README.md")
    assert any("duplicates source-artifact identity" in error for error in MODULE.validate(record))


def test_github_forks_remain_distinct_source_identities():
    record = valid_record()
    record["inputs"][1].update(source="https://github.com/owner-a/repo", revision="r1", locator="README.md")
    record["inputs"][2].update(source="https://github.com/owner-b/repo", revision="r1", locator="README.md")
    assert not any("duplicates source-artifact identity" in error for error in MODULE.validate(record))


def test_provenance_source_identity_uses_same_github_canonicalization():
    record = valid_record()
    row = next(item for item in record["results"] if item["input_id"] == "c")
    row["claim_provenance"][0]["source"] = "https://GitHub.com/Example/Repo.git"
    record["inputs"][2]["source"] = "https://github.com/example/repo"
    assert not any("provenance must reference its source artifact" in error for error in MODULE.validate(record))


def test_cli_duplicate_json_keys_are_bounded_error_without_traceback(tmp_path):
    path = tmp_path / "duplicate-key.json"
    path.write_text('{"candidate_sha":"' + "2" * 40 + '","candidate_sha":"' + "3" * 40 + '"}', encoding="utf-8")
    proc = subprocess.run(
        [sys.executable, str(SCRIPT), str(path)], capture_output=True, text=True, check=False,
    )
    assert proc.returncode == 2
    assert "duplicate JSON key: candidate_sha" in proc.stderr
    assert "Traceback" not in proc.stderr


def test_cli_invalid_utf8_is_bounded_error_without_traceback(tmp_path):
    path = tmp_path / "invalid-utf8.json"
    path.write_bytes(bytes([0xFF]))
    proc = subprocess.run(
        [sys.executable, str(SCRIPT), str(path)], capture_output=True, text=True, check=False,
    )
    assert proc.returncode == 2
    assert "ERROR: cannot read JSON record" in proc.stderr
    assert "Traceback" not in proc.stderr


def test_cli_malformed_enum_types_fail_deterministically(tmp_path):
    cases = (
        ("inputs", "eligibility", []),
        ("results", "disposition", {}),
        ("validation", "status", []),
        ("review", "status", {}),
    )
    for section, field, value in cases:
        record = valid_record()
        if section == "validation":
            record[section]["source"][field] = value
        elif section in {"inputs", "results"}:
            record[section][0][field] = value
        else:
            record[section][field] = value
        path = tmp_path / f"{section}.json"
        path.write_text(json.dumps(record), encoding="utf-8")
        proc = subprocess.run(
            [sys.executable, str(SCRIPT), str(path)],
            capture_output=True, text=True, check=False,
        )
        assert proc.returncode == 1
        assert "RESULT: FAIL" in proc.stdout
        assert "Traceback" not in proc.stderr


def test_unhashable_input_id_returns_structural_failure_without_traceback(tmp_path):
    record = valid_record()
    record["inputs"][0]["id"] = []
    path = tmp_path / "unhashable-input-id.json"
    path.write_text(json.dumps(record), encoding="utf-8")
    proc = subprocess.run(
        [sys.executable, str(SCRIPT), str(path)], capture_output=True, text=True, check=False,
    )
    assert proc.returncode == 1
    assert "RESULT: FAIL" in proc.stdout
    assert "Traceback" not in proc.stderr
    assert MODULE.validate(record)


def test_non_string_reasons_are_rejected():
    cases = [
        ("input", "unresolved", None),
        ("input", "unresolved", []),
        ("input", "excluded", []),
        ("result", "deferred", None),
        ("result", "deferred", {}),
        ("result", "unresolved", {}),
    ]
    for section, state, reason in cases:
        record = valid_record()
        if section == "input":
            row = record["inputs"][0]
            row["eligibility"] = state
            row["reason"] = reason
        else:
            row = record["results"][0]
            row["disposition"] = state
            row["reason"] = reason
        assert MODULE.validate(record), (section, state, reason)


def test_governing_issue_url_rejects_query_delimiter_components():
    record = valid_record()
    record["issue"] = "https://github.com/acme?x/repo/issues/1"
    assert any("canonical GitHub Issue" in error for error in MODULE.validate(record))
    record = valid_record()
    record["issue"] = "https://github.com/acme/repo/issues/1?x=1"
    assert any("canonical GitHub Issue" in error for error in MODULE.validate(record))


def test_duplicate_source_artifact_identity_is_rejected_but_distinct_revision_is_allowed():
    record = valid_record()
    duplicate = dict(record["inputs"][0], id="duplicate-id")
    record["inputs"].append(duplicate)
    record["results"].append({"input_id": "duplicate-id", "disposition": "not_assessed"})
    errors = MODULE.validate(record)
    assert any("duplicates source-artifact identity" in error for error in errors)
    distinct = valid_record()
    distinct["inputs"][1] = dict(distinct["inputs"][0], id="revision-two", revision="different revision")
    distinct["results"].append({"input_id": "revision-two", "disposition": "studied", "assessment": {"scope": "synthetic", "date": "2026-01-01", "reviewer": "fixture", "outcome": "claims reviewed", "limitations": "synthetic"}})
    distinct["inputs"] = [row for row in distinct["inputs"] if row["id"] in {"a", "revision-two"}]
    distinct["results"] = [row for row in distinct["results"] if row["input_id"] in {"a", "revision-two"}]
    distinct["gate"] = "PASS"
    assert MODULE.validate(distinct) == []


def test_synthesized_target_must_be_internal_canonical_path():
    for target in ("https://example.com/x", "../../outside.md", "kb/wiki/../private.md", r"kb/wiki\\private.md", "kb/wiki/%2e%2e/out.md"):
        record = valid_record()
        row = next(item for item in record["results"] if item["input_id"] == "c")
        row["disposition"] = "synthesized"
        row["targets"] = [target]
        row["claim_provenance"] = [{"source": "https://example.test/source", "revision": "synthetic revision", "locator": "c.md#claim", "claim": "claim-a"}]
        assert any("canonical internal target" in error for error in MODULE.validate(record)), target


def test_provenance_for_different_source_and_revision_does_not_count_for_input():
    record = valid_record()
    row = next(item for item in record["results"] if item["input_id"] == "c")
    row["claim_provenance"] = [{"source": "https://foreign.example/source", "revision": "other", "locator": "c.md#claim", "claim": "claim"}]
    assert any("provenance must reference its source artifact" in error for error in MODULE.validate(record))


def test_provenance_for_matching_source_revision_and_locator_is_accepted():
    record = valid_record()
    row = next(item for item in record["results"] if item["input_id"] == "c")
    row["claim_provenance"] = [{"source": "https://example.test/source", "revision": "synthetic revision", "locator": "c.md#claim", "claim": "claim"}]
    assert MODULE.validate(record) == []


def test_provenance_with_compatible_exact_document_anchor_is_accepted():
    record = valid_record()
    row = next(item for item in record["results"] if item["input_id"] == "c")
    row["claim_provenance"] = [{"source": "https://example.test/source", "revision": "synthetic revision", "locator": "c.md#claim", "claim": "claim"}]
    assert MODULE.validate(record) == []


def test_claim_provenance_must_bind_current_source_revision_and_locator():
    record = valid_record()
    row = next(item for item in record["results"] if item["input_id"] == "c")
    row["claim_provenance"] = [{"source": "https://foreign.example/source", "revision": "other", "locator": "c.md#claim", "claim": "claim"}]
    assert any("provenance must reference its source artifact" in error for error in MODULE.validate(record))
    row["claim_provenance"] = [{"source": "https://example.test/source", "revision": "synthetic revision", "locator": "other.md#claim", "claim": "claim"}]
    assert any("provenance must reference its source artifact" in error for error in MODULE.validate(record))
    row["claim_provenance"].append({"source": "https://example.test/source", "revision": "synthetic revision", "locator": "c.md#claim", "claim": "claim"})
    assert MODULE.validate(record) == []


def test_malformed_claim_provenance_relation_is_rejected():
    record = valid_record()
    row = next(item for item in record["results"] if item["input_id"] == "c")
    row["disposition"] = "synthesized"
    row["targets"] = ["kb/wiki/entities/example.md"]
    row["claim_provenance"] = [None]
    assert any("provenance relations" in error for error in MODULE.validate(record))


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
    assert any("synthesized disposition requires canonical internal target relations" in error for error in errors)
    assert any("synthesized disposition requires claim/source provenance relations" in error for error in errors)
    assert any("unresolved disposition requires a reason" in error for error in errors)


def test_duplicate_artifact_ids_and_double_ownership_fail():
    record = valid_record()
    record["inputs"].append({"id": "a", "eligibility": "eligible"})
    record["results"].append({"input_id": "a", "disposition": "studied"})
    errors = MODULE.validate(record)
    assert any("duplicate input id" in error for error in errors)
    assert any("duplicate result ownership" in error for error in errors)


def test_unknown_identity_component_cannot_be_marked_eligible():
    record = valid_record()
    record["inputs"][0]["revision"] = "unknown"
    errors = MODULE.validate(record)
    assert any("with unknown identity components must remain unresolved" in error for error in errors)


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


def test_eligible_incomplete_results_force_partial_gate_and_block_release():
    for disposition in ("not_assessed", "deferred", "unresolved"):
        record = valid_record()
        row = record["results"][0]
        row.clear()
        row.update({"input_id": "a", "disposition": disposition})
        if disposition in {"deferred", "unresolved"}:
            row["reason"] = "synthetic incomplete state"
        record["gate"] = "PASS"
        record["release"] = {"authorized": True, "decision_ref": "synthetic owner decision"}
        errors = MODULE.validate(record)
        assert any("gate must be PARTIAL" in error for error in errors)
        assert record["gate"] == "PASS" and record["release"]["authorized"] is True


def test_required_pass_layer_requires_structural_execution_receipt():
    record = valid_record()
    layer = record["validation"]["source"]
    for field in ("command", "tool", "version", "input_snapshot", "limitations", "exit_code"):
        layer.pop(field)
    errors = MODULE.validate(record)
    assert any("PASS requires command, tool, version, input_snapshot, and limitations" in error for error in errors)
    layer.update(command="synthetic command", tool="synthetic", version="1", input_snapshot="snapshot", limitations="synthetic", exit_code="0")
    assert any("PASS requires exit_code=0" in error for error in MODULE.validate(record))


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
