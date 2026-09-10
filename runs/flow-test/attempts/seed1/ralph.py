"""Ralph loop: next unchecked plan item, one agent run, gate, mark done. Stdlib."""
from __future__ import annotations
import re
import subprocess
import sys
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


def run_once(plan_path: str = "plan.md", agent_cmd: str = "echo",
             verify_cmd: str = "python3 -m pytest tests/ -q") -> dict:
    """One loop iteration. Returns receipt; never marks done on red gate."""
    plan = Plan(plan_path)
    task = plan.next_task()
    if task is None:
        return {"ok": True, "done": True, "task": None, "detail": "plan empty"}
    a = subprocess.run(agent_cmd.split() + [task], capture_output=True, text=True)
    if a.returncode != 0:
        return {"ok": False, "task": task, "detail": f"agent failed: {a.stderr[:200]}"}
    v = subprocess.run(verify_cmd.split(), capture_output=True, text=True)
    if v.returncode != 0:
        return {"ok": False, "task": task, "detail": "gate red — task left open"}
    plan.mark_done(task)
    return {"ok": True, "task": task, "detail": "done + gate green"}


if __name__ == "__main__":
    import os
    once = "--once" in sys.argv
    res = run_once(agent_cmd=os.getenv("AGENT_CMD", "echo"),
                   verify_cmd=os.getenv("VERIFY_CMD", "python3 -m pytest tests/ -q"))
    print(res["detail"], "-", res.get("task") or "nothing pending")
    if once:
        raise SystemExit(0 if res["ok"] else 1)
