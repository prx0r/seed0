"""Deterministic ranking engine.

Scoring formula: score(item) = 2*a + 1*b - 1*c, where missing/non-numeric values default to 0.

JSON round-trip: save(path, items) writes items as JSON; load(path) reads them back
preserving order, so load(save(items)) == items.
"""

import json


def _num(item, key):
    try:
        v = item.get(key, 0) if isinstance(item, dict) else 0
    except Exception:
        return 0.0
    if isinstance(v, bool):
        return float(v)
    if isinstance(v, (int, float)):
        return float(v)
    try:
        return float(v)
    except (TypeError, ValueError):
        return 0.0


def score(item: dict) -> float:
    """Return 2*a + b - c for generic dict, coercing missing/non-numeric to 0."""
    if not isinstance(item, dict):
        return 0.0
    return 2.0 * _num(item, "a") + 1.0 * _num(item, "b") - 1.0 * _num(item, "c")


def rank(items: list[dict]) -> list[dict]:
    """Return items sorted in descending score order (stable)."""
    return sorted(list(items), key=score, reverse=True)


def save(path: str, items) -> None:
    """Save items to JSON file preserving order (JSON round-trip writer)."""
    with open(path, "w") as f:
        json.dump(list(items), f)


def load(path: str) -> list[dict]:
    """Load items from JSON file preserving order (JSON round-trip reader)."""
    with open(path) as f:
        data = json.load(f)
    return list(data)
