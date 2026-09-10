#!/usr/bin/env python3
"""Binary validator, bout2-demand round 1. Pre-registered BEFORE lanes.
Usage: python3 runs/bout2-demand/validate.py <attempt-dir> -> JSON, exit 0/1."""
import json
import subprocess
import sys
from pathlib import Path


def main(argv: list[str]) -> int:
    att = Path(argv[1])
    reasons = []
    for f in ("demand.py", "tests/test_demand.py", "evidence.txt"):
        if not (att / f).exists():
            reasons.append(f"missing:{f}")
    src = (att / "demand.py").read_text() if (att / "demand.py").exists() else ""
    for fn in ("def weekly_demand(", "def rank("):
        if fn not in src:
            reasons.append(f"missing-fn:{fn}")
    if src and ("/ 52" not in src and "/52" not in src):
        reasons.append("no-weekly-math")
    ev = (att / "evidence.txt").read_text() if (att / "evidence.txt").exists() else ""
    if not ev.strip():
        reasons.append("evidence-empty")
    try:
        r = subprocess.run([sys.executable, "-m", "pytest", "tests/", "-q"],
                           cwd=att, capture_output=True, text=True, timeout=120)
        if r.returncode != 0:
            reasons.append("suite-red")
        tail = ((r.stdout + r.stderr).strip().splitlines() or ["?"])[-1][:120]
    except Exception as e:
        reasons.append(f"suite-error:{e}"[:60])
        tail = "?"
    ok = not reasons
    print(json.dumps({"pass": ok, "reasons": reasons, "suite_tail": tail}))
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
