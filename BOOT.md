# BOOT.md — session-start orders (read first, every session, no exceptions)

You are starting cold. Chat history is gone or untrustworthy. This file plus
the repo IS your memory. Follow exactly, then work.

## 1. Load state (in order, 2 minutes)

1. `AGENTS.md` — binding laws (logs, gates, secrets, mocks).
2. `loop/packet.json` — where the last run stopped + what's blocked.
3. `loop/tasks.jsonl` — `python3 loop.py list --status JUSTIFIED` and
   `--status PAUSED` first; those are your ready set.
4. `decisions.jsonl` tail (last 5 lines) — recent tier decisions.
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

Run `python3 loop.py init`, file the first task (the user's request) with
justification + acceptance + evidence plan, then work it per §2.

## 4. Non-goals for boot

Do not re-verify the whole suite at boot (wastes a turn). Trust the last
`6/6` + receipts; re-verify only what you touch. Do not summarize history
back to the user unless asked — work first, packet on disk, brief close.
