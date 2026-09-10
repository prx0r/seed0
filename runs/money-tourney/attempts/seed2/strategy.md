# Strategy: EICR + Remedial Wedge for Private Rentals (one city)

## Opportunity
Offer EICR inspections + fixed-price consumer-unit / remedial work for private
landlords in one city (e.g. Leeds LS postcodes), booked in 48h, cert in 24h.

## Bottleneck mechanism
Abundance → scarcity causal arrow: abundance of automated lettings / tenant-
churn software and tightening rental compliance rules induces demand for
physical electrical validation faster than supply of certified electricians
can respond. The bottleneck is qualified tester-hours: only a licensed sparky
can legally sign an EICR and do remedials on-site. Portals can create infinite
leads; tester-hours cannot scale. That bottleneck is where pricing power sits.

## Crowdedness read
Property-tech and "picks-and-shovels for AI data-centres" is the crowded
consensus trade — everyone pitches grid-scale or platform plays. This wedge is
not crowded: national contractors chase large commercial jobs and ignore
sub-£1k domestic remedials; local sparkies do not offer 48h booking + fixed
prices + agent integrations. Edge survives because incumbents are fragmented,
slow to quote, and avoid paperwork; we standardise one job type in one area.

## Falsifiable prediction (ONE)
Prediction #1 (falsifiable): median EICR-to-remedial lead time for private
rentals in our target postcodes will exceed 6 weeks by Q2 2027, and our
48h-slot offer will sustain >60% gross margin on 30+ jobs/month. This is
falsified if median lead time is ≤4 weeks in Q2 2027 OR we cannot hold 60%
margin at 30 jobs/month.

## Sliced scope
One wedge only: domestic EICR + remedials <£1k in one city. No commercial,
no EV, no solar. Gated independently on jobs/month and margin.

## Scorer inputs (documented floats)
| name | demand_growth | supply_inelasticity | score |
|---|---|---|---|
| eicr_remedials_rentals | 0.90 | 0.85 | 0.765 |
| ev_charger_installs | 0.80 | 0.60 | 0.480 |
| solar_maintenance | 0.70 | 0.55 | 0.385 |
| smart_home_retrofit | 0.60 | 0.40 | 0.240 |
| commercial_rewire | 0.75 | 0.50 | 0.375 |

Top rank is eicr_remedials_rentals by demand_growth × supply_inelasticity.

## Costed thinking
Tiny build: scorer + 4 tests, ~5 min, stdlib only.
