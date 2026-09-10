# seed3 — evidence-maximalist kernel

The audit-trail seed: every action leaves a hash-chained receipt, and the chain
itself is verified before any claim ships. For regulated, disputed, or
multi-party work where proof beats promises.

## 60-second start

```bash
cp .env.example .env
python3 -m pytest tests/ -q
python3 -c "from evidence import append, verify; append('demo', {'ok': True}); print(verify())"
```

## What this is / is not

- IS: tamper-evident logging plus the discipline to consult it.
- IS NOT: tamper-PROOF storage, a blockchain, or a judge. Verification detects
  edits; prevention is backups + access control (out of scope).

## Layout

`evidence.py` log + chain · `evidence/` logs · `docs/` · `tests/`.
