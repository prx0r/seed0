# Strategy: Same-Week EICR + Minor Remedials for Private Landlords

## Opportunity
Same-week Electrical Installation Condition Report (EICR) certification plus
minor remedials (consumer-unit fixes, bonding, fault-finding) for private
landlords facing compliance deadlines in one city.

## Bottleneck mechanism
The bottleneck is qualified physical validation. Abundance of cheap
lettings/property-tech onboarding and tightening rental compliance rules
induces a surge in demand for in-person electrical inspection, while the
supply of registered electricians responds slowly (multi-year training,
accreditation, insurance). So: regulatory + platform abundance → scarcity of
certified inspection slots. That causal arrow is the whole edge: digital
volume can scale overnight, EICR sign-off cannot.

## Crowdedness read
General "picks-and-shovels for rentals" (lettings agencies, property portals,
generic handyman apps) is crowded and consensus. This wedge is not the
consensus trade because it is unglamorous, geographically bound, and gated
on credentials: national platforms avoid sub-scale compliance jobs with
call-back liability, and generic tradespeople cannot sign off EICRs without
the right scheme membership. Edge survives because incumbents chase big
rewires/installs while landlords need a dated certificate plus small fixes
before they can legally let.

## Sliced scope (P4)
One wedge only: EICR + minor remedials (<half-day fixes) in one city,
booked direct with landlords/agents. No rewires, no commercial, no quant
factors, no biology, no grid work. Gated independently on booked EICRs/week.

## Mock inputs documented (for scorer.py)
Five hardcoded opportunities with demand_growth × supply_inelasticity floats:

| name | demand_growth | supply_inelasticity | score |
|---|---|---|---|
| eicr_landlord_rush | 0.9 | 0.85 | 0.765 |
| ev_charger_install | 0.8 | 0.6 | 0.48 |
| generic_handyman | 0.5 | 0.3 | 0.15 |
| solar_farm_dev | 0.7 | 0.5 | 0.35 |
| smart_home_gadgets | 0.6 | 0.25 | 0.15 |

## Falsifiable prediction #1
Falsifiable prediction: median quoted lead time for an EICR in our target
city exceeds 3 weeks (21 days) by 2026-12-31, measured by mystery-shopping
10 listed electricians; this prediction is falsified if the median lead time
is 21 days or fewer on that date.

## Cost log (P6)
Tests: 4. Time: minutes (single pytest run, stdlib only).
