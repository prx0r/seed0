#!/usr/bin/env python3
"""grants.py — M-grant ledger + treasury + BATS-lite + receipts. Stdlib only.

The lock (enforced in code, not policy):
  - Grants are integer cents, ceiling-not-balance, single purpose + expiry.
  - No standing money: spend paths check an ACTIVE grant first (fail closed).
  - Exact-amount release: a spend settles for exactly its receipted cents.
  - Receipt-or-it-didn't-happen: spend without a verified receipt is refused
    at record time; unverified spend anywhere else is a process failure.
  - Ledger is an append-only event log (proposed/activated/spent/revoked);
    state() folds it. Agent hot holdings = active grants only.

WorkerKit lineage: Treasury buckets + BATS escalation ported from mw@05119b2
(providers/treasury.py, providers/bats.py). x402 is the settlement rail
(live: /v1/work $0.005 mainnet); verify_receipt() checks receipt shape.
"""
from __future__ import annotations
import json
import secrets
import time
from pathlib import Path

MREG = "loop/registry_m.jsonl"


class GrantDenied(Exception):
    pass


def _events(path: str = MREG) -> list[dict]:
    p = Path(path)
    if not p.exists():
        return []
    return [json.loads(l) for l in p.read_text().splitlines() if l.strip()]


def _emit(ev: dict, path: str = MREG) -> dict:
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    with open(path, "a") as f:
        f.write(json.dumps(ev, sort_keys=True) + "\n")
    return ev


def new_grant(amount_cents: int, purpose: str, recipient: str,
              expiry_s: int = 86400, approved_by: str = "human",
              path: str = MREG) -> dict:
    """Propose a grant. Human activation (activate()) is what unlocks spend."""
    if not isinstance(amount_cents, int) or amount_cents <= 0:
        raise GrantDenied("amount must be positive integer cents")
    return _emit({"id": "g-" + secrets.token_hex(4), "kind": "proposed",
                  "amount_cents": amount_cents, "purpose": purpose,
                  "recipient": recipient, "expiry_ts": time.time() + expiry_s,
                  "approved_by": approved_by, "ts": time.time()}, path)


def state(gid: str, path: str = MREG, now: float | None = None) -> dict:
    """Fold the event log into current grant state."""
    now = time.time() if now is None else now
    base = spent = 0
    grant, active, revoked = None, False, False
    receipts = []
    for e in _events(path):
        if e.get("id") != gid and e.get("gid") != gid:
            continue
        k = e.get("kind")
        if k == "proposed":
            grant = e
        elif k == "activated":
            active = True
        elif k == "spent":
            spent += e.get("amount_cents", 0)
            receipts.append(e.get("receipt", {}))
        elif k == "revoked":
            revoked = True
    if grant is None:
        raise KeyError(f"unknown grant: {gid}")
    status = "revoked" if revoked else (
        "expired" if now > grant["expiry_ts"] else (
            "spent" if spent >= grant["amount_cents"] else (
                "active" if active else "proposed")))
    return {"id": gid, "status": status, "amount_cents": grant["amount_cents"],
            "spent_cents": spent, "remaining_cents": grant["amount_cents"] - spent,
            "purpose": grant["purpose"], "recipient": grant["recipient"],
            "expiry_ts": grant["expiry_ts"], "receipts": receipts}


def activate(gid: str, by: str = "human", path: str = MREG) -> dict:
    """Human button press. In production this is the inbox resolve handler."""
    st = state(gid, path)
    if st["status"] != "proposed":
        raise GrantDenied(f"cannot activate from {st['status']}")
    return _emit({"id": "g-" + secrets.token_hex(4), "kind": "activated",
                  "gid": gid, "by": by, "ts": time.time()}, path)


def check_spend(gid: str, amount_cents: int, purpose: str,
                path: str = MREG, now: float | None = None) -> dict:
    """Pre-check: raises GrantDenied unless an active grant covers it exactly."""
    st = state(gid, path, now)
    if st["status"] != "active":
        raise GrantDenied(f"grant not active ({st['status']})")
    if purpose != st["purpose"]:
        raise GrantDenied(f"purpose mismatch: {purpose!r} != {st['purpose']!r}")
    if amount_cents > st["remaining_cents"]:
        raise GrantDenied(
            f"ceiling exceeded: {amount_cents} > {st['remaining_cents']} remaining")
    return st


def record_receipt(gid: str, receipt: dict, path: str = MREG,
                   now: float | None = None) -> dict:
    """Post-check: settle spend against verified receipt (re-checks ceiling)."""
    if not verify_receipt(receipt):
        raise GrantDenied(f"bad receipt shape: {receipt}")
    st = check_spend(gid, receipt["amount_cents"], receipt.get("purpose", ""),
                     path, now) if receipt.get("purpose") else state(gid, path, now)
    if receipt["amount_cents"] > st["remaining_cents"]:
        raise GrantDenied("receipt exceeds remaining ceiling")
    return _emit({"id": "g-" + secrets.token_hex(4), "kind": "spent",
                  "gid": gid, "amount_cents": receipt["amount_cents"],
                  "receipt": receipt, "ts": time.time()}, path)


def verify_receipt(r: dict) -> bool:
    """x402 receipt shape: tx + integer cents + endpoint + ts."""
    return (isinstance(r, dict)
            and isinstance(r.get("tx"), str) and len(r["tx"]) > 8
            and isinstance(r.get("amount_cents"), int)
            and r["amount_cents"] >= 0
            and isinstance(r.get("endpoint"), str) and bool(r["endpoint"])
            and isinstance(r.get("ts"), (int, float)))


class Treasury:
    """WorkerKit port (minimal): quota buckets + cash, fail-closed charging."""

    def __init__(self):
        self.buckets: dict[str, dict] = {}
        self.cash_usd: float = 0.0

    def register_bucket(self, name: str, unit: str, daily_limit: float) -> None:
        self.buckets[name] = {"unit": unit, "daily_limit": daily_limit,
                              "remaining": daily_limit}

    def fund(self, usd: float) -> float:
        self.cash_usd = round(self.cash_usd + usd, 6)
        return self.cash_usd

    def charge(self, name: str, units: float, money_usd: float = 0.0) -> dict:
        b = self.buckets.get(name)
        if b is None:
            raise GrantDenied(f"unknown bucket: {name}")
        if b["remaining"] < units:
            raise GrantDenied(f"bucket {name} empty ({b['remaining']} < {units})")
        if self.cash_usd < money_usd:
            raise GrantDenied(f"cash shortfall ({self.cash_usd} < {money_usd})")
        b["remaining"] -= units
        self.cash_usd = round(self.cash_usd - money_usd, 6)
        return {"bucket": name, "remaining": b["remaining"],
                "cash_usd": self.cash_usd}


def select_tier(remaining_usd: float, uncertainty: float = 0.5) -> dict:
    """BATS-lite: cheapest tier that fits budget + uncertainty."""
    if remaining_usd < 0.001:
        return {"tier": "free", "reason": "budget_tight_use_free"}
    if uncertainty > 0.7 and remaining_usd > 0.01:
        return {"tier": "strong", "reason": "high_uncertainty_worth_it"}
    if remaining_usd > 0.01:
        return {"tier": "cheap", "reason": "budget_ok_mid_uncertainty"}
    return {"tier": "free", "reason": "budget_thin_default_free"}


TIER_ORDER = ("free", "cheap", "strong")


def escalate_tier(current: str, failed: bool) -> dict:
    """B4 escalation policy: step up one tier on failure, hold on success.
    At top tier + failing → escalate_human (never auto-spend past strong).
    Pure function (no spend, no calls) — wiring it into a live loop is a
    spend-profile change and stays queued behind explicit approval."""
    if current not in TIER_ORDER:
        return {"tier": "free", "reason": "unknown-tier-reset",
                "escalate_human": False}
    if not failed:
        return {"tier": current, "reason": "hold-on-success",
                "escalate_human": False}
    i = TIER_ORDER.index(current)
    if i >= len(TIER_ORDER) - 1:
        return {"tier": current, "reason": "top-tier-failing",
                "escalate_human": True}
    return {"tier": TIER_ORDER[i + 1],
            "reason": f"escalate-{current}-on-failure", "escalate_human": False}


def metered_call(fn, acc: dict, model: str = "", prices: dict | None = None):
    """Run fn() -> (result, in_tok, out_tok); accumulate + cost into acc.

    The enforcement wrapper a-metering-design asked for: every metered call
    lands in one accumulator the budget checks BEFORE the next call.
    """
    from telemetry import cost_usd
    result, inp, out = fn()
    acc["input_tokens"] = acc.get("input_tokens", 0) + int(inp)
    acc["output_tokens"] = acc.get("output_tokens", 0) + int(out)
    if model:
        c = cost_usd(model, int(inp), int(out))
        if c is not None:
            acc["cost_usd"] = round(acc.get("cost_usd", 0.0) + c, 6)
    return result


def log_spend(path: str, entry: dict) -> dict:
    """Append one metered spend line (pyeval SPEND_LOG hook target)."""
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    rec = {"ts": time.time(), **entry}
    with open(path, "a") as f:
        f.write(json.dumps(rec, sort_keys=True) + "\n")
    return rec
