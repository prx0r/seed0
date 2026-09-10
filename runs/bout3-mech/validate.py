#!/usr/bin/env python3
"""Binary validator, bout3-mech round 1. Pre-registered BEFORE lanes.
Usage: python3 runs/bout3-mech/validate.py <attempt-dir> -> JSON, exit 0/1."""
import json
import subprocess
import sys
from pathlib import Path


def main(argv: list[str]) -> int:
    att = Path(argv[1])
    reasons = []
    for f in ("ranker.py", "tests/test_ranker.py", "evidence.txt"):
        if not (att / f).exists():
            reasons.append(f"missing:{f}")
    src = (att / "ranker.py").read_text() if (att / "ranker.py").exists() else ""
    for fn in ("def score(", "def rank(", "def save(", "def load("):
        if fn not in src:
            reasons.append(f"missing-fn:{fn}")
    if src and "round-trip" not in src.lower().replace("_", "-") and "roundtrip" not in src.lower():
        reasons.append("no-roundtrip-doc")
    if (att / "ranker.py").exists():
        # Functional smoke: rank() must accept generic dicts and return all
        # 3 rows (order is the lane's formula — never asserted here).
        try:
            r = subprocess.run(
                [sys.executable, "-c",
                 "import json,sys; sys.path.insert(0, '.'); "
                 "from ranker import rank; "
                 "rows = rank([{'n': 'a', 'v': 1, 'w': 0}, {'n': 'b', 'v': 3, 'w': 1}, {'n': 'c', 'v': 2, 'w': 1}]); "
                 "print(json.dumps(len(rows) if isinstance(rows, list) else -1))"],
                cwd=att, capture_output=True, text=True, timeout=60)
            if (r.returncode != 0) or json.loads(r.stdout or "-1") != 3:
                reasons.append("ranker-not-functional")
        except Exception as e:
            reasons.append(f"ranker-error:{e}"[:60])
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
