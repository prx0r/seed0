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


def _gitrepo(path, files):
    import subprocess as sp
    path.mkdir(parents=True)
    for a in (["init", "-q"], ["config", "user.email", "t@t"],
              ["config", "user.name", "t"], ["branch", "-M", "main"]):
        sp.run(["git", *a], cwd=path, check=True, capture_output=True)
    (path / ".keep").write_text("x\n")
    for rel, content in files.items():
        p = path / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(content)
    sp.run(["git", "add", "-A"], cwd=path, check=True, capture_output=True)
    sp.run(["git", "commit", "-qm", "init"], cwd=path, check=True, capture_output=True)
    return path


def test_sync_clones_and_refreshes(tmp_path):
    import subprocess as sp
    from hplane import sync, collect, rank
    import hinbox
    src = _gitrepo(tmp_path / "src", {})
    (src / "loop").mkdir()
    hinbox.new_request("remote fix?", unlocks=[],
                       path=str(src / "loop" / "registry_h.jsonl"))
    (src / "loop" / "tasks.jsonl").write_text("")
    sp.run(["git", "add", "-A"], cwd=src, check=True, capture_output=True)
    sp.run(["git", "commit", "-qm", "queue"], cwd=src, check=True, capture_output=True)
    rem = tmp_path / "remotes.txt"
    rem.write_text(f"vps9-demo|{src}\n")
    out = sync(str(rem), str(tmp_path / "mirrors"))
    assert out[0]["ok"] is True and out[0]["op"] == "cloned"
    rows = rank(collect([f"vps9-demo|{tmp_path}/mirrors/vps9-demo|vps9"]))
    opens = [r for r in rows if r["status"] == "open"]
    assert len(opens) == 1 and opens[0]["repo"] == "vps9-demo"
    assert opens[0]["box"] == "vps9"
    # second sync fetches; broken remote records error without raising
    out = sync(str(rem), str(tmp_path / "mirrors"))
    assert out[0] == [r for r in out if r["label"] == "vps9-demo"][0]
    assert out[0]["ok"] is True and out[0]["op"] == "fetched"
    (tmp_path / "remotes2.txt").write_text("dead|/tmp/definitely-not-here-xyz\n")
    bad = sync(str(tmp_path / "remotes2.txt"), str(tmp_path / "mirrors2"))
    assert bad[0]["ok"] is False and "error" in bad[0]
