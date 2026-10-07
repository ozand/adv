#!/usr/bin/env python3
"""Normalize a Launcher catalog snapshot into local-only repository candidates.

The input and output stay outside tracked KB paths. This tool does not clone or
claim that a GitHub URL is a verified repository.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from collections import defaultdict
from pathlib import Path
from urllib.parse import urlparse


def normalize_github(value: str | None) -> tuple[str | None, str | None]:
    """Return canonical owner/repo and a status for a GitHub URL."""
    if not value:
        return None, "missing-url"
    parsed = urlparse(value.strip())
    if parsed.scheme not in ("http", "https") or parsed.hostname not in (
        "github.com",
        "www.github.com",
    ):
        return None, "unsupported-host-or-url"
    parts = [part for part in parsed.path.split("/") if part]
    if len(parts) < 2:
        return None, "account-or-path-only"
    if len(parts) > 2:
        return None, "extra-path-unverified"
    owner, repo = parts[0], re.sub(r"\.git$", "", parts[1], flags=re.I)
    if not owner or not repo or owner in (".", "..") or repo in (".", ".."):
        return None, "invalid-owner-repository"
    return f"{owner}/{repo}".lower(), None


def build_inventory(rows: list[dict], source: str) -> dict:
    """Group listings by candidate repository while preserving every listing."""
    groups: dict[str, list[dict]] = defaultdict(list)
    unresolved = []
    for row in rows:
        if str(row.get("category", "")).casefold() != "cardputer":
            continue
        target, reason = normalize_github(row.get("github"))
        listing = {
            "fid": row.get("fid"),
            "name": row.get("name"),
            "github": row.get("github"),
            "author": row.get("author"),
        }
        if target is None:
            unresolved.append({**listing, "status": reason})
        else:
            groups[target].append(listing)
    repositories = []
    for target, listings in sorted(groups.items()):
        # Hash the canonical identity so the local directory key remains
        # collision-resistant even for unusual punctuation in URL components.
        local_id = hashlib.sha256(target.encode("utf-8")).hexdigest()[:20]
        repositories.append(
            {
                "repository": f"https://github.com/{target}",
                "canonical": target,
                "local_id": local_id,
                "catalog_listings": listings,
                "status": "candidate-unverified",
            }
        )
    return {
        "schema_version": 1,
        "source": source,
        "category": "cardputer",
        "listing_count": sum(map(len, groups.values())) + len(unresolved),
        "repository_candidate_count": len(repositories),
        "repositories": repositories,
        "unresolved_listings": unresolved,
    }


def output_paths(project_root: Path, requested: Path) -> tuple[Path, Path]:
    """Resolve and validate an output destination under the local corpus root."""
    root = project_root.resolve(strict=True)
    configured_root = root / "sources" / "repo"
    allowed_root = configured_root.resolve()
    if allowed_root != configured_root:
        raise ValueError("sources/repo must not redirect through a symlink or junction")

    candidate = requested if requested.is_absolute() else root / requested
    resolved = candidate.resolve()
    if not resolved.is_relative_to(allowed_root):
        raise ValueError("output must resolve beneath the project sources/repo directory")
    return allowed_root, resolved


def write_inventory(output_root: Path, output_path: Path, payload: str) -> None:
    """Create a new inventory file without replacing an existing destination."""
    output_root.mkdir(parents=True, exist_ok=True)
    resolved_root = output_root.resolve(strict=True)
    resolved_output = output_path.resolve()
    if not resolved_output.is_relative_to(resolved_root):
        raise ValueError("output must resolve beneath the project sources/repo directory")
    resolved_output.parent.mkdir(parents=True, exist_ok=True)
    # Re-resolve after creating parents to catch symlink/junction redirection.
    resolved_output = resolved_output.resolve()
    if not resolved_output.is_relative_to(resolved_root):
        raise ValueError("output must resolve beneath the project sources/repo directory")
    with resolved_output.open("x", encoding="utf-8") as stream:
        stream.write(payload)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("snapshot", type=Path, help="Launcher API JSON snapshot")
    parser.add_argument(
        "--output", type=Path, default=Path("sources/repo/catalog-candidates.json")
    )
    args = parser.parse_args()
    project_root = Path(__file__).resolve().parents[1]
    try:
        output_root, output_path = output_paths(project_root, args.output)
    except (OSError, ValueError) as exc:
        raise SystemExit(f"unsafe output path: {exc}") from exc

    rows = json.loads(args.snapshot.read_text(encoding="utf-8"))
    if not isinstance(rows, list):
        raise SystemExit("snapshot must be a JSON array")
    result = build_inventory(rows, str(args.snapshot))
    payload = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    try:
        write_inventory(output_root, output_path, payload)
    except (OSError, ValueError) as exc:
        raise SystemExit(f"could not safely create inventory: {exc}") from exc
    print(
        f"listings={result['listing_count']} repositories={result['repository_candidate_count']} unresolved={len(result['unresolved_listings'])}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
