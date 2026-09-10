import io
import json
import sys
import urllib.request

sys.path.insert(0, ".")
from pyeval import run, grade_rule


class FakeResp:
    def __init__(self, payload):
        self._b = json.dumps(payload).encode()

    def __enter__(self):
        return self

    def __exit__(self, *a):
        return False

    def read(self):
        return self._b


def _stub(monkeypatch, answers):
    calls = {"n": 0}

    def fake_open(req, timeout=None):
        body = json.loads(req.data.decode())
        text = answers[min(calls["n"], len(answers) - 1)]
        calls["n"] += 1
        msg = body["messages"][-1]["content"]
        assert "sk-" not in msg and "OPENCODE_GO" not in msg  # key never in body
        return FakeResp({"choices": [{"message": {"content": text}}]})

    monkeypatch.setattr(urllib.request, "urlopen", fake_open)
    return calls


def test_rule_and_judge_paths(tmp_path, monkeypatch):
    ds = tmp_path / "d.json"
    ds.write_text(json.dumps({"cases": [
        {"id": "r1", "input": "q", "expect": {"contains": ["hello"]},
         "evaluator": "rule", "weight": 1},
        {"id": "j1", "input": "q", "evaluator": "judge", "rubric": "R",
         "weight": 2}]}))
    _stub(monkeypatch, ["hello there", "VERDICT: PASS. Reason: fine"])
    rep = run(str(ds), "m", "http://x", "k")
    assert rep["pass"] is True and rep["score"] == 3.0


def test_judge_fail_and_transport_error(tmp_path, monkeypatch):
    ds = tmp_path / "d.json"
    ds.write_text(json.dumps({"cases": [
        {"id": "j1", "input": "q", "evaluator": "judge", "rubric": "R",
         "weight": 1}]}))
    _stub(monkeypatch, ["blah", "VERDICT: FAIL. Reason: bad"])
    rep = run(str(ds), "m", "http://x", "k")
    assert rep["pass"] is False

    def boom(req, timeout=None):
        raise ConnectionError("down")

    monkeypatch.setattr(urllib.request, "urlopen", boom)
    rep2 = run(str(ds), "m", "http://x", "k")
    assert rep2["results"][0]["pass"] is False
    assert "transport" in rep2["results"][0]["why"]


def test_grade_rule_contract():
    ok, _ = grade_rule("Costs £950-£1400 depending on scope",
                       {"contains": ["£"], "absent": ["guaranteed"]})
    assert ok is True
    ok, why = grade_rule("Guaranteed £950 total", {"absent": ["guaranteed"]})
    assert ok is False and "forbidden" in why
