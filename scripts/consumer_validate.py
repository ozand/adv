"""Read-only validator for caller-selected Cardputer consumer-policy fixtures."""
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from pathlib import Path, PurePosixPath
from typing import Any
from urllib.parse import unquote, urlsplit

VERSION = "1.0"
PROFILE_LABEL = "universal-profile-structural-proxy"
FRAMEWORK_PIN = "73277fdb3e54184901f67268bc676a562b0a677a"
STATES = {"not_assessed", "studied", "synthesized", "deferred", "unresolved_eligible"}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", help="JSON file path, or - for stdin")
    parser.add_argument("--repo-root", help="explicit root for checking caller-listed canonical targets")
    parser.add_argument("--kb-bootstrap-source", help="verified kb-bootstrap Git checkout at ADR-012 pin")
    parser.add_argument("--kb-python", help="Python interpreter for that source checkout")
    args = parser.parse_args(argv)
    try:
        if args.input == "-":
            raw = sys.stdin.read(1_000_001)
        else:
            path = Path(args.input)
            if path.stat().st_size > 1_000_000:
                raise ValueError("input exceeds 1 MiB limit")
            raw = path.read_text(encoding="utf-8")
        if len(raw.encode("utf-8")) > 1_000_000:
            raise ValueError("input exceeds 1 MiB limit")
        report = validate(json.loads(raw), repo_root=Path(args.repo_root).resolve() if args.repo_root else None)
        if args.kb_bootstrap_source or args.kb_python:
            if not args.kb_bootstrap_source or not args.kb_python:
                raise ValueError("both --kb-bootstrap-source and --kb-python are required")
            report["universal"] = run_pinned_universal(
                Path(args.kb_bootstrap_source), args.kb_python, Path(__file__).parents[1]
            )
    except (OSError, UnicodeError, json.JSONDecodeError, ValueError, subprocess.SubprocessError) as exc:
        print(json.dumps({"version": VERSION, "error": str(exc)}, sort_keys=True))
        return 2
    print(json.dumps(report, sort_keys=True))
    return 1 if report["universal"]["status"] == "FAIL" or report["consumer"]["status"] != "PASS" else 0


def run_pinned_universal(source_root: Path, python_exe: str, consumer_root: Path) -> dict[str, Any]:
    """Invoke validate-core from an explicitly verified framework source checkout."""
    if not Path(python_exe).is_file():
        return {"status":"FAIL","profile":f"kb-bootstrap-source:{FRAMEWORK_PIN}","errors":["qualified Python interpreter not found"]}
    if source_root.resolve() != source_root or not source_root.is_dir() or source_root.is_symlink():
        return {"status":"FAIL","profile":f"kb-bootstrap-source:{FRAMEWORK_PIN}","errors":["framework source root must be an existing resolved non-symlink directory"]}
    checks = [("rev-parse", "HEAD")]

    observed: list[str] = []
    for command in checks:
        result = subprocess.run(
            ["git", "-C", str(source_root), *command],
            capture_output=True, text=True, encoding="utf-8", errors="replace",
            timeout=15, check=False,
        )
        if result.returncode != 0:
            return {"status":"FAIL","profile":f"kb-bootstrap-source:{FRAMEWORK_PIN}","errors":["cannot verify framework checkout"]}
        observed.append(result.stdout.strip())
    env = {**os.environ, "PYTHONDONTWRITEBYTECODE":"1"}
    status = subprocess.run(
        ["git", "-C", str(source_root), "status", "--porcelain", "--untracked-files=all"],
        capture_output=True, text=True, encoding="utf-8", errors="replace",
        timeout=15, check=False, env=env,
    )
    if status.returncode != 0 or observed[0] != FRAMEWORK_PIN or status.stdout.strip():
        return {"status":"FAIL","profile":f"kb-bootstrap-source:{FRAMEWORK_PIN}","errors":["framework checkout pin mismatch or source tree has unexpected changes"]}
    code = (
        "import sys; sys.path.insert(0, sys.argv[1]); "
        "import kb_bootstrap; "
        "from pathlib import Path; expected=Path(sys.argv[1]).resolve(); actual=Path(kb_bootstrap.__file__).resolve(); "
        "print(kb_bootstrap.__version__); print(actual); "
        "raise SystemExit(0 if actual.is_relative_to(expected) else 3)"
    )
    identity = subprocess.run(
        [python_exe, "-B", "-c", code, str(source_root)],
        cwd=str(source_root), env=env, capture_output=True, text=True,
        encoding="utf-8", errors="replace", timeout=20, check=False,
    )
    if identity.returncode != 0 or not identity.stdout.splitlines() or identity.stdout.splitlines()[0] != "0.4.0":
        return {"status":"FAIL","profile":f"kb-bootstrap-source:{FRAMEWORK_PIN}","errors":["runtime import does not match pinned framework source/version"]}
    if len(identity.stdout.splitlines()) < 2 or Path(identity.stdout.splitlines()[1]).resolve().parent != (source_root / "kb_bootstrap").resolve():
        return {"status":"FAIL","profile":f"kb-bootstrap-source:{FRAMEWORK_PIN}","errors":["runtime import path is outside pinned framework package"]}
    # The verified source tree is invoked explicitly, never via a global console script.
    cli = (
        "import sys; sys.path.insert(0, sys.argv[1]); "
        "sys.argv=['kb-bootstrap','validate-core','--dir',sys.argv[2]]; "
        "from kb_bootstrap.cli import main; raise SystemExit(main())"
    )
    result = subprocess.run(
        [python_exe, "-B", "-c", cli, str(source_root), str(consumer_root / "kb")],
        cwd=str(source_root), env={**env, "PYTHONDONTWRITEBYTECODE":"1"}, capture_output=True, text=True,
        encoding="utf-8", errors="replace", timeout=120, check=False,
    )
    output = (result.stdout + result.stderr)[-20_000:]
    return {
        "status":"PASS" if result.returncode == 0 else "FAIL",
        "profile":f"kb-bootstrap-validate-core:{FRAMEWORK_PIN}",
        "exit_code":result.returncode,
        "stdout":output,
        "stderr_truncated":len(result.stdout + result.stderr) > 20_000,
    }


def _bounded_shape(value: Any, depth: int = 0) -> None:
    if depth > 32:
        raise ValueError("input exceeds maximum nesting depth 32")
    if isinstance(value, dict):
        if len(value) > 1000:
            raise ValueError("object exceeds 1000 keys")
        for key, child in value.items():
            if not isinstance(key, str):
                raise ValueError("JSON object keys must be strings")
            _bounded_shape(child, depth + 1)
    elif isinstance(value, list):
        if len(value) > 5000:
            raise ValueError("array exceeds 5000 entries")
        for child in value:
            _bounded_shape(child, depth + 1)


def _json_size(value: Any) -> int:
    try:
        return len(json.dumps(value, ensure_ascii=False).encode("utf-8"))
    except (TypeError, ValueError, RecursionError) as exc:
        raise ValueError("input contains unsupported JSON values or excessive nesting") from exc


def validate(data: Any, repo_root: Path | None = None) -> dict[str, Any]:
    if repo_root is not None:
        repo_root = repo_root.resolve()
    if not isinstance(data, dict):
        raise ValueError("input must be a JSON object")
    _bounded_shape(data)
    allowed = {"cards", "graph", "coverage", "qmd"}
    if set(data) - allowed:
        raise ValueError("unsupported top-level key")
    if _json_size(data) > 1_000_000:
        raise ValueError("input exceeds 1 MiB limit")
    universal_errors: list[str] = []
    consumer_errors: list[str] = []
    warnings: list[str] = []
    cards = data.get("cards", [])
    if not isinstance(cards, list):
        raise ValueError("cards must be an array")
    if len(cards) > 1000:
        raise ValueError("cards must have at most 1000 entries")
    for index, card in enumerate(cards):
        if not isinstance(card, dict):
            universal_errors.append(f"cards[{index}]: expected object")
            continue
        kind = card.get("type")
        if not isinstance(kind, str) or not kind.strip():
            universal_errors.append(f"cards[{index}]: type must be a nonempty string")
        consumer_errors.extend(_check_card(card, index, warnings))
    graph = data.get("graph", {})
    if not isinstance(graph, dict):
        raise ValueError("graph must be an object")
    if set(graph) - {"canonical_targets"}:
        raise ValueError("unsupported graph key")
    targets = graph.get("canonical_targets", [])
    if isinstance(targets, list) and len(targets) > 5000:
        raise ValueError("canonical_targets exceeds 5000 entries")
    graph_errors = _check_links(targets, repo_root)
    consumer_errors.extend(graph_errors)
    coverage_errors, coverage_result = _check_coverage(data.get("coverage"), repo_root)
    consumer_errors.extend(coverage_errors)
    qmd = data.get("qmd", {})
    if not isinstance(qmd, dict):
        raise ValueError("qmd must be an object")
    if set(qmd) - {"claim"}:
        raise ValueError("unsupported qmd key")
    qmd_claim = qmd.get("claim")
    if qmd_claim is not None and not isinstance(qmd_claim, str):
        consumer_errors.append("QMD claim label must be a string")
    elif qmd_claim in {"fresh", "retrieved", "truth"}:
        consumer_errors.append("QMD declaration cannot establish freshness, retrieval, or truth")
    consumer_status = "FAIL" if consumer_errors else "PARTIAL" if warnings or coverage_result["state"] == "PARTIAL" else "PASS"
    return {
        "version": VERSION,
        "universal": {"status": "FAIL" if universal_errors else "PASS", "profile": PROFILE_LABEL, "errors": universal_errors},
        "graph": {"status": "FAIL" if graph_errors else "PASS", "errors": graph_errors},
        "consumer": {"status": consumer_status, "errors": consumer_errors, "warnings": warnings, "coverage": coverage_result},
    }


def _check_card(card: dict[str, Any], index: int, warnings: list[str]) -> list[str]:
    errors: list[str] = []
    # ADR-010 keeps object_profile optional and metadata extensible.
    selected, legacy = card.get("selected_for_review", False), card.get("legacy", False)
    if not isinstance(selected, bool) or not isinstance(legacy, bool):
        errors.append(f"cards[{index}]: selection and legacy flags must be boolean")
        selected = legacy = False
    if selected and not legacy and not card.get("title"):
        warnings.append(f"cards[{index}]: adv title recommendation not met")
    claims = card.get("claims", [])
    if not isinstance(claims, list):
        return errors + [f"cards[{index}]: claims must be an array"]
    if len(claims) > 5000:
        return errors + [f"cards[{index}]: claims exceeds 5000 entries"]
    for ci, claim in enumerate(claims):
        prefix = f"cards[{index}].claims[{ci}]"
        if not isinstance(claim, dict):
            errors.append(f"{prefix}: expected object")
            continue
        applicability = claim.get("applicability")
        if applicability is not None and (not isinstance(applicability, str) or applicability not in {"applicable", "not-applicable", "unsupported", "unknown"}):
            errors.append(f"{prefix}: invalid applicability state")
        evidence = claim.get("evidence", [])
        if not isinstance(evidence, list):
            errors.append(f"{prefix}: evidence must be an array")
            continue
        if len(evidence) > 5000:
            errors.append(f"{prefix}: evidence exceeds 5000 entries")
            continue
        required = claim.get("requires_source", False)
        if not isinstance(required, bool):
            errors.append(f"{prefix}: requires_source must be boolean")
            required = False
        if required and not evidence:
            errors.append(f"{prefix}: source evidence required")
        for ei, item in enumerate(evidence):
            if not isinstance(item, dict):
                errors.append(f"{prefix}.evidence[{ei}]: expected object")
                continue
            promotion_basis = item.get("status_promotion_basis")
            if isinstance(promotion_basis, str) and promotion_basis in {"structural_pass", "qmd_presence", "unreviewed"}:
                errors.append(f"{prefix}: invalid status promotion basis")
            if item.get("device_verified") is True and not _has_device_receipt(item):
                errors.append(f"{prefix}: device-verified evidence lacks required receipt fields")
            if required and not all(_nonempty(item.get(key)) for key in ("source", "revision", "locator")):
                errors.append(f"{prefix}: source, revision, and locator are required")
            source_url = item.get("source")
            if isinstance(source_url, str):
                parsed_source = urlsplit(source_url)
                if parsed_source.scheme and (parsed_source.scheme not in {"http", "https"} or not parsed_source.netloc):
                    errors.append(f"{prefix}: source citation must be an HTTP(S) URL when a URL is used")
    return errors


def _has_device_receipt(item: dict[str, Any]) -> bool:
    return all(_nonempty(item.get(key)) for key in ("device_model", "software_revision", "configuration", "procedure", "observed_result", "verifier"))


def _nonempty(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _check_links(targets: Any, repo_root: Path | None = None) -> list[str]:
    if not isinstance(targets, list):
        return ["canonical_targets must be an array"]
    errors = []
    for index, target in enumerate(targets):
        if not isinstance(target, str) or not target:
            errors.append(f"canonical_targets[{index}]: expected nonempty string")
            continue
        parsed = urlsplit(target)
        if parsed.scheme:
            errors.append(f"canonical_targets[{index}]: canonical targets are internal links; use source evidence for external citations")
            continue
        if "\\\\" in target or re.match(r"^(?:[A-Za-z]:|//|\\\\\\\\)", target):
            errors.append(f"canonical_targets[{index}]: Windows drive/UNC/separator form is not allowed")
            continue
        decoded = unquote(target)
        if "\\\\" in decoded or re.match(r"^(?:[A-Za-z]:|//|\\\\\\\\)", decoded):
            errors.append(f"canonical_targets[{index}]: encoded Windows drive/UNC/separator form is not allowed")
            continue
        path = PurePosixPath(decoded)
        if path.is_absolute() or ".." in path.parts or any(part.startswith(".") for part in path.parts):
            errors.append(f"canonical_targets[{index}]: target escapes approved repository content")
            continue
        private_parts = {"sources", "local-lessons", ".search", ".qmd", ".pi", ".agents", ".config", ".claude"}
        if any(part.casefold() in private_parts for part in path.parts):
            errors.append(f"canonical_targets[{index}]: target enters private/local content")
            continue
        if repo_root is None:
            errors.append(f"canonical_targets[{index}]: explicit repository root required to resolve internal target")
            continue
        if repo_root is not None:
            candidate = (repo_root / Path(*path.parts)).resolve()
            try:
                candidate.relative_to(repo_root)
            except ValueError:
                errors.append(f"canonical_targets[{index}]: resolved target escapes repository root")
                continue
            if not candidate.is_file():
                errors.append(f"canonical_targets[{index}]: target does not resolve to a file")
    return errors


def _check_coverage(value: Any, repo_root: Path | None = None) -> tuple[list[str], dict[str, Any]]:
    empty = {"n":0, "assessment":"NOT APPLICABLE", "synthesis":"NOT APPLICABLE", "scope":"KNOWN", "state":"NOT APPLICABLE"}
    if value is None:
        return [], empty
    if not isinstance(value, dict):
        return ["coverage must be an object"], empty
    errors: list[str] = []
    allowed_coverage = {"n", "counts", "artifacts", "exclusions", "unresolved_listings", "eligible_scope_unknown"}
    if set(value) - allowed_coverage:
        return ["unsupported coverage key"], empty
    counts = value.get("counts")
    if not isinstance(counts, dict) or set(counts) != STATES:
        return ["coverage counts must contain exactly the five eligible disposition states"], empty
    if any(not isinstance(n, int) or isinstance(n, bool) or n < 0 for n in counts.values()):
        return ["coverage counts must be nonnegative integers"], empty
    n = sum(counts.values())
    if value.get("n") != n:
        errors.append(f"coverage N must equal disposition partition total {n}")
    exclusions = value.get("exclusions", [])
    if not isinstance(exclusions, list):
        errors.append("coverage exclusions must be an array")
        exclusions = []
    if len(exclusions) > 5000:
        errors.append("coverage exclusions exceed 5000 entries")
        exclusions = exclusions[:5000]
    excluded_ids: set[str] = set()
    for index, exclusion in enumerate(exclusions):
        if not isinstance(exclusion, dict) or not _nonempty(exclusion.get("reason")) or not _nonempty(exclusion.get("id")):
            errors.append(f"coverage.exclusions[{index}]: unique id and explicit reason required")
            continue
        if exclusion["id"] in excluded_ids:
            errors.append(f"coverage.exclusions[{index}]: duplicate excluded id")
        excluded_ids.add(exclusion["id"])
    artifacts = value.get("artifacts", [])
    if not isinstance(artifacts, list):
        return errors + ["coverage artifacts must be an array"], empty
    if len(artifacts) > 5000:
        return errors + ["coverage artifacts exceed 5000 entries"], empty
    seen: dict[tuple[str, str, str], str] = {}
    seen_artifact_ids: set[str] = set()
    actual = {state:0 for state in STATES}
    for index, artifact in enumerate(artifacts):
        prefix = f"coverage.artifacts[{index}]"
        if not isinstance(artifact, dict):
            errors.append(f"{prefix}: expected object")
            continue
        identity = tuple(artifact.get(key) for key in ("source", "revision", "locator"))
        artifact_id = artifact.get("id")
        if not _nonempty(artifact_id):
            errors.append(f"{prefix}: stable artifact id required")
        elif artifact_id in seen_artifact_ids:
            errors.append(f"{prefix}: duplicate artifact id")
        else:
            seen_artifact_ids.add(artifact_id)
        if not all(_nonempty(item) for item in identity):
            errors.append(f"{prefix}: source, revision, and locator required")
            continue
        state = artifact.get("state")
        if not isinstance(state, str) or state not in STATES:
            errors.append(f"{prefix}: invalid disposition state")
            continue
        if identity in seen:
            if seen[identity] != state:
                errors.append(f"{prefix}: duplicate artifact identity has conflicting states")
            continue
        seen[identity] = state
        actual[state] += 1
        if state == "studied" and not _has_assessment_receipt(artifact.get("receipt")):
            errors.append(f"{prefix}: studied state requires receipt")
        if state == "synthesized":
            targets = artifact.get("targets")
            if not isinstance(targets, list) or not targets:
                errors.append(f"{prefix}: synthesized state requires target relation")
            else:
                errors.extend(f"{prefix}: {error}" for error in _check_links(targets, repo_root))
    if actual != counts:
        errors.append("coverage counts differ from distinct artifact records")
    overlap = seen_artifact_ids.intersection(excluded_ids)
    if overlap:
        errors.append("eligible artifact ID cannot also be listed as excluded")
    listings = value.get("unresolved_listings", [])
    if not isinstance(listings, list):
        errors.append("coverage unresolved_listings must be an array")
        listings = []
    for index, listing in enumerate(listings[:5000]):
        if not isinstance(listing, dict) or listing.get("eligibility") != "unknown" or not _nonempty(listing.get("id")):
            errors.append(f"coverage.unresolved_listings[{index}]: id and unknown eligibility required outside N")
    if len(listings) > 5000:
        errors.append("coverage unresolved_listings exceed 5000 entries")
    scope = "PARTIAL" if value.get("eligible_scope_unknown", False) or listings else "KNOWN"
    if not isinstance(value.get("eligible_scope_unknown", False), bool):
        errors.append("eligible_scope_unknown must be boolean")
    if n == 0:
        metrics = {"n":n, "assessment":"NOT APPLICABLE", "synthesis":"NOT APPLICABLE", "scope":scope, "state":"NOT APPLICABLE"}
    else:
        assessed = counts["studied"] + counts["synthesized"]
        synthesis_count = counts['synthesized']
        status = "PARTIAL" if scope == "PARTIAL" or assessed < n else "PASS"
        metrics = {"n":n, "assessment":f"{assessed}/{n}", "synthesis":f"{synthesis_count}/{n}", "scope":scope, "state":status}
    return errors, metrics


def _has_assessment_receipt(receipt: Any) -> bool:
    required = ("scope", "date", "reviewer", "outcome", "limitations")
    return isinstance(receipt, dict) and all(_nonempty(receipt.get(key)) for key in required)


if __name__ == "__main__":
    raise SystemExit(main())
