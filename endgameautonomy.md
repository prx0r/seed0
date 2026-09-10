# ENDGAME AUTONOMY — the crazy final version (SPEC, NOT BUILT)

Status: vision. Everything here is downstream of working code (`ham.py` is
v1: hand-labeled tiers, digest-bound approvals, count-based ratchet). Build
v1 first; each section below names the v1 mechanism it graduates.

## 1. Learned delegation policy (graduates `standing()`)

PARTIALLY BUILT 2026-09-10: `policy.py` (heuristic cold start + online SGD,
three-tier cascade, `tests/test_policy.py`). Full 13-feature version + nightly
export still open. Original spec below (kept as direction):

Hedwig-pattern online classifier, per-repo persisted weights. Features per
proposed action: diff size, blast radius (files × dirs), reversibility class,
security sensitivity (secret-adjacent paths), prior approvals/denials for the
action class, verification history, model self-confidence. Three outcomes:
proceed silently / proceed + surface one-liner / live check-in. Policy scores
never shown to the acting model (no gaming the gate). Nightly: export weights
+ decision log to `ham_policy.json` v2 format; human audits promotions.

## 2. Continuous delegation degree (graduates hard tiers)

SBD-pattern scalar α ∈ [0,1] per subtask: fraction of decision authority
transferred. High α = subagent acts; low α = principal or human holds control.
Meta-weights learn the safety↔efficiency tradeoff per context (medical vs
dev-tooling presets differ by orders). α below threshold auto-routes to human
with the reason attached. Tiers A/H/M remain as the human-legible projection
of α (α>0.9 → A, 0.4–0.9 → H-check-in, spend → M regardless of α).

## 3. Metered everything (graduates M-tier logging)

PARTIALLY BUILT 2026-09-10: `Budget.check()` pre-call refusal wired into
pyeval (zero-budget runs make zero calls); per-case time/tokens/cost rows;
`metered_run` (pydantic-optional). Still open: invoice reconciliation,
subagent-cognition metering, funnel-subprocess observability. Original:

Every inference call wrapped: model, input/output tokens (provider-reported +
invoice-reconciled, never estimated — see `TELEMETRY_HONESTY.md`), wall time,
cost. Per-seed, per-bout, per-idea budgets with hard caps (`budgets.py`
advertises; the wrapper enforces — advertise ≠ enforce is today's theatre).
Bout reports answer "who won, at what cost, on which frozen idea version."

## 4. Typed delegation contracts (multi-agent)

LDP-pattern: delegations carry typed failure semantics (timeout, refusal,
budget-exhausted, unverified-output) with explicit failure policies per type.
Subagents attest; principals verify — quality-based routing on self-reports
fails catastrophically, so evidence (receipts, green suites) rides with every
return. No evidence → treated as failure, not as "probably fine."

## 5. Candidate-bound everything (graduates `approval_valid()`)

Approvals, reviews, and release sign-offs bind to content digests of the exact
artifact inspected. Any byte change voids downstream approvals automatically
(verified by CI, not by discipline). Tournaments re-run, don't carry over.

## 6. Capability ≠ permission certificates (graduates tier labels)

Per-agent, per-repo autonomy certificate: assessed capability level (what it
can do, from assisted-evaluation logs) vs allowed level (what it may do, set
by risk × reversibility × owner readiness). A high-capability agent deliberately
constrained to low allowed autonomy is the normal case, not a failure mode.
Certificates live in-repo, versioned, auditable.

## 7. Assisted-evaluation harness (graduates gut feel about autonomy)

Standby-human protocol: run the agent with zero involvement; on failure, add
L4-style involvement (approvals only), then L3 (consultation), until the task
passes at threshold T. The minimal involvement level IS the measured autonomy.
Run quarterly per agent surface; track drift (more involvement needed over
time = regression, investigate).

## 8. Prohibited-tier hardware (graduates `PROHIBITED`)

Move the prohibited screen out of the model's reach: CLI-layer enforcement
(independent of model reasoning), TEE-attested receipts for high-stakes runs,
authorization broker (untrusted-model assumption: a fully prompt-injected
agent still cannot exceed delegated authority). Microsecond cost, same as
today's regex screen, minus the trust-me.

## Build order (each is a bout-sized chunk)

Status 2026-09-10: items 1–2 PARTIAL (policy.py, Budget.check); 3–5 OPEN.

1. Metering wrapper + enforced budgets (kills the worst theatre item).
2. Learned policy v1 (logistic, 13 features, per-repo weights).
3. α-routing + typed contracts (needs 2+ agent surfaces to matter).
4. Certificates + assisted-eval harness (governance layer).
5. Hardware tier (only when stakes justify it).

## Explicitly not

Not a daemon, not a control plane, not an orchestrator. Same dormitory
doctrine as seed0: house the work correctly, inspect on exit. The endgame
is boring infrastructure that makes the crazy autonomy legible — not a
foreman, a building inspector with perfect records.
