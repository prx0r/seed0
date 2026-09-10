# prx0r/cmail

sha=98b5f850b941485a376a0c15c78f84f11082df90

## README excerpt

# cmail — the agentic business stack

**One name, owned everywhere, touched once. One business, run by agents, seen as one queue.**

Email, voice, WhatsApp, SMS, and socials converge into a job pipeline
(lead → quote → schedule → invoice) with drafts everywhere and human confirm
on every send. Untrusted input stays untrusted all the way down.

```text
name ──► checker ──► buy ──► zone ──► mail + business + number + socials
                                                         │
              voice ──►┐                                 ▼
           whatsapp ──►┤► brain (jobs/quotes/slots) ──► desk (one queue)
              email ──►┘
```

## Bring-up (fresh machine, 5 min)

```bash
git clone https://github.com/prx0r/cmail.git && cd cmail
# brain
cd stevejobless && python3 -m venv .venv && source .venv/bin/activate
pip install -e '.[dev]' && cp .env.example .env
python3 -m pytest tests/ -q        # 80+ pass, no keys needed
steve serve                        # → http://127.0.0.1:8787, desk at /desk
# email bus
cd ../cmail && npm install && npx tsc --noEmit && npm test
npx wrangler deploy                # after filling wrangler.toml IDs
# names
cd ../domainnamechecker/worker && npm install && npx wrangler deploy
```

Everything degrades gracefully without creds: sends stub, providers 409 with
the next step, slots fall back to scheduled-job blocks, quotes mark `tbd`.

## What's inside

| Dir | Role |
|---|---|
| `cmail/` | Cloudflare-native email bus: Worker + MailboxDO + D1 ind
