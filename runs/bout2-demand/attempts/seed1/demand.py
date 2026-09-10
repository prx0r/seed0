"""Weekly demand estimator for domestic gas-boiler annual servicing.

Market: residential gas-boiler annual service visits, by postcode district.

Model: demand = dwellings x annual_service_rate / 52.

Sources (all figures are ESTIMATES for modelling only, not official stats):
- Dwelling counts: estimates synthesised from ONS Census 2021 household
  counts and local-authority housing totals, rounded for this exercise.
- Annual service rates: estimates based on Gas Safe Register guidance that
  boilers should be serviced yearly, adjusted down for landlord-vs-owner
  mix and affordability (industry commentary typically cites 60-90%).
"""

from __future__ import annotations

# postcode -> {"dwellings": int, "turnover": float (annual service rate)}
AREAS: dict[str, dict[str, float]] = {
    "OX1": {"dwellings": 12500, "turnover": 0.82},
    "OX2": {"dwellings": 14800, "turnover": 0.78},
    "OX3": {"dwellings": 11200, "turnover": 0.85},
    "OX4": {"dwellings": 18400, "turnover": 0.75},
    "OX33": {"dwellings": 6300, "turnover": 0.88},
    "SW1A": {"dwellings": 4100, "turnover": 0.65},
}

WEEKS_PER_YEAR = 52


def _norm(postcode: str) -> str:
    return postcode.strip().upper()


def weekly_demand(postcode: str) -> float:
    """Estimated boiler-service jobs per week for a postcode district.

    Returns 0.0 for unknown postcodes.
    """
    area = AREAS.get(_norm(postcode))
    if area is None:
        return 0.0
    return area["dwellings"] * area["turnover"] / 52


def rank(postcodes: list[str]) -> list[str]:
    """Return postcodes sorted by descending weekly demand (stable)."""
    return sorted(postcodes, key=lambda p: weekly_demand(p), reverse=True)
