"""Weekly demand estimator for residential boiler annual service.

Market: residential gas-boiler annual service visits (compliance/service trade).

Model: expected service jobs per week per postcode area =
    dwellings * annual_turnover_rate / 52.

Data below are illustrative estimates (not official statistics):
dwellings approximated from local housing-stock estimates, turnover rate
approximated from assumed share of homes booking a paid annual service
each year. Sources documented as estimates per brief.
"""

AREAS = {
    # postcode: (dwellings estimate, annual turnover rate estimate)
    "LE1": {"dwellings": 12000, "turnover": 0.60},
    "LE2": {"dwellings": 18000, "turnover": 0.55},
    "LE3": {"dwellings": 9000, "turnover": 0.70},
    "LE4": {"dwellings": 15000, "turnover": 0.40},
    "LE5": {"dwellings": 7000, "turnover": 0.65},
    "LE6": {"dwellings": 20000, "turnover": 0.30},
}


def weekly_demand(postcode: str) -> float:
    """Return estimated service jobs per week for a postcode.

    Returns 0.0 for unknown postcodes.
    """
    area = AREAS.get(postcode)
    if area is None:
        return 0.0
    return area["dwellings"] * area["turnover"] / 52.0


def rank(postcodes: list[str]) -> list[str]:
    """Rank postcodes in descending order of weekly demand."""
    return sorted(postcodes, key=lambda p: weekly_demand(p), reverse=True)
