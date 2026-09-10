# seed2 — spec-first kernel

The contract-gated seed: an idea becomes a SPEC with acceptance criteria, and only
approved, verifiable criteria become code. For ideas where building the wrong thing
costs more than specifying slowly.

## 60-second start

```bash
cp .env.example .env
python3 -m pytest tests/ -q
python3 scripts/spec_check.py   # expect SPEC OK
```

## What this is / is not

- IS: a machine-checkable definition of done, enforced before and during building.
- IS NOT: a planner or an agent. It cannot tell you WHAT to specify — only whether
  your spec has teeth.

## Layout

`SPEC.md` contract · `scripts/spec_check.py` gate · `docs/` · `tests/`.
