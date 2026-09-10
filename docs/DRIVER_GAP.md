# DRIVER GAP — the exact block (SPEC, verified on this box 2026-09-10)

## The block in one sentence

The agent executes ONLY inside a turn; turns start ONLY on an external pulse
(user message or scheduler); the agent's final text ends the turn; no tool in
its set can schedule, delay, or continue execution past that point. META_LOOP
governs what happens *inside* a turn. Nothing governs *between* turns. That
nothing is the block — this session returned to the user 4 times with zero
way not to.

## Anatomy (three layers, all verified)

1. **Pulse layer.** Verified: `opencode run "msg"` (v1.18.30, on box),
   Hermes `cron create/run/tick`, system cron/atd all exist and work. None is
   currently aimed at seed0. Turns begin here or from the user. No third source.
2. **Turn layer.** The agent's tools (bash/read/edit/write/web) all execute
   synchronously inside the turn. There is no sleep-until, no background-task,
   no self-message primitive. Emitting the final response IS halting — the
   "decision to stop" is an illusion; stopping is the default, continuing is
   what needs machinery.
3. **Memory layer.** Context is ephemeral (compaction, fresh sessions). The
   harness (tiers, loop, queues) survives ONLY as files: `BOOT.md` (orders),
   `loop/` (state), `decisions.jsonl` (log). A session that doesn't read them
   starts feral. Portability = files + a pointer the next session can't miss.

## Why META_LOOP alone can't fix it

§4b continuity rules (no questions, split blocked, dryness proof) maximize
work *per turn* and forbid *asking*. They cannot create the next turn. A loop
with no driver is a car with no starter: perfect engine, parked. The 4 returns
this session were all turn-endings, not question-askings — §4b was never
violated, yet motion still stopped. That distinguishes the two problems.

## Fix space (all real, pick one — H-driver decision)

| # | Driver | Pulse | Cost | Reversibility |
|---|---|---|---|---|
| D1 | system cron → `opencode run` | `*/180 * * * * cd /tmp/opencode/seed0 && opencode run "$(cat BOOT_PULSE.txt)"` | each pulse = 1 autonomous session: weekly ox-alpha quota + CF neurons | `crontab -r` one line; pulses logged to file |
| D2 | Hermes native cron | `hermes cron create --schedule ... -- hermes -z "$(cat BOOT_PULSE.txt)"` | same inference spend, Hermes-native retries/audit | `hermes cron pause/remove` |
| D3 | manual pulses (status quo) | user sends `go` | $0 marginal, owner attention per pulse | n/a |

D1/D2 both need: BOOT_PULSE.txt (frozen resume prompt — written, see BOOT.md),
log file per pulse, spend cap per pulse (M-class: quota math first), and a
KILL file convention (`STOP` file present → pulse exits immediately, no work).
Unattended execution is M+H territory: it spends quota (M) and acts without
live oversight (H) — hence this choice is queued, not taken.

## BOOT sequence (what every pulse/session runs first — see BOOT.md)

1. Read `BOOT.md` → `AGENTS.md` → `loop/packet.json` → `loop/tasks.jsonl`
   (JUSTIFIED/PAUSED first) → `decisions.jsonl` tail → `docs/THREADS.md`.
2. Resume: highest-priority ready A-task executes; report/validate/bank;
   propose next; update packet on disk.
3. Stop only at H/M with dryness proof. Never emit questions.

## Precise statement (for the record)

Continuity = harness (META_LOOP, done) × state on disk (loop/, done) ×
portable orders (BOOT.md, this turn) × external driver (QUEUED as H-driver).
Three of four are now true. The returns stop when the fourth lands.
