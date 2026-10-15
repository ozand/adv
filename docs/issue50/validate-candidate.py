"""Build a transient ADR-012 CLI input from the four Issue #50 concept cards.

Run from any directory with Python and PyYAML available. The adapter reads only
four explicit card paths in this repository; it writes no fixture or source data.
It validates field/link structure and frozen source-to-target mapping, not facts,
rights, publication eligibility, or device behavior.
"""
from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import sys

import yaml

ROOT = Path(__file__).resolve().parents[2]
EXPECTED = {
    "incremental-multiline-repl-assembly.md": ("5d0fef94f389161421b1f7559c15d8303effa7be", "lines 23-90, 116-179"),
    "sd-initialization-frequency-retry.md": ("6a648e32ad54457946ff7eb5a3b55a0dfaaa6cd2", "lines 11-27"),
    "expression-evaluator-pipeline.md": ("d70d88d707f9fd289d096c4295b61159963c9b47", "lines 70-100, 144-188"),
    "cooperative-script-loop-budget.md": ("16e42a58bf67da0a4930ca7f257bdfd5b8c4f254", "lines 41-79, 1138-1145"),
}


def main() -> int:
    validator_path = ROOT / "scripts" / "consumer_validate.py"
    spec = importlib.util.spec_from_file_location("consumer_validate", validator_path)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load the repository's existing consumer validator")
    validator = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(validator)

    files = sorted((ROOT / "kb" / "wiki" / "concepts").glob("*.md"))
    if {path.name for path in files} != set(EXPECTED):
        raise ValueError("Issue #50 concepts directory does not equal the approved four-card set")

    cards = []
    targets = []
    artifacts = []
    for path in files:
        text = path.read_text(encoding="utf-8")
        parts = text.split("---", 2)
        if len(parts) != 3 or parts[0].strip():
            raise ValueError(f"invalid front matter: {path.name}")
        card = yaml.safe_load(parts[1])
        revision, locator = EXPECTED[path.name]
        if card.get("type") != "Concept" or card.get("status") != "draft":
            raise ValueError(f"unexpected type/status: {path.name}")
        if card.get("issue") != "https://github.com/ozand/adv/issues/50":
            raise ValueError(f"wrong governing issue: {path.name}")
        if card.get("applicability", {}).get("state") != "unknown":
            raise ValueError(f"unverified applicability must remain unknown: {path.name}")
        if len(card.get("sources", [])) != 1 or len(card.get("evidence", [])) != 1:
            raise ValueError(f"expected one bounded source/claim record: {path.name}")
        source = card["sources"][0]
        evidence = card["evidence"][0]
        if source.get("revision") != revision or evidence.get("revision") != revision:
            raise ValueError(f"source revision mismatch: {path.name}")
        if evidence.get("locator") != locator or evidence.get("method") != "code-inspected":
            raise ValueError(f"evidence locator/method mismatch: {path.name}")
        if evidence.get("source") != source.get("resource"):
            raise ValueError(f"claim/source mapping mismatch: {path.name}")

        target = path.relative_to(ROOT).as_posix()
        targets.append(target)
        cards.append({
            "type": card["type"],
            "title": card["title"],
            "selected_for_review": True,
            "claims": [{
                "requires_source": True,
                "applicability": card["applicability"]["state"],
                "evidence": [{
                    "source": evidence["source"],
                    "revision": evidence["revision"],
                    "locator": evidence["locator"],
                }],
            }],
        })
        artifact_id = f"{evidence['source']}|{revision}|{locator}"
        artifacts.append({
            "id": artifact_id,
            "source": evidence["source"],
            "revision": revision,
            "locator": locator,
            "state": "synthesized",
            "targets": [target],
        })
        for target_link in __import__("re").finditer(r"\[[^\]]+\]\(([^)]+)\)", parts[2]):
            link = target_link.group(1)
            if link.startswith(("http://", "https://")):
                continue
            resolved = (path.parent / link.split("#", 1)[0]).resolve()
            if not resolved.is_relative_to(ROOT) or not resolved.is_file():
                raise ValueError(f"broken/escaping card link in {path.name}: {link}")

    if len({item["id"] for item in artifacts}) != 4:
        raise ValueError("source-artifact identity is not unique")
    coverage = {
        "n": 4,
        "counts": {"not_assessed": 0, "studied": 0, "synthesized": 4, "deferred": 0, "unresolved_eligible": 0},
        "artifacts": artifacts,
        "exclusions": [],
        "unresolved_listings": [],
        "eligible_scope_unknown": False,
    }
    payload = {"cards": cards, "graph": {"canonical_targets": targets}, "coverage": coverage}
    result = validator.validate(payload, repo_root=ROOT)
    print(json.dumps({
        "adapter": "local AST-like field mapping from four actual OKF front-matters; not a new canonical schema",
        "framework_profile": "universal-profile-structural-proxy (the adapter does not pass its payload through validate-core)",
        "mapping": {"n": 4, "state": "synthesized", "source-revision-locator-to-target": artifacts},
        "layers": result,
        "limits": ["Does not parse full OKF prose or prove factual truth, rights, applicability, publication readiness, or device behavior."],
    }, indent=2))
    if result["universal"]["status"] != "PASS" or result["consumer"]["status"] != "PASS" or result["graph"]["status"] != "PASS":
        return 1
    if result["consumer"]["coverage"]["n"] != 4 or result["consumer"]["coverage"]["synthesis"] != "4/4":
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
