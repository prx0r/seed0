import os
import ledger


def setup_function(fn):
    ledger._balances.clear()


def test_add_and_total():
    ledger.add("alice", 10)
    ledger.add("alice", 5)
    assert ledger.total("alice") == 15


def test_total_unknown_is_zero():
    assert ledger.total("nobody") == 0


def test_save_load_roundtrip(tmp_path):
    ledger.add("bob", 7)
    ledger.add("carol", 3)
    p = os.path.join(str(tmp_path), "ledger.json")
    ledger.save(p)
    ledger._balances.clear()
    assert ledger.total("bob") == 0
    ledger.load(p)
    assert ledger.total("bob") == 7
    assert ledger.total("carol") == 3
