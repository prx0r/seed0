# RECIPES — seed3 operations

## Log an action
```bash
python3 -c "from evidence import append; append('deploy', {'version': '1.2.3'})"
```

## Verify before claiming anything
```bash
python3 -c "from evidence import verify; print(verify())"   # expect ok: True
```

## Detect tampering (try it: edit evidence/run.jsonl, re-run verify)
