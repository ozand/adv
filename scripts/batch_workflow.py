"""Read-only structural checker for a bounded batch JSON receipt.

It does not authenticate human decisions, reviewers, source bytes, truth, rights,
or publication permission. PASS means only that declared fields are consistent.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

SHA1 = re.compile(r"^[0-9a-f]{40}$")
SHA256 = re.compile(r"^[0-9a-f]{64}$")
ISSUE_URL = re.compile(r"https://github\.com/[^/\s]+/[^/\s]+/issues/[1-9][0-9]*")
RECEIPT_URL = re.compile(r"https://github\.com/[^/\s]+/[^/\s]+/issues/[1-9][0-9]*(?:#issuecomment-[1-9][0-9]*)?")
LAYERS = {"source", "content", "retrieval"}
OUTCOMES = {"PASS", "FAIL", "PARTIAL", "NOT RUN", "NOT APPLICABLE"}
DISPOSITIONS = {"not_assessed", "studied", "synthesized", "deferred", "unresolved", "excluded"}


def validate(record: Any) -> list[str]:
    """Return deterministic structural errors in stable declaration order."""
    if not isinstance(record, dict):
        return ["record must be a JSON object"]
    errors: list[str] = []
    required = (
        "batch_id", "issue", "base", "candidate_sha", "writer", "inputs",
        "results", "validation", "gate", "review", "receipt", "release",
    )
    for key in required:
        if key not in record:
            errors.append(f"missing required field: {key}")
    if errors:
        return errors

    if not isinstance(record["batch_id"], str) or not record["batch_id"].strip():
        errors.append("batch_id must be a non-empty identifier")
    if not isinstance(record.get("objective"), str) or not record["objective"].strip():
        errors.append("objective must be explicit in the batch record")
    if not isinstance(record["issue"], str) or not ISSUE_URL.fullmatch(record["issue"]):
        errors.append("issue must be a canonical GitHub Issue HTTPS URL")
    if not isinstance(record["writer"], str) or not record["writer"].strip():
        errors.append("writer must be a non-empty identifier")
    if not isinstance(record.get("owner"), str) or not record["owner"].strip():
        errors.append("owner must be a non-empty identifier")
    if not isinstance(record.get("objective"), str) or not record["objective"].strip():
        errors.append("objective must be explicit in the batch record or governing issue")
    for field in ("base", "candidate_sha"):
        value = record[field]
        if not isinstance(value, str) or not SHA1.fullmatch(value):
            errors.append(f"{field} must be a full 40-character lowercase commit SHA")

    inputs = record["inputs"]
    ids: set[str] = set()
    if not isinstance(inputs, list) or not inputs:
        errors.append("inputs must be a non-empty array")
        inputs = []
    for i, item in enumerate(inputs):
        if not isinstance(item, dict):
            errors.append(f"inputs[{i}] must be an object")
            continue
        input_id = item.get("id")
        if not isinstance(input_id, str) or not input_id.strip():
            errors.append(f"inputs[{i}] requires a non-empty id")
            continue
        if input_id in ids:
            errors.append(f"duplicate input id: {input_id}")
        ids.add(input_id)
        for field in ("source", "revision", "locator"):
            if not isinstance(item.get(field), str) or not item[field].strip():
                errors.append(f"inputs[{i}].{field} must be explicit (use a stated unknown value when unavailable)")
        if item.get("eligibility") not in {"eligible", "excluded", "unresolved"}:
            errors.append(f"inputs[{i}].eligibility must be eligible, excluded, or unresolved")
        if item.get("eligibility") == "excluded" and not str(item.get("reason", "")).strip():
            errors.append(f"inputs[{i}] excluded input requires a reason")
        digest = item.get("sha256")
        if digest is not None and (not isinstance(digest, str) or not SHA256.fullmatch(digest)):
            errors.append(f"inputs[{i}].sha256 must be 64 lowercase hex characters")

    result_rows = record["results"]
    result_ids: set[str] = set()
    if not isinstance(result_rows, list):
        errors.append("results must be an array")
        result_rows = []
    for i, item in enumerate(result_rows):
        if not isinstance(item, dict) or item.get("input_id") not in ids:
            errors.append(f"results[{i}] must reference a declared input_id")
            continue
        input_id = item["input_id"]
        if input_id in result_ids:
            errors.append(f"duplicate result ownership for input: {input_id}")
        result_ids.add(input_id)
        if item.get("disposition") not in DISPOSITIONS:
            errors.append(f"results[{i}] has invalid disposition")
    for item in inputs:
        if isinstance(item, dict) and item.get("eligibility") == "eligible" and item.get("id") not in result_ids:
            errors.append(f"eligible input missing result: {item.get('id')}")
        if isinstance(item, dict) and item.get("eligibility") == "eligible" and item.get("id") in result_ids:
            disposition = next(
                row.get("disposition") for row in result_rows
                if isinstance(row, dict) and row.get("input_id") == item.get("id")
            )
            if disposition == "excluded":
                errors.append(f"eligible input cannot have excluded disposition: {item.get('id')}")
        if isinstance(item, dict) and item.get("eligibility") == "excluded" and item.get("id") in result_ids:
            disposition = next(
                row.get("disposition") for row in result_rows
                if isinstance(row, dict) and row.get("input_id") == item.get("id")
            )
            if disposition != "excluded":
                errors.append(f"excluded input must have excluded disposition: {item.get('id')}")

    layers = record["validation"]
    if not isinstance(layers, dict) or set(layers) != LAYERS:
        errors.append("validation must contain exactly source, content, retrieval layers")
    elif all(isinstance(layer, dict) and layer.get("status") in OUTCOMES for layer in layers.values()):
        for name, layer in layers.items():
            if layer["status"] == "NOT RUN" and not str(layer.get("reason", "")).strip():
                errors.append(f"validation.{name} NOT RUN requires reason")
        required_layers = [layer for layer in layers.values() if layer["status"] != "NOT APPLICABLE"]
        expected = "PASS"
        if any(layer["status"] == "FAIL" for layer in required_layers):
            expected = "FAIL"
        elif any(layer["status"] in {"PARTIAL", "NOT RUN"} for layer in required_layers):
            expected = "PARTIAL"
        if record["gate"] != expected:
            errors.append(f"gate must be {expected} based on layer outcomes")
    elif isinstance(layers, dict):
        for name, layer in layers.items():
            if not isinstance(layer, dict) or layer.get("status") not in OUTCOMES:
                errors.append(f"validation.{name}.status is invalid")

    review = record["review"]
    if not isinstance(review, dict):
        errors.append("review must be an object")
    else:
        if not isinstance(review.get("candidate_sha"), str) or not SHA1.fullmatch(review["candidate_sha"]):
            errors.append("review requires full candidate_sha")
        elif review["candidate_sha"] != record["candidate_sha"]:
            errors.append("review candidate_sha does not match current candidate_sha")
        if review.get("mode") != "read-only":
            errors.append("review mode must be read-only")
        reviewer_role = review.get("reviewer_role")
        if not isinstance(reviewer_role, str) or not reviewer_role.strip() or reviewer_role == record["writer"]:
            errors.append("reviewer_role must be explicit and distinct from writer")
        if not isinstance(review.get("reviewer"), str) or not review["reviewer"].strip():
            errors.append("review requires reviewer identifier")
        if review.get("status") not in {"PASS", "FAIL", "PARTIAL"}:
            errors.append("review status must be PASS, FAIL, or PARTIAL")
        elif review["status"] != "PASS" and record["gate"] == "PASS":
            errors.append("gate cannot PASS when exact-candidate review is not PASS")

    receipt = record["receipt"]
    if not isinstance(receipt, dict):
        errors.append("receipt must be an object")
    else:
        if not isinstance(receipt.get("url"), str) or not RECEIPT_URL.fullmatch(receipt["url"]):
            errors.append("receipt requires a canonical GitHub Issue or issue-comment URL")
        if not isinstance(receipt.get("retention"), str) or not receipt["retention"].strip():
            errors.append("receipt requires a retention statement")
        if receipt.get("sanitized") is not True:
            errors.append("receipt must assert sanitized public-safe content")
        if not isinstance(receipt.get("issue"), str) or not ISSUE_URL.fullmatch(receipt["issue"]):
            errors.append("receipt must link its governing GitHub Issue")
        elif receipt["issue"] != record["issue"]:
            errors.append("receipt Issue does not match batch Issue")

    release = record["release"]
    if not isinstance(release, dict) or not isinstance(release.get("authorized"), bool):
        errors.append("release.authorized must be an explicit boolean")
    elif release["authorized"]:
        if not isinstance(release.get("decision_ref"), str) or not release["decision_ref"].strip():
            errors.append("authorized release requires decision_ref")
        if record.get("gate") != "PASS":
            errors.append("release cannot be authorized when aggregate gate is not PASS")
        if isinstance(review, dict) and review.get("status") != "PASS":
            errors.append("release cannot be authorized without a PASS review")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("record", type=Path, help="path to a batch JSON record")
    args = parser.parse_args()
    try:
        record = json.loads(args.record.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"ERROR: cannot read JSON record: {exc}", file=sys.stderr)
        return 2
    errors = validate(record)
    for error in errors:
        print(f"FAIL: {error}")
    if errors:
        print(f"RESULT: FAIL ({len(errors)} errors)")
        return 1
    print("RESULT: STRUCTURE PASS; human-decision authenticity, truth, rights, and release consent are not verified")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
