import os
import ledger


def _reset():
    ledger._balances.clear()


def test_add_and_total():
    _reset()
    ledger.add("alice", 10)
    ledger.add("alice", 5)
    assert ledger.total("alice") == 15


def test_total_unknown_is_zero():
    _reset()
    assert ledger.total("nobody") == 0


def test_save_load_round_trip(tmp_path):
    _reset()
    ledger.add("alice", 10)
    ledger.add("bob", 7)
    p = os.path.join(str(tmp_path), "ledger.json")
    ledger.save(p)
    _reset()
    assert ledger.total("alice") == 0
    ledger.load(p)
    assert ledger.total("alice") == 10
    assert ledger.total("bob") == 7
