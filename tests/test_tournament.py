import sys
from pathlib import Path

from seed0 import new
from tournament import leaderboard, score_seed


def test_tournament_ranks_working_seed_first(tmp_path):
    new("good", "a good idea", dest=str(tmp_path))
    (tmp_path / "bad").mkdir()  # empty: nothing built
    rows = leaderboard([str(tmp_path / "bad"), str(tmp_path / "good")])
    assert [r["seed"] for r in rows] == ["good", "bad"]
    assert rows[0]["compliant"] is True and rows[0]["tests_green"] is True


def test_score_seed_marks_missing_suite(tmp_path):
    (tmp_path / "empty").mkdir()
    r = score_seed(str(tmp_path / "empty"))
    assert r["tests_green"] is None and r["compliant"] is False


def test_weights_recorded_and_reorder(tmp_path):
    from tournament import leaderboard
    a = tmp_path / "a"
    b = tmp_path / "b"
    a.mkdir()
    b.mkdir()
    (a / "AGENTS.md").write_text("x")
    rows = leaderboard([str(a), str(b)],
                       meta={"__weights__": {"tests_green": 1, "compliant": 100,
                                             "evidence": 0}})
    assert rows[0]["weights"] == {"tests_green": 1.0, "compliant": 100.0,
                                  "evidence": 0.0}
    assert all("rank_score" in r for r in rows)


def test_cli_weights_value_not_scored_as_seed(tmp_path):
    import json as _json
    import subprocess as _sp
    for d in ("s1", "s2"):
        (tmp_path / d).mkdir()
    w = tmp_path / "weights.json"
    w.write_text(_json.dumps({"tests_green": 100, "compliant": 10, "evidence": 1}))
    r = _sp.run([sys.executable, str(Path(__file__).resolve().parent.parent / "tournament.py"), str(tmp_path / "s1"),
                 str(tmp_path / "s2"), "--weights", str(w)],
                capture_output=True, text=True,
                cwd=tmp_path)  # cwd=tmp: tournament jsonl + receipts land outside the repo
    assert r.returncode == 0, r.stderr
    ranked = [l for l in r.stdout.splitlines() if l.startswith("#")]
    assert len(ranked) == 2, r.stdout
    assert "weights.json" not in r.stdout


def test_notes_flag_attaches_verdict(tmp_path):
    import subprocess as _sp
    repo = tmp_path / "repo"
    repo.mkdir()
    for a in (["init", "-q"], ["config", "user.email", "t@t"],
              ["config", "user.name", "t"], ["branch", "-M", "main"]):
        _sp.run(["git", *a], cwd=repo, check=True, capture_output=True)
    for d in ("s1", "s2"):
        (repo / d).mkdir()
        (repo / d / "AGENTS.md").write_text("x\n")
    _sp.run(["git", "add", "-A"], cwd=repo, check=True, capture_output=True)
    _sp.run(["git", "commit", "-qm", "init"], cwd=repo, check=True, capture_output=True)
    r = _sp.run([sys.executable, str(Path(__file__).resolve().parent.parent / "tournament.py"),
                 "s1", "s2", "--notes", "scores-test"],
                capture_output=True, text=True, cwd=repo)
    assert r.returncode == 0 and "noted." in r.stdout, r.stderr
    from gitnotes import read
    note = read(str(repo), "HEAD", "scores-test")
    assert note and note["kind"] == "tournament" and "top" in note
