# seed4 — multi-agent lanes kernel

The parallel-agents seed: ownership lanes plus git worktrees so N agents build
one codebase without stepping on each other. For ideas big enough to split.

## 60-second start

```bash
cp .env.example .env
python3 -m pytest tests/ -q
python3 scripts/lane_check.py   # expect LANES OK
```

## What this is / is not

- IS: collision-proofing for parallel builders (ownership + isolation + seams).
- IS NOT: a task scheduler or a merge bot. Agents still need a plan (seed1) and
  a contract (seed2); lanes only keep them apart.

## Layout

`LANES.md` ownership · `scripts/lane_check.py` + `new-lane.sh` · `docs/` · `tests/`.
