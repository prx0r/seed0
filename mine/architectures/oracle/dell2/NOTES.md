# prx0r/dell2

sha=976116c129e6b89da52469541b77017d48c7c255

## README excerpt

# Dell2 — Proof-Carrying Coding Deals

> Discovery is cheap. Verification is the product.

## What Is This?

Dell2 is a **proof-carrying registry of currently available coding-AI deals**. It is NOT:

- Another LiteLLM price database
- A generic model router
- A benchmark site
- A list of open-source models
- An LLM-generated recommendations page
- A crawler that treats text as verified truth

## How It Works

```
Hermes / ChatGPT / search
        =
untrusted candidate generator

Dell2
        =
deterministic evidence + verification + certification layer
```

The valuable object is a **DealCertificate** — not a deals list.

## Quick Start

```bash
# Install
cd dell2 && pip install -e .

# Verify OpenCode Go
PYTHONPATH=src python3 -c "from dell2.verifiers.opencode_go.verify import verify; verify()"

# Run tests
PYTHONPATH=src pytest tests/ -v
```

## Verification Dimensions

Each deal has 11 independent verification dimensions. A deal can be PROVEN on some dimensions and UNKNOWN on others — this is honest, not incomplete.

```
source_identity: PROVEN       ← hostname matches official provider
content_integrity: PROVEN     ← artifact hash matches
claim_support: PROVEN         ← atomic claims found in evidence
eligibility: UNKNOWN          ← no auth, can't test
purchaseability: UNKNOWN      ← no auth, can't test
service_availability: PROVEN  ← API endpoint responded
model_availability: NOT_RUN   ← not tested yet
quota_behavior: NOT_RUN       ← requires live usage
economics: PROVE
