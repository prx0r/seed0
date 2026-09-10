import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from variant import NaiveInbox


def test_naive_appends():
    box = NaiveInbox()
    box.file("a", key="k")
    box.file("a", key="k")
    assert len(box.records) == 2
