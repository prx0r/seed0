# GOALS — a-goal as a dumb algorithm (SPEC v1, no Monte Carlo)

## 1. Definitions

- **a-goal**: the end desired state the user wants, written as acceptance
  criteria + evidence paths. A goal is a NORTHSTAR frozen file + the task DAG
  that closes it. It is DONE iff every acceptance item is covered by ≥1 DONE
  task receipt (goal-level stoplight).
- **a-task**: one DAG node. Carries `acceptance[]`, `evidence_required[]`,
  `blocked_by[]` (other task ids, default []), `branch` (git branch name).
- **Validator contract** (the whole trick): the validator expects EXACTLY the
  acceptance items + evidence paths named when the task was JUSTIFIED —
  nothing else, no judgment, no partial credit. Accept iff all check;
  reject with the missing list. `loop.py stoplight` IS this contract.

## 2. The algorithm (runs every pulse)

```
1. READY = {t : status in (JUSTIFIED, EXECUTING) and all blocked_by DONE}
2. For each ready t (parallel where independent):
     branch = tasks/<tid> (create from main, or resume if exists)
     execute → log A-log lines tagging covers[] → report → receipt
     stoplight GO → DONE + merge branch FF + delete branch
     stoplight NOGO → keep working, or REJECTED with reason
3. GOAL-DONE iff goal acceptance all covered by DONE receipts.
4. Otherwise halt-legal packet (H/M queues or empty-ready + dryness proof).
```

Branches die after merge (GIT_ARCHITECTURE). Blocked tasks wait; nothing polls.

**Queue-state rule** (found by live fire): the queue file lives in the repo
being branched, so COMMIT queue state before every branch switch (`git add
tasks.jsonl && git commit -m "queue: <tid> <transition>"`). A dirty queue
blocks checkout — that friction is the control plane refusing split-brain,
not a bug. History: `tasks/<tid>` branches interleave `queue:` state commits
(see live-fire log in a-goals report).

## 3. Improvement over time (base rates, not MCTS)

Why not Monte Carlo: no adversary, no hidden state worth sampling —
verification is cheap and exact, so search budget belongs on attempts, not
tree search. The learning that actually compounds:

- `loop.py history [--like kw]` — per-task-class base rates from the queue +
  A-log timestamps: n, DONE/REJECTED, median hours. The planner orders the
  ready-set by (unlock value × base pass-rate) instead of vibes.
- `learn.py` failure clusters → rubric rows (already built).
- `ham_policy.json` standing promotions (already built).
- All three read the same append-only logs. Nothing to tune, nothing to train.

## 4. Anti-cheat (why the LLM can't grade its own homework)

1. Acceptance + evidence paths frozen at JUSTIFIED (before work).
2. Evidence = re-runnable commands + files, re-run by the validator pass.
3. `set-status DONE` + `stoplight` enforce receipt + report + covers in CODE.
4. Receipts content-hash inputs; history reads logs, not claims.
The model does generation and judgment-calls; the tools do accept/reject.
Same split as ip-graph's MASTER doctrine (Hermes proposes, gates dispose).

## 5. Commands

```bash
python3 loop.py ready                         # actionable now (deps satisfied)
python3 loop.py branch a-amend11              # tasks/a-amend11 branch + record
python3 loop.py history                       # base rates over all tasks
python3 loop.py history --like amend          # base rates for similar tasks
python3 loop.py log a-x --covers 0 --action .. # A-log line
python3 loop.py stoplight a-x                 # GO/NOGO + missing
```
