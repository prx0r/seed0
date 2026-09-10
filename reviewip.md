# REVIEW ip-graph (openpatalaproject export, reviewed 2026-09-10)

Source: `/tmp/opencode/ip-graph` (8.4M export, NO `.git` — can't pull or
version-check; treat as snapshot). Disk: 5.7G free (93%) — clone cost
negligible, but do NOT install anything (their venv/pg/R2 live outside).
What it is: Sanskrit translation graph (ingest → verse JSONL → translation
lookup → prove downloadable → serve FastAPI → verify), driven end-to-end by
a Hermes agent with kanban + cron + crypto-proofed runs.

## 1. Functions map (file → what it does)

| File | Function |
|---|---|
| `/tmp/opencode/ip-graph-gh/skills/openpatala/SKILL.md` | THE skill: command map (9 steps), trace/verify/audit tools, kanban rules, honest rules, RAM discipline. Agent loads this, not docs. |
| `/tmp/opencode/ip-graph-gh/AGENT-ORCHESTRATION.md` | closed agent loop: claim kanban → load skill → run step → read ledger → crypto-commit → comment/complete → watchdog cron. |
| `/tmp/opencode/ip-graph-gh/docs/agentic.md` | driving pattern: Hermes GENERATES, Python REDUCES+VERIFIES; eligibility deterministic; task-DONE ≠ object-ACCEPTED. |
| `/tmp/opencode/ip-graph-gh/HERMES-API.md` | machine interface: every orchestrator call, args, returns; run_recorder signature `sha256(gold‖code‖config)`. |
| `/tmp/opencode/ip-graph-gh/agent/run.py` | single entry for ALL steps (compile/verify/judge/ingest/proof/report/watchdog); logs + commits every run. |
| `/tmp/opencode/ip-graph-gh/agent/run_recorder.py` | content-addressed recorder + nanopublication `{assertion, evidence, provenance}`. |
| `/tmp/opencode/ip-graph-gh/agent/watchdog.py` | bounded autonomous cycle (compile→verify→report), box-safe one work. |
| `/tmp/opencode/ip-graph-gh/agent/audit.py` + `trace.py` + `verify.py` | golden-baseline freeze/recompute; ledger counts; 4-pillar gate. |
| `/tmp/opencode/ip-graph-gh/pipeline/pipeline_verify.py` | A/B/C checks: deterministic-always (A1–A4 red-team findings), LLM-judge-sampled (B1–B3), reconciliation (C1–C2 stale detector). |
| `/tmp/opencode/ip-graph-gh/tools/experiment_lab.py` | hypothesis-per-layer lab on FIXED gold sets; `EXP-<layer>-<config>-<hash>-<ts>` naming; `--report` compares registry. |
| `/tmp/opencode/ip-graph-gh/research/EXPERIMENT-MUKTABODHA-5-WORKS.md` | end-to-end proof on 5 real works (2437 verses, 998 SOURCE objects, API-verified). |
| `/tmp/opencode/ip-graph-gh/contracts/CANONICAL-DAG.yaml` | ONE dependency manifest (SOURCE→T1→L0→ARGMAP→L2→…); scheduler/rebuild/tests all derive — no independent DAGs. |
| `/tmp/opencode/ip-graph-gh/MANIFEST.json` + `check.py` | machine pointer (file→id/owner/validator) + drift gate (refs resolve, no dup roles). |
| `/tmp/opencode/ip-graph-gh/docs/NAVIGATION.md` | master index with read-order + per-doc "read when". |
| `/tmp/opencode/ip-graph-gh/docs/AUTONOMOUS-INGESTION-VISION.md` | desired-endpoint doc: one-line vision + closed loop + hard-case deconstruction (DLI chaos → adapter architecture). |
| `/tmp/opencode/ip-graph-gh/docs/MASTER.md` | layers-of-agentness (CLI 0-smart → skill → kanban → cron → model-judgment); division of intelligence. |
| `/tmp/opencode/ip-graph-gh/docs/recipes.md` | R1–R7 copy-paste, each verifiable (our RECIPES twin). |
| `/tmp/opencode/ip-graph-gh/schemas/` | JSON schemas (agent-run, discovery, fetch, source-register, verse-object, work-meta). |

## 2. The visions-skill question (honest answer)

No file named visions/skill exists anywhere found (15 SKILL.mds swept).
The remembered FUNCTION — map desired endpoint → break down the path — is
covered jointly by three artifacts: `AUTONOMOUS-INGESTION-VISION.md`
(endpoint + closed loop), `CANONICAL-DAG.yaml` (layer path with eligibility
rules), `MASTER.md` §1 (who-decides-what per layer). If the memory is of a
single skill that did endpoint-decomposition, the only unchecked candidate
is `/root/z2m/tools/ecommerce-dtc-skills/SKILL.md` (mentions vision, likely
brand-sense — verify before chasing; NOT fetched this review).

## 3. Steal list (mapped to our estate, tiered)

**Steal now (A, ready backlog):**
- S1 MANIFEST+check pattern → extend our index-links-live beyond docs/README
  (all docs + impl refs resolve; drift gate). File: `check.py` + `MANIFEST.json`.
- S2 EXP-naming + fixed-gold discipline → our bout runs
  (`EXP-<layer>-<config>-<hash>-<ts>`, registries append-only — we already do
  the second half).
- S3 A/B/C check taxonomy → our validators: deterministic gates run ALWAYS,
  judge-gates SAMPLED, reconciliation gates detect stale indexes (we lack C-class).
- S4 nanopublication shape `{assertion, evidence, provenance}` → our receipts'
  content schema (additive fields).
- S5 RAM/box-budget preflight block → our BOOT.md (their box: 8GB/4-core rules;
  ours: 75G/93% disk rules — same doctrine, our numbers).
- S6 "claim without a committed run is theater" + task-DONE ≠ object-ACCEPTED
  → our AGENTS laws (one-line additions, same spirit as no-log-no-claim).

**Steal later (needs their runtime):** kanban-claim flow (needs hermes kanban),
watchdog cron (needs H-driver choice first), R2 content-addressing, Postgres
entity-truth, lxml venv pathing.

**Don't steal:** project-specific adapters (GRETIL/Muktabodha/OCR), FastAPI
surface, box paths (`/root/openpatalaproject` — portability caveat: several
docs hardcode them).

## 4. Gaps / cautions
- Clone is version-pinned (`2ac554b`); re-pull before porting anything
  load-bearing (snapshot drift is now detectable via `git pull`).
- Heavy assumptions unverified here: hermes CLI, Postgres, R2 creds, the
  atlas venv. Nothing executed this review (read-only).
- Their doctrine twin confirms ours independently (deterministic gates over
  model judgment, receipts over claims, isolation over trust) — convergent
  evolution, good sign for both.

## 5. Deep dive (fresh clone, full read 2026-09-10)

**Kanban goal machinery** (`/tmp/opencode/ip-graph-gh/docs/MASTER.md` §1.3) —
the strongest find. `kanban create --goal` (persistent goals),
`request-review` / `request-changes` / `reopen-review` (explicit review gate,
reviewer can send back), `specify` (triage → spec+gate before workable),
`decompose` (children with dependencies; parent can't complete first),
`reclaim` (abandoned claims return to ready, never silently done). Governing
sentence: *"the gate is external to the agent (Python), so the agent cannot
mark a task done by declaring it so."* Maps 1:1 onto our loop (JUSTIFIED≈
specify, blocked_by≈decompose, PAUSED≈reclaim, stoplight≈gate) — except they
have reviewer-reject as a FIRST-CLASS transition and we only have REJECTED as
a status. Steal: reviewer send-back path with reasons (S7).

**Performance doctrine** (MASTER §5, 10 rules) + storage split (JSONL verses /
Postgres entities / immutable-bytes projections / R2 source): *"never let one
store pretend to be another."* Our registries already split this way
(queue/tasks/decisions/receipts); adopt their one-line rule verbatim (S8).

**Expansion rule** (MASTER §7.5, non-negotiable): every new capability must be
(1) logged+committed step, (2) deterministic-gate verifiable, (3) MANIFEST-
registered, (4) resource-safe — else it isn't real. Steal as our BACKLOG
ADMISSION gate: no B-item schedules without meeting all four (S9).

**Discovery engine** (VISION §3): curated-deterministic first, agentic second;
discovery registry (never re-scrape); score candidate sources by REAL numbers
(works yielded, not feelings). Their `hermes kanban propose-source` loop =
our H-driver targeting problem, solved. Steal the score-by-yield rule (S10).

**Stages×adoptions table** (VISION §7): every stage names the cloned repo/paper
it adopts FROM (Think-on-Graph, EvoScientist, vidyut, Mitrasamgraha...).
Steal the FORMAT: our steal list should carry adopts-from attribution per
item, not just names (S11 — applied retroactively to §3 above by file links).

**Watchdog --no-agent mode** (ORCHESTRATION §5): the script IS the job, stdout
delivered verbatim — deterministic pulses with ZERO agent spend. Direct input
to H-driver design: D1 pulses should default to gateless deterministic checks,
escalating to agent runs only on findings (S12).

**Verse lifecycle states** (MASTER §3.1: EXTRACTED→LABELED→TRANSLATED→
PROOF-PASSED→COMMITTED): state machines beat status flags. Our task statuses
are flat; consider lifecycle-typed records at the next schema bump (noted,
not scheduled).

**Ecommerce router-tree** (`/root/z2m/tools/ecommerce-dtc-skills/SKILL.md`):
a skill DAG (business question → decomposition → sub-skills, IF-THEN routing).
Closest-in-spirit to the remembered visions skill, wrong domain (marketing
analytics). Verdict stands: no generic endpoint-decomposition skill found;
function covered by VISION+DAG+MASTER per §2.
