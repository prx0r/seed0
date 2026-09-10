# seed5 — red-team-first kernel

The adversarial seed: threat model first, attack packs alongside features, grading
against both fallback and production paths. For anything facing untrusted input —
which, on the internet, is everything.

## 60-second start

```bash
cp .env.example .env
python3 -m pytest tests/ -q
python3 run_packs.py --self-check   # runs example probes against the example guard
```

## What this is / is not

- IS: a threat model plus executable probes plus grading, growing with the code.
- IS NOT: a pentest, a scanner, or a guarantee. It catches regressions and gaping
  holes; clever adversaries need humans (see THREATMODEL.md non-goals).

## Layout

`THREATMODEL.md` · `packs/` · `run_packs.py` (grader + self-check demo) · `docs/` · `tests/`.
