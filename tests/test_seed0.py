import subprocess
from pathlib import Path
import sys

import pytest

from seed0 import check, new


def test_good_fixture_compliant():
    rep = check(str(Path(__file__).resolve().parent.parent / "tests" / "fixtures" / "good"))
    assert rep["compliant"] is True, rep["checks"]


def test_bad_fixture_fails_with_reasons():
    # Standalone, the bad fixture IS a project with a committed secret —
    # the fixtures skip only applies when checking the seed0 repo itself.
    rep = check(str(Path(__file__).resolve().parent.parent / "tests" / "fixtures" / "bad"))
    assert rep["compliant"] is False
    failed = {c["check"] for c in rep["checks"] if not c["pass"]}
    assert {"required-files", "tests-exist", "no-committed-secrets"} <= failed


def test_repo_root_skips_own_fixtures_but_nothing_else():
    root = Path(__file__).resolve().parent.parent
    rep = check(str(root))
    sec = next(c for c in rep["checks"] if c["check"] == "no-committed-secrets")
    assert sec["pass"] is True and "skipped" in sec["detail"], sec


def test_real_secret_outside_fixtures_still_trips_scanner(tmp_path):
    out = new("leaky", "a leaky project", dest=str(tmp_path))
    (out / "oops.py").write_text("KEY = 'sk-" + "abc123XYZ4567890'\n")
    rep = check(str(out))
    sec = next(c for c in rep["checks"] if c["check"] == "no-committed-secrets")
    assert sec["pass"] is False and "oops.py" in sec["detail"]


def test_new_scaffold_is_compliant(tmp_path):
    out = new("demo", "a demo project", dest=str(tmp_path))
    assert (out / "AGENTS.md").read_text().startswith("# AGENTS.md — demo")
    rep = check(str(out))
    assert rep["compliant"] is True, rep["checks"]
    r = subprocess.run([sys.executable, "-m", "pytest", "tests/", "-q"],
                       cwd=out, capture_output=True, text=True)
    assert r.returncode == 0, r.stdout[-500:]
