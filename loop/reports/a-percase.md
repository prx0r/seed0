# a-percase — progress report

## 1. claim
Per-case time/tokens/cost now metered; live re-run still 429-blocked ($0.00).

## 2. evidence
- pyeval results rows carry `elapsed_s/input_tokens/output_tokens/cost_usd`
  on ALL paths (pass, transport-fail, budget-stop, pre-call refusal).
  Receipt cases mirror the fields. Stub test proves nonzero attribution.
- Live re-run (capped $0.01): 3× 429, per-case elapsed 0.48/0.45/0.47s,
  tokens 0/0, cost $0.0. Receipt sha256:d4e4… verifies. Quota still out;
  stopped after 1 attempt (no hammering).

## 3. self-review
Correction landed before live data exists to fill it — schema proven by
stubs, production values pending quota. Judge-model second calls share the
case row (documented, not split).

## 4. needs
M4 (quota-gated re-run). Nothing else.

## 5. cost
$0.00 verified (3 consecutive capped runs, budget caps untouched).
