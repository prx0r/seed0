"""chain grammar + press log."""
import pytest

import chain as C
import press as P


def test_parse_verbs_and_args():
    acts = C.parse("2943")
    assert [(a["key"], a["name"], a["arg"]) for a in acts] == [
        ("2", "ZOOM", None), ("9", "FIX", None), ("4", "PICK", 3)]
    assert C.parse("0")[0]["name"] == "STOP"
    assert C.parse("81")[-1]["arg"] == 1


def test_parse_rejects_loudly():
    with pytest.raises(ValueError, match="not keys"):
        C.parse("29x3")
    with pytest.raises(ValueError, match="needs a digit"):
        C.parse("4")
    with pytest.raises(ValueError, match="needs a digit"):
        C.parse("28")
    with pytest.raises(ValueError, match="non-empty"):
        C.parse("")


def test_describe():
    assert C.describe(C.parse("51")) == "5 OK -> 1 GO"


def test_keys_json_valid():
    defs = C.key_defs()
    assert len(defs) == 10 and set(defs) == set("0123456789")
    for k, d in defs.items():
        assert {"name", "hand", "arg", "acts", "close"} <= set(d)
    assert defs["4"]["arg"] == "digit" and defs["8"]["arg"] == "digit"


def test_press_log_miner_shape(tmp_path):
    row = P.log(str(tmp_path), "s1", "5", None, "51",
                {"open_h": []}, {"ok": True, "action": "approve"})
    assert row["shown"][row["picked"]] == "OK" == row["picked_text"]
    assert row["shown"] == P.SHOWN and len(P.SHOWN) == 10
    rows = P.read(str(tmp_path))
    assert len(rows) == 1 and rows[0]["chain"] == "51"
    assert P.read(str(tmp_path / "nowhere")) == []
