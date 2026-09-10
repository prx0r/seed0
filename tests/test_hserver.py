"""hserver tests: routes + resolve roundtrip over a live localhost socket."""
import json
import threading
import urllib.request

from hserver import serve
import hinbox


def _call(base, method, path, body=None):
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(base + path, data=data, method=method,
                                 headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=5) as r:
            return r.status, r.read()
    except urllib.error.HTTPError as e:
        return e.code, e.read()


def test_pending_resolve_roundtrip(tmp_path, monkeypatch):
    reg = tmp_path / "h.jsonl"
    monkeypatch.setattr(hinbox, "HREG", str(reg))
    import hserver
    monkeypatch.setattr(hserver.hinbox, "HREG", str(reg))
    r = hinbox.new_request("push main?", context="25 files")
    srv = serve(0)
    port = srv.server_address[1]
    t = threading.Thread(target=srv.serve_forever, daemon=True)
    t.start()
    try:
        base = f"http://127.0.0.1:{port}"
        s, body = _call(base, "GET", "/api/h/pending")
        assert s == 200
        items = json.loads(body)
        assert len(items) == 1 and items[0]["id"] == r["id"]
        assert items[0]["priority_score"] == 0.5  # urgency-only, no unlocks
        s, body = _call(base, "POST", "/api/h/resolve",
                        {"id": r["id"], "decision": "approved", "note": "go"})
        assert s == 200 and json.loads(body)["ok"] is True
        s, body = _call(base, "GET", "/api/h/pending")
        assert json.loads(body) == []
        s, body = _call(base, "POST", "/api/h/resolve",
                        {"id": r["id"], "decision": "approved"})
        assert s == 400  # double-resolve rejected
        s, body = _call(base, "GET", "/")
        assert s == 200 and b"Human Queue" in body
    finally:
        srv.shutdown()


def test_funnel_route_multi_repo(tmp_path, monkeypatch):
    import json as _json
    import threading as _th
    import urllib.request as _url
    import urllib.parse as _up
    from hserver import serve
    import hinbox
    r = tmp_path / "r1"
    (r / "loop").mkdir(parents=True)
    (r / "loop" / "tasks.jsonl").write_text("")
    reg = r / "loop" / "registry_h.jsonl"
    monkeypatch.setattr(hinbox, "HREG", str(reg))
    import hserver as _hs
    monkeypatch.setattr(_hs.hinbox, "HREG", str(reg))
    hinbox.new_request("fix rail", unlocks=["x"])
    srv = serve(0)
    port = srv.server_address[1]
    _th.Thread(target=srv.serve_forever, daemon=True).start()
    try:
        base = f"http://127.0.0.1:{port}"
        qs = _up.urlencode({"repos": f"{r},{tmp_path}/dark"})
        with _url.urlopen(base + "/api/h/funnel?" + qs, timeout=5) as resp:
            rows = _json.loads(resp.read().decode())
        by_repo = {x.get("repo"): x for x in rows}
        assert by_repo["r1"]["status"] == "open"  # label travels, not path
        assert by_repo["r1"]["box"] == ""
        assert by_repo["dark"]["status"] == "dark"
        assert rows[0]["status"] == "dark"  # darkness ranks top
    finally:
        srv.shutdown()
