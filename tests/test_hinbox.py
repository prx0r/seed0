"""hinbox.py tests: idempotency, resolve-once, expiry, unlock priority."""
import json

import pytest

from hinbox import new_request, poll, resolve, priority_score


def test_idempotent_filing(tmp_path):
    p = str(tmp_path / "h.jsonl")
    a = new_request("approve push?", path=p)
    b = new_request("approve push?", path=p)
    assert a["id"] == b["id"]
    assert len([l for l in open(p).read().splitlines()]) == 1


def test_resolve_once_and_unknown(tmp_path):
    p = str(tmp_path / "h.jsonl")
    r = new_request("ok?", path=p)
    resolve(r["id"], "approved", note="lgtm", path=p)
    assert poll(p) == []
    with pytest.raises(ValueError):
        resolve(r["id"], "denied", path=p)
    with pytest.raises(KeyError):
        resolve("h-nope", "approved", path=p)
    with pytest.raises(ValueError):
        new_request("x", path=p) and resolve(
            new_request("y", path=p)["id"], "maybe", path=p)


def test_expiry_materializes(tmp_path):
    p = str(tmp_path / "h.jsonl")
    r = new_request("stale?", timeout_s=10, path=p)
    assert len(poll(p, now=r["ts"] + 5)) == 1
    assert poll(p, now=r["ts"] + 99) == []
    kinds = [json.loads(l)["kind"] for l in open(p).read().splitlines()]
    assert "expiry" in kinds


def graph():
    return [
        {"id": "a", "status": "DONE", "acceptance": ["x"]},
        {"id": "b", "status": "EXECUTING", "acceptance": ["x", "y"],
         "blocked_by": ["a"]},
        {"id": "c", "status": "PROPOSED", "acceptance": ["x"],
         "blocked_by": ["b"]},
        {"id": "d", "status": "PROPOSED", "acceptance": ["x"]},
    ]


def test_priority_unlock_value_transitive():
    tasks = graph()
    hi_b = {"unlocks": ["b"], "urgency": 1}   # unlocks b -> transitively c
    hi_d = {"unlocks": ["d"], "urgency": 1}   # unlocks d only
    hi_a = {"unlocks": ["a"], "urgency": 1}   # a DONE: transitive b,c still count
    sb, sd, sa = (priority_score(hi_b, tasks), priority_score(hi_d, tasks),
                  priority_score(hi_a, tasks))
    assert sb > sd > 0, (sb, sd)
    assert sa > 0  # DONE node itself scores 0 direct but unlocks live dependents


def test_poll_order_is_priority(tmp_path):
    p = str(tmp_path / "h.jsonl")
    q = tmp_path / "tasks.jsonl"
    q.write_text("\n".join(json.dumps(t) for t in graph()) + "\n")
    small = new_request("small thing", unlocks=["d"], path=p)
    big = new_request("big unlock", unlocks=["b"], path=p)
    order = [r["id"] for r in poll(p, queue_path=str(q))]
    assert order == [big["id"], small["id"]]
