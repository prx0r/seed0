#!/usr/bin/env python3
"""hinbox.py — H-registry + pollable inbox. Stdlib only.

Turn-safe by construction: the agent NEVER blocks waiting for a human.
It files requests (append-only), goes away, and `poll()`s on later pulses.
The human resolves via hqueue.html (or any client of the same JSONL).

Record kinds in loop/registry_h.jsonl:
  request    — {id, kind:"request", h_kind, summary, context, options,
                unlocks:[a-task ids], urgency, idempotency_key, timeout_s,
                ts, status:"open"}  (status is write-once here)
  resolution — {id, kind:"resolution", supersedes, decision, note, by, ts}
  expiry     — {kind:"expiry", supersedes, ts} (materialized by poll())

pending() = open requests minus superseded ones, priority-sorted.
Priority = sum of values of transitively unlocked unfinished A-tasks, where
value(task) = 1 + len(acceptance), walking blocked_by edges from tasks in
loop/tasks.jsonl (extra keys allowed). This IS the human's queue order.
"""
from __future__ import annotations
import hashlib
import json
import secrets
import time
from pathlib import Path

HREG = "loop/registry_h.jsonl"
OPEN = "open"
DECISIONS = {"approved", "denied", "answered"}


def _read(path: str | None = None) -> list[dict]:
    path = path or HREG
    p = Path(path)
    if not p.exists():
        return []
    return [json.loads(l) for l in p.read_text().splitlines() if l.strip()]


def _append(rec: dict, path: str | None = None) -> dict:
    path = path or HREG
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    with open(path, "a") as f:
        f.write(json.dumps(rec, sort_keys=True) + "\n")
    return rec


def new_request(summary: str, context: str = "", h_kind: str = "approval",
                options: list | None = None, unlocks: list | None = None,
                urgency: int = 1, timeout_s: int = 86400,
                idempotency_key: str = "", from_task: str = "",
                exact_steps: list | None = None, send_back: str = "",
                grant: dict | None = None,
                path: str | None = None) -> dict:
    """File a request. Same idempotency_key returns the existing record.

    Promotion rule (HAM): human-ready requests carry from_task (the blocked
    A-task id), exact_steps (the lowest-barrier form: exact pages + exact
    instructions), and send_back (what the human returns, e.g. a pasted key).
    Direct filing without these is allowed but flagged unpromoted — the
    human queue sorts promoted first.
    """
    key = idempotency_key or hashlib.sha256(summary.encode()).hexdigest()[:16]
    for r in _read(path):
        if r.get("kind") == "request" and r.get("idempotency_key") == key:
            return r
    rec = {"id": "h-" + secrets.token_hex(4), "kind": "request",
           "h_kind": h_kind, "summary": summary, "context": context,
           "options": options or ["approve", "deny"],
           "unlocks": unlocks or [], "urgency": urgency,
           "idempotency_key": key, "timeout_s": timeout_s,
           "from_task": from_task, "exact_steps": exact_steps or [],
           "send_back": send_back, "grant": grant or {},
           "promoted": bool(from_task and exact_steps and send_back),
           "ts": time.time(), "status": OPEN}
    return _append(rec, path)


def _superseded(recs: list[dict]) -> set[str]:
    return {r["supersedes"] for r in recs
            if r.get("kind") in ("resolution", "expiry") and r.get("supersedes")}


def poll(path: str | None = None, queue_path: str = "loop/tasks.jsonl",
         now: float | None = None) -> list[dict]:
    """Materialize expiries, then return open requests priority-sorted."""
    now = time.time() if now is None else now
    recs = _read(path)
    done = _superseded(recs)
    for r in recs:
        if (r.get("kind") == "request" and r["id"] not in done
                and now - r.get("ts", now) > r.get("timeout_s", 86400)):
            rec = {"id": "h-" + secrets.token_hex(4), "kind": "expiry",
                   "supersedes": r["id"], "ts": now}
            _append(rec, path)
            done.add(r["id"])
    tasks = []
    try:
        tasks = [json.loads(l) for l in Path(queue_path).read_text().splitlines()
                 if l.strip()]
    except Exception:
        pass
    out = [dict(r, priority_score=priority_score(r, tasks))
           for r in _read(path)
           if r.get("kind") == "request" and r["id"] not in _superseded(_read(path))]
    out.sort(key=lambda r: (-r["priority_score"], r["ts"]))
    return out


def resolve(rid: str, decision: str, note: str = "", by: str = "human",
            path: str | None = None, mreg_path: str | None = None) -> dict:
    path = path or HREG
    """Resolve a request (append-only resolution record). B5 wiring: an
    approved request carrying a grant spec activates the grant inline, so
    the human button press IS the exact-amount release. Denials and
    grant-less requests resolve with no money movement. Activation failure
    is recorded on the resolution (never silent), and the decision stands
    while spend stays locked."""
    if decision not in DECISIONS:
        raise ValueError(f"decision must be one of {sorted(DECISIONS)}")
    recs = _read(path)
    req = next((r for r in recs
                if r.get("kind") == "request" and r.get("id") == rid), None)
    if req is None:
        raise KeyError(f"unknown request: {rid}")
    if rid in _superseded(recs):
        raise ValueError(f"already resolved: {rid}")
    rec = {"id": "h-" + secrets.token_hex(4), "kind": "resolution",
           "supersedes": rid, "decision": decision,
           "note": note, "by": by, "ts": time.time()}
    spec = req.get("grant") or {}
    if decision == "approved" and spec:
        try:
            from grants import new_grant, activate
            kw = {} if mreg_path is None else {"path": mreg_path}
            g = new_grant(int(spec["amount_cents"]), str(spec["purpose"]),
                          str(spec.get("recipient", "")),
                          expiry_s=int(spec.get("expiry_s", 86400)),
                          approved_by=by, **kw)
            activate(g["id"], by=by, **kw)
            rec["grant_id"] = g["id"]
        except Exception as e:
            rec["grant_error"] = f"{type(e).__name__}: {e}"[:160]
    return _append(rec, path)


def priority_score(h: dict, tasks: list[dict]) -> float:
    """Unlock value: BFS from h.unlocks through blocked_by edges (unfinished only)."""
    by_id = {t.get("id"): t for t in tasks}
    dependents: dict[str, list[str]] = {}
    for t in tasks:
        for b in t.get("blocked_by", []) or []:
            dependents.setdefault(b, []).append(t.get("id"))
    seen, frontier = set(), list(h.get("unlocks", []) or [])
    total = 0.0
    while frontier:
        cur = frontier.pop()
        if cur in seen:
            continue
        seen.add(cur)
        for dep in dependents.get(cur, []):
            t = by_id.get(dep, {})
            if t and t.get("status") != "DONE" and dep not in seen:
                total += 1 + len(t.get("acceptance", []) or [])
                frontier.append(dep)
    direct = sum(1 for u in (h.get("unlocks", []) or [])
                 if by_id.get(u, {}).get("status", "OPEN") != "DONE")
    value = float(h.get("value_usd") or 0)  # policy: $1 expected = 1pt
    return round(total + direct + 0.5 * (h.get("urgency", 1) or 0) + value, 2)
