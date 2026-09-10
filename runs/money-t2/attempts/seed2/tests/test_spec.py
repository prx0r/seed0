import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
from spec_check import check


def test_example_spec_passes():
    root = Path(__file__).resolve().parent.parent
    assert check(str(root / "SPEC.md")) == []


def test_missing_owner_and_method_fail(tmp_path):
    bad = tmp_path / "SPEC.md"
    bad.write_text("| ID | Statement | Verification | Owner |\n"
                   "| AC-1 | Does stuff | trust me | TBD |\n")
    errs = check(str(bad))
    assert any("owner" in e for e in errs)


def test_dangling_test_reference_fails(tmp_path):
    bad = tmp_path / "SPEC.md"
    (tmp_path / "tests").mkdir()
    bad.write_text("| ID | Statement | Verification | Owner |\n"
                   "| AC-1 | Does stuff | test `test_nothing` | human |\n")
    assert any("no test" in e for e in check(str(bad)))


def test_missing_demo_script_fails(tmp_path):
    bad = tmp_path / "SPEC.md"
    bad.write_text("| ID | Statement | Verification | Owner |\n"
                   "| AC-1 | Does stuff | demo scripts/gone.sh | human |\n")
    assert any("demo script" in e for e in check(str(bad)))
