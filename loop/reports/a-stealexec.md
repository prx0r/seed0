# a-stealexec — progress report

## 1. claim
Exec-layer steals live: evidence memo, intent fields, lane risk, falsifiers.

## 2. evidence
- Evidence memo: `command: || inputs:` skips green reruns on unchanged hashes
  (test: marker absent on 2nd run, re-runs after touch). No inputs list =
  always re-run (no free lunch, enforced).
- `intent` on A-log lines + `--intent` flag (STORM annotations).
- `funnel.lane_risk`: overlap pairs + greedy phases (test: overlapping lanes
  never share a phase, all lanes placed).
- `funnel.amend(..., falsifier=...)` recorded in AMENDMENTS.jsonl (tested).

## 3. self-review
Memo lives beside queue (loop/.memo.json, untracked state — survives nothing
by design; recompute is cheap). Greedy phasing is not optimal packing
(scheduling NP-hard; greedy documented as heuristic). Intent is free text,
unenforced content (v1 honesty over v2 structure).

## 4. needs
None. Queues unchanged.

## 5. cost
$0, no manual actions.
