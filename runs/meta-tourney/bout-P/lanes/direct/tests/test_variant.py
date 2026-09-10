import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from variant import order


def test_direct_shape_and_stability():
    reqs = [{"id": "B", "unlocks": ["t4"]}, {"id": "A", "unlocks": ["t2"]}]
    assert order(reqs) == order(reqs)
    assert sorted(order(reqs)) == ["A", "B"]
