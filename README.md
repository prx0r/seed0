# seed0 — project-shape standard + tournament harness

Point an agent at seed0 plus an idea; get back a compliant codebase with evidence.
See THESIS.md (vision) + HUMAN_LOOP.md (reporting contract) + ECOSYSTEM.md (landscape).

## Cold start (fresh clone → working in 4 commands, stdlib only)

```bash
git clone <url> seed0 && cd seed0
python3 -m pytest tests/ -q             # 160 green or stop and report
python3 seed0.py check .                # 5/5 COMPLIANT or stop and report
python3 loop.py init                    # create your queue (runtime state, never committed)
python3 acheck.py                       # 0 findings = your queue is native
python3 instrument.py press 2           # ZOOM: achieved vs missing right now
```
No install step: stdlib only. `pydantic` is optional — telemetry uses it when
importable, identical stdlib checks otherwise (same contract, both paths tested).

## Measured agent runs (Hermes)

```bash
python3 agentrun.py --name lane1 --model mimo-v2.5 --timeout 600 \
  --usage-file lane1/usage.json -- hermes -z "build per brief.md" --usage-file lane1/usage.json
```
Time comes from our stopwatch (monotonic), tokens from the usage file,
cost from the price table. No usage channel = `unknown`, never zero-by-guess.
Every run ends in a receipt or it didn't happen. Budgets refuse before the
call (`Budget.check`) and after crossing (`record`); see `budgets.py`.

## Use
```bash
python3 seed0.py new NAME --idea "..."   # scaffold a standard-shaped project
python3 seed0.py check ./proj           # compliance gate (5 checks, exit 1 if red)
python3 tournament.py ./seedA ./seedB   # rank seeds, write tournament_*.jsonl
python3 -m pytest tests/ -q             # self-tests
OPENCODE_GO_API_KEY=... python3 pyeval.py run datasets/safety_sample.json --model mimo-v2.5
python3 learn.py runs/idea1             # shared failures -> criteria1.1 proposals
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
