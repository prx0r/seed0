# RECIPES — seed2 operations

## Validate the spec
```bash
python3 scripts/spec_check.py   # expect SPEC OK
```

## Add a criterion (the ONLY way to add behavior)
1. Append a row: `| AC-N | Statement | test \`test_name\` | owner |`.
2. Write the named test (red first).
3. Implement until green + `spec_check.py` passes.
