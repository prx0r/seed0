#!/usr/bin/env python3
"""validate_criteria: rubric rows need teeth. Stdlib only.
Usage: python3 criteria0/validate_criteria.py criteria/criteria1.md
Checks: table present; each row has ID/statement/verification/owner; method is
test|demo|review; statements avoid weasel words (good/robust/better/seamless).
Exit 1 with reasons otherwise. Prints elapsed.
"""
import re
import sys
import time
from pathlib import Path

METHODS = ("test", "demo", "review")
WEASEL = re.compile(r"\b(good|robust|better|best|seamless|powerful|strong)\b", re.I)


def validate(path: str) -> list[str]:
    text = Path(path).read_text()
    rows = re.findall(r"^\| (C\d+) \| (.+?) \| (.+?) \| (.+?) \|$", text, re.M)
    if not rows:
        return ["no criteria rows (need | ID | Statement | Verification | Owner |)"]
    errs = []
    for cid, stmt, verif, owner in rows:
        verif, owner = verif.strip(), owner.strip()
        if not owner or owner.lower() in ("tbd", "?"):
            errs.append(f"{cid}: owner missing")
        if verif.split()[0].lower() not in METHODS:
            errs.append(f"{cid}: unknown verification method in '{verif}'")
        if WEASEL.search(stmt):
            errs.append(f"{cid}: weasel word in statement — rewrite binary")
    return errs


if __name__ == "__main__":
    t0 = time.time()
    errs = validate(sys.argv[1])
    dt = time.time() - t0
    print(("CRITERIA OK" if not errs else "\n".join("FAIL " + e for e in errs))
          + f" [{dt*1000:.0f}ms]")
    raise SystemExit(0 if not errs else 1)
