"""registries: one read API + schema gate over A/H/M streams."""
import json

import registries as R


def _write(root, stream, recs):
    p = R.path(stream, str(root))
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text("\n".join(json.dumps(r, sort_keys=True) for r in recs) + "\n")


def test_missing_file_is_empty_stream(tmp_path):
    assert R.read("a", str(tmp_path)) == []
    assert R.read("h", str(tmp_path)) == []
    assert R.read("m", str(tmp_path)) == []
    assert R.check_all(str(tmp_path)) == []


def test_unknown_stream_rejected(tmp_path):
    import pytest
    with pytest.raises(ValueError, match="stream must be"):
        R.read("z", str(tmp_path))
    assert R.validate("z", {"id": "x"}) == ["unknown stream: z"]


def test_a_schema(tmp_path):
    good = {"id": "a-1", "tier": "A", "summary": "work", "status": "DONE"}
    assert R.validate("a", good) == []
    assert R.validate("a", {"id": "a-2"}) != []          # missing tier/summary/status
    assert R.validate("a", {**good, "status": "YOLO"}) == ["bad status: 'YOLO'"]
    _write(tmp_path, "a", [good])
    assert R.check_all(str(tmp_path)) == []
    _write(tmp_path, "a", [good, {"id": "a-9", "status": "DONE"}])
    assert any(e.startswith("a[1]") for e in R.check_all(str(tmp_path)))


def test_h_schema_envelope_plus_hkind(tmp_path):
    good = {"id": "h-1", "kind": "request", "h_kind": "input",
            "summary": "email?", "status": "open", "unlocks": []}
    assert R.validate("h", good) == []
    assert R.validate("h", {**good, "kind": "bribe"}) != []
    assert R.validate("h", {**good, "h_kind": "bribe"}) != []
    assert R.validate("h", {**good, "status": "maybe"}) != []
    assert R.validate("h", {"id": "h-2", "kind": "resolution",
                            "supersedes": "h-1", "decision": "approved"}) == []


def test_m_schema_matches_grants_events(tmp_path):
    from grants import new_grant, activate
    g = new_grant(298, "domain", "https://x402.egoic.ai/v1/work",
                  path=str(tmp_path / "loop" / "registry_m.jsonl"))
    activate(g["id"], path=str(tmp_path / "loop" / "registry_m.jsonl"))
    recs = R.read("m", str(tmp_path))
    assert len(recs) == 2
    assert R.check_all(str(tmp_path)) == []  # grants events pass the M gate


def test_no_delete_api():
    assert not hasattr(R, "delete")
    assert not hasattr(R, "remove")
    assert not hasattr(R, "update")
