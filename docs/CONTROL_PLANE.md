# CONTROL PLANE — one human funnel across all codebases, git as the bus
# SPEC v1, primitives verified on box 2026-09-10 (bundle/notes/refs/worktree)

## 1. Model

Every active repo keeps `loop/registry_h.jsonl` (hinbox format + optional
`value_usd`: expected revenue impact of resolving, T0 ladder). The plane
AGGREGATES — it is not another database. No registry in a repo = that repo
is dark, and the plane reports darkness as its own top funnel item
(adoption bootstraps itself).

## 2. Git as the bus (each primitive verified this turn in /tmp/gitbus)

| Primitive | Verified behavior | Plane use |
|---|---|---|
| Files on main | ferry free with every clone/bundle | queue state lives HERE (`loop/registry_h.jsonl`) — zero-config transport |
| `git log -- <path>` | per-file history | event stream per repo queue; `log -- runs/` stays the journal (GIT_ARCHITECTURE) |
| Custom refs `refs/queue/h/<repo>` | work, but DROPPED by default clone/fetch | "reviewed-at" watermarks; require explicit refspec `+refs/queue/*:refs/queue/*` (proven) |
| Notes | work, same drop-by-default | commit-bound approvals (approve THIS push sha); same refspec rule |
| `git bundle --all` | full ferry incl. all refs into one file | sneakernet between boxes; restore with explicit refspecs (proven sequence) |
| Worktrees | one repo, lanes per run (mw LabWorkspace precedent) | parallel builder lanes without clone sprawl |
| Attempt branches | die after merge (GIT_ARCHITECTURE law) | lanes never accumulate |

Design rule from the transport test: **state in tree, pointers in refs.**
Anything that must survive a default `clone`/`bundle` lives in files.
Refs/notes are overlay only (watermarks, commit approvals).

## 3. Priority (the funnel's brain — T0 first)

Global rank key per open H-record: `(value_usd or 0, priority_score)` desc.
Revenue dominates (T0: the prompt is always make-me-money); unlock value
breaks ties. No blended fake-math scores. Review pass (scheduled pulse or
manual `hplane.py review`) re-scores, flags STALE (open past timeout with no
resolution → escalate_to), and files a `plane-review` receipt in the plane
repo's runs/. The review itself is evidence, receipted like everything else.

## 4. hplane.py v1 (this turn — scan, rank, report; reads all, writes receipts only)

```
python3 hplane.py funnel [--repos plane/repos.txt]   # ranked JSON to stdout
python3 hplane.py review [--repos ...]               # + STALE flags + receipt
```

- `plane/repos.txt`: one repo path per line (this repo + adoption targets).
- Resolution stays per-repo (hserver) — the plane never split-brains a
  decision. It reads queues, writes only its own review receipts.
- Dark repos (no registry file) reported as `{repo, status: dark}` — first
  funnel item until adopted.

## 5. Lineage (what we stole from our own estate)

- Branches-die-after-merge + `git log -- runs/` journal: seed0 GIT_ARCHITECTURE
  (from mw peer review's branches-as-components warning).
- Content-addressed receipts + verify-by-reexecution: cg GIT-LEDGER.
- One-repo + worktrees-per-run: mwgym LabWorkspace.
- Frozen experiment tasks + real rubrics: HARBOR-PLAN (Harbor itself is the
  evaluation substrate, not the bus — not imported).
- Human Queue cards + stdlib server: mw queue.html/dashboard_server (already
  ported as hqueue/hserver).

## 6. Build order

1. hplane scan+rank+review receipt (THIS TURN).
2. Multi-repo hqueue view (plane renders all queues, resolves per-repo).
3. `refs/queue/h/*` watermarks + fetch refspecs documented per box.
4. pre-push hook: seed0 check + loop check (proposed, not yet).
5. HydraDB experience graph (exists, live) — only if funnel outgrows JSONL.
