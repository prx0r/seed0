# GUIDE — operating seed0 (start here)

seed0 is two things: a **standard** (what a compliant autonomous-build repo looks
like) and a **harness** (checker, tournament, funnel, evals, receipts). This guide
covers bring-up through running tournaments. Philosophy + landscape live in
THESIS.md, HUMAN_LOOP.md, ECOSYSTEM.md.

## Core loop (every routine lives inside this)

```
freeze (brief+rubric+validator+weights) → lanes/attempts (isolated)
   → operator re-runs validators → score (mechanical) → blind review
   → reveal → tournament → receipts verify → bank (queue+THREADS+packet)
```
Full session routines (R1 bring-up … R6 resume), WHEN matrix, and workflow
combinations: `docs/ROUTINES.md`. Copy-paste ops: `docs/RECIPES.md`.

## Bring-up (fresh machine)

```bash
git clone <seed0> && cd seed0
python3 -m pytest tests/ -q        # keyless, must be green, no excuses
python3 seed0.py check .           # expect 5/5 COMPLIANT
```

No keys, no network, no daemons needed for any of the above. Anything requiring
credentials is opt-in via env and documented at its call site.

## Workflows

**Start a project:** `python3 seed0.py new NAME --idea "..."` → fill NORTHSTAR →
build → `seed0.py check` gates every session.

**Run a tournament:** `python3 tournament.py ./seedA ./seedB` → leaderboard +
timestamped jsonl + content-addressed receipt in `runs/`.

**Run the funnel (idea → attempts → review):**
`python3 funnel.py run --idea ... --rubric rubric.json --seeds seed1,seed2
--agent-cmd ./agent.sh --out runs/idea1` → `review` scaffolds the main-agent
decision record → `amend` stamps VERSION + log. Attempts are isolated (seed +
brief + rubric only); agent failures recorded, never hidden.

**Run live evals:** `OPENCODE_GO_API_KEY=... python3 pyeval.py run
datasets/safety_sample.json --model mimo-v2.5 [--out runs/]` (cheap model
default; contributor tiers train on prompts — never eval with them).

**Human/agent work split:** `tasks.py` Feed — human blocks get predicted mock
data so agents keep moving; `deliver()` + `reconcile()` swaps real data in and
lists exactly what must re-verify. Expiry re-escalates, never auto-approves.

## Reference

- Receipts: `runs.py` (`new_receipt`/`save`/`verify`); verify with
  `python3 -c "from runs import verify_file; print(verify_file('runs/<id>.json'))"`.
- Validators: `idea0/validate_idea.py`, `criteria0/validate_criteria.py`
  (both print elapsed ms — time-to-verify is logged).
- Vendor docs: `docs/vendor/` (Hermes full corpus, Pydantic pages); handbook at
  `docs/HERMES_HANDBOOK.md`; cg doctrine import at `docs/CG_IMPORTS.md`.
- Runbook detail per area: criteria0/CRITERIA_TEMPLATE, `templates/docs/MCP.md`
  (skill-equivalent surface), RECIPES pattern in each seed under `seeds/`.
