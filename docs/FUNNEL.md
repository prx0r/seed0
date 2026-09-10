# FUNNEL — idea to ranked seeds to amended seeds

```bash
# one idea, N seeds, fresh-agent isolation, binary rubric:
python3 funnel.py run --idea "..." --rubric rubric.json --seeds seed1,seed2 \
    --agent-cmd ./agent.sh --out runs/idea1
# main-agent review scaffold (hypothesis/change/verdict per seed):
python3 funnel.py review --run runs/idea1 --round 1
# record a seed amendment (edits are yours; this stamps VERSION + log):
python3 funnel.py amend --seed seeds/seed1 --bump 1.1 --note "why" --run runs/idea1
```

Rules: attempts contain seed + brief + rubric ONLY (no thesis leakage);
agent failures recorded, never hidden; binary rubric (suite + compliance + checks)
gates promotion; every amendment links its run. Repeat until all binary_pass.
