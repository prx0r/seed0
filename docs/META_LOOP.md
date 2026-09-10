# META_LOOP — autonomous work protocol (SPEC v1, adopted 2026-09-10)

How the agent works a project with zero supervision between bottlenecks:
set its own A-tasks, execute them, validate each with evidence that counts as
proof, bank receipts, propose the next tasks with justification, repeat.
H/M needs surface as queues with demos — never executed unapproved.

## 1. Artifacts (all in-repo, git-tracked)

| Artifact | Path | Role |
|---|---|---|
| Task queue | `loop/tasks.jsonl` (one JSON record/line; `tasks.py` Feed is the substrate) | all PROPOSED→DONE state lives here |
| Progress reports | `loop/reports/<id>.md` | one per EXECUTING task, §5 schema |
| Decision log | `decisions.jsonl` (`ham.py log`) | every tier decision + approval, content-hashed |
| Standing policy | `ham_policy.json` | promotions from repeated approvals |
| Validation receipts | `runs/` (`runs.py`) | proof of DONE, `kind: task-validation` |
| Human surface | `docs/THREADS.md`, `docs/METAPROCESS.md` | open/closed threads, process reviews |

## 2. Task record schema (required keys, no extras without version bump)

```json
{
  "id": "a-cwdgate",
  "tier": "A",
  "summary": "make suite CWD-independent",
  "justification": {
    "parent": "METAPROCESS amendment 6 (CWD gate)",
    "why_now": "gate blocks honest green claims",
    "why_tier": "ham check CLEAR; free; reversible"
  },
  "acceptance": ["pytest green in-repo", "pytest green from /tmp",
                 "seed0.py check . --cwd-independent 6/6"],
  "evidence_required": [
    {"kind": "command", "spec": "python3 -m pytest tests/ -q"},
    {"kind": "command", "spec": "python3 seed0.py check . --cwd-independent"}
  ],
  "cost_note": "$0, no manual actions",
  "status": "DONE",
  "report_ref": "loop/reports/a-cwdgate.md",
  "validation_ref": "sha256:<receipt>"
}
```

`status` ∈ `PROPOSED, JUSTIFIED, EXECUTING, PAUSED, REPORTED, REJECTED, DONE`.
`PAUSED` = H/M need discovered mid-task (need id cited, task resumes on approval).
`REJECTED` must carry reasons; re-entry starts at PROPOSED, never direct to DONE.

## 3. Tier routing (decision procedure, in this order, per step)

1. `ham.py check --action "<step>"` → hit = PROHIBITED: stop, log, escalate
   to H with the rule id. No override exists.
2. Spends quota/cash, or inference no wrapper can meter → M: queue with cost
   estimate + demo of the expected response. Never execute.
3. Irreversible, externally visible (push, publish, share), log-schema
   changing, or barriered (needs human-only action) → H: ONLY via promotion
   (`loop.py promote` from the blocked A-task, lowest-barrier form enforced).
   Direct H-filing is grandfathered, sorted last. Queue carries the exact
   approval string (e.g. `go H1`) plus numbered steps + SEND BACK line.
4. Else A: execute, log completion via `ham.py log --kind A`.

## 4. A-task lifecycle

```
PROPOSED → JUSTIFIED → EXECUTING → REPORTED → VALIDATED → DONE
               ↑                        |
               └──── REJECTED (reasons) ┘
EXECUTING → PAUSED (H/M need) → EXECUTING (on approval)
```

Batch rule: drain all ready A-tasks (parallel where independent) before the
review pass. Then run the propose step (§7) and drain AGAIN — iterations
continue inside one run until the ready-set is truly empty. Never invent
filler tasks to look busy.

## 4b. Continuity rules (why the loop never stops to ask)

1. **No questions, ever.** Feedback requests are banned as turn endings. Any
   impulse to ask becomes a queued H-item with cost note + demo, and work
   continues on other lanes. Blocked lanes park; ready lanes drain.
2. **Split blocked tasks.** An H/M-blocked task must be split: the
   autonomous-legal prefix (design, code, tests, docs — everything short of
   the blocked step) becomes a ready A-task immediately. Only the rump stays
   queued. Example: M4 metering → A-design (wrapper code, no live calls) now,
   M-run (live spend) queued.
3. **Dryness proof required to halt.** Halt is legal only with proof of no
   ready work: THREADS open items checked, learn.py clusters checked,
   code TODOs grepped, T-list reviewed — all empty or all H/M-blocked with
   no splittable prefix. The proof is written to `loop/packet.json`
   (bottleneck packet on disk, not just in chat).
4. **Default-action, cheap-reversal.** Ambiguous calls resolve toward action;
   every action is logged with its reversal (usually `git checkout`/`git
   reset`). The owner reverts with one word instead of pre-approving with
   ten. Standing H7 may be paused with `pause H7` — the only question-shaped
   input the loop accepts, and it needs no answer.
5. **Turns are batches, not sessions.** One turn = as many loop iterations as
   fit. A turn ends with completed work + packet on disk. The next turn —
   any user message, even unrelated — resumes the queue first.

## 5. Progress report schema (`loop/reports/<id>.md`, required sections)

1. `claim` — one line, numbers first, adjectives banned unless followed by
   a reproducer.
2. `evidence` — commands run + exit codes + output tails; file paths written;
   digests (`sha256[:12]`) of key outputs.
3. `self-review` — how this could be wrong; what was NOT checked.
4. `needs` — H/M items discovered, each with cost note + demo response.
5. `cost` — incurred ($0 or metered tokens/cash).

## 6. Validation protocol (this is the step that makes evidence proof)

The validator re-runs, never re-reads-only. Same agent on a fresh pass is
acceptable; a second agent is better. MUST do all four:

1. Re-read every evidence file cited.
2. Re-run at least one evidence command verbatim (or verify stored digests).
3. Check every `acceptance` item individually; one fail = REJECTED.
4. Write a `task-validation` receipt via `runs.py` naming task id, per-item
   results, and evidence digests. DONE requires the receipt id in
   `validation_ref`. No receipt, no DONE (AGENTS.md law 1: no log, no claim).

## 7. Next-task justification (scheduling gate)

A new task is scheduled only with: `parent` (finding/validation-gap/learn.py
cluster id), `why_tier` (routing result), `cost_note` + manual actions,
`acceptance` + `evidence_required` plan. Missing any field → stays PROPOSED.

## 8. Bottleneck packet (the ONLY legal halt output)

```json
{
  "done": ["sha256:<validation receipt>", "..."],
  "blocked_on": [{"queue": "H1", "approval_string": "go H1",
                  "demo": "pushed <sha>, tree clean"}],
  "proposed_next": [{"id": "m-metering", "parent": "audit zero-token finding",
                     "tier": "M", "cost": "~$0 free tier"}]
}
```

## 9. Mapping to seed0 machinery (nothing new to build for v1)

- `tasks.py` Feed → queue substrate (predict/deliver/reconcile already exist).
- `runs.py` → validation receipts. `ham.py` → tiering, approvals, standing.
- `learn.py` → shared-failure clusters feed step "propose next" (§7 parents).
- `tournament.py` / `funnel.py` / `pyeval.py` → evidence generators.
- First graduation: `loop.py` driver (machine-readable queue + auto-validation).
  Until then this file is executed by hand, and deviations are process failures
  eligible for `learn.py` clustering like any other shared failure.

## 10. Worked example (this session, abridged)

Task `a-audit`: acceptance [read 6 logs + 4 receipts + bout1; trace
elapsed_s/tokens/model to code; negative grep]. Evidence: field table (§6 of
audit report), empty greps, bout1's 6 keys. Validation: greps re-run,
`verify()=True` on all receipts. → DONE. Spawned M4 (parent: zero-token
finding, cost ~$0) and H6 (parent: elapsed_s mislabel, schema change) with
demos. Halt reason: H1/H2/H6/M4 unapproved → bottleneck packet emitted as the
session summary's queue section.
