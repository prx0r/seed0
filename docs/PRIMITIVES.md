# PRIMITIVES — core moves every agent must make (bout1-proven marked ★)

1. ★ **Web-search + arXiv validate one technical choice, cite it.** All three
   bout1 agents did this unprompted once instructed (Theil-Sen robustness).
   Law candidate: no mechanism ships without one external citation in BUILDLOG.
2. ★ **Clone/hijack infra, never rebuild frameworks.** seed1 hijacked ralph.py
   verbatim; seed5 cloned guard patterns. Law candidate: new-dependency review.
3. **Suite green from any CWD.** Bout1's sharpest finding (seed5 passes home,
   fails away). Proposed criteria0 rule; seed0 checker candidate check.
4. **Honest self-review with a bet.** "Would you bet on this making money?"
   All three answered no/half — more signal than their code. Require the bet
   paragraph in every bout report.
5. **Fail-closed I/O.** seed5's RefuseError-on-missing-input beats silent NaN.
   Proposed pattern for all data tools.
6. **Log decisions + timings as you go** (BUILDLOG.md), not reconstructed after.
7. **Ablation before credit** (eval_arch.py): remove the clever part, re-run.
8. **Budget + telemetry on every scored run** (time/tokens/cost/model in receipt).
9. **Fresh-agent isolation** for judging (seed + brief + rubric only).
10. **Review writes back**: every bout ends in idea1.reviews.md-style log +
    learn.py proposals, or the tournament taught nothing.

---

## Part II — component catalog (canonical reference, 2026-09-10)

Every agent-side thing, one line of function. Format: name — file —
function — in/out — tier — proven-by (test or receipt).

**Harness core**
- checker/scaffolder — `seed0.py` — 5-check compliance gate (+foreign-CWD
  6th) + template scaffolder that git-inits — A — `tests/test_seed0.py`.
- checker — `seed0.py check` — scores a repo 5 checks (+6th foreign-CWD gate
  with `--cwd-independent`) — in: path; out: report + exit code — A —
  `tests/test_seed0.py` (40+ cases incl. self-scan).
- scaffolder — `seed0.py new` — canonical layout from templates/ — in: name +
  idea; out: compliant dir — A — `test_new_scaffold_is_compliant`.
- ranker — `tournament.py` — mechanical leaderboard (prereg `--weights`,
  sealed in receipt) — in: seed dirs; out: ranked rows + jsonl + receipt — A.
- loop-runner — `funnel.py` — isolated attempts → score → blind review →
  sealed reveal → amend — in: idea+rubric+seeds; out: scores/review/receipt — A.
- live-eval — `pyeval.py` — rule+judge evals on cheap models, metered,
  SPEND_LOG hook — in: dataset; out: score + telemetry + receipt — M (spend).
- falsifier — `eval_arch.py` — intact-vs-ablated verdict
  (load-bearing/inert/broken) — in: seed + ablate list; out: verdict + receipt — A.
- learner — `learn.py` — shared-failure clusters → criteria proposals
  (fires at ≥2 seeds, never auto-applies) — in: run dir; out: proposals — A.
- receipts — `runs.py` — content-hashed ids (volatile excluded), verify() —
  in: content; out: id + file — A — every receipt self-verifies.
- feed — `tasks.py` — human/agent tasks with blocked_by, predict/deliver/
  reconcile — in: ops; out: JSONL state — A.
- meter — `telemetry.py` — usage blocks marked `reported` (never estimated),
  price table, content-digest versions — in: payloads; out: block — A.
- caps — `budgets.py` — spend ceilings advertised to agents, GrantDenied on
  breach — in: limits; out: enforce/advertise — A.
- tracer — `trace.py` — run tracing helpers — A.
- rulers — `metrics.py` — footrule/rank_distance/storm_counts, tested before
  measuring — in: orders; out: integers — A — `tests/test_metrics.py`.
- spans — `spans.py` — OTel-shaped traces (monotonic timing, gen_ai attrs,
  JSONL sink, rollup $/run) without the SDK — A — `tests/test_spans.py`.
- check-in policy — `policy.py` — heuristic cold start + online SGD over
  approval/denial traces, three-tier cascade — A — `tests/test_policy.py`.
- git notes — `gitnotes.py` — scores as notes, outcomes as tags — A —
  `tests/test_gitnotes.py`.
- MCP surface — `mcp_server.py` — read-only stdio tools for any agent — A —
  `tests/test_mcp.py`.
- measured runs — `agentrun.py` — external timing + usage capture + budgets,
  three-valued token honesty — A — `tests/test_agentrun.py`.
- pre-commit gate — `scripts/install-hooks.py` — fast gates before commit
  (+`--with-push`) — A — installer roundtrip test.

**Delegation (H/A/M as code)**
- tiers — `ham.py` — prohibited screen, digest-bound approvals
  (VALID→VOID), count ratchet, M-cost logging — in: action/target; out:
  CLEAR/PROHIBITED/VALID/VOID/ask/allow — A (H/M approvals queued) —
  `tests/test_ham.py` (incl. self-clean).
- decision log — `decisions.jsonl` — every tier decision, content-hashed ids — A.
- standing policy — `ham_policy.json` — 3-approvals-0-denials → allow — A.

**Self-tasking loop**
- queue — `loop.py` + `loop/tasks.jsonl` — add/list/set-status/set with schema
  teeth (DONE needs receipt, REPORTED needs file) — A — `tests/test_loop.py`.
- a-logs — `loop/a-logs/<id>.jsonl` — per-task action lines tagging covered
  acceptance indices — A.
- stoplight — `loop.py stoplight` — GO iff all acceptance covered + report
  exists + receipt set, else NOGO + missing — A.
- packet — `loop/packet.json` — done/blocked_on/proposed_next + dryness proof — A.
- reports — `loop/reports/<id>.md` — claim/evidence/self-review/needs/cost — A.

**Streams (registries)**
- registry gate — `registries.py` — one read API + schema gate over
  A/H/M (`loop/tasks.jsonl`, `loop/registry_h.jsonl`,
  `loop/registry_m.jsonl`); missing file = empty stream; no delete API —
  in: hub polls; out: records or schema errors — A.
- inbox — `hinbox.py` — idempotent filing, resolve-once, expiry, transitive
  unlock priority; poll-never-block — in: requests; out: ranked opens — A.
- inbox UI+server — `hqueue.html` + `hserver.py` — localhost cards +
  approve/deny, stdlib backend — in: browser clicks; out: resolutions — H.
- grants — `grants.py` — integer-cent grants (ceiling-not-balance), Treasury
  buckets, BATS-lite tiers, receipt gate, metered_call, log_spend — in: grant
  ops; out: GrantDenied or receipted spend — A (live spend = M).
- plane — `hplane.py` + `plane/repos.txt` — cross-repo funnel, T0 rank
  (value_usd, priority), dark-repo reporting, review receipts — A.
- instrument — `keys.json` + `chain.py` + `press.py` + `instrument.py` —
  10-key press chains ("2943") parsed and dispatched to real machinery,
  every press logged (context -> decision -> outcome) to
  `loop/presses.jsonl`; 0 toggles `loop/HALT.json`; 8 writes
  `loop/goal.json`; 9 appends `loop/corrections.jsonl` — in: chains;
  out: result packet + close line — A (4/5/6/7 = H).
- self-audit — `acheck.py` — A-task nativeness gate (schema, DONE→receipt
  resolution mirroring loop.py, EXECUTING→fresh a-log else STALE, dangling
  refs); exit 0 = native — in: any queue; out: findings — A.

**Validators & seeds**
- idea gate — `idea0/validate_idea.py` — sections + falsifiable `- [ ]` rows +
  mechanism girth — A. criteria gate — `criteria0/` — binary rows, owners,
  no weasel words — A. bout pattern — `<run>/validate.py` exit 0/1 + JSON.
- seed1 ralph-minimal (1.1: workdir-anchored + A-logged) · seed2 spec-first ·
  seed3 evidence-maximalist · seed4 multi-agent lanes · seed5 red-team-first.

**State files (read at boot, not primitives)**
`BOOT.md` + `BOOT_PULSE.txt` (orders) · `AGENTS.md` (laws) · `META_LOOP.md`
(protocol) · `HAM_DELEGATION.md`/`REGISTRIES.md`/`CONTROL_PLANE.md`/
`TOURNAMENTS.md`/`DRIVER_GAP.md` (designs) · `docs/THREADS.md` (board) ·
`PROMPT_LIBRARY.md` (human side).
