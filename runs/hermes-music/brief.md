# NORTHSTAR hermes-music (frozen 2026-09-10 — full app, Hermes lanes)

Build the neuro-audio focus-mix app inside your attempt directory. End state:
a WORKING application a user can run, not a demo slice. Stdlib only, no
network, no secrets, no paid services.

## Contract
- `mixengine.py`: `generate_arc(duration_min, mood, novelty)` → segments
  `[{t_start, energy 0..1, label}]` (buildup ~20%, cooldown ~15%, peaks
  middle; novelty raises segment count/variance; deterministic per inputs).
- `mixcli.py`: CLI — `python3 mixcli.py --mood focus --minutes 60
  --novelty 0.5 [--out mix.json]` prints the arc as JSON, optionally saves.
- `save_mix`/`load_mix` JSON round-trip (in mixengine or mixcli).
- `tests/test_mix.py`: ≥5 tests (arc shape, novelty effect, determinism,
  round-trip, CLI exit 0 via subprocess).
- `evidence.txt`: pytest tail. `ATTEMPTS.md` (optional): what you tried.
- Run the bout validator (same dir pattern as brief); exit 0.

## Quota discipline (read carefully — the model API is rate-limited)
- If a step needs the model and gets HTTP 429: wait 60s, retry max 3 times,
  then STOP model-dependent work, log H-blocked, and finish everything that
  needs no model (code, tests, docs). Never hammer. Never spend.
- Hard cap: 45 minutes wall time per lane. When time's up, run the validator
  on what exists and stop.
