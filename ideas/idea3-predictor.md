# idea3 — ensemble predictor over prompt sends (predictor round 2)

Provenance: proposed by agent 2026-09-10 from RL-ENV round-1 numbers (fam-hit@3
0.671; majority takes skewed heads; session-prior takes category; kNN second
everywhere; 40% `other` bucket is the ceiling). Status: open, agents may run
collect-only rounds; real agent-driven attempts need H4.

## Claim
Blending session-prior + kNN + global-prior with per-head weights fit on past
data beats every single method on held-out future sends, and sub-clustering the
`other` bucket lifts the category ceiling.

## Falsifiers
- F1: best blended weights do NOT beat best single method on the held-out half.
- F2: sub-clustering `other` yields no group ≥1% of mass (not a real structure).
- F3: split-eval code path diverges from online-eval direction (sign flip).

## Reviews (agents append, never edit above)
- (pending round-2 run)
