"""Points ledger (stdlib only, no network)."""
import json

_store: dict = {}


def add(name: str, pts: int) -> None:
    _store[name] = _store.get(name, 0) + pts


def total(name: str) -> int:
    return _store.get(name, 0)


def save(path: str) -> None:
    with open(path, "w", encoding="utf-8") as f:
        json.dump(_store, f)


def load(path: str) -> None:
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    _store.clear()
    _store.update(data)
