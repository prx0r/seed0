"""Toy bottleneck scorer: score = demand_growth * supply_inelasticity."""
import json

OPPORTUNITIES = [
    {"name": "ev-panel-brokerage", "demand_growth": 0.85, "supply_inelasticity": 0.90},
    {"name": "charger-resale", "demand_growth": 0.70, "supply_inelasticity": 0.25},
    {"name": "generic-solar-leadgen", "demand_growth": 0.60, "supply_inelasticity": 0.30},
    {"name": "handyman-marketplace", "demand_growth": 0.50, "supply_inelasticity": 0.40},
    {"name": "battery-import-flip", "demand_growth": 0.75, "supply_inelasticity": 0.55},
]


def score(opp):
    return opp["demand_growth"] * opp["supply_inelasticity"]


def ranked():
    rows = [{"name": o["name"], "score": score(o)} for o in OPPORTUNITIES]
    return sorted(rows, key=lambda r: r["score"], reverse=True)


if __name__ == "__main__":
    print(json.dumps(ranked()))
