import json
import sys

from learn import collect, propose, normalize_sig


def _run(tmp_path, scores, reviews=None):
    (tmp_path / "scores.jsonl").write_text(
        "\n".join(json.dumps(r) for r in scores) + "\n")
    if reviews:
        (tmp_path / "review_r1.json").write_text(json.dumps(reviews))
    return str(tmp_path)


def _fail(seed, **kw):
    r = {"seed": seed, "binary_pass": False, "rubric": {}, "suite_green": True,
         "compliant": True, "agent_ok": True}
    r.update(kw)
    return r


def test_shared_rubric_failure_proposes_criteria11(tmp_path):
    d = _run(tmp_path, [
        _fail("s1", rubric={"c1": False, "c2": True}),
        _fail("s2", rubric={"c1": False, "c2": True}),
        _fail("s3", rubric={"c2": False})])
    rep = propose(collect(d), min_seeds=2)
    kinds = {p["signature"]: p["proposal"] for p in rep["proposals"]}
    assert kinds.get("rubric:c1") == "criteria1.1 row"
    assert "rubric:c2" not in kinds  # only one seed — below threshold
    assert rep["proposals"][0]["id"].startswith("CR-1.1-")


def test_shared_suite_failure_proposes_global_lesson(tmp_path):
    d = _run(tmp_path, [
        _fail("s1", suite_green=False, suite_detail="ModuleNotFoundError: foo"),
        _fail("s2", suite_green=False, suite_detail="ModuleNotFoundError: foo")])
    rep = propose(collect(d), min_seeds=2)
    assert any(p["proposal"] == "criteria0 rule" for p in rep["proposals"])
    assert len(rep["global_lessons"]) == 1


def test_review_verdicts_feed_in(tmp_path):
    d = _run(tmp_path, [_fail("s1")], reviews={
        "round": 1, "seeds": [
            {"seed": "s1", "verdict": "augment", "hypothesis": "needs retries"},
            {"seed": "s2", "verdict": "augment", "hypothesis": "needs retries"}]})
    rep = propose(collect(d), min_seeds=2)
    assert any(p["signature"].startswith("review:") for p in rep["proposals"])


def test_normalize_strips_ids():
    assert normalize_sig("token abc123 failed") == normalize_sig("token def456 failed")
