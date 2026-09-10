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
8. **Macros replay selection, never authorization.** A press-sequence macro may
   re-fire which action to take; money/irreversible steps re-resolve their
   gate (keyword, digest, grant) at replay time. No inherited approvals.

## Agentic OS (the instrument)

The human directs agents by pressing keys, not typing letters. 10 keys:
1 GO (drain ready A-tasks) · 2 ZOOM (achieved vs missing) · 3 DIG (review
until obvious) · 4 PICK#n (choose option n) · 5 OK (approve; money re-resolves
its gate, never inherits) · 6 NO (deny + replan) · 7 TELL (answer the open
input; key-shaped input refused) · 8 GOAL#Tn (switch goal) · 9 FIX (correction
becomes learn food; bare 9 = auto-context + replan) · 0 STOP (halt/resume;
read-only 2,3 survive halt).
Left hand directs (1,2,3,8,9), right hand responds (4,5,6,7), foot on brake.
Chains compose (`2943` = ZOOM, FIX, PICK#3); only 4 and 8 consume a digit.
Grammar lives in `keys.json`, parser in `chain.py`, dispatch in
`instrument.py` (`python3 instrument.py press <chain>`).
Every press logs (context → decision → outcome) to `loop/presses.jsonl`.
Frequent chains become one-press macros; thrice-identical approvals become
standing policy via the ratchet; predicted presses above per-key thresholds
go autonomous-with-undo. Money paths are never autonomous at any accuracy.
Agents: be A-task native per `ATASK.md`; prove it with `acheck.py` (exit 0).

## Where things are

`seed0.py` checker/scaffolder · `tasks.py` human/agent feeds · `tournament.py`
scorer · `funnel.py` idea→attempts→review loop · `pyeval.py` live eval runner ·
`runs.py` receipts · `idea0/`+`criteria0/` validators · `templates/` · `seeds/`
five kernels · `ideas/idea1.md` + `criteria/` live instance · `datasets/` ·
`docs/` (GUIDE start here, HERMES_HANDBOOK, CG_IMPORTS, FUNNEL, RECIPES? see index).

## Working style

- Cold start? Read `BOOT.md` first — it is the session-start orders (state,
  standing H7 autonomy rules, halt conditions). No chat history required.
- Small diffs, tested each step; regression test per fix.
- Process discipline: capture PIDs at launch (`SRV=$!`), kill by exact PID.
  Never pkill/pkill -f/killall (pattern kills hit wrong processes).
- Docs: `docs/README.md` index stays accurate (checker enforces live links).
- Keyless CI must stay green (`pytest tests/`); live runs (pyeval, funnel with
  agent cmds) are opt-in via env, never default.
