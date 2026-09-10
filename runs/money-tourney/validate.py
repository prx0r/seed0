#!/usr/bin/env python3
"""Binary validator, money-tourney round 1. Pre-registered BEFORE lanes.
Usage: python3 runs/money-tourney/validate.py <attempt-dir> -> JSON, exit 0/1.
Checks: files + suite green + strategy grounding (P5: lens vocabulary) +
scorer runs + emits ranked JSON."""
import json
import subprocess
import sys
from pathlib import Path


def main(argv: list[str]) -> int:
    att = Path(argv[1])
    reasons = []
    for f in ("strategy.md", "scorer.py", "tests/test_scorer.py", "evidence.txt"):
        if not (att / f).exists():
            reasons.append(f"missing:{f}")
    text = (att / "strategy.md").read_text().lower() if (att / "strategy.md").exists() else ""
    anchors = ["bottleneck", "crowd", "falsif"]
    if sum(1 for a in anchors if a in text) < 2:
        reasons.append("ungrounded: strategy needs >=2 of bottleneck/crowd*/falsif*")
    if (att / "scorer.py").exists():
        try:
            r = subprocess.run([sys.executable, "scorer.py"], cwd=att,
                               capture_output=True, text=True, timeout=60)
            rows = json.loads(r.stdout or "[]")
            scores = [x["score"] for x in rows]
            if not rows or scores != sorted(scores, reverse=True):
                reasons.append("scorer-not-ranked-json")
        except Exception as e:
            reasons.append(f"scorer-error:{e}"[:60])
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
