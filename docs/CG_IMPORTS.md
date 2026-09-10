# CG IMPORTS — what seed0 takes from /cg (cogymkernel), reviewed 2026-09-10

/cg is a deterministic agentic evolution lab with the strictest agent doctrine
encountered: absolute rules, content-addressed proofs, gates over objectives.
Import the doctrine, not the dependency.

## Adopted as seed0 law (already true — now cited)
- **Gates dominate objectives.** Never a scalar fitness trading quality for cost.
  Tournament ranks by gates first (tests_green, compliant); evidence count only
  breaks ties and is flagged gameable.
- **LLM judgment only as binary, criterion-bound checks above deterministic
  verification.** Criteria rows must be true/false; validators are pure functions.
- **Receipts as proofs.** Run logs + digests are the durable truth; derived views
  (leaderboards, dashboards) rebuild from them or they are lies.
- **Volatile fields out of content ids.** Timestamps beside digests, never inside
  canonical records (our digest uses sort_keys canonical JSON — same rule).

## Adopted as new convention
- **MCP tool-adding recipe** (entry + handler + stdio round-trip test) → copied
  into voiceagent `docs/MCP.md`; seed0 MCP future follows the same 3 steps.
- **Hypotheses as falsifiable predictions** (evo recipes + reasoning styles) →
  idea0 already requires "would be proven wrong if" rows; cg is the precedent cited.
- **Rebuild test**: deleting any derived artifact must destroy no evidence.
  Applies to: tournament leaderboards (rebuild from run logs), digests, indexes.

## Explicitly NOT imported
cg's kernel, HydraDB, evolution machinery — different problem (evolution vs
compliance). Doctrine crosses the gap; code does not. No dependency added.
