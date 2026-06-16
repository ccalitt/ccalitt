#!/usr/bin/env python3
"""plot-scout local browse UI server (stdlib only).

Serves a single-page UI + JSON API over the SQLite DB the pipeline produces.
No third-party dependencies. Enables no schedules — this is a viewer plus a
button to re-run the offline, deterministic pipeline.

Usage:
    python web/server.py                 # serve on http://127.0.0.1:8000
    python web/server.py --scan          # populate (scan all localities) then serve
    python web/server.py --port 9000 --db /tmp/scratch.db --open
"""

from __future__ import annotations

import argparse
import json
import sys
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from config import settings  # noqa: E402
from lib import state_store  # noqa: E402
from services import pipeline  # noqa: E402
from web import api  # noqa: E402

STATIC_DIR = Path(__file__).resolve().parent / "static"

CONTENT_TYPES = {
    ".html": "text/html; charset=utf-8",
    ".js": "application/javascript; charset=utf-8",
    ".css": "text/css; charset=utf-8",
    ".json": "application/json; charset=utf-8",
    ".svg": "image/svg+xml",
}


class Handler(BaseHTTPRequestHandler):
    server_version = "plot-scout/1.0"
    db_path = str(settings.DB_PATH)

    # ---- helpers -------------------------------------------------------
    def _conn(self):
        conn = state_store.connect(self.db_path)
        state_store.init_db(conn)  # idempotent; ensures tables exist
        return conn

    def _send_json(self, payload, status: int = 200) -> None:
        body = json.dumps(payload, default=str).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _send_static(self, rel: str) -> None:
        path = (STATIC_DIR / rel).resolve()
        if not str(path).startswith(str(STATIC_DIR)) or not path.is_file():
            self._send_json({"error": "not found"}, 404)
            return
        body = path.read_bytes()
        self.send_response(200)
        self.send_header("Content-Type", CONTENT_TYPES.get(path.suffix, "application/octet-stream"))
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _read_body(self) -> dict:
        length = int(self.headers.get("Content-Length", 0) or 0)
        if not length:
            return {}
        try:
            return json.loads(self.rfile.read(length).decode("utf-8"))
        except (json.JSONDecodeError, UnicodeDecodeError):
            return {}

    def log_message(self, fmt, *args):  # quieter logging
        sys.stderr.write("  %s\n" % (fmt % args))

    # ---- routing -------------------------------------------------------
    def do_GET(self) -> None:
        route = urlparse(self.path).path
        try:
            if route in ("/", "/index.html"):
                self._send_static("index.html")
            elif route.startswith("/static/"):
                self._send_static(route[len("/static/"):])
            elif route == "/api/summary":
                conn = self._conn()
                self._send_json(api.get_summary(conn))
                conn.close()
            elif route == "/api/plots":
                conn = self._conn()
                self._send_json(api.list_plots(conn))
                conn.close()
            elif route.startswith("/api/plot/"):
                pid = int(route.rsplit("/", 1)[-1])
                conn = self._conn()
                plot = api.get_plot(conn, pid)
                conn.close()
                self._send_json(plot if plot else {"error": "not found"},
                                200 if plot else 404)
            elif route == "/api/landmarks":
                self._send_json(api.get_landmarks())
            elif route == "/api/localities":
                conn = self._conn()
                self._send_json(api.get_localities(conn))
                conn.close()
            elif route == "/api/reports":
                conn = self._conn()
                self._send_json(api.get_reports(conn))
                conn.close()
            else:
                self._send_json({"error": "not found"}, 404)
        except Exception as exc:  # surface errors as JSON for the UI
            self._send_json({"error": str(exc)}, 500)

    def do_POST(self) -> None:
        route = urlparse(self.path).path
        body = self._read_body()
        try:
            if route == "/api/scan":
                localities = body.get("localities")  # None -> whole whitelist
                result = pipeline.run_scan(localities=localities, db_path=self.db_path)
                self._send_json({"ok": True, "scan": result})
            elif route == "/api/run":
                locality = body.get("locality")
                if not locality:
                    self._send_json({"error": "locality required"}, 400)
                    return
                result = pipeline.run_dry_run(locality, db_path=self.db_path)
                self._send_json({"ok": True, "locality": locality,
                                 "canonical_plots": result["canonical_plots"],
                                 "dropped": result["dropped"]})
            else:
                self._send_json({"error": "not found"}, 404)
        except Exception as exc:
            self._send_json({"error": str(exc)}, 500)


def main() -> None:
    ap = argparse.ArgumentParser(description="plot-scout browse UI")
    ap.add_argument("--port", type=int, default=8000)
    ap.add_argument("--host", default="127.0.0.1")
    ap.add_argument("--db", default=str(settings.DB_PATH))
    ap.add_argument("--scan", action="store_true",
                    help="run the pipeline across all whitelist localities before serving")
    ap.add_argument("--open", action="store_true", help="open the UI in a browser")
    args = ap.parse_args()

    Handler.db_path = args.db

    if args.scan:
        print("Scanning all whitelist localities (offline, deterministic)...")
        result = pipeline.run_scan(db_path=args.db)
        print(f"  {result['totals']['canonical_plots']} canonical plots across "
              f"{result['localities_scanned']} localities.")

    httpd = ThreadingHTTPServer((args.host, args.port), Handler)
    url = f"http://{args.host}:{args.port}"
    print(f"plot-scout UI → {url}   (DB: {args.db})")
    print("Ctrl-C to stop.")
    if args.open:
        import webbrowser
        webbrowser.open(url)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nstopped.")
        httpd.server_close()


if __name__ == "__main__":
    main()
