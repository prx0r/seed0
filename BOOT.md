# BOOT.md — session-start orders (read first, every session, no exceptions)

You are starting cold. Chat history is gone or untrustworthy. This file plus
the repo IS your memory. Do §0 before ANY other action — no building, no
planning, no domain work until boot passes.

## 0. Boot (one command, 30 seconds)

Run `python3 instrument.py boot` and follow its output exactly. It creates
the queue if missing, shows achieved-vs-missing, and tells you the next
action plus what to read. Report its close line, then do what it says.
If it says HALT-legal, propose next tasks with justification — never invent
unqueued work. The runtime drives; you execute judgment inside it.

## 1. Load state (only if boot tells you to dig deeper)

1. `AGENTS.md` — binding laws (logs, gates, secrets, mocks) + the 10-key
   instrument + A-task requirement.
2. `ATASK.md` — the one-page work contract (5 rules, record shape, turn loop).
3. `loop/packet.json` — where the last run stopped + what's blocked.
4. `loop/tasks.jsonl` — ready set = status JUSTIFIED/EXECUTING with all
   `blocked_by` DONE (`python3 instrument.py press 1` drains it).
5. `docs/THREADS.md` — open threads with owners.

## 2. Standing orders (H7 — revoke only with `pause H7`)

- Work the ready queue: execute → report (`loop/reports/<id>.md`, 5 sections)
  → validate (§6: re-run evidence, write receipt) → bank → propose next.
- Tier-route every step via `ham.py check` (prohibited → stop + escalate;
  spend → M-queue with cost + demo; irreversible/external → H-queue with
  exact approval string; else A, execute).
- Cost-note every response (per-step $/manual-action labels; H/M/A sections).
- Never end with a question. Blocked lanes park; ready lanes drain.
- Halt only at H/M with dryness proof (THREADS + learn clusters + TODOs all
  empty-or-blocked), packet written to `loop/packet.json`.
- Any user message — even unrelated — means: finish serving it, then resume
  the queue before closing.

## 3. First-run (no loop/ state yet)

`instrument.py boot` covers it: init, orientation, first action. File the
user's request as the first task (justification + acceptance + evidence
plan), then work it per §2.

## 4. Non-goals for boot

Do not re-verify the whole suite at boot (wastes a turn). Trust the last
green self-check + receipts; re-verify only what you touch. Do not summarize
history back to the user unless asked — work first, packet on disk, brief close.
