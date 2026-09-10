import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from variant import order, score


def test_transitive_shape_and_uses_tasks():
    tasks = [{"id": "t2", "status": "EXECUTING", "acceptance": ["a"]},
             {"id": "t0", "status": "DONE", "acceptance": ["z"]}]
    reqs = [{"id": "B", "unlocks": ["t0"]}, {"id": "A", "unlocks": ["t2"]}]
    assert sorted(order(reqs, tasks)) == ["A", "B"]
    assert score(reqs[1], tasks) > score(reqs[0], tasks)
