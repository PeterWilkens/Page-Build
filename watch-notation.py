#!/usr/bin/env python3
"""
Watch source/ch-four-chord-grids.ptx and run update-notation.py whenever it changes.

Usage:
    python3 watch-notation.py
"""

from __future__ import annotations

import subprocess
import sys
import time
from pathlib import Path

PROJECT = Path(__file__).parent
WATCH_FILE = PROJECT / "source" / "ch-four-chord-grids.ptx"
UPDATE_SCRIPT = PROJECT / "update-notation.py"

POLL_SECONDS = 1.0
DEBOUNCE_SECONDS = 0.75


def run_update() -> int:
    print("[watch] Running update-notation.py ...", flush=True)
    result = subprocess.run([sys.executable, str(UPDATE_SCRIPT)], cwd=PROJECT)
    if result.returncode == 0:
        print("[watch] Update complete.", flush=True)
    else:
        print(f"[watch] Update failed (exit {result.returncode}).", flush=True)
    return result.returncode


def main() -> int:
    if not WATCH_FILE.exists():
        print(f"[watch] File not found: {WATCH_FILE}", flush=True)
        return 1

    print(f"[watch] Watching: {WATCH_FILE}", flush=True)
    print("[watch] Save ch-four-chord-grids.ptx to regenerate notation.", flush=True)
    print("[watch] Press Ctrl+C to stop.", flush=True)

    try:
        last_mtime = WATCH_FILE.stat().st_mtime
    except OSError as exc:
        print(f"[watch] Could not stat watch file: {exc}", flush=True)
        return 1

    pending_since = None

    while True:
        try:
            current_mtime = WATCH_FILE.stat().st_mtime
        except OSError as exc:
            print(f"[watch] Could not stat watch file: {exc}", flush=True)
            time.sleep(POLL_SECONDS)
            continue

        if current_mtime != last_mtime:
            last_mtime = current_mtime
            pending_since = time.monotonic()

        if pending_since is not None and (time.monotonic() - pending_since) >= DEBOUNCE_SECONDS:
            pending_since = None
            run_update()

        time.sleep(POLL_SECONDS)


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except KeyboardInterrupt:
        print("\n[watch] Stopped.", flush=True)
        raise SystemExit(0)
