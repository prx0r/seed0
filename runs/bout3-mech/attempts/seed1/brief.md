# NORTHSTAR bout3-mech (frozen 2026-09-10 — pure mechanism, zero domain hints)

Build a deterministic ranking engine inside your attempt directory. No market,
trade, or domain language anywhere in this brief on purpose. Stdlib only, no
network, no secrets.

## Contract
- `ranker.py` with:
  - `score(item: dict) -> float` (documented formula in module docstring)
  - `rank(items: list[dict]) -> list[dict]` (descending score order)
  - `save(path: str, items) -> None` + `load(path: str) -> list[dict]`
    (JSON round-trip preserving order)
- `tests/test_ranker.py` with ≥3 tests (order, formula spot-check, round-trip).
- Run `python3 -m pytest tests/ -q` in your dir; save tail to `evidence.txt`.
- Run the bout validator (path in lane prompt); exit 0 (max 3 tries).
- Touch nothing outside your attempt directory.
