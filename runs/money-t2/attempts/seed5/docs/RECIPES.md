# RECIPES — seed5 operations

## Self-check (example probes vs example guard)
```bash
python3 run_packs.py --self-check   # expect 2/2 held
```

## Add a probe (the rule: defense ships WITH its attack)
1. Append to `packs/<target>_pack.py`: id/class/input/must_any/must_all/must_not.
2. Grade against fallback AND production paths before commit.
3. Record new attack classes in THREATMODEL.md vectors.
