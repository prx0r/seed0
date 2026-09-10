import subprocess
import sys
import time

sys.path.insert(0, ".")
sys.path.insert(0, "idea0")
sys.path.insert(0, "criteria0")
from validate_idea import validate as validate_idea
from validate_criteria import validate as validate_criteria


def test_idea1_passes_idea0():
    t0 = time.time()
    errs = validate_idea("ideas/idea1.md")
    dt = time.time() - t0
    print(f"\nidea1 validation took {dt*1000:.0f}ms")
    assert errs == [], errs


def test_criteria1_passes_criteria0():
    t0 = time.time()
    errs = validate_criteria("criteria/criteria1.md")
    dt = time.time() - t0
    print(f"\ncriteria1 validation took {dt*1000:.0f}ms")
    assert errs == [], errs


def test_bad_idea_fails(tmp_path):
    bad = tmp_path / "ideaX.md"
    bad.write_text("# X\n\nSome vibes about AI being big.\n")
    errs = validate_idea(str(bad))
    assert any("missing section" in e for e in errs)
    assert any("falsifiable" in e for e in errs)


def test_weasel_criteria_fails(tmp_path):
    bad = tmp_path / "cX.md"
    bad.write_text("| ID | Statement | Verification | Owner |\n"
                   "| C1 | System is robust and good | test `test_x` | human |\n")
    errs = validate_criteria(str(bad))
    assert any("weasel" in e for e in errs)


def test_validators_cli_time_logged():
    for cmd in (["idea0/validate_idea.py", "ideas/idea1.md"],
                ["criteria0/validate_criteria.py", "criteria/criteria1.md"]):
        r = subprocess.run([sys.executable] + cmd, capture_output=True, text=True)
        assert r.returncode == 0, r.stdout
        assert "ms]" in r.stdout  # elapsed always printed = time-to-verify logged


def test_kanban_and_pyeval_methods_accepted(tmp_path):
    from validate_criteria import validate
    good = tmp_path / "c.md"
    good.write_text("| ID | Statement | Verification | Owner |\n"
                    "| C1 | Board task completes | kanban `default/slug` per contract | human |\n"
                    "| C2 | Judge passes cases | pyeval `safety.refusal` evaluator llm-judge | human |\n")
    assert validate(str(good)) == []
    bad = tmp_path / "c2.md"
    bad.write_text("| ID | Statement | Verification | Owner |\n"
                   "| C1 | Board task completes | kanban `noslash` | human |\n"
                   "| C2 | Judge passes | pyeval `nodot` | human |\n")
    errs = validate(str(bad))
    assert any("board/task" in e for e in errs) and any("dataset.case" in e for e in errs)
