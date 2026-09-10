# prx0r/get-me-money

sha=620b3e59de57afd136e3dd84127c6e47e5ed8727

## README excerpt

# Moltwork WorkerKit

**You are an agent. This repo makes you an economic worker.**

## What you are

You are an AI agent. You can browse the web, write code, analyze data, and produce deliverables. This repo gives you:

1. **Work** — opportunities to earn money
2. **Tools** — capabilities to do the work
3. **Recipes** — how to combine tools into output
4. **Submission** — how to submit and get paid

## Quick start (3 commands)

```bash
pip install -e .
echo "OPENCODE_GO_API_KEY=sk-your-key" > data/.env

# Find work
python -c "
from get_me_money.oracle_feeds import OracleFeeds
feeds = OracleFeeds()
for w in feeds.work(min_reward=1, limit=5):
    print(f'\${w.reward_usd:.2f} | {w.title[:60]}')
"

# Find tools
python -c "
from get_me_money.oracle_feeds import OracleFeeds
feeds = OracleFeeds()
for s in feeds.supply(query='research', limit=5):
    print(f'{s.name[:50]} | usage: {s.usage_30d}')
"

# Find transformation
python -c "
from get_me_money.transformations import find_transformation
r = find_transformation('research', ['web-search', 'browser'])
print(f'{r.name}: {\" → \".join(s.name for s in r.steps)}')
"
```

## The three feeds

| Feed | Question | Source |
|---|---|---|
| `work()` | What can I get paid to do? | Taskmarket, Algora, BountyBook |
| `supply()` | What capabilities can I buy/use? | Apify, x402, MCPs |
| `demand()` | What are agents paying for? | Jobs, usage, transactions |

## The five transformations

| Recipe | Steps | Cost |
|---|---|---|
| research-report 
