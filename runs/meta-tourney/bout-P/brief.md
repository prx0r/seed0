# NORTHSTAR bout-P (frozen 2026-09-10): implement ONE ranking variant.

Direct lane: rank H-requests by len(unlocks) desc, ties keep filing order.
Transitive lane: rank by unlock-chain value (BFS through blocked_by, unfinished
tasks only, value = 1 + len(acceptance)), ties keep filing order.
`variant.py` exposes order(); `tests/test_variant.py` smokes it. Stdlib only.
