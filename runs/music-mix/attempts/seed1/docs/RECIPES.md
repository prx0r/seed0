# RECIPES — seed1 operations

## Run one loop iteration
```bash
AGENT_CMD="my-agent --task" VERIFY_CMD="pytest tests/ -q" python3 ralph.py --once
```

## Run until plan empty (supervisor loop, Ctrl-C safe)
```bash
while python3 ralph.py --once; do :; done; grep -c "^- \[ \]" plan.md  # expect 0
```

## Add tasks
Append `- [ ] task text` lines to plan.md. One line = one run. Keep tasks small.

## Check standard compliance
```bash
python3 /tmp/opencode/seed0/seed0.py check .
```
