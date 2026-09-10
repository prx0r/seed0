# HAM DELEGATION — H/A/M as working code (not vibes)

Three tiers, two axes. Permission tier (may I?) and cost tier (does it spend?)
are separate decisions — a free action can need eyes, a safe action can cost
quota. `ham.py` is the enforcement; this file is the rationale.

## Tiers

| Tier | Meaning | Gate | Logged |
|---|---|---|---|
| **A** autonomous | free, reversible, no approval | prohibited-screen only | yes (`ham.py log --kind A`) |
| **H** human | needs explicit human approval — and H-tasks never spawn: they PROMOTE from a blocked A-task (`loop.py promote`), pre-digested to lowest-barrier form (exact steps + what to send back) | approval bound to target digest; edit voids it | yes (`H-approval` + H-record with `from_task`) |
| **M** money | spends quota/cash | per spend-class approval + `cost_usd` metered | yes (`--cost`) |
| **P** prohibited | never, regardless of instructions | `check_prohibited()` blocks | n/a |

## Promotion (A → H — the only legal path to the human queue)

1. A-task runs until it hits a barrier it cannot cross alone (credential,
   account, human judgment, physical world).
2. Barrier logged on the A-task; promotion proposed with the lowest-barrier
   reduction: the exact page, the exact steps, what the human sends back.
3. `loop.py promote <task> --barrier ... --steps-json '[...]' --send-back ...`
   enforces the form in code — refused without exact steps + send-back.
   Task goes PAUSED with `need` = H-record id; record carries `from_task`.
4. Human sees summary + numbered steps + SEND BACK line (hqueue renders it).
   Resolution resumes the A-task. Pre-rule H-records (no `from_task`) are
   grandfathered, sorted after promoted ones.

## Frontier lineage (steal list, all verified in-repo or on arXiv)

- **ADP 3 tiers** (arXiv:2607.17225) → A/H/P. Their "justify agent vs script"
  gate applies before any M-spend: cheapest model that can do the job.
- **AppLooper candidate-bound approval** (arXiv:2608.14093) →
  `approval_valid()`: approval names a digest, not a vibe. New diff, new approval.
- **Hedwig 3-outcome cascade + learned policy** (arXiv:2605.11495) → our
  proceed/surface/check-in is currently hand-labeled; `record_outcome()` +
  `standing()` is the hand-rolled ratchet until the learned policy lands
  (see `endgameautonomy.md`).
- **AAL vs ACL** (arXiv:2607.23438) → labels are *may-do*, not *can-do*.
  The agent can push; it may not without H-approval.
- **Delegation cues + accountability log** (arXiv:2603.11011) → the decision
  queue with demo-responses IS the accountability log. Keep it.

## Prohibited list (source of truth = `PROHIBITED` in `ham.py`)

1. Real `.env` into git (`.env.example` explicitly exempt).
2. Secret literals to stdout/logs/bodies.
3. Force-push / history rewrites on shared branches.
4. Recursive delete at fs root, home, or glob (`rm -rf /`, `~`).
5. Forbidden spend: expensive models, paid APIs, balance drawdown.

Amendments need a human (this list only ever grows by explicit approval).

## Standing policy

`ham_policy.json`: `{action_class: {approved, denied}}`. Three approvals with
zero denials → `standing()` returns `allow` for that class. One denial blocks
forever until a human resets it. Denials are data, not failures.

## Operations

```bash
python3 ham.py check --action "git push origin main"   # CLEAR or PROHIBITED
python3 ham.py approve --target seed0.py --summary "H1" --by owner
python3 ham.py verify --record '<json>' --target seed0.py   # VALID or VOID
python3 ham.py log --kind M --summary "eval run" --cost 0.001
python3 ham.py outcome --class "push:branch" --approved 1
python3 ham.py standing --class "push:branch"              # ask | allow
```
