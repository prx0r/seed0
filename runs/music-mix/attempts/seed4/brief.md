# NORTHSTAR music-mix (frozen 2026-09-10 — the demo drive: idea in, apps out)

Build a focus-mix engine inside your attempt directory: given a mood, a
duration, and a novelty setting, it generates an energy arc (buildup → peaks
→ cooldown) and exports a shareable mix file. Stdlib only, no network, no secrets.

## Contract
- `mixengine.py` with:
  - `generate_arc(duration_min: int, mood: str, novelty: float) -> list[dict]`
    each segment `{"t_start": int (minutes), "energy": float 0..1, "label": str}`.
    Rules: first ~20% rising (buildup), last ~15% falling (cooldown), peaks in
    the middle; higher novelty → more segments / higher energy variance.
    Deterministic for same inputs (seeded internally — same call, same arc).
  - `save_mix(path: str, mix: dict) -> None` + `load_mix(path: str) -> dict`
    (JSON round-trip of `{"mood":..., "novelty":..., "segments":[...]}`).
- `tests/test_mix.py` with ≥3 tests (arc shape: starts low, ends low, peak
  inside; novelty effect: higher novelty → more segments; round-trip).
- Run `python3 -m pytest tests/ -q` in your dir; save tail to `evidence.txt`.
- Run the bout validator (path in lane prompt); exit 0 (max 3 tries).
- Touch nothing outside your attempt directory.
