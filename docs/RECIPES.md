# RECIPES — copy-paste operations (outputs verified 2026-09-10)

## Bring-up (fresh machine, no keys)
```bash
git clone <seed0> && cd seed0
python3 -m pytest tests/ -q        # expect 106 passed
python3 seed0.py check .           # expect 5/5 COMPLIANT
python3 seed0.py check . --cwd-independent   # + suite green from foreign CWD
```

## Start a project from an idea
```bash
python3 seed0.py new NAME --idea "one-paragraph idea"
# → NAME/ with AGENTS.md, README, NORTHSTAR, docs/, tests/, .env.example
```

## Rank seeds (tournament)
```bash
python3 tournament.py seeds/seed1 seeds/seed2 --model mock
echo '{"tests_green":100,"compliant":10,"evidence":1}' > weights.json
python3 tournament.py seeds/seed1 seeds/seed2 --weights weights.json  # preregistered
# expect ranked lines + receipt: runs/sha256_….json
```

## Run the funnel (idea → isolated attempts → review)
```bash
printf '{"checks": [{"id": "readme", "type": "file_exists", "path": "README.md"}]}' > rubric.json
python3 funnel.py run --idea "demo ledger API" --rubric rubric.json \
  --seeds seed1,seed2 --agent-cmd true --out runs/idea1
python3 funnel.py review --run runs/idea1 --round 1   # hypothesis scaffold
python3 funnel.py review --run runs/idea1 --round 1 --blind  # lanes + sealed map
python3 funnel.py reveal --run runs/idea1 --round 1  # AFTER verdicts only
python3 funnel.py amend --seed seeds/seed1 --bump 1.1 --note "why" --run runs/idea1
```

## Falsify a pattern (ablation)
```bash
python3 eval_arch.py --arch docs-removal --seed seeds/seed1 --rubric rubric.json \
  --ablate docs/README.md --agent-cmd true --out runs/eval-docs
# verdict: load-bearing | inert-here | broken-regardless (+ receipt)
```

## Learn from shared failures
```bash
python3 learn.py runs/idea1 --out learnings/
# clusters identical failure signatures (≥2 seeds) → CR-1.1-N proposals
```

## Live model evals (needs key, spends cents)
```bash
OPENCODE_GO_API_KEY=... python3 pyeval.py run datasets/safety_sample.json \
  --model mimo-v2.5 --out runs/     # expect SCORE 5.0/5.0 PASS + receipt
```

## Delegate a step (H/A/M tiers)
```bash
python3 ham.py check --action "git push origin main"   # CLEAR or PROHIBITED
python3 ham.py approve --target seed0.py --summary "H1" --by owner
python3 ham.py verify --record '<json>' --target seed0.py   # VALID or VOID
python3 ham.py log --kind M --summary "eval run" --cost 0.001
python3 ham.py outcome --class "push:branch" --approved 1   # x3 -> standing allow
```

## Work the queue (META_LOOP)
```bash
python3 loop.py list                  # 14 DONE + 1 PAUSED expected
python3 loop.py list --status PAUSED
python3 loop.py check                 # schema + DONE-needs-proof audit
```

## Human inbox (H-stream)
```bash
python3 -c "from hinbox import new_request; print(new_request('approve X?', unlocks=['a-push'])['id'])"
python3 hserver.py --port 8791        # inbox at http://127.0.0.1:8791 (localhost only)
```

## Money grants (M-stream)
```bash
python3 -c "from grants import new_grant, activate, check_spend;
g = new_grant(100, 'eval-run', 'https://x402.egoic.ai/v1/work');
activate(g['id']); print(check_spend(g['id'], 100, 'eval-run')['remaining_cents'])"
```

## Use seed0 from any agent (MCP, zero install beyond clone)

Dependencies: none — stdlib only (`tests/test_nodeps.py` proves it; adding a
third-party import breaks that test on purpose). Python 3.11+.
```json
// opencode.json
{"mcp": {"seed0": {"type": "local",
  "command": ["python3", "/path/to/seed0/mcp_server.py"]}}}
```
Read-only surface (check/list/ready/stoplight/history/screen) — the server
cannot approve, mutate, or spend. Writes stay on the CLI in front of a human.

## Validate idea / criteria files
```bash
python3 idea0/validate_idea.py ideas/idea1.md
python3 criteria0/validate_criteria.py criteria/criteria1.md
```

## Human/agent split with predicted data
```python
from tasks import Feed, new_task
f = Feed("tasks.jsonl")
creds = f.add(new_task("human", "Telnyx API key"))          # blocks…
build = f.add(new_task("agent", "wire dispatch", blocked_by=[creds["id"]]))
f.predict(creds["id"], {"TELNYX_API_KEY": "MOCK"})          # …until mocked
f.agent_tasks()          # build now runnable
f.deliver(creds["id"], {"TELNYX_API_KEY": "REAL"}, "owner pasted")
f.reconcile(creds["id"]) # → [build] must re-verify on real data
```
