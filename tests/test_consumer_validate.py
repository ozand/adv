import importlib.util
import json
from pathlib import Path

SCRIPT = Path(__file__).parents[1] / "scripts" / "consumer_validate.py"
SPEC = importlib.util.spec_from_file_location("consumer_validate", SCRIPT)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)

def receipt():
    return {"scope":"file", "date":"2026-10-09", "reviewer":"fixture", "outcome":"claims reviewed", "limitations":"synthetic"}

def artifact(state, revision="r1", source="https://example.test/repo", locator="README.md"):
    row = {"id":f"{source}|{revision}|{locator}", "source":source, "revision":revision, "locator":locator, "state":state}
    if state == "studied":
        row["receipt"] = receipt()
    if state == "synthesized":
        row["targets"] = ["kb/wiki/entities/example.md"]
    return row

def coverage(artifacts, counts=None, **extra):
    counts = counts or {state:0 for state in MODULE.STATES}
    for row in artifacts:
        counts[row["state"]] += 1
    return {"n":sum(counts.values()), "counts":counts, "artifacts":artifacts, "exclusions":[], "unresolved_listings":[], "eligible_scope_unknown":False, **extra}

def base_card(**extra):
    return {"type":"FutureType", "claims":[], **extra}

def test_extensible_type_and_optional_profile_remain_accepted():
    result = MODULE.validate({"cards":[base_card()]})
    assert result["universal"]["status"] == "PASS"
    assert result["universal"]["profile"] == "universal-profile-structural-proxy"
    assert result["consumer"]["status"] == "PASS"

def test_universal_failure_is_not_masked_by_consumer_warning():
    result = MODULE.validate({"cards":[{"type":"", "selected_for_review":True}]})
    assert result["universal"]["status"] == "FAIL"
    assert result["consumer"]["status"] == "PARTIAL"
    assert result["consumer"]["warnings"]

def test_title_recommendation_is_warning_only_and_legacy_not_checked():
    new = MODULE.validate({"cards":[base_card(selected_for_review=True)]})
    old = MODULE.validate({"cards":[base_card(selected_for_review=True, legacy=True)]})
    assert new["consumer"]["status"] == "PARTIAL"
    assert new["consumer"]["warnings"] and old["consumer"]["warnings"] == []
    assert old["consumer"]["status"] == "PASS"

def test_claim_source_provenance_is_conditional_and_locator_specific():
    missing = MODULE.validate({"cards":[base_card(claims=[{"requires_source":True,"evidence":[]}])]})
    valid = MODULE.validate({"cards":[base_card(claims=[{"requires_source":True,"evidence":[{"source":"https://public.example/source","revision":"abc123","locator":"docs/a.md#claim"}]}])]})
    assert missing["consumer"]["status"] == "FAIL"
    assert valid["consumer"]["status"] == "PASS"

def test_five_state_partition_arithmetic_and_reasoned_exclusions(tmp_path):
    rows = [artifact("not_assessed",locator="a.md"), artifact("studied",locator="b.md"), artifact("synthesized",locator="c.md"), artifact("synthesized",locator="d.md"), artifact("unresolved_eligible",locator="e.md")]
    target = tmp_path / "kb/wiki/entities/example.md"
    target.parent.mkdir(parents=True)
    target.write_text("synthetic target", encoding="utf-8")
    value = coverage(rows, exclusions=[{"id":"excluded-1","reason":"outside rights scope"},{"id":"excluded-2","reason":"excluded alias per snapshot rule"}])
    report = MODULE.validate({"coverage":value}, repo_root=tmp_path)
    assert report["universal"]["status"] == "PASS"
    assert report["graph"]["status"] == "PASS"
    assert report["consumer"]["status"] == "PARTIAL"
    assert report["consumer"]["coverage"] == {"n":5,"assessment":"3/5","synthesis":"2/5","scope":"KNOWN","state":"PARTIAL"}
    assert report["universal"]["status"] == "PASS"
    assert report["graph"]["status"] == "PASS"
    assert value["n"] == 5
    assert (value["counts"]["studied"]+value["counts"]["synthesized"])/5 == 0.6
    assert value["counts"]["synthesized"]/5 == 0.4

def test_unresolved_unknown_listing_is_outside_n_and_partial_scope_is_flagged():
    value = coverage([artifact("not_assessed"),artifact("unresolved_eligible",locator="b.md")], unresolved_listings=[{"id":"listing-unknown","eligibility":"unknown"}], eligible_scope_unknown=True)
    result = MODULE.validate({"coverage":value})
    assert result["consumer"]["status"] == "PARTIAL"
    assert result["consumer"]["coverage"] == {"n":2,"assessment":"0/2","synthesis":"0/2","scope":"PARTIAL","state":"PARTIAL"}
    assert value["n"] == 2 and value["eligible_scope_unknown"]

def test_zero_denominator_is_not_applicable_and_conflicting_duplicates_fail():
    zero = coverage([])
    result = MODULE.validate({"coverage":zero})
    assert result["consumer"]["status"] == "PASS"
    assert result["consumer"]["coverage"]["assessment"] == "NOT APPLICABLE"
    assert result["consumer"]["coverage"]["state"] == "NOT APPLICABLE"
    assert result["consumer"]["coverage"]["synthesis"] == "NOT APPLICABLE"
    first = artifact("studied")
    conflict = artifact("synthesized")
    bad = coverage([first,conflict])
    assert MODULE.validate({"coverage":bad})["consumer"]["status"] == "FAIL"
    # The same source path at a different revision is a distinct artifact.
    distinct = coverage([first,artifact("unresolved_eligible",revision="r2")])
    assert distinct["n"] == 2
    assert MODULE.validate({"coverage":distinct})["consumer"]["status"] == "PARTIAL"
    assert MODULE.validate({"coverage":distinct})["consumer"]["coverage"]["assessment"] == "1/2"

def test_windows_and_private_path_forms_are_rejected(tmp_path):
    hostile = [r"C:\private\card.md", r"\\server\share\card.md", "kb/wiki/%2e%2e/private.md", "kb/wiki/%43%3a/private.md", "kb/wiki/sources/private.md", "kb/wiki/.qmd/index.md", "kb/wiki/local-lessons/index.md"]
    for target in hostile:
        result = MODULE.validate({"graph":{"canonical_targets":[target]}}, repo_root=tmp_path)
        assert result["graph"]["status"] == "FAIL", target

def test_external_source_url_is_allowed_but_internal_escape_fails():
    external_target = MODULE.validate({"graph":{"canonical_targets":["https://public.example/doc"]}})
    escaped = MODULE.validate({"graph":{"canonical_targets":["kb/wiki/../../private.md"]}})
    unresolved = MODULE.validate({"graph":{"canonical_targets":["kb/wiki/card.md"]}})
    assert external_target["graph"]["status"] == "FAIL"
    assert escaped["graph"]["status"] == "FAIL"
    assert unresolved["graph"]["status"] == "FAIL"
    malformed_url = MODULE.validate({"graph":{"canonical_targets":["javascript:alert(1)"]}})
    assert malformed_url["graph"]["status"] == "FAIL"

def test_qmd_is_declaration_only_and_device_verification_needs_receipt():
    assert MODULE.validate({"qmd":{"claim":"fresh"}})["consumer"]["status"] == "FAIL"
    bad = MODULE.validate({"cards":[base_card(claims=[{"evidence":[{"device_verified":True}]}])]})
    good_receipt = {"device_verified":True,"device_model":"Cardputer","software_revision":"fw-1","configuration":"default","procedure":"synthetic procedure","observed_result":"synthetic outcome","verifier":"test"}
    good = MODULE.validate({"cards":[base_card(claims=[{"evidence":[good_receipt]}])]})
    assert bad["consumer"]["status"] == "FAIL"
    assert good["consumer"]["status"] == "PASS"

def test_canonical_target_must_resolve_inside_explicit_temp_root(tmp_path):
    inside = tmp_path / "kb" / "wiki" / "card.md"
    inside.parent.mkdir(parents=True)
    inside.write_text("fixture", encoding="utf-8")
    outside = tmp_path.parent / f"outside-{tmp_path.name}-card.md"
    outside.write_text("fixture", encoding="utf-8")
    try:
        valid = MODULE.validate({"graph":{"canonical_targets":["kb/wiki/card.md"]}}, repo_root=tmp_path)
        dangling = MODULE.validate({"graph":{"canonical_targets":["kb/wiki/missing.md"]}}, repo_root=tmp_path)
        assert valid["graph"]["status"] == "PASS"
        assert dangling["graph"]["status"] == "FAIL"
        link = tmp_path / "kb" / "wiki" / "escape.md"
        try:
            link.symlink_to(outside)
        except (OSError, NotImplementedError) as exc:
            import pytest
            pytest.skip(f"symlink creation unsupported: {type(exc).__name__}")
        escaped = MODULE.validate({"graph":{"canonical_targets":["kb/wiki/escape.md"]}}, repo_root=tmp_path)
        assert escaped["graph"]["status"] == "FAIL"
    finally:
        outside.unlink(missing_ok=True)

def test_target_relations_are_deduplicated_and_validation_is_read_only():
    import copy
    value = coverage([artifact("synthesized",locator="a.md")])
    value["artifacts"][0]["targets"] = ["kb/wiki/entities/a.md", "kb/wiki/entities/a.md"]
    before = copy.deepcopy(value)
    result = MODULE.validate({"coverage":value})
    assert result["consumer"]["coverage"]["synthesis"] == "1/1"
    assert "explicit repository root required" in " ".join(result["consumer"]["errors"])
    assert value == before

def test_conflicting_duplicate_states_fail_without_promoting_universal_result():
    first = artifact("studied")
    second = artifact("synthesized")
    report = MODULE.validate({"cards":[base_card()],"coverage":coverage([first,second])})
    assert report["consumer"]["status"] == "FAIL"
    assert report["universal"]["status"] == "PASS"

def test_artifact_ids_cannot_be_both_eligible_and_excluded_and_must_be_unique():
    row = artifact("not_assessed")
    overlapping = coverage([row], exclusions=[{"id":row["id"],"reason":"contradictory exclusion"}])
    assert "cannot also be listed as excluded" in " ".join(MODULE.validate({"coverage":overlapping})["consumer"]["errors"])
    duplicate = coverage([row,dict(row)])
    assert "duplicate artifact id" in " ".join(MODULE.validate({"coverage":duplicate})["consumer"]["errors"])
    excluded = coverage([], exclusions=[{"id":"x","reason":"outside scope"}])
    assert MODULE.validate({"coverage":excluded})["consumer"]["status"] == "PASS"

def test_overdeep_structured_object_is_rejected_without_traceback():
    nested = {}
    current = nested
    for _ in range(2000):
        child = {}
        current["cards"] = [child]
        current = child
    import pytest
    with pytest.raises(ValueError, match="nesting depth"):
        MODULE.validate(nested)

def test_malformed_untrusted_field_types_fail_cleanly():
    bad_app = MODULE.validate({"cards":[base_card(claims=[{"applicability":[]}])]})
    bad_state = MODULE.validate({"coverage":{"n":0,"counts":{state:0 for state in MODULE.STATES},"artifacts":[{"source":"s","revision":"r","locator":"p","state":[]}]} })
    bad_qmd = MODULE.validate({"qmd":{"claim":[]}})
    assert bad_app["consumer"]["status"] == "FAIL"
    assert bad_state["consumer"]["status"] == "FAIL"
    assert bad_qmd["consumer"]["status"] == "FAIL"

def test_malformed_top_level_input_rejected():
    import pytest
    with pytest.raises(ValueError):
        MODULE.validate([])
    with pytest.raises(ValueError):
        MODULE.validate({"unknown":True})

def test_pinned_universal_source_invocation_and_mismatch_fail_closed(tmp_path):
    import subprocess
    import sys
    source = Path("C:/Temp/adv-kb-bootstrap-pin-73277")
    python = "C:/Temp/adv-kb-bootstrap-73277-venv/Scripts/python.exe"
    fixture = tmp_path / "fixture.json"
    fixture.write_text(json.dumps({"cards":[]}), encoding="utf-8")
    good = subprocess.run([sys.executable,str(SCRIPT),str(fixture),"--kb-bootstrap-source",str(source),"--kb-python",python],capture_output=True,text=True)
    assert good.returncode == 0, good.stderr + good.stdout
    report = json.loads(good.stdout)
    assert report["universal"]["profile"] == f"kb-bootstrap-validate-core:{MODULE.FRAMEWORK_PIN}"
    assert report["universal"]["exit_code"] == 0
    assert "ERRORS: 0" in report["universal"]["stdout"]
    assert "ORPHANS (0 Incoming Links): 5" in report["universal"]["stdout"]
    assert "retrieval, index freshness and publication readiness: not checked" in report["universal"]["stdout"]
    unrelated = subprocess.run([sys.executable,str(SCRIPT),str(fixture),"--kb-python",python],capture_output=True,text=True)
    assert unrelated.returncode == 2 and "both --kb-bootstrap-source" in json.loads(unrelated.stdout)["error"]
    bad = subprocess.run([sys.executable,str(SCRIPT),str(fixture),"--kb-bootstrap-source",str(tmp_path),"--kb-python",python],capture_output=True,text=True)
    assert bad.returncode == 1
    assert json.loads(bad.stdout)["universal"]["status"] == "FAIL"
    unavailable = subprocess.run([sys.executable,str(SCRIPT),str(fixture),"--kb-bootstrap-source",str(source),"--kb-python",str(tmp_path / "missing-python.exe")],capture_output=True,text=True)
    assert unavailable.returncode == 1
    assert json.loads(unavailable.stdout)["universal"]["status"] == "FAIL"

def test_cli_separates_layers_and_bounds_input(tmp_path):
    import subprocess
    import sys
    valid = tmp_path / "valid.json"
    valid.write_text(json.dumps({"cards":[base_card()]}),encoding="utf-8")
    run = subprocess.run([sys.executable, str(SCRIPT), str(valid)], capture_output=True, text=True)
    assert run.returncode == 0
    report = json.loads(run.stdout)
    assert report["universal"]["status"] == report["consumer"]["status"] == "PASS"
    invalid = tmp_path / "invalid.json"
    invalid.write_text(json.dumps({"cards":[{"type":""}]}),encoding="utf-8")
    run = subprocess.run([sys.executable, str(SCRIPT), str(invalid)], capture_output=True, text=True)
    assert run.returncode == 1
    report = json.loads(run.stdout)
    assert report["universal"]["status"] == "FAIL" and report["consumer"]["status"] == "PASS"
    malformed = tmp_path / "malformed.json"
    malformed.write_text("{",encoding="utf-8")
    run = subprocess.run([sys.executable, str(SCRIPT), str(malformed)], capture_output=True, text=True)
    assert run.returncode == 2 and "error" in json.loads(run.stdout)
    oversized = tmp_path / "oversized.json"
    oversized.write_bytes(b" " * 1_000_001)
    run = subprocess.run([sys.executable, str(SCRIPT), str(oversized)], capture_output=True, text=True)
    assert run.returncode == 2
