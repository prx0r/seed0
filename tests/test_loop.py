"""loop.py tests: schema teeth (DONE needs proof), transitions, dogfood queue."""
import json
import subprocess
import sys
from pathlib import Path

from loop import load, problems, save_all


def good_record(i="t1"):
    return {"id": i, "tier": "A", "summary": "s",
            "justification": {"parent": "p", "why_now": "n", "why_tier": "t"},
            "acceptance": ["a1"], "evidence_required": [{"kind": "command", "spec": "c"}],
            "cost_note": "$0", "status": "PROPOSED",
            "report_ref": "", "validation_ref": ""}


def test_done_without_proof_rejected():
    r = good_record()
    r["status"] = "DONE"
    errs = problems(r)
    assert any("validation_ref" in e for e in errs), errs
    r["report_ref"] = "loop/reports/t1.md"
    r["validation_ref"] = "sha256:abc"
    assert problems(r) == []


def test_bad_records_rejected():
    r = good_record()
    r["tier"] = "Z"
    assert any("tier" in e for e in problems(r))
    r2 = good_record()
    r2["justification"] = {"parent": "only"}
    assert any("justification" in e for e in problems(r2))
    r3 = good_record()
    r3["acceptance"] = []
    assert any("acceptance" in e for e in problems(r3))


def test_add_list_transition_roundtrip(tmp_path):
    q = str(tmp_path / "tasks.jsonl")
    loop_py = str(Path(__file__).resolve().parent.parent / "loop.py")
    run = lambda *a: subprocess.run(
        [sys.executable, loop_py, *a, "--queue", q],
        capture_output=True, text=True, cwd=tmp_path)
    assert run("init").returncode == 0
    rec = good_record("demo")
    assert run("add", "--record", json.dumps(rec)).returncode == 0
    assert run("add", "--record", json.dumps(rec)).returncode == 1  # dup
    bad = good_record("bad")
    bad["status"] = "DONE"
    assert run("add", "--record", json.dumps(bad)).returncode == 1  # no proof
    assert run("set-status", "demo", "BOGUS").returncode == 2
    assert run("set-status", "demo", "DONE").returncode == 1  # guard holds
    assert run("set-status", "demo", "EXECUTING").returncode == 0
    out = run("list")
    assert "EXECUTING" in out.stdout and "demo" in out.stdout
    assert run("check").returncode == 0


def test_live_queue_passes_check():
    root = Path(__file__).resolve().parent.parent
    r = subprocess.run([sys.executable, "loop.py", "check"],
                       capture_output=True, text=True, cwd=root)
    assert r.returncode == 0, r.stdout  # our own queue eats its own dogfood


def test_reported_requires_existing_report(tmp_path):
    r = good_record("rep")
    r["status"] = "REPORTED"
    assert any("REPORTED" in e for e in problems(r)), "missing ref must fail"
    r["report_ref"] = "loop/reports/ghost.md"
    assert any("REPORTED" in e for e in problems(r)), "ghost file must fail"
    real = tmp_path / "r.md"
    real.write_text("# proof\n")
    r["report_ref"] = str(real)
    assert problems(r) == []


def test_set_field_revalidates(tmp_path):
    import subprocess as sp
    q = str(tmp_path / "tasks.jsonl")
    run = lambda *a: sp.run(
        [sys.executable, str(Path(__file__).resolve().parent.parent / "loop.py"),
         *a, "--queue", q], capture_output=True, text=True, cwd=tmp_path)
    assert run("init").returncode == 0
    rec = good_record("s1")
    rec["status"] = "EXECUTING"
    assert run("add", "--record", json.dumps(rec)).returncode == 0
    assert run("set", "s1", "report_ref", "--value", '"ghost.md"').returncode == 0
    assert run("set-status", "s1", "REPORTED").returncode == 1  # ghost fails
    real = tmp_path / "r.md"
    real.write_text("# proof\n")
    assert run("set", "s1", "report_ref", "--value", json.dumps(str(real))).returncode == 0
    assert run("set-status", "s1", "REPORTED").returncode == 0


def test_alog_stoplight_go_nogo(tmp_path):
    from loop import alog, stoplight, save_all
    q = tmp_path / "tasks.jsonl"
    rec = dict(good_record("sl"), acceptance=["a0", "a1", "a2"],
               status="REPORTED", report_ref="r.md",
               validation_ref="sha256:x")
    (tmp_path / "r.md").write_text("# rep\n")
    save_all([rec], str(q))
    alog("sl", "ran suite", [0], "50 green", queue_path=str(q))
    alog("sl", "validator re-run", [1], "exit 0", queue_path=str(q))
    rep = stoplight("sl", str(q))
    assert rep["go"] is False and any("acceptance[2]" in m for m in rep["missing"])
    alog("sl", "banked receipt", [2], "sha256:x", queue_path=str(q))
    rep = stoplight("sl", str(q))
    assert rep["go"] is True, rep
    assert stoplight("ghost", str(q))["go"] is False


def _mk(tmp_path, tid, status="JUSTIFIED", blocked=()):
    import subprocess as sp
    r = dict(good_record(tid), status=status)
    if blocked:
        r["blocked_by"] = list(blocked)
    return r


def test_ready_lists_only_unblocked(tmp_path):
    from loop import save_all
    import subprocess as sp
    q = str(tmp_path / "tasks.jsonl")
    save_all([_mk(tmp_path, "aaa"), _mk(tmp_path, "bbb", blocked=("aaa",))], q)
    out = sp.run([sys.executable, str(Path(__file__).resolve().parent.parent / "loop.py"),
                  "ready", "--queue", q], capture_output=True, text=True,
                 cwd=tmp_path).stdout
    assert "aaa" in out and "bbb" not in out


def test_branch_creates_and_resumes(tmp_path):
    import subprocess as sp
    repo = tmp_path / "repo"
    repo.mkdir()
    sp.run(["git", "init", "-q"], cwd=repo, check=True)
    sp.run(["git", "config", "user.email", "t@t"], cwd=repo, check=True)
    sp.run(["git", "config", "user.name", "t"], cwd=repo, check=True)
    (repo / "f.txt").write_text("x\n")
    sp.run(["git", "add", "."], cwd=repo, check=True)
    sp.run(["git", "commit", "-qm", "init"], cwd=repo, check=True)
    sp.run(["git", "branch", "-M", "main"], cwd=repo, check=True)
    q = str(tmp_path / "tasks.jsonl")
    from loop import save_all, load
    save_all([_mk(tmp_path, "w1")], q)
    lp = str(Path(__file__).resolve().parent.parent / "loop.py")
    r1 = sp.run([sys.executable, lp, "branch", "w1", "--repo", str(repo),
                 "--queue", q], capture_output=True, text=True, cwd=tmp_path)
    assert r1.returncode == 0 and "branched tasks/w1" in r1.stdout, r1.stderr
    assert load(q)[0]["branch"] == "tasks/w1"
    r2 = sp.run([sys.executable, lp, "branch", "w1", "--repo", str(repo),
                 "--queue", q], capture_output=True, text=True, cwd=tmp_path)
    assert "resumed tasks/w1" in r2.stdout


def test_history_base_rates(tmp_path):
    from loop import save_all, alog
    import subprocess as sp
    q = str(tmp_path / "tasks.jsonl")
    save_all([_mk(tmp_path, "amend-one", status="DONE"),
              _mk(tmp_path, "amend-two", status="REJECTED"),
              _mk(tmp_path, "other", status="DONE")], q)
    out = sp.run([sys.executable, str(Path(__file__).resolve().parent.parent / "loop.py"),
                  "history", "--like", "amend", "--queue", q],
                 capture_output=True, text=True, cwd=tmp_path).stdout
    rep = json.loads(out)
    assert rep["n"] == 2 and rep["by_status"] == {"DONE": 1, "REJECTED": 1}
    assert rep["base_rate_done"] == 0.5


def test_evidence_reexecuted_not_trusted(tmp_path):
    from loop import alog, stoplight, save_all
    q = tmp_path / "tasks.jsonl"
    rec = dict(good_record("ev"), acceptance=["a0"],
               status="REPORTED", report_ref="r.md",
               validation_ref="sha256:x")
    (tmp_path / "r.md").write_text("# rep\n")
    (tmp_path / "real.txt").write_text("x\n")
    save_all([rec], str(q))
    alog("ev", "ran green cmd", [0], "", "command:python3 -c 'pass'",
         queue_path=str(q))
    assert stoplight("ev", str(q))["go"] is True
    alog("ev", "claimed red cmd", [0], "", "command:python3 -c 'import sys; sys.exit(1)'",
         queue_path=str(q))
    rep = stoplight("ev", str(q))
    assert rep["go"] is False and any("exit 1" in m for m in rep["missing"])


def test_replan_breaker_trips_to_human(tmp_path):
    from loop import save_all, replan
    q = str(tmp_path / "tasks.jsonl")
    rec = dict(good_record("rp"), status="EXECUTING")
    save_all([rec], q)
    from loop import load
    recs = load(q)
    for i in (1, 2, 3):
        out = replan(recs, "rp", f"try {i} failed")
        assert out == {"ok": True, "replans": i, "status": "PROPOSED"}, out
    out = replan(recs, "rp", "try 4")
    assert out["ok"] is False and out.get("escalate") is True
    assert "breaker tripped" in out["error"]
    assert replan(recs, "ghost", "x")["ok"] is False


def test_metrics_and_leafcheck(tmp_path):
    from loop import save_all, plan_metrics, leafcheck, alog
    q = str(tmp_path / "tasks.jsonl")
    good = dict(good_record("m1"), status="DONE", report_ref="r.md",
                validation_ref="s:1",
                evidence_required=[{"kind": "command", "spec": "c"}],
                acceptance=["a0"])
    (tmp_path / "r.md").write_text("# r\n")
    bad = dict(good_record("m2"), status="DONE", report_ref="r.md",
               validation_ref="s:2",
               evidence_required=[{"kind": "review", "spec": "looks good"}],
               acceptance=["a0", "a1"])
    save_all([good, bad], q)
    alog("m1", "did", [0], queue_path=q)
    m = plan_metrics([good, bad], q)
    assert m["tasks"] == 2 and m["done_fully_covered"] == "1/2", m
    assert leafcheck(good) == []
    errs = leafcheck(bad)
    assert any("non-primitive" in e for e in errs), errs
    assert any("leaf not mappable" in e for e in errs), errs


def test_public_api_intact():
    import loop as _lp
    for name in ("load", "problems", "save_all", "alog", "alog_read",
                 "stoplight", "check_evidence", "replan", "plan_metrics",
                 "leafcheck", "main"):
        assert callable(getattr(_lp, name, None)), f"missing API: {name}"


def _lp():
    return str(Path(__file__).resolve().parent.parent / "loop.py")


def test_promote_requires_lowest_barrier_form(tmp_path):
    import subprocess as sp
    q = str(tmp_path / "tasks.jsonl")
    rec = dict(good_record("pa"), status="EXECUTING")
    from loop import save_all
    save_all([rec], q)
    base = [sys.executable, _lp(), "promote", "pa", "--queue", q]
    r = sp.run(base + ["--barrier", "need key"], capture_output=True, text=True, cwd=tmp_path)
    assert r.returncode == 1 and "lowest-barrier" in r.stdout
    r = sp.run(base + ["--barrier", "need key",
                       "--steps-json", '["open example.com/signup", "paste key here"]'],
               capture_output=True, text=True, cwd=tmp_path)
    assert r.returncode == 1 and "lowest-barrier" in r.stdout
    r = sp.run(base + ["--barrier", "need key",
                       "--steps-json", '["open example.com/signup", "paste key here"]',
                       "--send-back", "the api key"],
               capture_output=True, text=True, cwd=tmp_path)
    assert r.returncode == 0 and "promoted pa -> h-" in r.stdout, r.stdout
    from loop import load
    t = load(q)[0]
    assert t["status"] == "PAUSED" and t["need"].startswith("h-")
    reg = list((tmp_path / "loop" / "registry_h.jsonl").read_text().splitlines())
    h = __import__("json").loads(reg[-1])
    assert h["from_task"] == "pa" and h["promoted"] is True
    assert h["exact_steps"] == ["open example.com/signup", "paste key here"]
    assert h["send_back"] == "the api key"


def test_ingest_stores_lists_sections_and_dedupes(tmp_path):
    from loop import ingest_spec
    q = str(tmp_path / "tasks.jsonl")
    Path(str(tmp_path)).mkdir(parents=True, exist_ok=True)
    text = "# Big spec\n\n## Payments\n\n## Auth\n\nbody\n"
    r1 = ingest_spec("ingest1", text, queue_path=q)
    assert r1["sections"] == ["Payments", "Auth"] and r1["lines"] == 7
    r2 = ingest_spec("ingestX", text, queue_path=q)
    assert r2["duplicate_of"] == "ingest1"  # same bytes, any name


def test_goalcheck_traces_or_fails(tmp_path):
    from loop import goalcheck
    q = str(tmp_path / "tasks.jsonl")
    Path(str(tmp_path)).mkdir(parents=True, exist_ok=True)
    (tmp_path / "tasks.jsonl").write_text("")
    from loop import ingest_spec as _ing
    _ing("ingest1", "# S\n\n## Payments\n", queue_path=q)
    good = {"id": "g", "ingest": "ingest1",
            "acceptance": ["charge works [spec:Payments]"]}
    assert goalcheck(good, q) == []
    bad = {"id": "g", "ingest": "ingest1",
           "acceptance": ["charge works [spec:Refunds]", "no cite here"]}
    errs = goalcheck(bad, q)
    assert any("Refunds" in e for e in errs) and any("no [spec" in e for e in errs)
    assert goalcheck({"id": "g", "acceptance": []}, q) == [
        "no ingest linked (goal must restate a stored spec)"]


def test_map_renders_dag_with_branches():
    from loop import render_map
    recs = [{"id": "g", "status": "DONE", "branch": "tasks/g", "blocked_by": []},
            {"id": "a", "status": "EXECUTING", "blocked_by": ["g"]},
            {"id": "b", "status": "JUSTIFIED", "blocked_by": ["a", "ghost"]}]
    out = render_map(recs)
    assert "[x] g @tasks/g" in out
    assert "[ ] b" in out
    lines = out.splitlines()
    assert lines.index(next(l for l in lines if " g @" in l)) < lines.index(
        next(l for l in lines if l.rstrip().endswith(" a")))


def test_context_levels_nest(tmp_path):
    import subprocess as sp
    import json as _json
    q = tmp_path / "tasks.jsonl"
    from loop import save_all
    save_all([dict(good_record("c1"), status="JUSTIFIED"),
              _mk(tmp_path, "c2", blocked=("c1",))], str(q))
    (tmp_path / "packet.json").write_text(_json.dumps(
        {"done": ["x"], "blocked_on": [{"queue": "H9"}]}))
    lp = str(Path(__file__).resolve().parent.parent / "loop.py")

    def run(*a):
        return sp.run([sys.executable, lp, *a, "--queue", str(q)],
                      capture_output=True, text=True, cwd=tmp_path)
    l0 = run("context", "--level", "L0").stdout
    l1 = run("context", "--level", "L1").stdout
    assert "done=1" in l0 and "ready=" not in l0
    assert "ready=['c1']" in l1 and "c2" not in l1.split("paused=")[0].split("ready=")[1]
    assert run("context", "--level", "L2").stdout.count("- c") >= 1
    assert '"id": "c2"' in run("context", "--level", "L3").stdout


def test_rollback_restores_and_refuses_dirty(tmp_path):
    import subprocess as sp
    repo = tmp_path / "repo"
    repo.mkdir()
    for a in (["init", "-q"], ["config", "user.email", "t@t"],
              ["config", "user.name", "t"], ["branch", "-M", "main"]):
        sp.run(["git", *a], cwd=repo, check=True, capture_output=True)
    (repo / "loop").mkdir()
    q = repo / "loop" / "tasks.jsonl"
    from loop import save_all
    save_all([dict(good_record("r1"), status="DONE")], str(q))
    sp.run(["git", "add", "-A"], cwd=repo, check=True, capture_output=True)
    sp.run(["git", "commit", "-qm", "v1"], cwd=repo, check=True, capture_output=True)
    sha = sp.run(["git", "rev-parse", "HEAD"], capture_output=True, text=True,
                 cwd=repo).stdout.strip()
    save_all([dict(good_record("r1"), status="DONE"),
              dict(good_record("r2"), status="EXECUTING")], str(q))
    sp.run(["git", "add", "-A"], cwd=repo, check=True, capture_output=True)
    sp.run(["git", "commit", "-qm", "v2"], cwd=repo, check=True, capture_output=True)
    lp = str(Path(__file__).resolve().parent.parent / "loop.py")

    def run(*a):
        return sp.run([sys.executable, lp, *a, "--queue", str(q)],
                      capture_output=True, text=True, cwd=repo)
    (repo / "dirty.txt").write_text("x")
    assert run("rollback", "--ref", sha).returncode == 1  # dirty refuses
    (repo / "dirty.txt").unlink()
    assert run("rollback", "--ref", sha).returncode == 0
    import json as _json
    assert [_json.loads(l)["id"] for l in q.read_text().splitlines()] == ["r1"]


def test_evidence_memo_skips_unchanged_inputs(tmp_path):
    from loop import check_evidence
    src = tmp_path / "src.py"
    src.write_text("v1\n")
    hit = tmp_path / "hit.txt"
    ev = f"command:python3 -c \"import pathlib; pathlib.Path('{hit}').write_text('x')\" || inputs:src.py"
    base = tmp_path / "loop"
    base.mkdir()
    assert check_evidence(ev, base) is None
    assert hit.exists()
    hit.unlink()
    assert check_evidence(ev, base) is None  # skipped: inputs unchanged
    assert not hit.exists()
    src.write_text("v2\n")  # input changed -> re-runs
    assert check_evidence(ev, base) is None
    assert hit.exists()


def test_heuristics_distills_self_reviews(tmp_path):
    from loop import save_all
    import subprocess as sp
    q = tmp_path / "tasks.jsonl"
    (tmp_path / "r.md").write_text("# R\n\n## 1. claim\nx\n\n## 3. self-review\nNever trust covers tags alone.\nAll good.\n\n## 4. needs\n")
    rec = dict(good_record("h1"), status="DONE", report_ref="r.md",
               validation_ref="s:1")
    save_all([rec], str(q))
    r = sp.run([sys.executable, str(Path(__file__).resolve().parent.parent / "loop.py"),
                "heuristics", "--queue", str(q)],
               capture_output=True, text=True, cwd=tmp_path)
    assert r.returncode == 0, r.stderr
    body = (tmp_path / "heuristics.md").read_text()
    assert "Never trust covers tags alone" in body and "(from h1)" in body


def test_done_requires_resolvable_receipt(tmp_path):
    import subprocess as sp
    q = tmp_path / "tasks.jsonl"
    rec = dict(good_record("rz"), status="REPORTED", report_ref="r.md",
               validation_ref="sha256:deadbeef-no-such-file")
    (tmp_path / "r.md").write_text("# r\n")
    from loop import save_all
    save_all([rec], str(q))
    lp = str(Path(__file__).resolve().parent.parent / "loop.py")
    r = sp.run([sys.executable, lp, "set-status", "rz", "DONE",
                "--queue", str(q)], capture_output=True, text=True, cwd=tmp_path)
    assert r.returncode == 1 and "no receipt file" in r.stdout
