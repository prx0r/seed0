# ROUTINES — full session routines: what to run, when, and what proves it

**Rule (cg REPRODUCE doctrine):** receipts are truth. Every routine below ends
in files + receipts you can re-verify; prose claims nothing. Full command
outputs verified 2026-09-10 (suite 106, self-check 6/6).

## The core loop every routine lives in

```
freeze (brief+rubric+validator+weights) → lanes/attempts (isolated)
   → operator re-runs validators → score (mechanical) → blind review
   → reveal → tournament → receipts verify → bank (queue+THREADS+packet)
         ↑                                                      |
         └────────── amendments re-enter as tasks ──────────────┘
```

A routine states its situation, exact commands, expected outputs, and what
each step proves. Copy the block, fill `[slots]`, run top to bottom.

## R1 — bring-up & verify (cold box → trusted repo, ~2 min)

When: fresh clone, new box, start of any session that touches code.
```bash
git clone https://github.com/prx0r/seed0.git && cd seed0
python3 -m pytest tests/ -q                    # expect: 106 passed
python3 seed0.py check . --cwd-independent     # expect: 6/6 COMPLIANT
python3 loop.py check                          # expect: N records, 0 problems
python3 hplane.py funnel 2>/dev/null | head -5 # expect: ranked H-queue
```
Proves: harness intact (tests), repo compliant (checker), queue valid,
human funnel readable. No keys, no network (except clone), no daemons.

## R2 — hypothesis bout (rival implementations → measured verdict, ~10 min)

When: two mechanisms compete and reasoning can't settle it (priority scoring,
filing discipline, any A/B).
```bash
# 1. freeze BEFORE lanes (idea0/criteria0 enforce teeth)
python3 idea0/validate_idea.py ideas/[x].md        # expect: IDEA OK
python3 criteria0/validate_criteria.py criteria/[x].md  # expect: CRITERIA OK
printf '...' > runs/[bout]/brief.md   # + rubric.json + validate.py + weights.json
python3 runs/[bout]/validate.py [empty-dir]; echo $?   # expect 1 (calibration)
# 2. lanes: isolated builders, brief+rubric only, max 3 validator tries each
# 3. operator re-runs EVERY validator (builders never grade homework)
python3 runs/[bout]/validate.py [lane]; echo $?        # expect 0
# 4. score + blind review (verdicts cite lane-visible fields ONLY)
python3 funnel.py review --run runs/[bout] --round 1 --blind
python3 funnel.py reveal --run runs/[bout] --round 1   # AFTER verdicts
python3 tournament.py [lane-dirs] --model [label] --weights runs/[bout]/weights.json
# 5. receipts verify; verdicts come from preregistered thresholds, never rank
python3 -c "from runs import verify_file; ..."
```
Proves: integers, not prose. Worked example: `runs/meta-tourney/` (H1 0v2, H2 5v1).
Full schema table + verdict rules: `docs/TOURNAMENTS.md`.

## R3 — amendment chain (results → justified seed change → re-run, ~15 min)

When: analysis faults a kernel and the fix must carry its parents.
```bash
git checkout -qb tourn/chain1/[name]              # isolate (branches die after merge)
# edit + tests + VERSION bump + AMENDMENTS.jsonl entry citing parent findings
python3 -m pytest seeds/[k]/tests/ -q && python3 seed0.py check seeds/[k]
git add seeds/[k] && git commit -m "[k].1.1: [what] ([parents])"
git checkout -q main && git merge --ff-only tourn/chain1/[name]
git branch -D tourn/chain1/[name]                 # branch dies here, by law
echo '{"tests_green":100,"compliant":10,"evidence":1}' > runs/chain1/weights.json
python3 tournament.py seeds/seed* --model kernel --weights runs/chain1/weights.json
```
Proves: change traceable finding→diff→green→receipt. Worked: seed1→1.1
(CWD-anchoring + A-log, bout1-seed5 parents). A-log per task + `loop.py
stoplight [id]` must read GO before DONE.

## R4 — release (commit + push without breaking the ledger, ~3 min)

When: banked work leaves the box. Requires H1b-class approval (push is external).
```bash
python3 -m pytest tests/ -q && python3 seed0.py check . --cwd-independent  # green first
git status --short && git diff --stat              # inspect: stage ONLY intended files
git add -A && git commit -m "[what] ([tests] green, [checks])"
git push origin main                               # exact-URL transport if needed
git log --oneline -2 && git status --short         # expect: clean tree
```
Proves: clean tree on remote. Standing rules: never commit secrets (checker
enforces), never amend failed commits, never force-push.

## R5 — peer review (adversarial pass over results, ~15 min)

When: after any bout/chain, before claiming anything.
```bash
# 1. evidence table: re-run every validator + metric live (no memory quotes)
# 2. per-metric theater-vs-signal audit (elapsed jitter? evidence luck? label honesty?)
# 3. divergences → fixes (A now) or queues (H/M with demos)
# 4. bank: loop report (claim/evidence/self-review/needs/cost) + receipt + record
python3 -m pytest tests/ -q && python3 seed0.py check . --cwd-independent
```
Proves: the numbers survive a second reading. Worked: peer review caught the
blind leak (scores.jsonl names+counts) → `scores_blind_rN.jsonl` + judge rule.

## R6 — cold resume (any session, no history, ~2 min)

When: fresh context, new box, next pulse. Full orders: `BOOT.md`.
```bash
cat loop/packet.json                    # where it stopped + what's blocked
python3 loop.py list --status JUSTIFIED # ready set
python3 loop.py list --status PAUSED    # blocked set
tail -5 decisions.jsonl                 # recent tier decisions
```
Then work the ready queue; packet on disk before closing; never end with a question.

## WHEN matrix (situation → routine)

| Situation | Run | Why not something else |
|---|---|---|
| New box / session start | R6 → R1 | trust must be re-earned, not assumed |
| Two mechanisms compete | R2 | reasoning doesn't falsify; integers do |
| Analysis faults a kernel | R3 | fixes without parents are vibes |
| Work leaves the box | R4 | ledger must stay linear + clean |
| Results claimed anywhere | R5 | first reading is always charitable |
| Scheduled pulse fires | R6 → ready queue → R5-lite | pulses are cheap, claims are expensive |
| Human asks "status" | R6-reads only, keep working | reporting never pauses lanes |
| New repo joins estate | R1 + registry port (`hinbox` format) | plane reports darkness until adopted |

## Combinations (routines compose into workflows)

- **Full chain:** R1 → R2 (measure) → R3 (amend from findings) → R2 re-run →
  R5 (adversarial) → R4 (release). This is chain1, end to end.
- **Driver pulse:** R6 → drain ready A-tasks (loop) → R5-lite (re-run gates) →
  packet on disk → halt only at H/M with dryness proof.
- **Estate sweep:** R1 per repo → `hplane.py review` (cross-repo funnel) →
  H-items ordered by `(value_usd, priority)` → human works top-down.
- **Incident (red gate):** failing check → R5-mini (which gate, since when via
  `git log`) → R3 (fix as amendment) → R1 → R4.
