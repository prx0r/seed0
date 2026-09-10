#!/usr/bin/env python3
"""hserver.py — H-inbox backend. Stdlib only (http.server, no deps).

Pattern ported from mw dashboard_server.py, retargeted at the H-registry:
  GET  / or /hqueue.html  -> the inbox UI
  GET  /api/h/pending     -> open requests, priority-sorted
  POST /api/h/resolve     -> {id, decision, note} resolves one request
  GET  /api/health        -> {status}

Run: python3 hserver.py [--port 8791]   (localhost only, human's browser)
"""
from __future__ import annotations
import json
import sys
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse

sys.path.insert(0, str(Path(__file__).resolve().parent))
import hinbox

def api_funnel(query: str = "") -> tuple[int, dict | list]:
    """Cross-repo ranked funnel (hplane). ?repos=a,b overrides plane/repos.txt."""
    try:
        import hplane
        from urllib.parse import parse_qs
        qs = parse_qs(query)
        repos = qs["repos"][0].split(",") if "repos" in qs else hplane.repo_list()
        return 200, hplane.rank(hplane.collect(repos))
    except Exception as e:
        return 500, {"ok": False, "error": str(e)[:200]}

ROOT = Path(__file__).resolve().parent
PORT = 8791


def api_pending(query: str = "") -> tuple[int, dict | list]:
    try:
        return 200, hinbox.poll()
    except Exception as e:
        return 500, {"ok": False, "error": str(e)[:200]}


def api_resolve(body: dict) -> tuple[int, dict]:
    try:
        rid = body.get("id", "")
        decision = body.get("decision", "")
        note = body.get("note", "")
        rec = hinbox.resolve(rid, decision, note=note)
        return 200, {"ok": True, "resolution": rec["id"]}
    except (KeyError, ValueError) as e:
        return 400, {"ok": False, "error": str(e)[:200]}
    except Exception as e:
        return 500, {"ok": False, "error": str(e)[:200]}


class HHandler(BaseHTTPRequestHandler):
    server_version = "HInbox/0.1"

    def _json(self, code: int, obj) -> None:
        body = json.dumps(obj).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        parsed = urlparse(self.path)
        path, query = parsed.path, parsed.query
        if path in ("/", "/hqueue.html"):
            page = (ROOT / "hqueue.html").read_bytes()
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(page)))
            self.end_headers()
            self.wfile.write(page)
        elif path == "/api/h/pending":
            code, obj = api_pending()
            self._json(code, obj)
        elif path == "/api/h/funnel":
            code, obj = api_funnel(query)
            self._json(code, obj)
        elif path == "/api/health":
            self._json(200, {"status": "ok"})
        else:
            self._json(404, {"ok": False, "error": "not found"})

    def do_POST(self):
        path = urlparse(self.path).path
        if path != "/api/h/resolve":
            self._json(404, {"ok": False, "error": "not found"})
            return
        try:
            length = int(self.headers.get("Content-Length", 0) or 0)
        except ValueError:
            length = 0
        try:
            body = json.loads(self.rfile.read(length) or b"{}")
        except Exception:
            self._json(400, {"ok": False, "error": "bad json"})
            return
        code, obj = api_resolve(body)
        self._json(code, obj)

    def log_message(self, *a):
        pass


def serve(port: int = PORT) -> ThreadingHTTPServer:
    srv = ThreadingHTTPServer(("127.0.0.1", port), HHandler)
    return srv


def main(argv: list[str]) -> int:
    port = int(argv[argv.index("--port") + 1]) if "--port" in argv else PORT
    srv = serve(port)
    print(f"hinbox on http://127.0.0.1:{srv.server_port} (localhost only)")
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        pass
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
