"""naive rival: append-always inbox, no keys, no questions."""
from __future__ import annotations


class NaiveInbox:
    def __init__(self):
        self.records: list[dict] = []

    def file(self, summary: str, key: str = "") -> dict:
        rec = {"summary": summary, "key": key}
        self.records.append(rec)
        return rec
