# g-rail-probe — progress report

## 1. claim
x402 rail DOWN on all 3 endpoints (work/supply/demand: 308, $0 spent).

## 2. evidence
`curl --max-redirs 2` (no follow-loop, single probes): work/supply/demand
all `http=308`. Matches t0-e2e finding (self-loop) — rail still not serving
402 quotes. Read-only probes; nothing sent, nothing paid.

## 3. self-review
308 could be Caddy misconfig rather than dead service (can't distinguish
remotely — stated; H-x402 covers the box-side check).

## 4. needs
H-x402 (unchanged). Nothing else.

## 5. cost
$0, no manual actions.
