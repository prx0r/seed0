"""Toy bottleneck scorer: score = demand_growth * supply_inelasticity."""
import json

OPPORTUNITIES = [
    {"name": "eicr_remedials_rentals", "demand_growth": 0.90, "supply_inelasticity": 0.85},
    {"name": "ev_charger_installs", "demand_growth": 0.80, "supply_inelasticity": 0.60},
    {"name": "solar_maintenance", "demand_growth": 0.70, "supply_inelasticity": 0.55},
    {"name": "commercial_rewire", "demand_growth": 0.75, "supply_inelasticity": 0.50},
    {"name": "smart_home_retrofit", "demand_growth": 0.60, "supply_inelasticity": 0.40},
]


def score_opps(opps=None):
    opps = OPPORTUNITIES if opps is None else opps
    ranked = [
        {"name": o["name"], "score": o["demand_growth"] * o["supply_inelasticity"]}
        for o in opps
    ]
    ranked.sort(key=lambda d: d["score"], reverse=True)
    return ranked


def main():
    print(json.dumps(score_opps()))


if __name__ == "__main__":
    main()
