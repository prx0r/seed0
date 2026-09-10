"""Toy bottleneck scorer: score = demand_growth * supply_inelasticity."""
import json

OPPORTUNITIES = [
    {"name": "datacenter-loadbank-testing", "demand_growth": 0.85, "supply_inelasticity": 0.90},
    {"name": "ev-charger-repair", "demand_growth": 0.70, "supply_inelasticity": 0.60},
    {"name": "home-solar-inspection", "demand_growth": 0.60, "supply_inelasticity": 0.50},
    {"name": "ai-print-on-demand", "demand_growth": 0.90, "supply_inelasticity": 0.20},
    {"name": "generic-chatbot-agency", "demand_growth": 0.50, "supply_inelasticity": 0.30},
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
