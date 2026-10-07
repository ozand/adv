import importlib.util
import json
from pathlib import Path

SCRIPT = Path(__file__).parents[1] / "scripts" / "catalog_inventory.py"
SPEC = importlib.util.spec_from_file_location("catalog_inventory", SCRIPT)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


def test_groups_repeated_listing_without_losing_identity():
    rows = [
        {"fid": "a", "category": "cardputer", "name": "Fork label",
         "github": "https://github.com/Example/Repo.git"},
        {"fid": "b", "category": "cardputer", "name": "Other listing",
         "github": "https://github.com/example/repo"},
        {"fid": "c", "category": "stickc", "name": "ignored",
         "github": "https://github.com/example/repo"},
    ]
    result = MODULE.build_inventory(rows, "fixture")
    assert result["listing_count"] == 2
    assert result["repository_candidate_count"] == 1
    candidate = result["repositories"][0]
    assert candidate["canonical"] == "example/repo"
    assert [row["fid"] for row in candidate["catalog_listings"]] == ["a", "b"]
    assert candidate["status"] == "candidate-unverified"
    assert candidate["local_id"] == "example--repo"


def test_local_ids_preserve_owner_repository_boundary():
    rows = [
        {"fid": "a", "category": "cardputer", "name": "one",
         "github": "https://github.com/a-b/c"},
        {"fid": "b", "category": "cardputer", "name": "two",
         "github": "https://github.com/a/b-c"},
    ]
    ids = {row["local_id"] for row in MODULE.build_inventory(rows, "fixture")["repositories"]}
    assert ids == {"a-b--c", "a--b-c"}


def test_unresolved_urls_are_explicit():
    rows = [
        {"fid": "a", "category": "cardputer", "name": "No URL", "github": None},
        {"fid": "b", "category": "cardputer", "name": "Account", "github": "https://github.com/example"},
        {"fid": "c", "category": "cardputer", "name": "Other host", "github": "https://gitlab.com/a/b"},
        {"fid": "d", "category": "cardputer", "name": "Tree URL", "github": "https://github.com/a/b/tree/main"},
    ]
    result = MODULE.build_inventory(rows, "fixture")
    assert [row["status"] for row in result["unresolved_listings"]] == [
        "missing-url", "account-or-path-only", "unsupported-host-or-url",
        "extra-path-unverified"
    ]
    assert result["repository_candidate_count"] == 0


def test_snapshot_roundtrip(tmp_path):
    source = tmp_path / "snapshot.json"
    output = tmp_path / "sources" / "repo" / "candidates.json"
    source.write_text(json.dumps([{"fid": "f", "category": "cardputer",
                                  "name": "p", "github": "https://github.com/a/b"}]))
    import subprocess
    import sys
    subprocess.run([sys.executable, str(SCRIPT), str(source), "--output", str(output)], check=True)
    result = json.loads(output.read_text())
    assert result["listing_count"] == 1
    assert result["repositories"][0]["canonical"] == "a/b"
