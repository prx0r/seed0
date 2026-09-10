"""Toy bottleneck scorer: score = demand_growth * supply_inelasticity."""
import json

OPPORTUNITIES = [
    {"name": "eicr-hmo-validation", "demand_growth": 0.90, "supply_inelasticity": 0.85},
    {"name": "ev-charger-commissioning", "demand_growth": 0.70, "supply_inelasticity": 0.80},
    {"name": "heat-pump-retrofit-check", "demand_growth": 0.60, "supply_inelasticity": 0.75},
    {"name": "solar-inspection", "demand_growth": 0.50, "supply_inelasticity": 0.60},
    {"name": "smart-meter-install", "demand_growth": 0.40, "supply_inelasticity": 0.50},
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
