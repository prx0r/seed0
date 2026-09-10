"""Toy bottleneck scorer: score = demand_growth * supply_inelasticity.

Floats documented in strategy.md. Emits ranked JSON to stdout:
[{"name": ..., "score": ...}] sorted descending by score.
Stdlib only, no network.
"""
import json

OPPORTUNITIES = [
    {"name": "eicr-remedial-slots", "demand_growth": 0.90, "supply_inelasticity": 0.85},
    {"name": "ev-charger-installs", "demand_growth": 0.80, "supply_inelasticity": 0.60},
    {"name": "heat-pump-commissioning", "demand_growth": 0.70, "supply_inelasticity": 0.65},
    {"name": "solar-rooftop-retrofit", "demand_growth": 0.60, "supply_inelasticity": 0.50},
    {"name": "smart-meter-swaps", "demand_growth": 0.50, "supply_inelasticity": 0.40},
]


def score(opp):
    return opp["demand_growth"] * opp["supply_inelasticity"]


def ranked():
    items = [{"name": o["name"], "score": score(o)} for o in OPPORTUNITIES]
    return sorted(items, key=lambda d: d["score"], reverse=True)


def main():
    print(json.dumps(ranked()))


if __name__ == "__main__":
    main()
