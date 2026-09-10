import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from ralph import Plan, run_once


def test_next_and_mark(tmp_path):
    p = tmp_path / "plan.md"
    p.write_text("- [x] done thing\n- [ ] next thing\n- [ ] later\n")
    plan = Plan(p)
    assert plan.next_task() == "next thing"
    assert plan.mark_done("next thing") is True
    assert plan.next_task() == "later"
    assert plan.mark_done("nope") is False


def test_run_once_gate_red_leaves_open(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    (tmp_path / "plan.md").write_text("- [ ] thing\n")
    (tmp_path / "tests").mkdir()
    res = run_once("plan.md", agent_cmd="echo", verify_cmd="python3 -c 'import sys; sys.exit(1)'")
    assert res["ok"] is False and Plan("plan.md").next_task() == "thing"


def test_run_once_green_marks_done(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    (tmp_path / "plan.md").write_text("- [ ] thing\n")
    res = run_once("plan.md", agent_cmd="echo", verify_cmd="python3 -c 'pass'")
    assert res["ok"] is True and Plan("plan.md").next_task() is None


def test_empty_plan(tmp_path):
    p = tmp_path / "plan.md"
    p.write_text("- [x] all done\n")
    assert Plan(p).next_task() is None


def test_run_once_anchored_foreign_cwd(tmp_path, monkeypatch):
    import json as _json
    from ralph import run_once as _run
    work = tmp_path / "proj"
    (work / "tests").mkdir(parents=True)
    (work / "plan.md").write_text("- [ ] thing\n")
    (tmp_path / "far").mkdir()
    monkeypatch.chdir(tmp_path / "far")  # foreign CWD: must not matter
    (tmp_path / "unrelated.md").write_text("- [ ] decoy\n")
    res = _run(str(work / "plan.md"), agent_cmd="echo",
               verify_cmd="python3 -c 'pass'", workdir=str(work))
    assert res["ok"] is True
    assert "decoy" not in (work / "plan.md").read_text()
    assert "- [x] thing" in (work / "plan.md").read_text()
    lines = (work / "attempts.jsonl").read_text().splitlines()
    assert len(lines) == 1 and _json.loads(lines[0])["ok"] is True


def test_attempt_log_records_red_gate(tmp_path):
    import json as _json
    from ralph import run_once as _run
    work = tmp_path / "proj2"
    (work / "tests").mkdir(parents=True)
    (work / "plan.md").write_text("- [ ] thing\n")
    res = _run(str(work / "plan.md"), agent_cmd="echo",
               verify_cmd="python3 -c 'import sys; sys.exit(1)'",
               workdir=str(work))
    assert res["ok"] is False
    lines = (work / "attempts.jsonl").read_text().splitlines()
    assert len(lines) == 1 and _json.loads(lines[0])["ok"] is False
