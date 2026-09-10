# NORTHSTAR bout2-demand (frozen 2026-09-10 — demand side, de-primed brief)

Build a demand estimator inside your attempt directory. No domain examples
are given on purpose — pick your own market. Stdlib only, no network, no secrets.

## Contract
- `demand.py` with:
  - `weekly_demand(postcode: str) -> float` (0.0 for unknown postcodes)
  - `rank(postcodes: list[str]) -> list[str]` (descending demand order)
  - Data: ≥5 hardcoded areas, each with dwellings + annual turnover rate;
    demand = dwellings × turnover / 52. Document sources as estimates.
- `tests/test_demand.py` with ≥3 tests (unknown→0.0, rank order, math spot-check).
- Run `python3 -m pytest tests/ -q` in your dir; save tail to `evidence.txt`.
- Run the bout validator (path in lane prompt); exit 0 (max 3 tries).
- Touch nothing outside your attempt directory.
