# GITNATIVE — git-native agent patterns, mined 2026-09-10 (with steals)

Git is the tree: every agent start git-inits, every task branches, every
result merges as data, every memory version-controls. We arrived here
independently; the frontier validates it and sharpens the edges.

## 0. arXiv frontier (Sept 2026 sweep — the insane opportunities)

- **GCC** (2508.00031, 80.2% SWE-Bench Verified): COMMIT/BRANCH/MERGE/CONTEXT
  over a `.GCC/` filesystem (roadmap main.md, traces log.md, summaries
  commit.md, metadata.yaml). Ablation: BRANCH&MERGE is the biggest lever;
  detailed-logs+CONTEXT retrieval the second. Validates our branches +
  A-logs; we lack CONTEXT (hierarchical retrieval) — steal S25.
- **GitOfThoughts** (2606.14470): reasoning tree AS git (thoughts=commits,
  scores=NOTES, outcomes=tags, `git log` retrieval, cross-agent merge,
  bundles). Falsifiable H-substrate/H-memory with verdicts; honest boundary
  (memory helps only above copyability τ≈0.8; git's case = auditability).
  Steals: notes-for-scores S24, keyed-layout contradiction surfacing S26,
  pre-registrations-as-commits S30.
- **STORM** (2605.20563, +18.7 Commit0-Lite over worktree baselines):
  write-time conflict control (version counters, reject stale writes) +
  intent annotations. Direct challenge: pure isolation defers conflicts to
  expensive post-hoc merge. Steals: intent annotations S28; stale-view
  rejection where lanes share files.
- **Ledger** (2608.00808, +8pp/-29% cost): deterministic execution-state
  layer — inform path (compact state into context) + govern path (evaluate
  command, reuse valid prior results), zero extra LLM calls. Our stoplight
  is the govern path; we lack the inform path + change-counter invalidation
  S27.
- **OpenWeft** (NeuraCerebra, batch scheduler): durable Work Briefs,
  risk-scored phase scheduling, worktree isolation, checkpoint/resume,
  merge-in-priority-order, audit trail, per-call costs.jsonl. Our funnel +
  tournament + hplane as one product. Steal: risk-scored lane scheduling
  S29, merge-in-priority-order.
- **Self-evolving wave** (RHO 59→78% SWE-Pro; Self-Harness; Socratic-SWE;
  HarnessEvolve; One-Recipe): weakness mining → bounded edits → regression
  gates; falsifiable edit contracts; harness-as-compensation-layer. Validates
  learn.py + amend; steal: falsifiable contracts on OUR edits S31,
  episodic→procedural consolidation schedule S32 (LLMA-Mem pattern).
- **Memory wave** (ChronoMem rollback; MATM population trajectories;
  Governed Shared Memory fleet scopes; ERL heuristics>trajectories):
  steal rollback-by-reference S33 + heuristics pool over raw A-logs S34 +
  fleet failure taxonomy (leakage/staleness/contradiction/provenance).

## 1. What the frontier does (product layer)

- **Letta MemFS / Context Repositories** (docs.letta.com, 2026-02): agent
  memory IS a git repo (blocks as files); every edit committed; subagents
  (dreaming, memory-doctor) work in **worktrees** concurrently; skills
  versioned under memory; shared org repos across agents; frontmatter
  validation hooks; per-agent commit identity. Memory that isn't committed
  doesn't exist.
- **ait-vcs** (PyPI, MIT, dependency-free): worktree isolation + attempt
  provenance (prompt+output+commits linked) + apply/recover verbs + local
  memory feeding prior attempts into the next run + query DSL. Metadata in
  `.ait/` beside `.git/`. The closest thing to our funnel/attempt model.
- **git-lanes**: lane-per-agent (branch+worktree), WIP auto-checkpoint on
  crash/timeout, cross-session conflict detection, file locking,
  main-branch protection policy (block/allow/prompt).
- **aide-memory**: scoped memories (glob inheritance), lifecycle hooks
  (SessionStart recall, Stop reflection, PreCompact), SQLite rebuildable
  cache, `post-checkout` reimport. Recall stats stay out of git.
- **Hermes worktrees** (`-w` auto-mode): disposable worktree+branch per
  session, per-worktree checkpoints/rollback.
- **Aider**: auto-commit every change with sensible messages.

## 2. Telemetry + git-bus state of our estate (reviewed same turn)

- Telemetry arch: `Meter` + PRICES + `metered_run` (pydantic-optional) +
  `Budget.check` pre-call refusal + `grants.metered_call`/`log_spend` +
  pyeval SPEND_LOG hook. Honest gaps: funnel subprocess spend unobservable;
  agent-cognition spend unmetered (M4); live 429-blocked this turn ($0 spent).
- Git bus: CONTROL_PLANE primitives verified (tree ferries free, refs need
  refspecs, bundles sneakernet, worktrees parallel). `loop.py branch`
  implements branch-per-task; `map` renders the DAG as a tree.
- `workerun`: searched /root + /tmp/opencode — NOTHING by that name. Closest:
  WorkerKit (mw master), RunWorktree (mwgym), HarnessRun. Say the word if one
  of these was meant (one-word correction, no ceremony).

## 3. Steals (adopted + queued)

ADOPTED this turn:
- S17 `seed0.py new` git-inits with local identity + scaffold commit (Letta
  MemFS pattern: versioned tree from byte zero).
- S18 `loop.py map` (goal tree visible like git log --graph for tasks).
QUEUED (ready A-backlog):
- S19 WIP auto-checkpoint on crash/timeout (git-lanes pattern).
- S20 main-branch protection posture (block by default, explicit allow).
- S21 scoped recall by task area (aide-memory globs; BOOT reads everything).
- S22 attempt record schema with prompt→commits linkage (ait-vcs shape).
- S23 pre-commit structure hooks (Letta frontmatter pattern → our validators).
ADOPTED wave 2 (arXiv sweep, all tested):
- S24 `gitnotes.py` (attach/read/tag) + `tournament.py --notes NS` (verdicts
  as notes on HEAD, best-effort, never fails runs).
- S26 `learn.py --keyed DIR` (one file per failure signature = keyed layout;
  reruns idempotent, disagreements would merge-conflict).
- S27 evidence memo (`command: || inputs:` skips green reruns on unchanged
  inputs; no inputs list = always re-run).
- S28 A-log `intent` field + `--intent` flag (STORM shared-boundary notes).
- S29 `funnel.lane_risk` (file-overlap phases; overlapping lanes serialize).
- S30 `funnel.freeze_run` (pre-reg brief+rubric+validator+weights as commit).
- S31 `funnel.amend(..., falsifier=...)` (One-Recipe falsifiable contracts).
- S32 keyed proposals double as consolidation (stable ids, rerun-safe growth).
- S33 `loop.py rollback` (ChronoMem pattern; refuses dirty workdir).
- S34 `loop.py heuristics` (ERL-lite: self-review phrases + source tasks).
- S25 `loop.py context` L0–L3 (prior turn).
NOT taken: eager auto-commits of everything (Aider style — ours stay
deliberate), SaaS sync, SQLite caches (JSONL suffices at our scale).
