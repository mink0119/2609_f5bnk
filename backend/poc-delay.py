#!/usr/bin/env python3
"""Additive delay/status helper for Gateway API timeout and retry tests."""
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import time
import os

HOST = os.environ.get("POC_DELAY_HOST", "127.0.0.1")
PORT = int(os.environ.get("POC_DELAY_PORT", "18080"))


class Handler(BaseHTTPRequestHandler):
    def log_message(self, fmt, *args):
        return

    def _write(self, code, body, extra=None):
        payload = body.encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "text/plain")
        self.send_header("Content-Length", str(len(payload)))
        if extra:
            for k, v in extra:
                self.send_header(k, v)
        self.end_headers()
        self.wfile.write(payload)

    def do_GET(self):
        path = self.path.split("?", 1)[0]
        if path.startswith("/delay/"):
            try:
                sec = float(path.split("/", 2)[2])
            except (IndexError, ValueError):
                self._write(400, "bad delay\n")
                return
            time.sleep(max(0.0, sec))
            self._write(200, f"DELAYED {sec}s - 30.0.0.10\n")
            return
        if path.startswith("/status/"):
            try:
                code = int(path.split("/", 2)[2])
            except (IndexError, ValueError):
                self._write(400, "bad status\n")
                return
            self._write(code, f"STATUS {code} - 30.0.0.10\n")
            return
        self._write(404, "poc-delay unknown\n")


if __name__ == "__main__":
    ThreadingHTTPServer((HOST, PORT), Handler).serve_forever()
