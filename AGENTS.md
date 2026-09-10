# AGENTS.md — seed0 (project-shape standard + tournament harness)

Binding rules for any coding agent working in this repository.

## Absolute rules

1. **Every run logs. No log, no claim.** Test suites, pyeval runs, funnel rounds,
   tournaments, idea/criteria validations — each emits a digest-pinned receipt to
   `runs/` via `runs.py` (`new_receipt` + `save`). Cite run_ids, not adjectives.
2. **Run ids are content-addressed.** Same inputs ⇒ same id, any machine.
   Timestamps/hostnames/latencies live beside the id, never inside it. If
   `verify()` fails, stop — tampering or drift, never "probably fine".
3. **Gates dominate objectives.** Compliance + green suite gate everything;
   scores rank only among the gated. Never trade correctness for speed.
4. **LLM judgment only as binary checks above deterministic verification.**
   Criteria rows are true/false; validators are pure functions; judges grade
   narrow rubrics, never open-ended quality.
5. **Secrets travel via env only.** No keys in files, logs, bodies, or evidence.
   Tests assert their absence.
6. **Mocks prove wiring, never quality.** Simulated numbers labeled; no live
   claims without a live run; exit codes never masked by pipes.
7. **AGPL patterns-only, never pasted.** MIT/Apache vendored with attribution.

## Where things are

`seed0.py` checker/scaffolder · `tasks.py` human/agent feeds · `tournament.py`
scorer · `funnel.py` idea→attempts→review loop · `pyeval.py` live eval runner ·
`runs.py` receipts · `idea0/`+`criteria0/` validators · `templates/` · `seeds/`
five kernels · `ideas/idea1.md` + `criteria/` live instance · `datasets/` ·
`docs/` (GUIDE start here, HERMES_HANDBOOK, CG_IMPORTS, FUNNEL, RECIPES? see index).

## Working style

- Small diffs, tested each step; regression test per fix.
- Docs: `docs/README.md` index stays accurate (checker enforces live links).
- Keyless CI must stay green (`pytest tests/`); live runs (pyeval, funnel with
  agent cmds) are opt-in via env, never default.
