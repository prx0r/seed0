# Strategy: Landlord EICR + remedial works wedge (Greater Manchester)

## Opportunity
Sell fixed-price EICR inspections with next-day remedial quotes to landlords managing 1–10 units in Greater Manchester.

## Bottleneck mechanism
Abundance of rental regulation and cheap digital compliance reminders induces demand for physical electrical validation faster than supply responds. The bottleneck is certified electricians legally allowed to sign an EICR: every new rule creates more inspection demand, but the pool of qualified testers grows slowly (training + assessment + insurance), so lead times and call-out prices spike at the signing step.

## Crowdedness read
The crowded trade is generic "picks-and-shovels for landlords" (letting-agent referrals, national compliance platforms, checklists). Those players are crowded at the software/reminder layer but thin on the tools that do the physical sign-off. Edge survives because: (a) incumbents sell subscriptions, not same-week van visits; (b) national firms route through call centres, inflating lead time; (c) a one-postcode van route undercuts travel overhead they cannot match.

## Sliced scope (P4)
One wedge only: domestic EICR + C1/C2 remedials for private rentals in M-postcodes. No commercial EICR, no EV chargers, no solar — each gated independently later.

## Falsifiable prediction
PREDICTION 1 (falsifiable): by 2026-12-31, median quoted EICR lead time from 5 sampled Manchester electricians exceeds 14 days AND entry EICR price exceeds £150; if both are not true, the thesis is wrong and the wedge is falsified.

## Scorer inputs (documented floats)
| name | demand_growth | supply_inelasticity | score |
|---|---|---|---|
| landlord-eicr-remedials-manchester | 0.9 | 0.85 | 0.765 |
| ev-charger-domestic-installs | 0.8 | 0.7 | 0.56 |
| solar-battery-retrofit-surveys | 0.7 | 0.6 | 0.42 |
| smart-meter-install-support | 0.5 | 0.4 | 0.2 |
| generic-handyman-electrical | 0.3 | 0.3 | 0.09 |

## Cost log (P6)
Build: 3 tests, ~2 min pytest run. Tokens/time treated as real cost; kept build to 2 small files.
