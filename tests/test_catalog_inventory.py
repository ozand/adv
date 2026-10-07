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
        {
            "fid": "a",
            "category": "cardputer",
            "name": "Fork label",
            "github": "https://github.com/Example/Repo.git",
        },
        {
            "fid": "b",
            "category": "cardputer",
            "name": "Other listing",
            "github": "https://github.com/example/repo",
        },
        {
            "fid": "c",
            "category": "stickc",
            "name": "ignored",
            "github": "https://github.com/example/repo",
        },
    ]
    result = MODULE.build_inventory(rows, "fixture")
    assert result["listing_count"] == 2
    assert result["repository_candidate_count"] == 1
    candidate = result["repositories"][0]
    assert candidate["canonical"] == "example/repo"
    assert [row["fid"] for row in candidate["catalog_listings"]] == ["a", "b"]
    assert candidate["status"] == "candidate-unverified"
    assert (
        candidate["local_id"] == MODULE.hashlib.sha256(b"example/repo").hexdigest()[:20]
    )


def test_local_ids_preserve_owner_repository_boundary():
    rows = [
        {
            "fid": "a",
            "category": "cardputer",
            "name": "one",
            "github": "https://github.com/a-b/c",
        },
        {
            "fid": "b",
            "category": "cardputer",
            "name": "two",
            "github": "https://github.com/a/b-c",
        },
    ]
    ids = {
        row["local_id"] for row in MODULE.build_inventory(rows, "fixture")["repositories"]
    }
    assert len(ids) == 2


def test_unresolved_urls_are_explicit():
    rows = [
        {"fid": "a", "category": "cardputer", "name": "No URL", "github": None},
        {
            "fid": "b",
            "category": "cardputer",
            "name": "Account",
            "github": "https://github.com/example",
        },
        {
            "fid": "c",
            "category": "cardputer",
            "name": "Other host",
            "github": "https://gitlab.com/a/b",
        },
        {
            "fid": "d",
            "category": "cardputer",
            "name": "Tree URL",
            "github": "https://github.com/a/b/tree/main",
        },
    ]
    result = MODULE.build_inventory(rows, "fixture")
    assert [row["status"] for row in result["unresolved_listings"]] == [
        "missing-url",
        "account-or-path-only",
        "unsupported-host-or-url",
        "extra-path-unverified",
    ]
    assert result["repository_candidate_count"] == 0


def test_output_paths_default_and_allowed_destinations(tmp_path):
    project = tmp_path / "project"
    (project / "scripts").mkdir(parents=True)
    (project / "sources" / "repo").mkdir(parents=True)

    root, default = MODULE.output_paths(
        project, Path("sources/repo/catalog-candidates.json")
    )
    assert root == (project / "sources" / "repo").resolve()
    assert default == root / "catalog-candidates.json"

    relative = Path("sources/repo/nested/candidates.json")
    assert MODULE.output_paths(project, relative)[1] == (project / relative).resolve()
    absolute = root / "absolute.json"
    assert MODULE.output_paths(project, absolute)[1] == absolute.resolve()


def test_output_paths_reject_traversal_and_outside_targets(tmp_path):
    project = tmp_path / "project"
    (project / "scripts").mkdir(parents=True)
    (project / "sources" / "repo").mkdir(parents=True)
    outside = tmp_path / "outside.json"

    for requested in (Path("sources/repo/../../outside.json"), outside):
        try:
            MODULE.output_paths(project, requested)
        except ValueError:
            pass
        else:
            raise AssertionError(f"accepted out-of-root output: {requested}")
    assert not outside.exists()


def test_output_paths_reject_symlink_escape(tmp_path):
    project = tmp_path / "project"
    allowed = project / "sources" / "repo"
    allowed.mkdir(parents=True)
    outside = tmp_path / "outside"
    outside.mkdir()
    link = allowed / "redirect"
    try:
        link.symlink_to(outside, target_is_directory=True)
    except (OSError, NotImplementedError) as exc:
        import pytest

        pytest.skip(f"directory symlink unavailable: {exc}")

    try:
        MODULE.output_paths(project, Path("sources/repo/redirect/candidates.json"))
    except ValueError:
        pass
    else:
        raise AssertionError("accepted symlink escape")
    assert not (outside / "candidates.json").exists()


def test_output_paths_rejects_sources_root_symlink_escape(tmp_path):
    project = tmp_path / "project"
    project.mkdir()
    outside = tmp_path / "outside"
    outside.mkdir()
    try:
        (project / "sources").symlink_to(outside, target_is_directory=True)
    except (OSError, NotImplementedError) as exc:
        import pytest

        pytest.skip(f"directory symlink unavailable: {exc}")

    try:
        MODULE.output_paths(project, Path("sources/repo/candidates.json"))
    except ValueError:
        pass
    else:
        raise AssertionError("accepted redirected sources root")
    assert not (outside / "repo" / "candidates.json").exists()


def test_output_paths_rejects_repo_root_symlink_escape(tmp_path):
    project = tmp_path / "project"
    allowed_sources = project / "sources"
    allowed_sources.mkdir(parents=True)
    outside = tmp_path / "outside"
    outside.mkdir()
    try:
        (allowed_sources / "repo").symlink_to(outside, target_is_directory=True)
    except (OSError, NotImplementedError) as exc:
        import pytest

        pytest.skip(f"directory symlink unavailable: {exc}")

    try:
        MODULE.output_paths(project, Path("sources/repo/candidates.json"))
    except ValueError:
        pass
    else:
        raise AssertionError("accepted redirected repo root")
    assert not (outside / "candidates.json").exists()


def test_write_inventory_refuses_existing_file_unchanged(tmp_path):
    root = tmp_path / "sources" / "repo"
    root.mkdir(parents=True)
    target = root / "candidates.json"
    target.write_text("keep me", encoding="utf-8")

    try:
        MODULE.write_inventory(root, target, "replace me")
    except FileExistsError:
        pass
    else:
        raise AssertionError("overwrote existing output")
    assert target.read_text(encoding="utf-8") == "keep me"


def test_write_inventory_rejects_parent_symlink_escape_before_write(tmp_path):
    root = tmp_path / "sources" / "repo"
    root.mkdir(parents=True)
    outside = tmp_path / "outside"
    outside.mkdir()
    try:
        (root / "redirect").symlink_to(outside, target_is_directory=True)
    except (OSError, NotImplementedError) as exc:
        import pytest

        pytest.skip(f"directory symlink unavailable: {exc}")

    try:
        MODULE.write_inventory(root, root / "redirect" / "new.json", "payload")
    except ValueError:
        pass
    else:
        raise AssertionError("wrote through symlink escape")
    assert not (outside / "new.json").exists()


def test_snapshot_roundtrip_uses_project_local_root(tmp_path):
    project = tmp_path / "project"
    scripts = project / "scripts"
    scripts.mkdir(parents=True)
    script = scripts / "catalog_inventory.py"
    script.write_text(SCRIPT.read_text(encoding="utf-8"), encoding="utf-8")
    source = tmp_path / "snapshot.json"
    source.write_text(
        json.dumps(
            [
                {
                    "fid": "f",
                    "category": "cardputer",
                    "name": "p",
                    "github": "https://github.com/a/b",
                }
            ]
        )
    )
    import subprocess
    import sys

    subprocess.run([sys.executable, str(script), str(source)], check=True)
    output = project / "sources" / "repo" / "catalog-candidates.json"
    result = json.loads(output.read_text(encoding="utf-8"))
    assert result["listing_count"] == 1
    assert result["repositories"][0]["canonical"] == "a/b"
