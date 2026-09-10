"""Run telemetry: time + model + tokens + cost, linked to idea/criteria versions.
Stdlib only. Every scored run carries one telemetry block so tournaments answer
not just 'which seed won' but 'at what cost, on which model, against which
frozen idea/criteria versions'.

Versions are content digests (sha256[:12] of the idea/criteria files), not
hand-bumped numbers — reruns after an edit automatically count as new versions.
PRICES covers known models (USD per 1M tokens); unknown models record tokens
with cost null rather than guessing.
"""
from __future__ import annotations
import hashlib
import time
from pathlib import Path

PRICES = {
    # (input_per_1M, output_per_1M) USD — opencode-go table, 2026-09-10
    "mimo-v2.5": (0.14, 0.28),
    "mimo-v2.5-pro": (0.435, 0.87),
    "muse-spark-1.3-contributor": (0.10, 0.20),
    "muse-spark-1.2-contributor": (0.10, 0.20),
}


def file_version(path: str) -> str:
    try:
        h = hashlib.sha256(Path(path).read_bytes()).hexdigest()[:12]
        return h
    except Exception:
        return "missing"


def extract_usage(payload: dict) -> dict:
    """Pull token counts out of Responses- or chat-completions-style payloads."""
    u = (payload or {}).get("usage") or {}
    inp = u.get("input_tokens", u.get("prompt_tokens", 0)) or 0
    out = u.get("output_tokens", u.get("completion_tokens", 0)) or 0
    return {"input_tokens": int(inp), "output_tokens": int(out)}


def cost_usd(model: str, inp: int, out: int) -> float | None:
    if model not in PRICES:
        return None
    pi, po = PRICES[model]
    return round(inp / 1e6 * pi + out / 1e6 * po, 6)


class Meter:
    """Accumulate one run's telemetry. time() it, meter.model()/tokens() it."""

    def __init__(self, model: str = "", idea: str = "", criteria: str = ""):
        self.t0 = time.time()
        self.model = model
        self.idea = idea
        self.criteria = criteria
        self.input_tokens = 0
        self.output_tokens = 0

    def add_usage(self, payload: dict):
        u = extract_usage(payload)
        self.input_tokens += u["input_tokens"]
        self.output_tokens += u["output_tokens"]

    def block(self) -> dict:
        # usage_source: "reported" ALWAYS. Token counts come from the provider's
        # own usage blocks, which current research shows are unaudited claims:
        # hidden-reasoning inflation up to 1469% undetectable without TEEs/proofs
        # (CoIn; Token Inflation 2605.30040). We record verbatim + reconcile
        # against provider invoices. Never present these numbers as verified.
        return {"model": self.model,
                "usage_source": "reported",
                "idea": self.idea,
                "idea_version": file_version(self.idea) if self.idea else "",
                "criteria": self.criteria,
                "criteria_version": file_version(self.criteria) if self.criteria else "",
                "elapsed_s": round(time.time() - self.t0, 2),
                "input_tokens": self.input_tokens,
                "output_tokens": self.output_tokens,
                "cost_usd": cost_usd(self.model, self.input_tokens,
                                     self.output_tokens)}
