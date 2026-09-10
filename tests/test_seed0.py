import subprocess
import sys

import pytest

sys.path.insert(0, ".")
from seed0 import check, new


def test_good_fixture_compliant():
    rep = check("tests/fixtures/good")
    assert rep["compliant"] is True, rep["checks"]


def test_bad_fixture_fails_with_reasons():
    rep = check("tests/fixtures/bad")
    assert rep["compliant"] is False
    failed = {c["check"] for c in rep["checks"] if not c["pass"]}
    assert {"required-files", "tests-exist", "no-committed-secrets"} <= failed


def test_new_scaffold_is_compliant(tmp_path):
    out = new("demo", "a demo project", dest=str(tmp_path))
    assert (out / "AGENTS.md").read_text().startswith("# AGENTS.md — demo")
    rep = check(str(out))
    assert rep["compliant"] is True, rep["checks"]
    r = subprocess.run([sys.executable, "-m", "pytest", "tests/", "-q"],
                       cwd=out, capture_output=True, text=True)
    assert r.returncode == 0, r.stdout[-500:]
