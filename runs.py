"""Run receipts: content-addressed proof that a run happened. Stdlib only.

run_id = sha256(canonical_json(content)) where content EXCLUDES volatile fields
(timestamps, hostnames, latencies, wall times). Same inputs ⇒ same run_id, any
machine, any year. Volatile fields live BESIDE the id inside the receipt.

Receipts land in runs/<run_id>.json (git-tracked ledger). Verification recomputes
the id from content — mismatch means tampering or drift. Mirrors /cg GIT-LEDGER
doctrine, stdlib-only.
"""
from __future__ import annotations
import hashlib
import json
import time
from pathlib import Path

VOLATILE = {"ts", "timestamp", "started_at", "finished_at", "elapsed_s",
            "elapsed_ms", "wall_ms", "hostname", "host", "duration_s"}


def canonical(content: dict) -> str:
    stable = {k: v for k, v in content.items() if k not in VOLATILE}
    return json.dumps(stable, sort_keys=True, default=str)


def run_id(content: dict) -> str:
    return "sha256:" + hashlib.sha256(canonical(content).encode()).hexdigest()


def new_receipt(kind: str, content: dict, root: str = "runs") -> dict:
    body = dict(content)
    body["kind"] = kind
    rid = run_id({**body})
    return {"run_id": rid, "ts": time.time(), "kind": kind, "content": body}


def save(receipt: dict, root: str = "runs") -> Path:
    d = Path(root)
    d.mkdir(parents=True, exist_ok=True)
    p = d / (receipt["run_id"].replace(":", "_") + ".json")
    p.write_text(json.dumps(receipt, indent=1, sort_keys=True))
    return p


def verify(receipt: dict) -> bool:
    return run_id(receipt.get("content", {})) == receipt.get("run_id")


def verify_file(path: str) -> bool:
    return verify(json.loads(Path(path).read_text()))
