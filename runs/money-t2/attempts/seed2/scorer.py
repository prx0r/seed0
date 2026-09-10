"""Toy bottleneck scorer: score = demand_growth * supply_inelasticity."""
import json

OPPORTUNITIES = [
    {"name": "dc_backup_witness_test", "demand_growth": 0.90, "supply_inelasticity": 0.85},
    {"name": "substation_thermography", "demand_growth": 0.70, "supply_inelasticity": 0.60},
    {"name": "home_battery_install_audit", "demand_growth": 0.60, "supply_inelasticity": 0.40},
    {"name": "ev_charger_site_survey", "demand_growth": 0.50, "supply_inelasticity": 0.35},
    {"name": "solar_drone_inspection", "demand_growth": 0.45, "supply_inelasticity": 0.30},
]


def score_opp(opp):
    return opp["demand_growth"] * opp["supply_inelasticity"]


def ranked():
    rows = [{"name": o["name"], "score": score_opp(o)} for o in OPPORTUNITIES]
    rows.sort(key=lambda r: r["score"], reverse=True)
    return rows


def main():
    print(json.dumps(ranked()))


if __name__ == "__main__":
    main()
