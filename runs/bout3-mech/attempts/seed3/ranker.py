"""Deterministic ranking engine.

Scoring formula: score(item) = 2.0 * alpha + 1.0 * beta - 1.0 * gamma,
where alpha = numeric value of item.get("alpha", 0), beta = item.get("beta", 0),
gamma = item.get("gamma", 0); missing/non-numeric values coerce to 0.0;
non-dict items score 0.0.

Persistence: save/load provide a JSON round-trip (roundtrip) preserving order.
"""

import json


def _num(value) -> float:
    try:
        if value is None or isinstance(value, bool):
            return 0.0
        return float(value)
    except (TypeError, ValueError):
        return 0.0


def score(item: dict) -> float:
    """Return 2.0*alpha + 1.0*beta - 1.0*gamma as floats (missing -> 0.0)."""
    if not isinstance(item, dict):
        return 0.0
    return 2.0 * _num(item.get("alpha", 0)) + 1.0 * _num(item.get("beta", 0)) - 1.0 * _num(item.get("gamma", 0))


def rank(items: list[dict]) -> list[dict]:
    """Return new list sorted by score descending (stable)."""
    return sorted(list(items), key=score, reverse=True)


def save(path: str, items) -> None:
    """Save items as JSON list to path, preserving order."""
    with open(path, "w", encoding="utf-8") as f:
        json.dump(list(items), f)


def load(path: str) -> list[dict]:
    """Load JSON list from path, preserving order."""
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return list(data)
