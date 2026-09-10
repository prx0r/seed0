"""keyed rival: idempotency-key filing over the shipped hinbox primitive."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[5]))
from hinbox import new_request


def file_storm(path: str, summary: str, key: str, n: int = 5) -> list[dict]:
    return [new_request(summary, path=path, idempotency_key=key) for _ in range(n)]
