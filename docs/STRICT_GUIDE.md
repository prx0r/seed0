# STRICT GUIDE — how all future work runs (no exceptions, no vibes)

## 1. Every agent run is measured from the outside

- Launch agents with `agentrun.py` (or equivalent): `--name`, `--model`,
  `--timeout`, `--usage-file`, then `-- <command>`.
- Time comes from OUR stopwatch (monotonic), never the agent's report.
- Tokens come from a usage file (`hermes -z ... --usage-file lane/usage.json`)
  or API usage block. No usage channel = `unknown`, never zero-by-guess.
  No inference at all = `no-inference`, zero by fact.
- Timeout kills the process. Kills, failures, and timeouts are RECORDED
  with their tails — never raised past the runner, never hidden.

## 2. Every run ends in a receipt with all five numbers

`agent, model, elapsed_s, input_tokens, output_tokens, cost_usd,
usage_source, returncode/timed_out, log_tail`. Missing any one = incomplete
run. Receipts verify (`runs.verify_file`) or the run didn't happen.

## 3. Money rules (absolute)

- No spend without a grant stating integer cents + purpose + expiry.
- Every run carries `--timeout` and (for model runs) a `--budget-usd` cap.
- Cost = tokens × priced model table. Unpriced model = cost null, stated.
- Quota 429 = stop after the capped attempt. No hammering, ever.

## 4. Work rules (absolute)

- Frozen brief + rubric + validator BEFORE lanes. Baseline validator exit 1
  on empty work (proves the gate can fail).
- Isolated lanes, validator exit 0 to finish, max 3 tries.
- Independent re-run of every validator by the reviewer.
- Blind review before reveal. Hypothesis verdicts from preregistered
  thresholds, never from rank.
- A-log every action with re-runnable evidence. No log, no claim.
- H-promotion only from blocked A-tasks, lowest-barrier form enforced.
- Plain-language close: what was done, what came out, what's blocked on
  a human, what it cost. Anyone reading must know what happened.

## 5. Banned

Estimating tokens. Quoting memory as measurement. Grading your own lanes.
Asking the user questions to avoid deciding. Filler tasks. Adjectives
without numbers. Pushing secrets. Rewriting history (append corrections).
