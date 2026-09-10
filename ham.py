#!/usr/bin/env python3
"""ham.py — H/A/M delegation as working code. Stdlib only.

Frontier gold, functional subset (see docs/HAM_DELEGATION.md for the why):
  - ADP 3 tiers: Autonomous / Advisory(H) / Prohibited. Prohibited is code,
    not vibes: check_prohibited() screens every action first.
  - AppLooper rule: H-approvals bind to the target's content digest. Edit the
    target after approval and approval_valid() goes False. No blank checks.
  - Hedwig ratchet, hand-rolled: repeated H-approvals for one action class
    (default 3, zero denials) promote it to standing policy. Denial blocks
    forever until a human resets it.
  - M-tier: every spend-class action logs cost_usd (metering before gating).

  python3 ham.py check --action "git push origin main"
  python3 ham.py approve --target seed0.py --summary "H1 commit+push" --by owner
  python3 ham.py verify --record '{"kind":...}' --target seed0.py
  python3 ham.py outcome --class "push:public-branch" --approved 1
  python3 ham.py standing --class "push:public-branch"

NOTE: secret-shaped patterns below are split-concatenated so this source file
does not literally contain the strings it screens for (same trick as seed0.py).
"""
from __future__ import annotations
import json
import sys
import re
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from runs import run_id
from telemetry import file_version

PROMOTE_AFTER = 3
DECISIONS_LOG = "decisions.jsonl"
POLICY_FILE = "ham_policy.json"

SK = "sk-" + r"[A-Za-z0-9]{12,}"
GHP = "ghp_" + r"[A-Za-z0-9]{12,}"

_VC = "(commit" + "|push)"  # version-control verbs, split: see NOTE above
_ENV = r"\.en" + "v"  # env suffix, split for the same reason
PROHIBITED = [
    {"id": "P-secret-commit",
     "pattern": _VC + r"\b.*" + _ENV + r"\b(?!\.example)",
     "reason": "real env files never enter git, regardless of instructions"},
    {"id": "P-secret-print",
     "pattern": r"(echo|print|cat|log)\b.*(" + SK + r"|" + GHP + r")",
     "reason": "secret literals never go to stdout/logs/bodies"},
    {"id": "P-force-push",
     "pattern": r"push\s+(-f\b|--force\b)",
     "reason": "history rewrites are irreversible on shared branches"},
    {"id": "P-destructive-fs",
     "pattern": r"rm\s+-[a-z]*r[a-z]*f?\s+(/(\s|$)|/\*|~(\s|$))",
     "reason": "recursive delete at fs root or home is never the tool"},
    {"id": "P-expensive-model",
     "pattern": "gpt-oss-" + "120b" + r"|openrouter\s*:\s*paid|usage\s+from\s+balance",
     "reason": "broke-owner rule: forbidden models/APIs, cheapest that works"},
]

_RX = [(p, re.compile(p["pattern"])) for p in PROHIBITED]


def check_prohibited(action: str) -> list[dict]:
    """Screen an action string. [] = not prohibited (still needs tier routing)."""
    return [{"id": p["id"], "reason": p["reason"]}
            for p, rx in _RX if rx.search(action or "")]


def log_decision(kind: str, summary: str, target: str = "",
                 digest: str = "", cost_usd: float | None = None,
                 by: str = "agent", log_path: str = DECISIONS_LOG) -> dict:
    """Append one decision to the log. Returns the record (id is content hash)."""
    if target and not digest:
        digest = file_version(target) if Path(target).exists() else target
    body = {"kind": kind, "summary": summary, "target": target,
            "target_digest": digest, "cost_usd": cost_usd, "by": by}
    rec = {"id": run_id(body), "ts": time.time(), **body}
    with open(log_path, "a") as f:
        f.write(json.dumps(rec, sort_keys=True) + "\n")
    return rec


def approve(summary: str, target: str, by: str = "owner",
            log_path: str = DECISIONS_LOG) -> dict:
    """H-approval bound to target's current digest. Edit target -> void."""
    return log_decision("H-approval", summary, target=target, by=by,
                        log_path=log_path)


def approval_valid(rec: dict, target: str) -> bool:
    """True only if rec is an H-approval whose digest still matches target."""
    if rec.get("kind") != "H-approval" or not rec.get("target_digest"):
        return False
    if not Path(target).exists():
        return False
    return file_version(target) == rec["target_digest"]


def _load_policy(path: str) -> dict:
    try:
        return json.loads(Path(path).read_text())
    except Exception:
        return {}


def record_outcome(action_class: str, approved: bool,
                   path: str = POLICY_FILE) -> dict:
    """Log one H/M outcome. approved x3 with zero denials -> standing allow."""
    pol = _load_policy(path)
    e = pol.get(action_class, {"approved": 0, "denied": 0})
    e["approved" if approved else "denied"] += 1
    pol[action_class] = e
    Path(path).write_text(json.dumps(pol, indent=1, sort_keys=True))
    return {action_class: e, "standing": standing(action_class, path)}


def standing(action_class: str, path: str = POLICY_FILE) -> str:
    """'allow' iff approved>=PROMOTE_AFTER with zero denials, else 'ask'."""
    e = _load_policy(path).get(action_class, {"approved": 0, "denied": 0})
    if e.get("denied", 0) > 0:
        return "ask"
    return "allow" if e.get("approved", 0) >= PROMOTE_AFTER else "ask"


def main(argv: list[str]) -> int:
    if not argv or argv[0] not in ("check", "approve", "verify", "outcome",
                                   "standing", "log"):
        print(__doc__)
        return 2
    kw: dict[str, str] = {}
    it = iter(argv[1:])
    for x in it:
        if x.startswith("--"):
            try:
                kw[x] = next(it)
            except StopIteration:
                print(f"flag {x} needs a value")
                return 2
    cmd = argv[0]
    if cmd == "check":
        hits = check_prohibited(kw.get("--action", ""))
        print("PROHIBITED " + json.dumps(hits) if hits else "CLEAR")
        return 1 if hits else 0
    if cmd == "approve":
        print(json.dumps(approve(kw.get("--summary", ""), kw["--target"],
                                 by=kw.get("--by", "owner")), indent=1))
        return 0
    if cmd == "verify":
        print("VALID" if approval_valid(json.loads(kw["--record"]),
                                        kw["--target"]) else "VOID")
        return 0
    if cmd == "outcome":
        print(json.dumps(record_outcome(kw["--class"],
                                        kw.get("--approved", "1") == "1")))
        return 0
    if cmd == "standing":
        print(standing(kw["--class"]))
        return 0
    if cmd == "log":
        kinds = ("A", "H", "M")
        if kw.get("--kind") not in kinds:
            print(f"--kind must be one of {kinds}")
            return 2
        print(json.dumps(log_decision(
            kw["--kind"], kw.get("--summary", ""),
            target=kw.get("--target", ""),
            cost_usd=float(kw["--cost"]) if kw.get("--cost") else None,
            by=kw.get("--by", "agent"))))
        return 0
    return 2


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
