"""Read-only structural checker for a bounded batch JSON receipt.

It does not authenticate human decisions, reviewers, source bytes, truth, rights,
or publication permission. PASS means only that declared fields are consistent.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path, PurePosixPath
from typing import Any
from urllib.parse import urlsplit

SHA1 = re.compile(r"^[0-9a-f]{40}$")
SHA256 = re.compile(r"^[0-9a-f]{64}$")
ISSUE_PATH = re.compile(r"^/([^/]+)/([^/]+)/issues/([1-9][0-9]*)$")
PR_PATH = re.compile(r"^/([^/]+)/([^/]+)/pull/([1-9][0-9]*)$")
ISSUE_COMMENT = re.compile(r"^(?:issuecomment-[1-9][0-9]*|discussion_r[1-9][0-9]*|pullrequestreview-[1-9][0-9]*|pullrequestreviewcomment-[1-9][0-9]*)$")


def has_reason(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def valid_target(value: Any) -> bool:
    if not isinstance(value, str) or "\\" in value or "%" in value or "://" in value:
        return False
    path = PurePosixPath(value)
    return (
        not path.is_absolute()
        and value == path.as_posix()
        and value.startswith("kb/wiki/")
        and all(part not in {"", ".", ".."} for part in path.parts)
    )


def valid_claim_relation(value: Any) -> bool:
    return isinstance(value, dict) and all(
        has_reason(value.get(field))
        for field in ("source", "revision", "locator", "claim")
    )


def canonical_source_identity(value: Any) -> Any:
    if not isinstance(value, str):
        return value
    try:
        parsed = urlsplit(value)
    except ValueError:
        return value
    if parsed.scheme.casefold() == "https" and parsed.netloc.casefold() == "github.com":
        path = parsed.path.rstrip("/")
        if path.endswith(".git"):
            path = path[:-4]
        parts = path.split("/")
        if len(parts) == 3 and all(parts[1:]):
            owner, repository = parts[1:]
            if re.fullmatch(r"[A-Za-z0-9-]+", owner) and re.fullmatch(r"[A-Za-z0-9_.-]+", repository):
                return f"github.com/{owner.casefold()}/{repository.casefold()}"
    return value


def locator_compatible(artifact: Any, evidence: Any) -> bool:
    if not isinstance(artifact, str) or not isinstance(evidence, str):
        return False
    artifact_path, _, artifact_anchor = artifact.partition("#")
    evidence_path, _, evidence_anchor = evidence.partition("#")
    return artifact_path == evidence_path and (not artifact_anchor or artifact_anchor == evidence_anchor)


def github_pointer(value: Any, *, allow_comment: bool = False) -> tuple[str, str, str, str] | None:
    if not isinstance(value, str):
        return None
    try:
        parsed = urlsplit(value)
        match = ISSUE_PATH.fullmatch(parsed.path)
        kind = "issue"
        if match is None:
            match = PR_PATH.fullmatch(parsed.path)
            kind = "pull"
        if (
            parsed.scheme != "https" or parsed.netloc.casefold() != "github.com"
            or parsed.username is not None or parsed.password is not None
            or parsed.port is not None or parsed.query or match is None
        ):
            return None
        owner, repo, number = match.groups()
        if not re.fullmatch(r"[A-Za-z0-9-]+", owner) or not re.fullmatch(r"[A-Za-z0-9_.-]+", repo):
            return None
        if parsed.fragment and (not allow_comment or not ISSUE_COMMENT.fullmatch(parsed.fragment)):
            return None
        return owner.casefold(), repo.casefold(), kind, number
    except ValueError:
        return None


LAYERS = {"source", "content", "retrieval"}
OUTCOMES = {"PASS", "FAIL", "PARTIAL", "NOT RUN", "NOT APPLICABLE"}
DISPOSITIONS = {"not_assessed", "studied", "synthesized", "deferred", "unresolved"}


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
    batch_issue = github_pointer(record["issue"])
    if batch_issue is None:
        errors.append("issue must be a canonical GitHub Issue HTTPS URL")
    if not isinstance(record["writer"], str) or not record["writer"].strip():
        errors.append("writer must be a non-empty identifier")
    if not isinstance(record.get("owner"), str) or not record["owner"].strip():
        errors.append("owner must be a non-empty identifier")
    if not isinstance(record.get("objective"), str) or not record["objective"].strip():
        errors.append("objective must be explicit in the batch record")
    for field in ("base", "candidate_sha"):
        value = record[field]
        if not isinstance(value, str) or not SHA1.fullmatch(value):
            errors.append(f"{field} must be a full 40-character lowercase commit SHA")

    inputs = record["inputs"]
    ids: set[str] = set()
    source_identities: set[tuple[str, str, str]] = set()
    if not isinstance(inputs, list) or not inputs:
        errors.append("inputs must be a non-empty array")
        inputs = []
    valid_input_ids: set[str] = set()
    valid_inputs: dict[str, dict[str, Any]] = {}
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
            continue
        source_identity = tuple(item.get(field) for field in ("source", "revision", "locator"))
        if not all(isinstance(part, str) and part.strip() for part in source_identity):
            errors.append(f"inputs[{i}] source/revision/locator identity must be non-empty strings")
            continue
        source_identity = (canonical_source_identity(source_identity[0]), *source_identity[1:])
        if source_identity in source_identities:
            errors.append(f"inputs[{i}] duplicates source-artifact identity")
            continue
        ids.add(input_id)
        source_identities.add(source_identity)
        valid_input_ids.add(input_id)
        valid_inputs[input_id] = item
        for field in ("source", "revision", "locator"):
            if not isinstance(item.get(field), str) or not item[field].strip():
                errors.append(f"inputs[{i}].{field} must be explicit (use a stated unknown value when unavailable)")
        identity_unknown = any(part.strip().casefold() in {"unknown", "unavailable", "not available"} for part in source_identity)
        eligibility = item.get("eligibility")
        if not isinstance(eligibility, str) or eligibility not in {"eligible", "excluded", "unresolved"}:
            errors.append(f"inputs[{i}].eligibility must be eligible, excluded, or unresolved")
        elif identity_unknown and eligibility != "unresolved":
            errors.append(f"inputs[{i}] with unknown identity components must remain unresolved")
        if eligibility == "unresolved" and not has_reason(item.get("reason")):
            errors.append(f"inputs[{i}] unresolved eligibility requires a reason")
        if eligibility == "excluded" and not has_reason(item.get("reason")):
            errors.append(f"inputs[{i}] excluded input requires a reason")
        digest = item.get("sha256")
        if digest is not None and (not isinstance(digest, str) or not SHA256.fullmatch(digest)):
            errors.append(f"inputs[{i}].sha256 must be 64 lowercase hex characters")

    scope_partial = any(
        isinstance(item, dict) and item.get("eligibility") == "unresolved"
        for item in inputs
    )
    result_rows = record["results"]
    result_ids: set[str] = set()
    result_dispositions: dict[str, str] = {}
    if not isinstance(result_rows, list):
        errors.append("results must be an array")
        result_rows = []
    for i, item in enumerate(result_rows):
        if not isinstance(item, dict):
            errors.append(f"results[{i}] must be an object")
            continue
        input_id = item.get("input_id")
        if not isinstance(input_id, str) or not input_id.strip() or input_id not in ids:
            errors.append(f"results[{i}].input_id must be a declared non-empty string")
            continue
        if input_id in result_ids:
            errors.append(f"duplicate result ownership for input: {input_id}")
        result_ids.add(input_id)
        disposition = item.get("disposition")
        if not isinstance(disposition, str) or disposition not in DISPOSITIONS:
            errors.append(f"results[{i}] has invalid disposition")
        else:
            result_dispositions.setdefault(input_id, disposition)
        if disposition == "excluded":
            errors.append(f"results[{i}] cannot use excluded; exclusions are outside the eligible partition")
        elif isinstance(disposition, str) and disposition == "deferred" and not has_reason(item.get("reason")):
            errors.append(f"results[{i}] deferred disposition requires a reason")
        elif isinstance(disposition, str) and disposition == "unresolved" and not has_reason(item.get("reason")):
            errors.append(f"results[{i}] unresolved disposition requires a reason")
        elif isinstance(disposition, str) and disposition in {"studied", "synthesized"}:
            assessment = item.get("assessment")
            if not isinstance(assessment, dict) or any(
                not isinstance(assessment.get(field), str) or not assessment[field].strip()
                for field in ("scope", "date", "reviewer", "outcome", "limitations")
            ):
                errors.append(f"results[{i}] {item['disposition']} requires a complete assessment receipt")
            if item["disposition"] == "synthesized":
                targets = item.get("targets")
                if not isinstance(targets, list) or not targets or any(
                    not valid_target(target)
                    for target in targets
                ):
                    errors.append(f"results[{i}] synthesized disposition requires canonical internal target relations")
                provenance = item.get("claim_provenance")
                artifact = valid_inputs.get(input_id)
                if not isinstance(provenance, list) or not provenance or any(
                    not valid_claim_relation(relation) for relation in provenance
                ):
                    errors.append(f"results[{i}] synthesized disposition requires claim/source provenance relations")
                elif artifact is None or not any(
                    canonical_source_identity(relation["source"]) == canonical_source_identity(artifact["source"])
                    and relation["revision"] == artifact["revision"]
                    and locator_compatible(artifact["locator"], relation["locator"])
                    for relation in provenance
                ):
                    errors.append(f"results[{i}] synthesized provenance must reference its source artifact")
    incomplete_result = any(
        isinstance(item, dict)
        and isinstance(item.get("input_id"), str)
        and item["input_id"] in valid_input_ids
        and item.get("input_id") in result_dispositions
        and result_dispositions[item["input_id"]] in {"not_assessed", "deferred", "unresolved"}
        for item in result_rows
    )
    scope_partial = scope_partial or incomplete_result
    for item in inputs:
        item_id = item.get("id") if isinstance(item, dict) else None
        if not isinstance(item_id, str) or not item_id.strip() or item_id not in valid_input_ids:
            continue
        if item.get("eligibility") == "eligible" and item_id not in result_ids:
            errors.append(f"eligible input missing result: {item_id}")
        identity_unknown = any(
            isinstance(item.get(field), str)
            and item[field].strip().casefold() in {"unknown", "unavailable", "not available"}
            for field in ("source", "revision", "locator")
        )
        if identity_unknown and item.get("eligibility") != "unresolved":
            errors.append(f"unknown identity must remain unresolved: {item_id}")
        if item.get("eligibility") == "unresolved" and item_id not in result_ids:
            errors.append(f"unresolved eligibility must remain visible as unresolved: {item_id}")
        if item.get("eligibility") == "unresolved" and item_id in result_ids:
            disposition = result_dispositions.get(item_id)
            if disposition != "unresolved":
                errors.append(f"unresolved eligibility cannot receive assessed disposition: {item_id}")
            if disposition == "unresolved" and not has_reason(valid_inputs[item_id].get("reason")):
                errors.append(f"unresolved artifact requires a reason: {item_id}")
        if item.get("eligibility") == "excluded" and item_id in result_ids:
            errors.append(f"excluded input must remain outside results: {item_id}")

    layers = record["validation"]
    if not isinstance(layers, dict) or set(layers) != LAYERS:
        errors.append("validation must contain exactly source, content, retrieval layers")
    elif all(
        isinstance(layer, dict)
        and isinstance(layer.get("status"), str)
        and layer["status"] in OUTCOMES
        for layer in layers.values()
    ):
        required_layers = []
        for name, layer in layers.items():
            status = layer["status"]
            if not isinstance(layer.get("required"), bool):
                errors.append(f"validation.{name}.required must explicitly declare applicability")
            if status == "NOT RUN" and not has_reason(layer.get("reason")):
                errors.append(f"validation.{name} NOT RUN requires reason")
            if status == "NOT APPLICABLE":
                if not isinstance(layer.get("precondition"), str) or not layer["precondition"].strip():
                    errors.append(f"validation.{name} NOT APPLICABLE requires declared precondition")
                if not isinstance(layer.get("reason"), str) or not layer["reason"].strip():
                    errors.append(f"validation.{name} NOT APPLICABLE requires reason")
                if layer.get("required") is not False:
                    errors.append(f"validation.{name} NOT APPLICABLE requires required=false")
            elif layer.get("required") is True:
                required_layers.append(layer)
                if status == "PASS":
                    evidence_fields = ("command", "tool", "version", "input_snapshot", "limitations")
                    if any(not has_reason(layer.get(field)) for field in evidence_fields):
                        errors.append(f"validation.{name} PASS requires command, tool, version, input_snapshot, and limitations")
                    exit_code = layer.get("exit_code")
                    if isinstance(exit_code, bool) or not isinstance(exit_code, int) or exit_code != 0:
                        errors.append(f"validation.{name} PASS requires exit_code=0")
            elif status != "NOT APPLICABLE":
                errors.append(f"validation.{name} required=false must be reported NOT APPLICABLE")
        all_not_applicable = not required_layers
        expected = "NOT CHECKED" if all_not_applicable else "PASS"
        if any(layer["status"] == "FAIL" for layer in required_layers):
            expected = "FAIL"
        elif any(layer["status"] in {"PARTIAL", "NOT RUN"} for layer in required_layers):
            expected = "PARTIAL"
        if scope_partial and expected == "PASS":
            expected = "PARTIAL"
        if record["gate"] != expected:
            errors.append(f"gate must be {expected} based on layer and scope outcomes")
        if not required_layers:
            errors.append("gate cannot be established when no validation layer is required")
    elif isinstance(layers, dict):
        for name, layer in layers.items():
            if (
                not isinstance(layer, dict)
                or not isinstance(layer.get("status"), str)
                or layer["status"] not in OUTCOMES
            ):
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
        elif (
            not isinstance(record["writer"], str)
            or review["reviewer"].strip().casefold() == record["writer"].strip().casefold()
        ):
            errors.append("reviewer identity must differ from writer identity")
        review_status = review.get("status")
        if not isinstance(review_status, str) or review_status not in {"PASS", "FAIL", "PARTIAL"}:
            errors.append("review status must be PASS, FAIL, or PARTIAL")
        elif review_status != "PASS" and record["gate"] == "PASS":
            errors.append("gate cannot PASS when exact-candidate review is not PASS")

    receipt = record["receipt"]
    if not isinstance(receipt, dict):
        errors.append("receipt must be an object")
    else:
        receipt_pointer = github_pointer(receipt.get("url"), allow_comment=True)
        if receipt_pointer is None or receipt_pointer[2] not in {"issue", "pull"}:
            errors.append("receipt requires a canonical GitHub Issue or pull-request URL")
        elif batch_issue is not None and receipt_pointer[:2] != batch_issue[:2]:
            errors.append("receipt URL must belong to the governing repository")
        if not isinstance(receipt.get("retention"), str) or not receipt["retention"].strip():
            errors.append("receipt requires a retention statement")
        if receipt.get("sanitized") is not True:
            errors.append("receipt must assert sanitized public-safe content")
        receipt_issue = github_pointer(receipt.get("issue"))
        if receipt_issue is None or receipt_issue[2] != "issue":
            errors.append("receipt must link its governing GitHub Issue")
        elif batch_issue is not None and receipt_issue != batch_issue:
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


class DuplicateJSONKeyError(ValueError):
    """Raised when a JSON object repeats a member name."""


def reject_duplicate_json_keys(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise DuplicateJSONKeyError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("record", type=Path, help="path to a batch JSON record")
    args = parser.parse_args()
    try:
        record = json.loads(args.record.read_text(encoding="utf-8"), object_pairs_hook=reject_duplicate_json_keys)
    except (OSError, UnicodeDecodeError, json.JSONDecodeError, DuplicateJSONKeyError) as exc:
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
