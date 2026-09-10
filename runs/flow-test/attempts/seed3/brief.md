# NORTHSTAR (frozen 2026-09-10, flow-test round 1 — do not edit, amend only)

Build a points ledger inside your attempt directory. Nothing else is graded.

## Contract
- `ledger.py` (stdlib only, no network) with:
  - `add(name: str, pts: int) -> None`
  - `total(name: str) -> int` (0 for unknown names)
  - `save(path: str) -> None` + `load(path: str) -> None` (JSON round-trip)
- `tests/test_ledger.py` with >=3 tests, including a save/load round-trip test.
- Run `python3 -m pytest tests/ -q` inside your attempt dir; save the full
  output tail to `evidence.txt`.
- Run `python3 validate.py` (in run root, pointed at your dir); it must exit 0.
- Do not touch anything outside your attempt directory. Do not write secrets.
