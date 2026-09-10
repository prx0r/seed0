# Strategy: Landlord EICR + Remedial Sparky Slots (London rentals wedge)

## Opportunity
Dedicated EICR testing + fixed-price remedial slots for London letting agents:
book the test, fail items fixed in the same 14-day window, certificate issued.

## Bottleneck mechanism
Abundance → scarcity causal arrow: an abundance of rental listings churn plus
cheap automated compliance reminders induces demand for physical validation
faster than supply responds. Every reminder needs a certified sparky inside the
flat with a tester. The bottleneck is qualified electrician-hours for EICR
tests and C1/C2 remedials — training + accreditation take years, so short-run
supply is near-vertical while reminder-driven demand spikes each quarter.

## Crowdedness read
"Picks-and-shovels for landlords" ( Tenant-find apps, compliance SaaS, lead-gen
directories) is the crowded consensus trade — dozens of platforms already
there. This wedge is NOT that: it sells the unsexy physical bottleneck slot
itself, not software. Edge survives the crowded field because directories
cannot conjure sparky-hours; agents pay for guaranteed 14-day certificate
turnaround, and generalist electricians prefer bigger rewire jobs, leaving the
small remedial wedge underserved.

## Falsifiable prediction
Prediction 1 (falsifiable, with numbers): median EICR-booking to certificate
lead time for London lets managed by our partner agents exceeds 6 weeks by
end of Q2 2027, and our slot price of £249 holds with ≥70% utilisation. This
is proved wrong (falsify condition): if by 2027-06-30 the median lead time is
under 4 weeks OR our utilisation at £249 falls below 40% for 2 straight
months, the bottleneck thesis for this wedge is false and we kill it.

## Sliced scope (P4)
One wedge only: EICR + remedials via letting-agent channel in London. Gated
independently. Explicitly OUT: rewires, EV chargers, heat pumps, solar —
scored below only as mock comparisons.

## Scorer inputs (documented floats)
| name | demand_growth | supply_inelasticity | score |
|---|---|---|---|
| eicr-remedial-slots | 0.90 | 0.85 | 0.765 |
| ev-charger-installs | 0.80 | 0.60 | 0.480 |
| heat-pump-commissioning | 0.70 | 0.65 | 0.455 |
| solar-rooftop-retrofit | 0.60 | 0.50 | 0.300 |
| smart-meter-swaps | 0.50 | 0.40 | 0.200 |
Score = demand_growth × supply_inelasticity.

## Cost log (P6)
Tiny build: 4 tests, pytest run ~1s, stdlib only.
