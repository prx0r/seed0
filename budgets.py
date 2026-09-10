"""Spend budgets: brake on runaway loops, not an accounting ledger. Stdlib only.

Mirrors Pydantic AI's SpendLimits semantics honestly: a budget refuses the NEXT
request once exhausted, but the request that crosses the line completes, and
anything unmetered (subprocess agents, cached answers) is invisible here.
Reconcile against provider invoices for real money; this stops fires, nothing more.

Two shapes (following Google BATS + Pydantic):
  Budget      — in-process cap (usd and/or tokens) with on_spend callbacks.
  advertise() — env block exposing remaining budget to a subprocess agent, so the
                agent itself can be budget-aware (BATS Budget Tracker pattern).
"""
from __future__ import annotations
import os


class BudgetExceeded(Exception):
    pass


class Budget:
    def __init__(self, max_usd: float | None = None,
                 max_tokens: int | None = None,
                 on_spend=None):
        self.max_usd = max_usd
        self.max_tokens = max_tokens
        self.spent_usd = 0.0
        self.spent_tokens = 0
        self.unpriced = 0
        self._on_spend = on_spend if on_spend is not None else []

    def record(self, tokens: int = 0, cost: float | None = None,
               label: str = ""):
        """Record AFTER the billed call. Raises BudgetExceeded to refuse next."""
        self.spent_tokens += int(tokens or 0)
        if cost is None:
            self.unpriced += 1
        else:
            self.spent_usd = round(self.spent_usd + cost, 6)
        snap = self.snapshot(label)
        for cb in self._on_spend:
            cb(snap)
        if self.exhausted():
            raise BudgetExceeded(
                f"budget exhausted after {label or 'call'}: {snap}")

    def check(self, label: str = ""):
        """Pre-call refusal (XBSTACK billing-guard pattern): raise BEFORE the
        billed call if the budget is already exhausted. Call this before
        every metered operation; record() stays the post-call accounting."""
        if self.exhausted():
            raise BudgetExceeded(
                f"budget already exhausted before {label or 'call'}: "
                f"{self.snapshot(label)}")

    def exhausted(self) -> bool:
        if self.max_tokens is not None and self.spent_tokens >= self.max_tokens:
            return True
        if self.max_usd is not None and self.spent_usd >= self.max_usd:
            return True
        return False

    def snapshot(self, label: str = "") -> dict:
        return {"label": label, "spent_usd": self.spent_usd,
                "spent_tokens": self.spent_tokens,
                "max_usd": self.max_usd, "max_tokens": self.max_tokens,
                "unpriced": self.unpriced, "exhausted": self.exhausted()}

    def advertise(self) -> dict:
        """Env block for a subprocess agent (BATS pattern: budget in context)."""
        return {"SEED_BUDGET_USD": "" if self.max_usd is None else str(
                    round(self.max_usd - self.spent_usd, 6)),
                "SEED_BUDGET_TOKENS": "" if self.max_tokens is None else str(
                    self.max_tokens - self.spent_tokens)}


def from_env(prefix: str = "SEED_") -> Budget:
    def _f(k):
        v = os.getenv(prefix + k, "")
        try:
            return float(v) if v not in ("", None) else None
        except ValueError:
            return None

    def _i(k):
        v = os.getenv(prefix + k, "")
        try:
            return int(float(v)) if v not in ("", None) else None
        except ValueError:
            return None

    return Budget(max_usd=_f("BUDGET_USD"), max_tokens=_i("BUDGET_TOKENS"))
