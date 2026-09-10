import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import ledger


def setup_function(fn):
    ledger._store.clear()


def test_add_and_total():
    ledger.add("alice", 10)
    ledger.add("alice", 5)
    assert ledger.total("alice") == 15


def test_total_unknown_is_zero():
    assert ledger.total("nobody-xyz") == 0


def test_save_load_roundtrip(tmp_path):
    ledger.add("bob", 7)
    ledger.add("carol", 3)
    p = str(tmp_path / "ledger.json")
    ledger.save(p)
    ledger._store.clear()
    assert ledger.total("bob") == 0
    ledger.load(p)
    assert ledger.total("bob") == 7
    assert ledger.total("carol") == 3
