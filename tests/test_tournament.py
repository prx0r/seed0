import sys

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
