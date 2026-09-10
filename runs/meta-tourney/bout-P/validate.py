#!/usr/bin/env python3
"""Bout-P validator: footrule distances for both variants x both filing orders.
Preregistered thresholds: transitive_total < direct_total AND transitive invariant.
Exit 0 = H1 holds. Prints integers, not adjectives."""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from metrics import rank_distance

sys.path.insert(0, str(Path(__file__).resolve().parent / "lanes" / "direct"))
sys.path.insert(0, str(Path(__file__).resolve().parent / "lanes" / "transitive"))
import variant as _v  # noqa: F401  (rebound below per lane)
import importlib


def run_variant(name: str, requests: list[dict], tasks: list[dict]) -> list[str]:
    for mod in list(sys.modules):
        if mod == "variant":
            del sys.modules[mod]
    for p in list(sys.path):
        if "lanes" in p:
            sys.path.remove(p)
    sys.path.insert(0, str(Path(__file__).resolve().parent / "lanes" / name))
    import variant
    import inspect
    if len(inspect.signature(variant.order).parameters) == 1:
        return variant.order(requests)
    return variant.order(requests, tasks)


def main() -> int:
    fx = json.loads(Path(__file__).with_name("fixture.json").read_text())
    truth, tasks = fx["ground_truth"], fx["tasks"]
    by_id = {r["id"]: r for r in fx["requests"]}
    dist, orders = {}, {}
    for name in ("direct", "transitive"):
        orders[name] = []
        for filing in fx["filing_orders"]:
            reqs = [dict(by_id[i]) for i in filing]
            got = run_variant(name, reqs, tasks)
            orders[name].append(got)
        dist[name] = rank_distance(orders[name], truth)
    invariant = orders["transitive"][0] == orders["transitive"][1] == truth
    ok = dist["transitive"] < dist["direct"] and invariant
    print(json.dumps({"transitive_total": dist["transitive"],
                      "direct_total": dist["direct"],
                      "transitive_orders": orders["transitive"],
                      "direct_orders": orders["direct"],
                      "invariant": invariant, "pass": ok}))
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
