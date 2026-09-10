import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from variant import file_storm


def test_keyed_storm_collapses(tmp_path):
    recs = file_storm(str(tmp_path / "h.jsonl"), "s", "k", 3)
    assert len({r["id"] for r in recs}) == 1
