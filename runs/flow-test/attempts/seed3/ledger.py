"""Points ledger (stdlib only, no network)."""
import json

_balances: dict = {}


def add(name: str, pts: int) -> None:
    _balances[name] = _balances.get(name, 0) + pts


def total(name: str) -> int:
    return _balances.get(name, 0)


def save(path: str) -> None:
    with open(path, "w", encoding="utf-8") as f:
        json.dump(_balances, f)


def load(path: str) -> None:
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    _balances.clear()
    _balances.update(data)
