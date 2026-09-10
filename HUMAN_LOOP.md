# HUMAN_LOOP — when the agent stops and asks (vision, not built)

Autonomy without a reporting contract is either a micromanaged chatbot or an
unattended bulldozer. seed0 defines the contract up front: the agent decides
everything EXCEPT the classes below, which become human tasks automatically.

## Report-back classes (escalate, don't proceed)
1. **Irreversible or costly actions** — spend, delete, publish, send-as, legal or
   compliance exposure. Proposal with diff + cost + rollback plan; human approves.
2. **Ambiguity that changes the goal** — the idea admits two real readings; agent
   states both, recommends one, waits. Never guesses the goal silently.
3. **Blocked on the outside world** — credentials, access, purchases, another human's
   decision. Task records exactly what is needed from whom, with a readiness check.
4. **Confidence below the bar** — verification impossible (no test, no oracle, no
   precedent). Agent says what it tried, what would prove it, and what it costs.
5. **Checkpoints, not check-ins** — scaffold approved → plan approved → first green
   build → live/merge. Four human touches per project maximum by default.

## Human task shape (populated, not messaged)
Every escalation is a record, not a ping:
`{id, project, class, summary, options[], recommendation, cost_of_wait, needed_from,
readiness_check, created, expires}`. Tasks queue in THREADS.md / HumanAction-style
queues, expire loudly (expiry re-escalates, never auto-approves), and resolve into
receipts the agent can verify against. No "quick question?" DMs; no silent waiting.

## Autonomy ladder (per project, human sets the rung)
- **L0 observe** — agent reads, maps, proposes. Nothing executes.
- **L1 sandbox** — executes locally/test env only; no external writes.
- **L2 guarded** — external writes behind approvals/tokens (the default).
- **L3 trusted** — pre-approved classes auto-run within caps; everything else L2.
Rung recorded in AGENTS.md. Promotion is a human decision with evidence cited.

## Anti-patterns (contract violations)
Approval floods (batching trivia to manufacture consent), expiry auto-approve,
goal-guessing, silent credential requests, progress theater (green checks that
prove nothing — every gate must assert a falsifiable property).
