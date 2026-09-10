import json
import sys

from funnel import run_funnel, review_template, amend, score_attempt
from seed0 import new


def _idea(tmp_path, n=2):
    seeds = []
    for i in range(n):
        seeds.append(str(new(f"s{i}", "idea", dest=str(tmp_path))))
    return seeds


def test_full_mock_tournament_loop(tmp_path):
    seeds = _idea(tmp_path)
    rubric = {"checks": [{"id": "readme", "type": "file_exists", "path": "README.md"}]}
    out = run_funnel("demo idea", rubric, seeds, "true", str(tmp_path / "run"))
    assert len(out["results"]) == 2
    assert all(r["binary_pass"] for r in out["results"])
    assert (tmp_path / "run" / "scores.jsonl").exists()
    # isolation: attempts contain seed + brief only, no thesis leakage
    att = list((tmp_path / "run" / "attempts" / "s0").iterdir())
    names = {p.name for p in att}
    assert "THESIS.md" not in names and "brief.md" in names and "rubric.json" in names
    # review template + amend flow
    rp = review_template(str(tmp_path / "run"), 1)
    doc = json.loads(rp.read_text())
    assert len(doc["seeds"]) == 2 and doc["seeds"][0]["hypothesis"] == ""
    rec = amend(seeds[0], "1.1", "hypothesis: more docs", str(tmp_path / "run"))
    assert rec["version"] == "1.1"
    assert (tmp_path / "s0" / "VERSION").read_text().strip() == "1.1"


def test_rubric_contains_check(tmp_path):
    seeds = _idea(tmp_path, 1)
    (tmp_path / "s0" / "README.md").write_text("# hi\nmagic-word\n")
    rubric = {"checks": [{"id": "c1", "type": "contains", "path": "README.md",
                          "text": "magic-word"},
                         {"id": "c2", "type": "contains", "path": "README.md",
                          "text": "absent-xyz"}]}
    out = run_funnel("x", rubric, seeds, "true", str(tmp_path / "run2"))
    assert out["results"][0]["rubric"] == {"c1": True, "c2": False}
    assert out["results"][0]["binary_pass"] is False


def test_agent_failure_recorded_not_hidden(tmp_path):
    seeds = _idea(tmp_path, 1)
    out = run_funnel("x", {"checks": []}, seeds, "false", str(tmp_path / "run3"))
    assert out["results"][0]["agent_ok"] is False


def test_blind_review_hides_and_reveals(tmp_path):
    from funnel import review_template, reveal
    (tmp_path / "scores.jsonl").write_text(
        '{"seed": "seed1", "binary_pass": true}\n'
        '{"seed": "seed2", "binary_pass": false}\n')
    p = review_template(str(tmp_path), 1, blind=True)
    doc = json.loads(p.read_text())
    assert doc["blind"] is True
    assert not any("seed1" in json.dumps(e) or "seed2" in json.dumps(e)
                   for e in doc["seeds"])
    assert {e["lane"] for e in doc["seeds"]} == {"Lane A", "Lane B"}
    p2 = review_template(str(tmp_path), 1, blind=True)  # deterministic
    assert json.loads(p2.read_text())["seeds"] == doc["seeds"]
    m = reveal(str(tmp_path), 1)
    assert set(m.values()) == {"Lane A", "Lane B"}
    doc2 = json.loads(p.read_text())
    assert doc2["revealed"] is True
    assert {e["seed"] for e in doc2["seeds"]} == {"seed1", "seed2"}


def test_telemetry_marks_usage_reported():
    from telemetry import Meter
    b = Meter(model="mimo-v2.5").block()
    assert b["usage_source"] == "reported"


def test_blind_scores_view_leaks_nothing(tmp_path):
    from funnel import review_template
    (tmp_path / "scores.jsonl").write_text(
        '{"seed": "seed1", "binary_pass": true, "suite_detail": "7 passed"}\n'
        '{"seed": "seed2", "binary_pass": false, "suite_detail": "1 failed"}\n')
    review_template(str(tmp_path), 1, blind=True)
    blind = [json.loads(l) for l in
             (tmp_path / "scores_blind_r1.jsonl").read_text().splitlines()]
    assert {b["lane"] for b in blind} == {"Lane A", "Lane B"}
    blob = json.dumps(blind)
    assert "seed1" not in blob and "seed2" not in blob
    assert "7 passed" not in blob and "1 failed" not in blob
    assert all(set(b) == {"lane", "binary_pass"} for b in blind)


def test_freeze_run_pins_brief(tmp_path):
    import subprocess as _sp
    from funnel import freeze_run, amend, lane_risk
    repo = tmp_path / "repo"
    (repo / "run").mkdir(parents=True)
    for a in (["init", "-q"], ["config", "user.email", "t@t"],
              ["config", "user.name", "t"], ["branch", "-M", "main"]):
        _sp.run(["git", *a], cwd=repo, check=True, capture_output=True)
    run = repo / "run"
    (run / "brief.md").write_text("# B\n")
    (run / "rubric.json").write_text("{}\n")
    sha = freeze_run(str(run))
    assert len(sha) == 40
    (run / "brief.md").write_text("# B EDITED\n")
    (run / "rubric.json").write_text("{}\n")
    assert "EDITED" in (run / "brief.md").read_text()
    shown = _sp.run(["git", "show", f"{sha}:run/brief.md"], capture_output=True,
                    text=True, cwd=repo).stdout
    assert shown.strip() == "# B"  # frozen copy immune to later edits


def test_lane_risk_phases_overlap(tmp_path):
    from funnel import lane_risk
    a, b, c = (tmp_path / d for d in ("a", "b", "c"))
    for d in (a, b, c):
        d.mkdir()
    (a / "same.py").write_text("x")
    (b / "same.py").write_text("y")
    (c / "solo.py").write_text("z")
    rep = lane_risk([str(a), str(b), str(c)])
    assert any("same.py" in f for v in rep["pairs"].values() for f in v)
    flat = [d for ph in rep["phases"] for d in ph]
    assert sorted(flat) == sorted([str(a), str(b), str(c)])
    assert not any(str(a) in ph and str(b) in ph for ph in rep["phases"])


def test_amend_records_falsifier(tmp_path):
    import json as _json
    from funnel import amend
    s = tmp_path / "seed9"
    s.mkdir()
    rec = amend(str(s), "1.1", "note", falsifier="suite goes red on rerun")
    assert _json.loads((s / "AMENDMENTS.jsonl").read_text().splitlines()[-1])["falsifier"].startswith("suite")


def test_attempt_record_and_spend_lines(tmp_path):
    import json as _json
    from funnel import run_funnel
    seeds = tmp_path / "seeds"
    (seeds / "s1").mkdir(parents=True)
    (seeds / "s1" / "README.md").write_text("# s\n")
    out = run_funnel("idea x", {"checks": []}, ["s1"], "true",
                     str(tmp_path / "run9"), seed_root=str(seeds))
    att = tmp_path / "run9" / "attempts" / "s1"
    rec = _json.loads((att / "attempt.json").read_text())
    assert rec["seed"] == "s1" and len(rec["brief_sha12"]) == 12
    spend = [_json.loads(l) for l in
             (tmp_path / "run9" / "spend.jsonl").read_text().splitlines()]
    assert spend[0]["usage_source"] == "subprocess-unobservable"
    assert spend[0]["input_tokens"] == 0 and spend[0]["elapsed_s"] >= 0


def test_wip_checkpoint_on_timeout(tmp_path):
    from funnel import run_funnel
    seeds = tmp_path / "seeds"
    (seeds / "s1").mkdir(parents=True)
    (seeds / "s1" / "README.md").write_text("# s\n")
    (tmp_path / "sleepy.py").write_text("import time\ntime.sleep(30)\n")
    out = run_funnel("idea x", {"checks": []}, ["s1"],
                     f"python3 {tmp_path / 'sleepy.py'}",
                     str(tmp_path / "run10"), seed_root=str(seeds), timeout_s=1)
    r = out["results"][0]
    assert r["agent_ok"] is False and r["agent_log"] == "agent timeout"
    att = tmp_path / "run10" / "attempts" / "s1"
    import subprocess as _sp
    log = _sp.run(["git", "log", "--oneline"], capture_output=True, text=True,
                  cwd=att).stdout
    assert "wip: agent timeout snapshot" in log


def test_agent_cmd_quoted_survives_split(tmp_path):
    from funnel import run_funnel
    seeds = tmp_path / "seeds"
    (seeds / "s1").mkdir(parents=True)
    (seeds / "s1" / "README.md").write_text("# s\n")
    (tmp_path / "flag.txt").write_text("x\n")
    out = run_funnel("idea x", {"checks": []}, ["s1"],
                     f"python3 -c \"open('{tmp_path}/touched.txt','w').write('1')\"",
                     str(tmp_path / "run11"), seed_root=str(seeds))
    assert out["results"][0]["agent_ok"] is True
    assert (tmp_path / "touched.txt").read_text() == "1"
