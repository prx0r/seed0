# Strategy: Mobile XRF Assay Verification for P2P Gold/Bullion Trades

## Opportunity
On-demand mobile XRF (X-ray fluorescence) assay verification for peer-to-peer
gold coin / bullion trades in one metro area: a van with a certified operator
and an XRF gun meets buyer+seller at a bank or police safe-trade station and
issues a signed assay slip for a flat $49 fee.

## Bottleneck mechanism
The bottleneck is trusted physical validation. Abundance of online P2P
listings (zero-marginal-cost posts, AI-generated photos/descriptions, cheap
tungsten-filled fakes) induces demand for physical validation faster than
supply responds: anyone can list 100 fake coins in an hour, but each trade
still needs 15 minutes of instrumented assay by a trained operator with a
calibrated $20k device. Demand for verification scales with listing abundance;
supply of assay slots scales with vans, devices, and operators — slow and
inelastic. That bottleneck (unverified value-at-risk piling up at the assay
step) is where the fee wedge lives.

## Crowdedness read
The crowded consensus trade is another marketplace feature or AI photo
authentication app — pure software, zero marginal cost, infinitely
replicable. This wedge is crowded-free by construction: it is unglamorous
field work (driving, calibrating, handling disputes), requires capex plus
skill, and earns per-test fees instead of venture scale. Software founders
avoid it; pawn shops stay in-store; labs serve refiners, not consumers. Not
the consensus trade.

## Scorer inputs (documented floats for scorer.py)
| name | demand_growth | supply_inelasticity | score |
|---|---|---|---|
| p2p_gold_xrf_verification | 0.90 | 0.85 | 0.765 |
| ai_listing_authentication_app | 0.85 | 0.40 | 0.340 |
| general_home_inspection | 0.50 | 0.55 | 0.275 |
| online_bullion_marketplace | 0.80 | 0.30 | 0.240 |
| pawn_shop_franchise | 0.40 | 0.45 | 0.180 |

Score = demand_growth × supply_inelasticity; ranked descending.

## Falsifiable prediction
Falsifiable prediction #1: running 3 paid weekend assay pop-ups within 60
days will complete ≥30 paid assays at ≥$49 with ≥40% of customers citing
"fake-listing fear" as the reason; if paid assays <15 or cited-fear share
<20%, the thesis is wrong and the wedge is abandoned.
