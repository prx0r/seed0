# g-quota-probe — progress report

## 1. claim
Quota still exhausted (3× 429); spend $0.00; per-case metering verified live.

## 2. evidence
Capped run ($0.01 hard cap): 3 cases refused at transport, each row carries
elapsed_s/tokens/cost ($0.0). Receipt sha256:f41d… verifies. Budget cap
untouched. 4th consecutive 429 day — free-tier day boundary unknown.

## 3. self-review
Retrying daily is correct; retrying hourly would be hammering. Next probe
belongs to a pulse, not this turn.

## 4. needs
M4 (quota-gated). Nothing else.

## 5. cost
$0.00 (cap enforced, verified in receipt telemetry).
