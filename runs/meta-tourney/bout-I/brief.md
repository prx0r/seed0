# NORTHSTAR bout-I (frozen 2026-09-10): implement ONE filing variant.

Naive lane: append-always inbox (file() appends every call).
Keyed lane: idempotency-key filing (same key returns existing record).
`variant.py` exposes the inbox; `tests/test_variant.py` smokes it. Stdlib only.
