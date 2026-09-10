# T0-E2E TRIAGE 2026-09-10 — "make me money" run (all $ figures traced or absent)

## Probe outputs (verbatim, $0 spent, no payment sent)

- P1 x402 GET /v1/work: `HTTP/2 308 location: <same URL>` ×5 (self-redirect
  loop, followed with -L). P2 GET /v1/supply: `http=308`. No 402 quote, no
  body. Rail DOWN-or-moved at probe time (contradicts bundle "live" claim —
  divergence logged, not hidden).
- P3 hplane funnel: 3 rows, all `dark` (seed0, voiceagent, mw — zero
  registries estate-wide, including ours).
- P4 spend state: `loop/registry_m.jsonl` absent, `spend.jsonl` absent →
  run spend $0. Receipts on disk: 40 (pre-existing).

## Rank (binary columns; rank = count of YES)

| surface | live? | priced? | receipt-path? | $0-next-action? | score |
|---|---|---|---|---|---|
| x402 rail | NO (308 loop) | YES ($0.005/work, bundle docs) | YES (x402 receipts) | YES (fix server) | 3 |
| sparky pilot | NO (unpiloted) | YES (ranges in profile) | PARTIAL (call logs exist, no pay path) | YES (book pilot call) | 2.5 |
| mw oracle/market | PARTIAL (code, no trunk) | NO | PARTIAL | NO (needs H5 first) | 1 |
| seed0 machine | n/a (cost center) | n/a | YES (receipts) | YES (leverage) | — |

No surface is autonomously monetizable today. That is the finding, not a failure.

## Executed A-prefix ($0, reversible)

- Probes P1–P4 run and logged above. Triage ranked. Queues filed below.
- No grant proposed, none activated (no spend target exists — proposing one
  would invent a reason to spend).

## Queued remainder (exact, with demos)

- **H-x402**: check server (Caddy → :4021/systemd per bundle README). Demo of
  done: `curl -s -o /dev/null -w "%{http_code}" https://x402.egoic.ai/v1/work`
  returns **402** (quote, not 308). No amount (ops time).
- **H-sparky**: book 1 pilot electrician call on sparky-vertical. Demo of
  done: call log + transcript in repo. No amount (owner time).
- **M**: NONE. $0 state held; next spend (if any) arrives as a grant with
  cents+purpose+expiry for explicit approval.
