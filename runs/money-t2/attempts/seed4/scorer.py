"""Toy bottleneck scorer: score = demand_growth * supply_inelasticity."""
import json

OPPORTUNITIES = [
    {"name": "p2p_gold_xrf_verification", "demand_growth": 0.90, "supply_inelasticity": 0.85},
    {"name": "ai_listing_authentication_app", "demand_growth": 0.85, "supply_inelasticity": 0.40},
    {"name": "general_home_inspection", "demand_growth": 0.50, "supply_inelasticity": 0.55},
    {"name": "online_bullion_marketplace", "demand_growth": 0.80, "supply_inelasticity": 0.30},
    {"name": "pawn_shop_franchise", "demand_growth": 0.40, "supply_inelasticity": 0.45},
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
