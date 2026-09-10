"""Weekly demand estimator for residential gas-boiler annual servicing.

Market: compliance-driven annual servicing of domestic gas boilers.
Each postcode area has an estimated dwelling stock and an estimated
share of dwellings with a gas boiler serviced annually (turnover rate).
Weekly demand = dwellings * turnover / 52.

Sources (estimates): dwelling counts are illustrative estimates modelled
on ONS household-stock magnitudes; turnover rates are estimates based on
typical gas-central-heating penetration (~75-85%) and annual service
compliance (~60-75%). All figures are planning estimates, not official stats.
"""

AREAS = {
    "B1": {"dwellings": 45000, "turnover": 0.55},
    "B2": {"dwellings": 62000, "turnover": 0.60},
    "B3": {"dwellings": 30000, "turnover": 0.50},
    "B4": {"dwellings": 80000, "turnover": 0.65},
    "B5": {"dwellings": 52000, "turnover": 0.58},
    "B6": {"dwellings": 38000, "turnover": 0.62},
}


def weekly_demand(postcode: str) -> float:
    """Return estimated weekly boiler-service jobs for a postcode.

    Returns 0.0 for unknown postcodes.
    """
    area = AREAS.get(postcode)
    if area is None:
        return 0.0
    return area["dwellings"] * area["turnover"] / 52.0


def rank(postcodes: list[str]) -> list[str]:
    """Rank postcodes by descending weekly demand."""
    return sorted(postcodes, key=lambda p: weekly_demand(p), reverse=True)
