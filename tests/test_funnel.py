import json
import sys

sys.path.insert(0, ".")
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
