# HANDOVER — seed0, 2026-09-10 (for a fresh agent: read BOOT.md first, then this)

## Where it stands (all verified this session)

- Suite 108 green (both CWDs), self-check 6/6, queue 48 records / 0 problems,
  receipts verify, decisions logged. Read `docs/SESSION_REVIEW.md` for the
  full story, `docs/THREADS.md` for the board (T0: make me money).
- Standing rules: H7 autonomy active (no questions, halt only at H/M with
  dryness proof); tiers H/A/M via ham.py; commit queue state before branch
  switches; no receipt, no DONE.

## Queues awaiting the human (packet.json has demos + approval strings)

- H1b push (done — this handover rides it), H2 revoke read token, H6 rename,
  H-driver D1/D2/D3, H-x402 (rail 308-loop), H-sparky (pilot call),
  H-credrotate (mw vault password in public history).
- M4 live metered re-run ($0.01 cap, command ready; quota 429-blocked).

## What to do next (ranked)

1. **M-watch**: re-fire the capped pyeval when quota clears; first nonzero
   telemetry closes the metering loop.
2. **Backlog (ready A-work):** B1 funnel Meter/SPEND_LOG, B3 unlock weights,
   S19–S23 (WIP checkpoints, branch protection, scoped recall, attempt
   schema, pre-commit hooks), S-ports (kanban claim flow, Hydra posteriors).
3. **Bout2** demand-side slice with de-primed briefs (fix EICR convergence).
4. **H-driver**: on approval, wire cron or hermes-cron pulses with BOOT_PULSE.
5. Keep the laws: freeze before lanes, re-run validators, blind before
   reveal, receipts verify, packet on disk, THREADS current.

## Watch-outs (earned the hard way)

- `$0` in double-quoted bash becomes `/bin/bash` — single-quote money strings.
- Docstring glued to `def` line = simple-suite IndentationError.
- `validation_ref` must resolve to a real receipt file (enforced at DONE).
- Queue file must be committed before branch switches.
- Never push secrets: scanner + push protection both guard; `.env` stays out.
