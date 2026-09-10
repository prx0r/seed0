"""hplane tests: revenue-first rank, dark repos reported, stale flagged."""
import json
import time

from hplane import collect, rank


def _repo(tmp_path, name, requests=(), tasks=()):
    r = tmp_path / name
    (r / "loop").mkdir(parents=True)
    if requests is not None:
        (r / "loop" / "registry_h.jsonl").write_text(
            "\n".join(json.dumps(x) for x in requests) + "\n")
    (r / "loop" / "tasks.jsonl").write_text(
        "\n".join(json.dumps(t) for t in tasks) + ("\n" if tasks else ""))
    return str(r)


def _req(rid, summary, value=0, unlocks=(), age=0, timeout=10**9):
    return {"id": rid, "kind": "request", "h_kind": "approval",
            "summary": summary, "context": "", "options": ["approve"],
            "unlocks": list(unlocks), "urgency": 1, "idempotency_key": rid,
            "value_usd": value,
            "timeout_s": timeout, "ts": time.time() - age, "status": "open"}


def test_revenue_first_unlocks_break_ties(tmp_path):
    a = _repo(tmp_path, "a", [_req("h-1", "rich", value=500),
                              _req("h-2", "unlocky", unlocks=["x"])],
              tasks=[{"id": "x", "status": "EXECUTING", "acceptance": ["a", "b"]}])
    rows = rank(collect([a]))
    assert [r["id"] for r in rows] == ["h-1", "h-2"]  # T0: revenue dominates
    b = _repo(tmp_path, "b", [_req("h-3", "rich-unlocky", value=500,
                                   unlocks=["y"])],
              tasks=[{"id": "y", "status": "EXECUTING", "acceptance": ["a"]}])
    rows = rank(collect([a, b]))
    assert [r["id"] for r in rows][:2] == ["h-3", "h-1"]  # tie -> unlocks


def test_dark_and_stale_surfaced(tmp_path):
    dark = _repo(tmp_path, "dark", None)
    aging = _repo(tmp_path, "old", [_req("h-9", "rotting", age=60, timeout=100)])
    rows = rank(collect([dark, aging]))
    assert rows[0]["status"] == "dark"  # darkness is the top funnel item
    stale = [r for r in rows if r.get("id") == "h-9"][0]
    assert stale["stale"] is True
    fresh = _repo(tmp_path, "new", [_req("h-8", "fresh", age=1, timeout=100)])
    rows = rank(collect([fresh]))
    assert rows[0]["stale"] is False
