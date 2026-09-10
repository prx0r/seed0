"""Ralph loop: next unchecked plan item, one agent run, gate, mark done. Stdlib.

1.1: run_once takes workdir (all paths + subprocess anchored — CWD-fragility
kills: bout1 seed5, gate saga x10) and appends every iteration to an attempt
log (A-log: the chain's evidence substrate).
"""
from __future__ import annotations
import json
import re
import subprocess
import sys
import time
from pathlib import Path

OPEN = re.compile(r"^- \[ \] (.*)$")
DONE = re.compile(r"^- \[x\] (.*)$", re.I)


class Plan:
    def __init__(self, path: str | Path = "plan.md"):
        self.path = Path(path)
        self.lines = self.path.read_text().splitlines() if self.path.exists() else []

    def pending(self) -> list[str]:
        return [m.group(1).strip() for l in self.lines if (m := OPEN.match(l))]

    def next_task(self) -> str | None:
        tasks = self.pending()
        return tasks[0] if tasks else None

    def mark_done(self, task: str) -> bool:
        for i, l in enumerate(self.lines):
            if (m := OPEN.match(l)) and m.group(1).strip() == task:
                self.lines[i] = f"- [x] {m.group(1).strip()}"
                self.path.write_text("\n".join(self.lines) + "\n")
                return True
        return False


def log_attempt(workdir: str | Path, task: str | None, ok: bool,
                detail: str) -> dict:
    """Append one A-log line. Returns the entry (ts-ordered JSONL)."""
    entry = {"ts": time.time(), "task": task, "ok": bool(ok), "detail": detail}
    p = Path(workdir) / "attempts.jsonl"
    with open(p, "a") as f:
        f.write(json.dumps(entry, sort_keys=True) + "\n")
    return entry


def run_once(plan_path: str = "plan.md", agent_cmd: str = "echo",
             verify_cmd: str = "python3 -m pytest tests/ -q",
             workdir: str | Path | None = None) -> dict:
    """One loop iteration. Returns receipt; never marks done on red gate."""
    root = Path(workdir) if workdir else Path(plan_path).parent
    plan = Plan(root / Path(plan_path).name if workdir else plan_path)
    task = plan.next_task()
    if task is None:
        return {"ok": True, "done": True, "task": None, "detail": "plan empty"}
    a = subprocess.run(agent_cmd.split() + [task], capture_output=True,
                       text=True, cwd=root)
    if a.returncode != 0:
        res = {"ok": False, "task": task, "detail": f"agent failed: {a.stderr[:200]}"}
        log_attempt(root, task, False, res["detail"])
        return res
    v = subprocess.run(verify_cmd.split(), capture_output=True, text=True,
                       cwd=root)
    if v.returncode != 0:
        res = {"ok": False, "task": task, "detail": "gate red — task left open"}
        log_attempt(root, task, False, res["detail"])
        return res
    plan.mark_done(task)
    res = {"ok": True, "task": task, "detail": "done + gate green"}
    log_attempt(root, task, True, res["detail"])
    return res


if __name__ == "__main__":
    import os
    once = "--once" in sys.argv
    res = run_once(agent_cmd=os.getenv("AGENT_CMD", "echo"),
                   verify_cmd=os.getenv("VERIFY_CMD", "python3 -m pytest tests/ -q"))
    print(res["detail"], "-", res.get("task") or "nothing pending")
    if once:
        raise SystemExit(0 if res["ok"] else 1)
