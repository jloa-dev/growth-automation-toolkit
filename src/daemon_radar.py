"""
Daemon Background Radar.
Runs continuously, scanning for active bounties and updating live logs.
"""

from __future__ import annotations

import datetime as dt
import json
import subprocess
import time
from pathlib import Path

LOG_FILE = Path("radar_live.log")
PROGRESS_FILE = Path("progress.md")


def log(msg: str) -> None:
    timestamp = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    formatted = f"[{timestamp}] {msg}"
    print(formatted, flush=True)
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(formatted + "\n")


def scan_once() -> int:
    cmd = [
        "gh", "search", "issues",
        "bounty",
        "--state", "open",
        "--sort", "updated",
        "--limit", "15",
        "--json", "title,url,repository,commentsCount,updatedAt"
    ]
    try:
        res = subprocess.run(cmd, capture_output=True, text=True, check=True)
        issues = json.loads(res.stdout)
        log(f"🛰️ Radar Scan Completed: {len(issues)} open bounty issues monitored.")
        for iss in issues[:3]:
            repo = iss.get("repository", {}).get("nameWithOwner", "unknown")
            title = iss.get("title", "")[:60]
            log(f"   -> [{repo}] {title} ({iss.get('url')})")
        return len(issues)
    except Exception as exc:
        log(f"⚠️ Radar query error: {exc}")
        return 0


def main():
    log("🚀 [DAEMON RADAR INITIALIZED] Continuous bounty monitoring active.")
    iteration = 1
    while True:
        log(f"--- Cycle #{iteration} Starting ---")
        count = scan_once()
        log(f"--- Cycle #{iteration} Finished. Sleeping for 180s ---")
        iteration += 1
        time.sleep(180)


if __name__ == "__main__":
    main()
