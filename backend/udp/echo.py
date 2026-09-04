#!/usr/bin/env python3
"""UDP echo that prefixes a pool label. Bind one process per member IP.

  BIND_ADDR=30.0.0.10 BIND_PORT=9053 POOL_NAME='COFFEE UDP - 30.0.0.10' python3 echo.py
"""
from __future__ import annotations

import os
import socket


def main() -> None:
    addr = os.environ.get("BIND_ADDR", "0.0.0.0")
    port = int(os.environ.get("BIND_PORT", "9053"))
    label = os.environ.get("POOL_NAME", "COFFEE UDP - 30.0.0.10")
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((addr, port))
    print(f"udp echo on {addr}:{port} label={label}", flush=True)
    while True:
        data, src = sock.recvfrom(2048)
        payload = data.decode("utf-8", errors="replace")
        reply = f"{label} {payload}".encode("utf-8")
        sock.sendto(reply, src)


if __name__ == "__main__":
    main()
