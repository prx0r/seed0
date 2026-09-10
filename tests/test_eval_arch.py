import json
import sys
from pathlib import Path

sys.path.insert(0, ".")
from eval_arch import run_eval


def _seed(tmp_path, name="s9", breakable=True):
    d = tmp_path / name
    (d / "tests").mkdir(parents=True)
    (d / "AGENTS.md").write_text("# A\n")
    (d / "README.md").write_text("# R\n")
    (d / ".env.example").write_text("K=V\n")
    for f in ("docs/README.md", "docs/RECIPES.md", "docs/FILES.md",
              "docs/THREADS.md"):
        p = d / f
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text("# D\n")
    (d / "calc.py").write_text("def add(a, b):\n    return a + b\n")
    (d / "tests" / "test_calc.py").write_text(
        "from calc import add\ndef test_add():\n    assert add(1, 2) == 3\n")
    return str(d)


def _rubric():
    return {"checks": [{"id": "has-calc", "type": "file_exists",
                        "path": "calc.py"}]}


def test_load_bearing_pattern(tmp_path):
    s = _seed(tmp_path)
    rep = run_eval("test-pattern", s, _rubric(), ["calc.py"], "true",
                   str(tmp_path / "out"))
    assert rep["A_pass"] is True and rep["B_pass"] is False
    assert rep["verdict"] == "load-bearing"
    assert (tmp_path / "out" / "eval.json").exists()


def test_inert_pattern(tmp_path):
    s = _seed(tmp_path)
    (Path(s) / "notes.txt").write_text("decorative")
    rep = run_eval("nothing", s, _rubric(), ["notes.txt"], "true",
                   str(tmp_path / "out2"))
    assert rep["verdict"] == "inert-here"


def test_broken_regardless(tmp_path):
    s = _seed(tmp_path)
    (Path(s) / "tests" / "test_calc.py").write_text("def test_x():\n    assert False\n")
    rep = run_eval("broken", s, _rubric(), ["notes-missing.txt"], "true",
                   str(tmp_path / "out3"))
    assert rep["verdict"] == "broken-regardless"
