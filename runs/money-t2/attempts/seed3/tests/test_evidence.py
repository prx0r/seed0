import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from evidence import append, verify


def test_chain_links_and_verifies(tmp_path, monkeypatch):
    monkeypatch.setenv("EVIDENCE_DIR", str(tmp_path))
    append("start", {"a": 1})
    append("done", {"ok": True})
    rep = verify()
    assert rep["ok"] is True and rep["records"] == 2


def test_tamper_detected(tmp_path, monkeypatch):
    monkeypatch.setenv("EVIDENCE_DIR", str(tmp_path))
    append("start", {"a": 1})
    p = tmp_path / "run.jsonl"
    rec = json.loads(p.read_text().splitlines()[0])
    rec["payload"] = {"a": 999}
    p.write_text(json.dumps(rec) + "\n")
    assert verify()["ok"] is False


def test_reorder_detected(tmp_path, monkeypatch):
    monkeypatch.setenv("EVIDENCE_DIR", str(tmp_path))
    append("one", {})
    append("two", {})
    p = tmp_path / "run.jsonl"
    lines = p.read_text().splitlines()
    p.write_text("\n".join(reversed(lines)) + "\n")
    assert verify()["ok"] is False


def test_empty_log_ok(tmp_path, monkeypatch):
    monkeypatch.setenv("EVIDENCE_DIR", str(tmp_path))
    assert verify()["ok"] is True
