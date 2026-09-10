# seed0 — project-shape standard + tournament harness

Point an agent at seed0 plus an idea; get back a compliant codebase with evidence.
See THESIS.md (vision) + HUMAN_LOOP.md (reporting contract) + ECOSYSTEM.md (landscape).

## Use
```bash
python3 seed0.py new NAME --idea "..."   # scaffold a standard-shaped project
python3 seed0.py check ./proj           # compliance gate (5 checks, exit 1 if red)
python3 tournament.py ./seedA ./seedB   # rank seeds, write tournament_*.jsonl
python3 -m pytest tests/ -q             # self-tests
```

## Primitives (all future seeds share these)
- `seed0.py` — checker (required files, tests exist, no committed secrets, live index)
  + scaffolder (templates/ with `{{PROJECT}}`/`{{IDEA}}` substitution).
- `tasks.py` — human/agent feeds in one JSONL: predict mock data to unblock,
  deliver real data, reconcile lists exactly what must re-verify, expire re-escalates.
- `tournament.py` — mechanical scoring (compliance + own-suite + evidence) with
  `substrate` field for cross-platform bake-offs.
- `templates/` — AGENTS.md laws, README, NORTHSTAR, docs set, boot test, .env example.
- `seeds/seed1..seed5` — five starting kernels (ralph-minimal, spec-first,
  evidence-maximalist, multi-agent lanes, red-team-first). Tournament fodder:
  `python3 tournament.py seeds/seed*`.
