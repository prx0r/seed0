"""Human vs agent task feeds with predicted-data reconciliation. Stdlib only.

The core loop this enables: an agent hits a human block (credential, decision,
access), files a HUMAN task with a PREDICTED payload, keeps working all AGENT
tasks against the prediction, and when the human delivers, reconcile() swaps
predicted->real and returns exactly what must re-run. No stalled agents, no
silent goal-guessing.

Task record:
  {id, kind: human|agent, status: open|predicted|done|expired, summary,
   needed_from, options[], recommendation, payload (predicted or real),
   predicted: bool, blocked_by: [ids], receipts[], created, expires}
"""
from __future__ import annotations
import json
import time
import uuid
from pathlib import Path


def new_task(kind: str, summary: str, needed_from: str = "human",
             options: list | None = None, recommendation: str = "",
             blocked_by: list | None = None, ttl_s: float = 86400) -> dict:
    assert kind in ("human", "agent")
    now = time.time()
    return {"id": "T-" + uuid.uuid4().hex[:8].upper(), "kind": kind,
            "status": "open", "summary": summary, "needed_from": needed_from,
            "options": options or [], "recommendation": recommendation,
            "payload": None, "predicted": False,
            "blocked_by": blocked_by or [], "receipts": [],
            "created": now, "expires": now + ttl_s}


class Feed:
    """Two feeds, one file. Persisted JSONL so crashes lose nothing."""

    def __init__(self, path: str | Path = "tasks.jsonl"):
        self.path = Path(path)
        self.tasks: dict[str, dict] = {}
        if self.path.exists():
            for line in self.path.read_text().splitlines():
                try:
                    t = json.loads(line)
                    self.tasks[t["id"]] = t
                except Exception:
                    continue

    def _save(self, t: dict):
        self.tasks[t["id"]] = t
        with open(self.path, "a") as f:
            f.write(json.dumps(t) + "\n")

    def add(self, task: dict) -> dict:
        task["status"] = "open"
        self._save(task)
        return task

    def human_tasks(self, include_done=False) -> list[dict]:
        return [t for t in self.tasks.values() if t["kind"] == "human"
                and (include_done or t["status"] in ("open", "predicted"))]

    def agent_tasks(self, runnable_only=True) -> list[dict]:
        out = []
        for t in self.tasks.values():
            if t["kind"] != "agent" or t["status"] not in ("open", "predicted"):
                continue
            if runnable_only and any(self.tasks.get(b, {}).get("status") == "open"
                                     and not self.tasks.get(b, {}).get("predicted")
                                     for b in t.get("blocked_by", [])):
                continue
            out.append(t)
        return out

    def predict(self, task_id: str, mock_payload, note: str = "") -> dict:
        """Attach predicted data so dependents keep moving. Marks predicted."""
        t = self.tasks[task_id]
        t["payload"] = mock_payload
        t["predicted"] = True
        t["status"] = "predicted"
        t["receipts"].append({"t": time.time(), "event": "predicted", "note": note})
        self._save(t)
        return t

    def deliver(self, task_id: str, real_payload, receipt: str = "") -> dict:
        """Human delivers. Flips predicted->real. Does NOT auto-rerun."""
        t = self.tasks[task_id]
        was_predicted = t.get("predicted", False)
        t["payload"] = real_payload
        t["predicted"] = False
        t["status"] = "done"
        t["receipts"].append({"t": time.time(), "event": "delivered",
                              "receipt": receipt, "was_predicted": was_predicted})
        self._save(t)
        return t

    def reconcile(self, task_id: str) -> list[dict]:
        """After deliver(): every task that consumed the prediction must re-run.

        Returns affected agent tasks (predicted inputs). Caller re-verifies them;
        nothing silently passes on stale mock data."""
        t = self.tasks[task_id]
        affected = [x for x in self.tasks.values()
                    if task_id in x.get("blocked_by", [])
                    and x.get("status") in ("open", "predicted", "done")]
        for x in affected:
            x["status"] = "open"
            x["receipts"].append({"t": time.time(),
                                  "event": "reverify",
                                  "reason": f"{task_id} real data landed"})
            self._save(x)
        return affected

    def expire(self) -> list[dict]:
        """Expired human tasks re-escalate loudly. Never auto-approve."""
        now = time.time()
        out = []
        for t in self.tasks.values():
            if t["kind"] == "human" and t["status"] in ("open", "predicted") \
                    and t["expires"] < now:
                t["status"] = "open"
                t["receipts"].append({"t": now, "event": "expired-re-escalated"})
                self._save(t)
                out.append(t)
        return out
