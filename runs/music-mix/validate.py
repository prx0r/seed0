#!/usr/bin/env python3
"""Binary validator, music-mix round 1. Pre-registered BEFORE lanes.
Usage: python3 runs/music-mix/validate.py <attempt-dir> -> JSON, exit 0/1."""
import json
import subprocess
import sys
from pathlib import Path


def main(argv: list[str]) -> int:
    att = Path(argv[1])
    reasons = []
    for f in ("mixengine.py", "tests/test_mix.py", "evidence.txt"):
        if not (att / f).exists():
            reasons.append(f"missing:{f}")
    src = (att / "mixengine.py").read_text() if (att / "mixengine.py").exists() else ""
    for fn in ("def generate_arc(", "def save_mix(", "def load_mix("):
        if fn not in src:
            reasons.append(f"missing-fn:{fn}")
    if (att / "mixengine.py").exists():
        try:
            r = subprocess.run(
                [sys.executable, "-c",
                 "import json,sys; sys.path.insert(0, '.'); "
                 "from mixengine import generate_arc; "
                 "a = generate_arc(60, 'focus', 0.5); "
                 "b = generate_arc(60, 'focus', 0.5); "
                 "print(json.dumps({'n': len(a), 'det': a == b, "
                 "'keys': sorted(a[0].keys()) if a else []}))"],
                cwd=att, capture_output=True, text=True, timeout=60)
            d = json.loads(r.stdout or "{}")
            if not d.get("det"):
                reasons.append("arc-nondeterministic")
            if set(d.get("keys", [])) != {"t_start", "energy", "label"}:
                reasons.append("arc-bad-shape")
        except Exception as e:
            reasons.append(f"engine-error:{e}"[:60])
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
