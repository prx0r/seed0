"""Toy bottleneck scorer: score = demand_growth * supply_inelasticity."""
import json

OPPORTUNITIES = [
    {"name": "landlord-eicr-remedials-manchester", "demand_growth": 0.9, "supply_inelasticity": 0.85},
    {"name": "ev-charger-domestic-installs", "demand_growth": 0.8, "supply_inelasticity": 0.7},
    {"name": "solar-battery-retrofit-surveys", "demand_growth": 0.7, "supply_inelasticity": 0.6},
    {"name": "smart-meter-install-support", "demand_growth": 0.5, "supply_inelasticity": 0.4},
    {"name": "generic-handyman-electrical", "demand_growth": 0.3, "supply_inelasticity": 0.3},
]


def score_opp(opp):
    return opp["demand_growth"] * opp["supply_inelasticity"]


def ranked():
    scored = [{"name": o["name"], "score": score_opp(o)} for o in OPPORTUNITIES]
    scored.sort(key=lambda d: d["score"], reverse=True)
    return scored


def main():
    print(json.dumps(ranked()))


if __name__ == "__main__":
    main()
