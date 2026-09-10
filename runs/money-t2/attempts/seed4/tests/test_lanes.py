import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
from lane_check import load, check_table, owner_of


def test_example_lanes_valid():
    root = Path(__file__).resolve().parent.parent
    lanes = load(str(root / "LANES.md"))
    assert check_table(lanes) == []
    assert owner_of(lanes, "app/api/server.py") == "api"
    assert owner_of(lanes, "static/logo.png") == "web"
    assert owner_of(lanes, "docs/RECIPES.md") == "docs"
    assert owner_of(lanes, "mystery/file.py") is None


def test_duplicate_and_overlap_fail():
    bad = [{"lane": "a", "owner": "x", "paths": ["app/**"]},
           {"lane": "a", "owner": "y", "paths": ["app/**"]}]
    errs = check_table(bad)
    assert any("duplicate" in e for e in errs)
    assert any("overlap" in e for e in errs)


def test_missing_owner_fails():
    assert any("owner" in e for e in
               check_table([{"lane": "a", "owner": "TBD", "paths": ["x"] }]))
