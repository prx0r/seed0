# RECIPES — seed4 operations

## Validate lanes
```bash
python3 scripts/lane_check.py   # expect LANES OK
```

## Check who owns a diff
```bash
git diff --name-only | xargs python3 scripts/lane_check.py
```

## Spawn a lane worktree
```bash
sh scripts/new-lane.sh api
```
