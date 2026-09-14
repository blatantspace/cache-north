#!/usr/bin/env python3
"""Local static server + Ben-only Wear faves disk sync (localhost).

Serves site files like http.server, plus:
  GET  /api/faves  and  /shop/ben-faves.json
  POST /api/faves  → writes shop/ben-faves.json (never remote)
"""
from __future__ import annotations

import json
import os
import sys
from datetime import datetime, timezone
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import unquote, urlparse

SITE_DIR = Path(__file__).resolve().parent
FAVES_PATH = SITE_DIR / "shop" / "ben-faves.json"
CATALOG_PATH = SITE_DIR / "shop" / "catalog.json"
PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 8765


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"


def empty_payload() -> dict:
    return {"updated": utc_now(), "faves": {}}


def load_catalog_index() -> dict:
    try:
        data = json.loads(CATALOG_PATH.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}
    out = {}
    for p in data.get("products") or []:
        pid = p.get("id")
        if not pid:
            continue
        out[pid] = p
    return out


def normalize_entry(entry) -> dict | None:
    if entry is True or entry == 1:
        return {"favedAt": utc_now(), "note": ""}
    if isinstance(entry, dict):
        return {
            "favedAt": entry.get("favedAt") or utc_now(),
            "note": entry.get("note") if isinstance(entry.get("note"), str) else "",
        }
    return None


def enrich_faves(raw_faves: dict) -> dict:
    catalog = load_catalog_index()
    out = {}
    if not isinstance(raw_faves, dict):
        return out
    for pid, entry in raw_faves.items():
        norm = normalize_entry(entry)
        if not norm:
            continue
        enriched = dict(norm)
        p = catalog.get(pid)
        if p:
            for key in ("sku", "name", "theme", "kit", "mash", "image", "price"):
                if key in p and p[key] is not None:
                    enriched[key] = p[key]
            lineage = p.get("parentKeeper") or p.get("lineage")
            if lineage:
                enriched["lineage"] = lineage
        else:
            # Keep client-supplied extras if present
            if isinstance(entry, dict):
                for key in ("sku", "name", "theme", "kit", "mash", "image", "price", "lineage"):
                    if key in entry and entry[key] is not None:
                        enriched[key] = entry[key]
        out[pid] = enriched
    return out


def read_faves_file() -> dict:
    if not FAVES_PATH.is_file():
        return empty_payload()
    try:
        data = json.loads(FAVES_PATH.read_text(encoding="utf-8"))
        if not isinstance(data, dict):
            return empty_payload()
        faves = data.get("faves")
        if not isinstance(faves, dict):
            faves = {}
        return {
            "updated": data.get("updated") or utc_now(),
            "faves": faves,
        }
    except (OSError, json.JSONDecodeError):
        return empty_payload()


def write_faves_file(raw_faves: dict) -> dict:
    payload = {
        "updated": utc_now(),
        "faves": enrich_faves(raw_faves),
    }
    FAVES_PATH.parent.mkdir(parents=True, exist_ok=True)
    tmp = FAVES_PATH.with_suffix(".json.tmp")
    tmp.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    os.replace(tmp, FAVES_PATH)
    return payload


class FavesHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(SITE_DIR), **kwargs)

    def log_message(self, fmt, *args):
        sys.stderr.write("%s - - [%s] %s\n" % (self.address_string(), self.log_date_time_string(), fmt % args))

    def _json_response(self, code: int, payload: dict):
        body = json.dumps(payload, indent=2, ensure_ascii=False).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def _read_json_body(self) -> dict | None:
        length = int(self.headers.get("Content-Length") or 0)
        if length <= 0:
            return {}
        if length > 2_000_000:
            return None
        raw = self.rfile.read(length)
        try:
            data = json.loads(raw.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError):
            return None
        return data if isinstance(data, dict) else None

    def do_GET(self):
        path = unquote(urlparse(self.path).path)
        if path in ("/api/faves", "/shop/ben-faves.json"):
            self._json_response(200, read_faves_file())
            return
        return super().do_GET()

    def do_POST(self):
        path = unquote(urlparse(self.path).path)
        if path != "/api/faves":
            self.send_error(404, "Not Found")
            return
        data = self._read_json_body()
        if data is None:
            self._json_response(400, {"ok": False, "error": "invalid JSON"})
            return
        raw = data.get("faves", data)
        if not isinstance(raw, dict):
            self._json_response(400, {"ok": False, "error": "faves must be an object"})
            return
        try:
            payload = write_faves_file(raw)
        except OSError as exc:
            self._json_response(500, {"ok": False, "error": str(exc)})
            return
        self._json_response(200, {"ok": True, **payload})

    def do_OPTIONS(self):
        path = unquote(urlparse(self.path).path)
        if path == "/api/faves":
            self.send_response(204)
            self.send_header("Allow", "GET, POST, OPTIONS")
            self.send_header("Cache-Control", "no-store")
            self.end_headers()
            return
        self.send_error(404, "Not Found")


def main():
    os.chdir(SITE_DIR)
    server = ThreadingHTTPServer(("0.0.0.0", PORT), FavesHandler)
    print(f"cache.north serve_faves on :{PORT} (cwd={SITE_DIR})", flush=True)
    print(f"ben faves → {FAVES_PATH}", flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nshutting down", flush=True)


if __name__ == "__main__":
    main()
