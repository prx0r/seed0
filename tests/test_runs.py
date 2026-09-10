import json
import sys

from runs import new_receipt, save, verify, verify_file, run_id


def test_receipt_deterministic_and_volatile_excluded():
    a = new_receipt("t", {"x": 1})
    import time
    time.sleep(0.01)
    b = new_receipt("t", {"x": 1})
    assert a["run_id"] == b["run_id"]  # timestamps beside id, not inside
    assert verify(a) is True and verify(b) is True


def test_tamper_breaks_verify():
    r = new_receipt("t", {"x": 1})
    r["content"]["x"] = 2
    assert verify(r) is False


def test_save_and_verify_file(tmp_path):
    r = new_receipt("t", {"x": [1, 2]})
    p = save(r, root=str(tmp_path))
    assert verify_file(str(p)) is True
    assert run_id({"x": 1}) == run_id({"x": 1, "ts": 999})  # volatile excluded


def test_verify_all_counts(tmp_path):
    from runs import new_receipt, save, verify_all
    r1 = new_receipt("t", {"a": 1})
    save(r1, root=str(tmp_path))
    rep = verify_all(str(tmp_path))
    assert rep == {"files": 1, "valid": 1, "invalid": []}
    (tmp_path / "sha256_deadbeef.json").write_text("{bad json")
    rep = verify_all(str(tmp_path))
    assert rep["files"] == 2 and len(rep["invalid"]) == 1
