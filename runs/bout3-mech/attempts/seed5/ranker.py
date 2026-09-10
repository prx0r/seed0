"""Deterministic ranking engine.

Scoring formula: score(item) = 2.0 * x + 3.0 * y - 1.0 * z, where x = float(item.get("x", 0)), y = float(item.get("y", 0)), z = float(item.get("z", 0)); non-numeric or missing values coerce to 0.0.

Persistence: save/load provide a JSON round-trip preserving order.
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
    """Score a generic dict; missing/non-numeric x,y,z treated as 0.0."""
    if not isinstance(item, dict):
        return 0.0
    x = _num(item.get("x", 0))
    y = _num(item.get("y", 0))
    z = _num(item.get("z", 0))
    return 2.0 * x + 3.0 * y - 1.0 * z


def rank(items: list[dict]) -> list[dict]:
    """Return new list sorted by score descending (stable)."""
    return sorted(list(items), key=score, reverse=True)


def save(path: str, items) -> None:
    """Save items as JSON round-trip preserving order."""
    with open(path, "w", encoding="utf-8") as f:
        json.dump(list(items), f)


def load(path: str) -> list[dict]:
    """Load JSON round-trip preserving order."""
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return list(data)
