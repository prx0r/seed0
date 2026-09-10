"""boot + pulse: clone-to-runtime and one driver iteration."""
import json

import instrument as I


def _reported(tmp_path, complete=True):
    loop = tmp_path / "loop"
    (loop / "a-logs").mkdir(parents=True, exist_ok=True)
    (loop / "reports").mkdir(exist_ok=True)
    (loop / "runs").mkdir(exist_ok=True)
    (loop / "runs" / "sha256_abc123.json").write_text("{}")
    (loop / "reports" / "a-p.md").write_text(
        "# t\n## 1. claim\n## 2. evidence\n## 3. self-review\n## 4. needs\n## 5. cost\n")
    alog = [{"ts": 1, "action": "did it", "covers": [0],
             "evidence": "command:true" if complete else "command:false"}]
    (loop / "a-logs" / "a-p.jsonl").write_text(
        "\n".join(json.dumps(l) for l in alog) + "\n")
    (loop / "tasks.jsonl").write_text(json.dumps(
        {"id": "a-p", "tier": "A", "summary": "provable work",
         "acceptance": ["thing works"], "evidence_required": [],
         "blocked_by": [], "status": "REPORTED",
         "justification": {"parent": "test", "why_now": "test",
                           "why_tier": "test"},
         "cost_note": "$0", "report_ref": "reports/a-p.md",
         "validation_ref": "sha256:abc123"}) + "\n")
    return str(tmp_path)


def test_boot_creates_and_orients(tmp_path):
    b = I.boot(str(tmp_path), session="t")
    assert b["booted"] and b["created_queue"]
    assert b["read"] == ["ATASK.md", "AGENTS.md", "BOOT.md"]
    assert b["suggested_chain"] in ("1", "2", "9")
    b2 = I.boot(str(tmp_path), session="t")
    assert b2["created_queue"] is False  # idempotent


def test_pulse_promotes_proven_reported(tmp_path):
    r = _reported(tmp_path)
    p = I.pulse(r, session="t")
    assert p["promoted"] == ["a-p"]
    recs = [json.loads(l) for l in (tmp_path / "loop" / "tasks.jsonl")
            .read_text().splitlines()]
    assert recs[0]["status"] == "DONE"
    assert (tmp_path / "loop" / "pulse.jsonl").exists()


def test_pulse_nogo_keeps_unproven(tmp_path):
    r = _reported(tmp_path, complete=False)
    p = I.pulse(r, session="t")
    assert p["promoted"] == [] and "a-p" in p["nogo"]
    recs = [json.loads(l) for l in (tmp_path / "loop" / "tasks.jsonl")
            .read_text().splitlines()]
    assert recs[0]["status"] == "REPORTED"  # untouched


def test_pulse_halt_and_legal(tmp_path):
    r = _reported(tmp_path)
    I.pulse(r, session="t")  # promotes a-p; nothing ready after
    p = I.pulse(r, session="t2")
    assert p["halt_legal"] is True and p["orders"] == []
    I.run("0", session="t", root=r)  # halt
    p = I.pulse(r, session="t")
    assert p.get("halted") is True
    I.run("0", session="t", root=r)  # resume
