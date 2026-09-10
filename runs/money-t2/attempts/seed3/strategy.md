# Strategy: Permitted EV panel-upgrade brokerage for older homes

## Opportunity
A local brokerage that turns abundant cheap Level-2 EV chargers + installer
capacity into booked, permitted 100A→200A panel upgrades for pre-1990 homes:
fixed-price site survey, permit filing, vetted electrician slot, utility
interconnect paperwork — margin on the coordination wedge.

## Bottleneck mechanism
Abundance of cheap EVs and sub-$500 Level-2 chargers induces demand for
physical validation (a permitted panel with spare capacity) faster than supply
responds: licensed electrician hours and permit-desk throughput are the
bottleneck. The charger is abundant; the bottleneck is the inspected panel
behind it — every new EV in an older home must pass through that scarce slot.

## Crowdedness read
The consensus trade is crowded at the abundant layer: selling chargers,
generic solar/EV lead-gen, and national installer marketplaces compete on ad
spend. Almost nobody wants the unglamorous permit queue in one county —
paperwork, inspections, reschedules. This wedge is uncrowded because it is
local, slow-looking, and unscalable-in-software, which is exactly why the
bottleneck rent persists.

## Inputs (documented floats for scorer.py)
| name | demand_growth | supply_inelasticity |
|---|---|---|
| ev-panel-brokerage | 0.85 | 0.90 |
| charger-resale | 0.70 | 0.25 |
| generic-solar-leadgen | 0.60 | 0.30 |
| handyman-marketplace | 0.50 | 0.40 |
| battery-import-flip | 0.75 | 0.55 |

Score = demand_growth × supply_inelasticity.

## Falsifiable prediction
1. FALSIFIABLE: within 90 days of launch in one county, we book ≥25 paid
surveys at ≥$49 with ≥30% converting to ≥$1,800 upgrades; WRONG if paid
surveys <15 or conversion <15% or median permit-to-install exceeds 45 days —
then the bottleneck thesis is falsified for this market and we shut it down.
