#!/usr/bin/env python3
"""validate_idea: idea files need teeth. Stdlib only.
Usage: python3 idea0/validate_idea.py ideas/idea1.md
Checks: required sections present; ≥1 falsifiable prediction checkbox;
mechanism section non-trivial (>200 chars); non-goals present.
Exit 1 with reasons otherwise. Prints elapsed (time-to-verify is logged).
"""
import re
import sys
import time
from pathlib import Path

REQUIRED = ["## Problem", "## Mechanism", "## Falsifiable predictions",
            "## Non-goals", "## Verification plan"]


def validate(path: str) -> list[str]:
    t0 = time.time()
    text = Path(path).read_text()
    errs = [f"missing section: {s}" for s in REQUIRED if s not in text]
    preds = re.findall(r"^- \[ \] (.+)$", text, re.M)
    if not preds:
        errs.append("no falsifiable predictions (need `- [ ] …` rows)")
    m = re.search(r"## Mechanism\n(.+?)(?=\n## )", text, re.S)
    if m and len(m.group(1).strip()) < 200:
        errs.append("mechanism too thin (<200 chars) — adjectives, not parts")
    return errs


if __name__ == "__main__":
    t0 = time.time()
    errs = validate(sys.argv[1])
    dt = time.time() - t0
    print(("IDEA OK" if not errs else "\n".join("FAIL " + e for e in errs))
          + f" [{dt*1000:.0f}ms]")
    raise SystemExit(0 if not errs else 1)
