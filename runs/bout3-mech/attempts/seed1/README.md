# seed1 — ralph-minimal kernel

The trivial autonomous loop: plan → fresh run → one task → verify → mark done.
Lower bound every fancier seed must beat to justify its complexity.

## 60-second start

```bash
cp .env.example .env
python3 -m pytest tests/ -q
python3 ralph.py --once --agent echo   # dry run: picks next task, no-op agent
```

## What this is / is not

- IS: the smallest harness that runs an idea to completion unattended.
- IS NOT: a planner, a company, or a judge. Planning lives in plan.md (human or
  another seed writes it); this seed executes.

## Layout

`ralph.py` loop + plan state · `plan.md` task list · `docs/` index, recipes,
files, threads.
