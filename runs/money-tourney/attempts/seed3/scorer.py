"""Toy bottleneck scorer: score = demand_growth * supply_inelasticity."""
import json

OPPORTUNITIES = [
    {"name": "eicr_landlord_rush", "demand_growth": 0.9, "supply_inelasticity": 0.85},
    {"name": "ev_charger_install", "demand_growth": 0.8, "supply_inelasticity": 0.6},
    {"name": "solar_farm_dev", "demand_growth": 0.7, "supply_inelasticity": 0.5},
    {"name": "generic_handyman", "demand_growth": 0.5, "supply_inelasticity": 0.3},
    {"name": "smart_home_gadgets", "demand_growth": 0.6, "supply_inelasticity": 0.25},
]


def score(opps=None):
    opps = opps if opps is not None else OPPORTUNITIES
    ranked = [
        {"name": o["name"], "score": o["demand_growth"] * o["supply_inelasticity"]}
        for o in opps
    ]
    ranked.sort(key=lambda r: r["score"], reverse=True)
    return ranked


def main():
    print(json.dumps(score()))


if __name__ == "__main__":
    main()
