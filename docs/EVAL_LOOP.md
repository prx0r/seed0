# EVAL LOOP — testing essay architectures for real

Pipeline: essay pattern → seed variant → binary rubric → funnel tournament →
ablation → review. Every step runnable, every verdict a receipt.

```bash
# 1. implement the pattern as a seed (or seed variant) + rubric with checks
# 2. prove the pattern earns its keep (ablation falsifier):
python3 eval_arch.py --arch ledger --seed seeds/seed1 --rubric rubric.json \
    --ablate ralph.py --agent-cmd true --out runs/eval-ledger
# 3. read runs/eval-ledger/eval.json: load-bearing | inert-here | broken-regardless
```

Verdict meanings: **load-bearing** (passes intact, fails ablated — keep and dig
deeper), **inert-here** (passes either way — cut it or find a harder rubric),
**broken-regardless** (fails intact — fix the seed before crediting ideas).

Substrate note: patterns mined from `mine/proclusagent/` (ledgers, dossiers,
debate with provenance, guardrails) are the first candidates. Each gets the same
treatment — no essay concept ships on narrative alone.
