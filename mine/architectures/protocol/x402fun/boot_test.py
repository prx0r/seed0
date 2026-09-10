"""Boot test for prx0r/x402fun (mine-side only, $0). Asserts packet gate hypothesis."""
def test_packet_has_truth_condition():
    import json,pathlib
    d=json.loads(pathlib.Path(__file__).with_name("packet.json").read_text())
    assert d.get("truth_condition") and d.get("commit_sha")
