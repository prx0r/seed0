"""metrics.py — shared tournament rulers. Stdlib only.

One ruler per measurement so lanes can't grade themselves with private math:
import these in bout validators, never reimplement. (cg doctrine: canonical
records + shared verification; the ruler is infrastructure, not opinion.)
"""
from __future__ import annotations


def footrule(cand: list[str], truth: list[str]) -> int:
    """Sum |position_in_cand - position_in_truth| over shared ids."""
    pos = {x: i for i, x in enumerate(truth)}
    return sum(abs(i - pos[x]) for i, x in enumerate(cand) if x in pos)


def rank_distance(orders: list[list[str]], truth: list[str]) -> int:
    """Total footrule across filing orders (order-invariance included)."""
    return sum(footrule(o, truth) for o in orders)


def storm_counts(filer, summary: str, key: str, n: int = 5) -> tuple[int, int]:
    """Fire n identical filings; return (records, unique_ids)."""
    recs = [filer(summary, key) for _ in range(n)]
    ids = [r.get("id", r.get("summary")) for r in recs]
    return len(recs), len(set(ids))
