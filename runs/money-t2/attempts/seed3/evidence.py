"""Hash-chained evidence log. Stdlib only.

Each record: {seq, ts, event, payload, prev, digest} where digest = sha256 of
the canonical record WITHOUT digest. verify() replays the file: order, linkage,
recomputed digests. Tampering (edit/delete/reorder) breaks verification.
"""
from __future__ import annotations
import hashlib
import json
import os
import time
from pathlib import Path


def _dir() -> Path:
    d = Path(os.getenv("EVIDENCE_DIR", "evidence"))
    d.mkdir(parents=True, exist_ok=True)
    return d


def _digest(rec: dict) -> str:
    return "sha256:" + hashlib.sha256(
        json.dumps(rec, sort_keys=True, default=str).encode()).hexdigest()


def append(event: str, payload: dict | None = None,
           log: str = "run.jsonl") -> dict:
    path = _dir() / log
    prev = "GENESIS"
    seq = 0
    if path.exists():
        lines = path.read_text().splitlines()
        if lines:
            last = json.loads(lines[-1])
            prev, seq = last["digest"], last["seq"] + 1
    rec = {"seq": seq, "ts": time.time(), "event": event,
           "payload": payload or {}, "prev": prev}
    rec["digest"] = _digest(rec)
    with open(path, "a") as f:
        f.write(json.dumps(rec) + "\n")
    return rec


def verify(log: str = "run.jsonl") -> dict:
    path = _dir() / log
    if not path.exists():
        return {"ok": True, "records": 0, "detail": "empty log"}
    prev, n = "GENESIS", 0
    for line in path.read_text().splitlines():
        try:
            rec = json.loads(line)
        except Exception:
            return {"ok": False, "records": n, "detail": f"unparseable line {n}"}
        if rec.get("seq") != n or rec.get("prev") != prev:
            return {"ok": False, "records": n, "detail": f"chain break at seq {n}"}
        want = _digest({k: v for k, v in rec.items() if k != "digest"})
        if rec.get("digest") != want:
            return {"ok": False, "records": n, "detail": f"digest mismatch seq {n}"}
        prev, n = rec["digest"], n + 1
    return {"ok": True, "records": n, "detail": f"{n} linked records"}
