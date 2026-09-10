# NORTHSTAR money-tourney (frozen 2026-09-10 — T0 prompt as tournament idea)

Goal "make me money" through the lens of ideas/idea1.md (scarcity thesis):
abundance induces demand for physical validation faster than supply responds;
find the bottleneck, check crowdedness, slice a wedge, predict falsifiably.

## Build (inside your attempt dir ONLY, stdlib, no network, no secrets)

1. `strategy.md`: one opportunity seen through the lens. Must contain:
   - the bottleneck mechanism (what abundance induces what scarcity),
   - a crowdedness read (why this isn't the consensus trade),
   - ONE falsifiable prediction with numbers (what would prove it wrong).
2. `scorer.py`: toy bottleneck scorer over 5 hardcoded mock opportunities.
   Score = demand_growth × supply_inelasticity (floats you choose, documented
   in strategy.md). Emits ranked JSON to stdout: `[{"name":..., "score":...}]`.
3. `tests/test_scorer.py`: ≥3 tests (ranking order, score math, JSON shape).
4. Run `python3 -m pytest tests/ -q` in your dir; save tail to `evidence.txt`.
5. Run the bout validator (path given in your lane prompt); exit 0 (max 3 tries).
