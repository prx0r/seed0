# a-wave1 — progress report (10 items)

## 1. claim
Wave 1 closed: metering, hooks, attempt records, WIP checkpoints, stability
bout, value weights, claim flow, eval_arch verdict, recall, catalog test.

## 2. evidence (per item)
- B1: funnel writes spend.jsonl per attempt (elapsed measured, tokens honest
  zeros); test asserts shape.
- S23: scripts/install-hooks.py (install refuses overwrite, uninstall,
  local-only); roundtrip tested.
- S22: attempt.json (seed/brief-sha/rubric-ids/cmd/started) in every attempt.
- S19: TimeoutExpired → git-init + WIP commit (genuine timeout proven after
  fixing a test that faked timeouts via argv echo — see §3).
- bout4: stability under input shuffle — seed5 5/5 stable, seed1 0/5, seed3
  1/5; mechanism = tie order follows input (sorted stability); receipted.
- B3: value_usd counts as priority points (documented policy); tested delta.
- claim/release: ownership enforced (held-by refuses takeover); tested.
- eval_arch on bout3 winner: evidence.txt load-bearing (first real use).
- recall: keyword-scoped report+decisions search; tested hit/miss.
- B12: catalog test caught 4 missing modules (fixed docs, not test).

## 3. self-review (findings that seed wave 2)
- F1: funnel agent_cmd uses naive .split() — quoted commands SyntaxError
  (found live). → W2: shlex.
- F2: tournament_*.jsonl accumulates in CWD (50 files) → W2: --out flag.
- F3: pre-commit installed; no pre-push story → W2: --with-push.
- F4: policy.py unused by ham → W2: ham policy command.
- F5: judge-model tokens share case rows → W2: separate attribution.
- F6: no ledger-level verify-all → W2: runs.verify_all.
- F7: stability verdict needs a tie-break rule → W2: metaguide line.
- F8: learn.py never fired (all green) → W2: run on meta scores, record zero.

## 4. needs
Nothing new (queues unchanged).

## 5. cost
$0, no manual actions.
