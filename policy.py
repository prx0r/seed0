#!/usr/bin/env python3
"""policy.py — learned check-in policy (Hedwig port, stdlib only).

Paper: Shukla et al., CAIS '26 (arXiv:2605.11495). Hedwig learns WHEN to
check in from longitudinal approval/denial traces: hard constraints first,
then a learned policy engine (online classifier), three outcomes (proceed
silently / surface summary / live check-in).

This port, kept dumb on purpose:
  - features per proposed action: diff size, blast radius, security
    sensitivity, prior approvals/denials for the action class (13-dim in
    Hedwig; 6 here — same shape, fewer knobs).
  - online logistic regression via SGD, per-repo persisted weights JSON.
  - cold start = heuristic scorer (deterministic risk signals), identical
    interface; classifier takes over after MIN_SAMPLES outcomes.
  - outcomes feed back: approve/deny → training sample; revert/verify-fail
    → corrective sample (Hedwig's regret loop, single application).

  from policy import CheckinPolicy
  pol = CheckinPolicy("ham_policy.json")
  verdict = pol.score({"diff_lines": 40, "files": 3, "security": 0,
                       "action_class": "push:branch"})   # proceed|surface|checkin
  pol.observe("push:branch", approved=True)              # learn
"""
from __future__ import annotations
import json
import math
from pathlib import Path

MIN_SAMPLES = 10
LR = 0.5
T_PROCEED = 0.35
T_CHECKIN = 0.7
FEATURES = ("diff", "blast", "security", "denials", "approvals", "novelty")


def featurize(action: dict, history: dict) -> list[float]:
    """Deterministic risk signals in [0,1]-ish ranges. No model involved."""
    h = history.get(action.get("action_class", ""), {"approved": 0, "denied": 0})
    tot = h["approved"] + h["denied"]
    return [
        min(1.0, action.get("diff_lines", 0) / 200.0),
        min(1.0, action.get("files", 1) / 10.0),
        1.0 if action.get("security") else 0.0,
        min(1.0, h["denied"] / 3.0),
        min(1.0, h["approved"] / 5.0),
        0.0 if tot else 1.0,
    ]


def sigmoid(z: float) -> float:
    return 1.0 / (1.0 + math.exp(-max(-60.0, min(60.0, z))))


class CheckinPolicy:
    """Online check-in policy with JSON persistence. Cold = heuristic."""

    def __init__(self, path: str = "ham_policy.json"):
        self.path = path
        try:
            state = json.loads(Path(path).read_text())
        except Exception:
            state = {}
        self.weights = state.get("weights", [0.0] * len(FEATURES))
        self.bias = state.get("bias", 0.0)
        self.history = state.get("history", {})
        self.samples = state.get("samples", 0)

    def save(self) -> None:
        Path(self.path).parent.mkdir(parents=True, exist_ok=True)
        Path(self.path).write_text(json.dumps(
            {"weights": self.weights, "bias": self.bias,
             "history": self.history, "samples": self.samples},
            indent=1, sort_keys=True))

    def risk(self, action: dict) -> float:
        """Heuristic score (cold start): weighted risk signals, no learning."""
        f = featurize(action, self.history)
        w = [1.2, 1.0, 2.0, 1.5, -1.0, 0.5]
        return max(0.0, min(1.0, sum(wi * fi for wi, fi in zip(w, f)) / 3.0))

    def predict(self, action: dict) -> float:
        """P(check-in needed). Learned after MIN_SAMPLES, heuristic before."""
        f = featurize(action, self.history)
        if self.samples < MIN_SAMPLES:
            return self.risk(action)
        return sigmoid(sum(w * x for w, x in zip(self.weights, f)) + self.bias)

    def decide(self, action: dict) -> dict:
        """Three-tier cascade (Hedwig §3): proceed / surface / checkin."""
        p = self.predict(action)
        verdict = ("proceed" if p < T_PROCEED
                   else "surface" if p < T_CHECKIN else "checkin")
        return {"verdict": verdict, "p_checkin": round(p, 4),
                "learned": self.samples >= MIN_SAMPLES,
                "action_class": action.get("action_class", "")}

    def observe(self, action: dict, approved: bool,
                regret: bool = False) -> dict:
        """Training sample on the REAL scored features (not prototypes).
        regret=True (revert/verify-fail) counts as denial, applied once —
        the corrective gradient."""
        cls = action.get("action_class", "")
        h = self.history.get(cls, {"approved": 0, "denied": 0})
        label = 0 if approved and not regret else 1
        f = featurize(action, self.history)
        if approved and not regret:
            h["approved"] += 1
        else:
            h["denied"] += 1
        self.history[cls] = h
        if self.samples >= MIN_SAMPLES - 1:
            pred = sigmoid(sum(w * x for w, x in zip(self.weights, f)) + self.bias)
            err = label - pred
            self.weights = [w + LR * err * x for w, x in zip(self.weights, f)]
            self.bias += LR * err
        self.samples += 1
        self.save()
        return {"samples": self.samples, "learned": self.samples >= MIN_SAMPLES}
