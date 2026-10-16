"""Validate the exact four Issue #50 cards and map their bounded assessment records.

This adapter reads the candidate's actual front matter and the independent, linked
assessment receipt. It writes no data and proves no factual truth, legal clearance,
device behavior, or publication eligibility.
"""
from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import re
import sys

import yaml

ROOT = Path(__file__).resolve().parents[2]
RECEIPT_URL = "https://github.com/ozand/adv/issues/50#issuecomment-6207606025"
RECEIPT_DATE = "2026-10-16"
RECEIPT_REVIEWER = "01a122d6-c790-761b-9cf7-687200c76ee1"
EXPECTED = {
    "incremental-multiline-repl-assembly.md": ("5d0fef94f389161421b1f7559c15d8303effa7be", "lines 23-90, 116-179"),
    "sd-initialization-frequency-retry.md": ("6a648e32ad54457946ff7eb5a3b55a0dfaaa6cd2", "lines 11-27"),
    "expression-evaluator-pipeline.md": ("d70d88d707f9fd289d096c4295b61159963c9b47", "lines 70-100, 144-188"),
    "cooperative-script-loop-budget.md": ("16e42a58bf67da0a4930ca7f257bdfd5b8c4f254", "lines 41-79, 1138-1145"),
}


def load_validator():
    path = ROOT / "scripts" / "consumer_validate.py"
    spec = importlib.util.spec_from_file_location("consumer_validate", path)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load existing consumer validator")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def parse_receipt():
    path = ROOT / "docs" / "issue50" / "assessment-receipts.md"
    text = path.read_text(encoding="utf-8")
    header, *sections = text.split("\n## ")
    date_match = re.search(r"\*\*Assessment date:\*\* ([0-9]{4}-[0-9]{2}-[0-9]{2}) UTC", header)
    reviewer_match = re.search(r"\*\*Reviewer:\*\* Pi reviewer session `([^`]+)` \(agent/session identity; not human-authorship attestation\)", header)
    for required in (RECEIPT_URL, "not human-authorship attestation"):
        if required not in header:
            raise ValueError(f"receipt-level provenance is missing: {required}")
    if date_match is None or reviewer_match is None:
        raise ValueError("assessment receipt date or reviewer identity is missing/misrepresented")
    receipt_date = date_match.group(1)
    receipt_reviewer = reviewer_match.group(1)
    if receipt_date != RECEIPT_DATE or receipt_reviewer != RECEIPT_REVIEWER:
        raise ValueError("assessment receipt date/reviewer does not match the cited review record")
    parsed = {}
    for section in sections:
        title, _, body = section.partition("\n")
        if not title or title.startswith("Scope boundary"):
            continue
        source_line = re.search(r"(?m)^- \*\*Source artifact:\*\* `([^`]+)`$", body)
        rev_line = re.search(r"(?m)^- \*\*Revision / locator:\*\* `([^`]+)`; `([^`]+)`\.$", body)
        outcome = re.search(r"(?m)^- \*\*Assessment outcome:\*\* (.+)$", body)
        limits = re.search(r"(?m)^- \*\*Limitations:\*\* (.+)$", body)
        decisions = re.search(r"(?m)^- \*\*Review decisions / rights:\*\* (.+)$", body)
        target = re.search(r"(?m)^- \*\*Target relation:\*\* `([^`]+)` .+$", body)
        if not all((source_line, rev_line, outcome, limits, decisions, target)):
            raise ValueError(f"incomplete per-artifact receipt section: {title}")
        if not all(match.group(1).strip() for match in (source_line, rev_line, outcome, limits, decisions, target)):
            raise ValueError(f"blank required assessment field: {title}")
        source, revision, locator = source_line.group(1), rev_line.group(1), rev_line.group(2)
        key = (source, revision, locator)
        if key in parsed:
            raise ValueError(f"duplicate receipt identity: {key}")
        parsed[key] = {
            "title": title,
            "outcome": outcome.group(1),
            "limitations": limits.group(1),
            "review_decisions": decisions.group(1),
            "target": target.group(1),
        }
    return parsed, text


def main() -> int:
    validator = load_validator()
    files = sorted((ROOT / "kb" / "wiki" / "concepts").glob("*.md"))
    if {path.name for path in files} != set(EXPECTED):
        raise ValueError("concept directory does not equal the exact four-card candidate set")
    receipts, receipt_text = parse_receipt()
    if len(receipts) != 4:
        raise ValueError("assessment receipt must contain exactly four artifact records")

    cards, targets, artifacts = [], [], []
    for path in files:
        parts = path.read_text(encoding="utf-8").split("---", 2)
        if len(parts) != 3 or parts[0].strip():
            raise ValueError(f"invalid front matter: {path.name}")
        card = yaml.safe_load(parts[1])
        revision, locator = EXPECTED[path.name]
        if card.get("type") != "Concept" or card.get("status") != "draft":
            raise ValueError(f"unexpected type/status: {path.name}")
        if card.get("issue") != "https://github.com/ozand/adv/issues/50":
            raise ValueError(f"wrong governing Issue: {path.name}")
        if card.get("applicability", {}).get("state") != "unknown":
            raise ValueError(f"unverified applicability must remain unknown: {path.name}")
        if len(card.get("sources", [])) != 1 or len(card.get("evidence", [])) != 1:
            raise ValueError(f"expected one source and one claim-evidence record: {path.name}")
        source, evidence = card["sources"][0], card["evidence"][0]
        if source.get("revision") != revision or evidence.get("revision") != revision:
            raise ValueError(f"source revision mismatch: {path.name}")
        if evidence.get("locator") != locator or evidence.get("method") != "code-inspected":
            raise ValueError(f"evidence locator/method mismatch: {path.name}")
        if evidence.get("source") != source.get("resource"):
            raise ValueError(f"claim/source relation mismatch: {path.name}")

        target = path.relative_to(ROOT).as_posix()
        key = (evidence["source"], revision, locator)
        receipt = receipts.get(key)
        if receipt is None or receipt["target"] != target:
            raise ValueError(f"missing or mismatched per-artifact assessment/target receipt: {path.name}")
        for value in (receipt["outcome"], receipt["limitations"], receipt["review_decisions"]):
            if not value.strip():
                raise ValueError(f"blank receipt assessment field: {path.name}")
        targets.append(target)
        cards.append({
            "type": card["type"],
            "title": card["title"],
            "selected_for_review": True,
            "claims": [{
                "requires_source": True,
                "applicability": card["applicability"]["state"],
                "evidence": [{"source": evidence["source"], "revision": revision, "locator": locator}],
            }],
        })
        artifacts.append({
            "id": f"{evidence['source']}|{revision}|{locator}",
            "source": evidence["source"],
            "revision": revision,
            "locator": locator,
            "state": "synthesized",
            "receipt": {
                "scope": f"{evidence['source']} at {locator}",
                "date": RECEIPT_DATE,
                "reviewer": f"Pi session {RECEIPT_REVIEWER}; not human-authorship attestation",
                "outcome": receipt["outcome"],
                "limitations": receipt["limitations"] + " Review decisions: " + receipt["review_decisions"],
            },
            "targets": [target],
        })
        for match in re.finditer(r"\[[^\]]+\]\(([^)]+)\)", parts[2]):
            link = match.group(1)
            if link.startswith(("http://", "https://")):
                continue
            resolved = (path.parent / link.split("#", 1)[0]).resolve()
            if not resolved.is_relative_to(ROOT) or not resolved.is_file():
                raise ValueError(f"broken or escaping card link in {path.name}: {link}")

    if { (item["source"], item["revision"], item["locator"]) for item in artifacts } != set(receipts):
        raise ValueError("source-artifact assessments and card set are not a bijection")
    coverage = {
        "n": 4,
        "counts": {"not_assessed": 0, "studied": 0, "synthesized": 4, "deferred": 0, "unresolved_eligible": 0},
        "artifacts": artifacts,
        "exclusions": [],
        "unresolved_listings": [],
        "eligible_scope_unknown": False,
    }
    result = validator.validate({"cards": cards, "graph": {"canonical_targets": targets}, "coverage": coverage}, repo_root=ROOT)
    print(json.dumps({
        "adapter": "receipt-bound mapping from four actual card front matters and independent assessment receipt; no new canonical schema",
        "assessment_receipt": RECEIPT_URL,
        "assessor_identity": f"Pi session {RECEIPT_REVIEWER}; not a human identity attestation",
        "framework_profile": "universal-profile-structural-proxy (separate validate-core result required)",
        "mapping": {"n": 4, "state": "synthesized", "artifacts": artifacts},
        "layers": result,
        "limits": ["Structural and declared assessment provenance only; not factual truth, legal clearance, device/runtime behavior, or release eligibility."],
    }, indent=2))
    ok = result["universal"]["status"] == result["consumer"]["status"] == result["graph"]["status"] == "PASS"
    ok = ok and result["consumer"]["coverage"]["n"] == 4 and result["consumer"]["coverage"]["synthesis"] == "4/4"
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
