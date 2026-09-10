# REGISTRIES — 3 global streams (SPEC v1, imports verified 2026-09-10)

Three append-only registries. Agent owns A, human owns H at human pace, money
owns M under lock. Streams run parallel; the graph joins them.

## 1. Shape (all three)

`loop/registry_{a,h,m}.jsonl` — one JSON record per line, append-only, never
deleted, never edited (corrections are new records referencing the old id).
Removal rule per stream: A dies only by proof (§2); H dies only by human
action in the inbox (§3); M dies only by expiry/spend/revocation (§4).
`loop.py check` enforces record SCHEMA; DONE-gating (report+receipt) lives
in `loop.py set-status` + `stoplight`, not in `check` (separation: shape vs
proof).

## 2. A-registry (agent stream — exists today as loop/tasks.jsonl)

No change except the removal law made explicit: the ONLY way to remove an
A-task is to satisfy the validation criteria it set at creation (acceptance
+ evidence → validation receipt → DONE). No delete command exists and none
will be added. REJECTED returns to PROPOSED; history is forever (INVALIDATED
pattern from evidence lifecycle).

## 3. H-registry + inbox (human stream — the build)

Record: `{id, kind: request|resolution|expiry, h_kind: approval|input|review,
summary, context, options,
unlocks: [a-task ids], priority_score, idempotency_key, timeout_s,
escalate_to, status: open|approved|denied|answered|expired, resolution}`.
(envelope `kind` + taxonomy `h_kind` per hinbox.py; corrected 2026-09-10 —
spec previously conflated the two.)
Schema mirrors HumanLayer's approval record (idempotency + timeout +
escalation) so a future HumanLayer webhook can replace the file backend
without changing the agent side.

Inbox (import, don't build): mw's `queue.html` (Human Queue cards, priority
badges, action buttons) + `dashboard_server.py` (stdlib `http.server`, GET +
POST JSON). Retarget POSTs from `/api/vault/set` to `/api/h/resolve`.
Agent side: `hinbox.py` — `pending()` lists open records, `resolve()` applies
a human resolution, `poll()` is the turn-safe primitive (read files, never
block — blocking waits don't survive turn ends; polling does).

Unlock graph + human order: every H-record carries `unlocks:` (A-task ids it
unblocks). Priority = transitively-unblocked A-tasks weighted by their
acceptance value, topologically sorted. The human's queue order IS the
agent's computed priority — no separate triage meeting. `tasks.py` Feed
already has `blocked_by` + predict/deliver/reconcile: the graph substrate
exists, H-records reference it.

## 4. M-registry + grant lock (money stream — the build)

Grant record: `{id, amount_cents: int, purpose, recipient_endpoint,
expiry_ts, approved_by, status: proposed|active|spent|expired|revoked,
receipts: [x402 receipts]}`. Rules (all enforced in code, not policy):

- **Integer cents, ceiling-not-balance** (stolen from AIP/IBCT): a grant
  authorizes spend UP TO N cents on ONE purpose. It is not a balance.
- **No standing money.** Agent hot holdings = active grants only. No grant,
  no spend path exists (treasury pre-check fails closed).
- **Exact-amount release.** Human button press releases EXACTLY the granted
  cents to EXACTLY the recipient (EIP-3009 mental model; our x402 endpoints
  already settle exact amounts — `/v1/work` $0.005 live on mainnet).
- **Receipt-or-it-didn't-happen.** Every spend needs its x402 receipt in the
  grant record; unverified spend = process failure, learn.py-eligible.
- **Pre-check + post-check.** Pre: WorkerKit Treasury (quota buckets + cash,
  shadow pricing) + BATS escalation ladder (FREE→CHEAP→STRONG, cheapest that
  passes). Post: receipt in record. Both must pass; either fails closed.

## 5. Import verdict (what we take, what we don't, why)

IMPORT NOW ($0, no deps, fits stdlib doctrine — vendor the pattern):
- mw `queue.html` + `dashboard_server.py` → H-inbox UI + backend pattern.
- WorkerKit `treasury.py` + `bats.py` logic (~150 lines, ours) → M pre-check.
- HumanLayer approval-record schema (pattern only) → H-record shape.
- Our x402 live endpoints → exact-amount settlement rail (already running).
DON'T IMPORT: Temporal server (ops + disk we don't have), HumanLayer package
(Slack app + SaaS + non-polling blocks die at turn end), Biscuit/AIP stack
(crypto infra heavier than our threat model). Revisit each when revenue, not
before.

## 6. Constraints (load-bearing)

- Disk 93% full: no npm/pip heavies. Everything above is stdlib Python +
  one static HTML file.
- seed0 stdlib-only: x402 TS side stays behind an adapter; registry code
  never imports framework SDKs.
- Turn-bound agent: H and M NEVER block execution — poll/resume only.
  HumanLayer's blocking `await approval` is the exact pattern we invert.

## 7. Build order (all four DONE 2026-09-10 — kept as history)

1. ~~`hinbox.py` + H-record schema + `pending/poll/resolve`~~ DONE.
2. ~~Port `queue.html` → `hqueue.html` + server retarget~~ DONE (+funnel route).
3. ~~`unlocks:` + priority sort~~ DONE (transitive + value_usd points).
4. ~~M-grant schema + Treasury/BATS port + x402 receipt check~~ DONE
   (grants.py; live settlement awaits rail + human button).

## 8. Canonical M-failsafe stack (7 layers, each enforced in code)

No single mechanism holds money; the stack does. Every layer fails closed
(refuse + log), never open:

- **L0 no standing money.** Agent holdings = active grants only. No grant →
  no spend path exists (treasury pre-check fails on unknown/empty).
- **L1 exact-amount + purpose + expiry.** Integer cents, ceiling-not-balance,
  single purpose, timestamp expiry. Matches Moltwork Grant semantics
  (their scopes: actions/netuids/TEE digests; ours: purpose/endpoint/cents).
- **L2 pre-check + post-check.** Pre: treasury/budget refuse before the call.
  Post: x402 receipt required or the spend didn't happen (unverified spend =
  process failure, learn.py-eligible).
- **L3 circuit breakers.** Per-grant ceiling, per-run caps (`--budget-usd`
  aborts mid-run), max 3 validator tries / 3 replans → escalate, never loop.
- **L4 human button + revocation.** Exact cents released by explicit press;
  grant status machine ACTIVE/EXHAUSTED/EXPIRED/REVOKED (same four as
  Moltwork). Revocation is one record append, effective immediately.
- **L5 reconciliation.** Provider-reported usage (unaudited claims) vs
  invoices vs receipts — three numbers that must agree within tolerance;
  disagreement is a finding, not an error to average away.
- **L6 audit + blast radius.** Append-only grant events (nothing deleted);
  per-task grants (no pooling across purposes); hot holdings = active grant
  only; cold keys offline; KILL/STOP file halts all lanes.
- **L7 drill.** Failsafes are TESTED (grant refusal tests, zero-budget
  no-transport test, breaker trip test) — an untested failsafe is a wish.
