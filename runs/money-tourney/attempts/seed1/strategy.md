# Strategy: Independent EICR + Thermal Validation for London HMO Landlords

## Opportunity (one wedge, P4)
Independent Electrical Installation Condition Report (EICR) + thermal-imaging
validation for HMO landlords in London Zones 2–3. Fixed-fee, 48h report
turnaround, remedial upsell gated separately. Nothing else: no rewires, no
heat pumps, no EV chargers — one wedge, gated independently.

## Bottleneck mechanism (P1)
Abundance → scarcity causal arrow: abundance of cheap rental-listing flow and
AI-assisted landlord onboarding induces demand for physical electrical
validation faster than supply responds. Every new listing/tenant churn legally
needs a certified human sparky to inspect, test, and sign the EICR. The
bottleneck is certified sign-off capacity: only qualified electricians can
legally clear a property, and training/accreditation is slow, so supply is
inelastic while validation demand compounds. That bottleneck mechanism is the
whole trade — sell the scarce sign-off, not the abundant listings.

## Crowdedness read (P2)
"Crowded" check: picks-and-shovels electrical firms, letting-agent panels, and
Checkatrade generalists are already there. This is not the consensus trade
because (a) panels optimise for cheap pass-through, not 48h SLA with thermal
evidence photos landlords use in disputes; (b) generalist sparkies chase big
rewires, leaving sub-£250 EICRs underserved; (c) agent panels take 30–50% cuts,
so independents undercutting them on speed keep the margin. The edge survives
the crowded field by slicing one micro-wedge (HMO EICRs, Zones 2–3) and winning
on lead time, not price.

## Falsifiable prediction (P3)
1. Falsifiable prediction: by 2027-03-31, the median bookable EICR lead time
for 5 sampled Zone 2–3 independents exceeds 21 days AND our 48h-slot fill rate
exceeds 80%; if median lead time is below 14 days, the scarcity thesis is
falsified and we shut the wedge down.

## Scorer inputs (documents scorer.py floats)
| name | demand_growth | supply_inelasticity | score |
|---|---|---|---|
| eicr-hmo-validation | 0.90 | 0.85 | 0.765 |
| ev-charger-commissioning | 0.70 | 0.80 | 0.560 |
| heat-pump-retrofit-check | 0.60 | 0.75 | 0.450 |
| solar-inspection | 0.50 | 0.60 | 0.300 |
| smart-meter-install | 0.40 | 0.50 | 0.200 |

Score = demand_growth × supply_inelasticity. Ranking puts the EICR bottleneck first.

## Cost log (P6)
Tiny build: 4 tests, ~30s pytest run, stdlib only.
