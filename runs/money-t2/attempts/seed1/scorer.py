"""Toy bottleneck scorer: score = demand_growth * supply_inelasticity.

Mock inputs are hardcoded and documented in strategy.md.
Emits ranked JSON to stdout: [{"name":..., "score":...}].
Stdlib only, no network, no secrets.
"""
import json

OPPORTUNITIES = [
    {"name": "pre-listing inspection wedge", "demand_growth": 0.90, "supply_inelasticity": 0.85},
    {"name": "ev-charger commissioning", "demand_growth": 0.80, "supply_inelasticity": 0.70},
    {"name": "rural septic/well validation", "demand_growth": 0.70, "supply_inelasticity": 0.75},
    {"name": "generic handyman marketplace", "demand_growth": 0.60, "supply_inelasticity": 0.40},
    {"name": "ai-staging software", "demand_growth": 0.95, "supply_inelasticity": 0.20},
]


def score_opportunity(demand_growth, supply_inelasticity):
    return demand_growth * supply_inelasticity


def ranked():
    scored = [
        {"name": o["name"], "score": score_opportunity(o["demand_growth"], o["supply_inelasticity"])}
        for o in OPPORTUNITIES
    ]
    scored.sort(key=lambda d: d["score"], reverse=True)
    return scored


def main():
    print(json.dumps(ranked()))


if __name__ == "__main__":
    main()
