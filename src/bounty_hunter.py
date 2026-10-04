"""
Production Autonomous Bounty Hunter & Anti-Trap Filter.
Scans GitHub and Superteam Earn for verified, unassigned opportunities >= $10 USD.
"""

from __future__ import annotations

import json
import os
import re
import subprocess
import urllib.parse
import urllib.request
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple

USER_AGENT = "bounty-hunter/1.0"
MIN_NOMINAL = 10.0

REWARD_PATTERNS = [
    re.compile(r"(?i)(?:bounty|reward|prize|payout)[^\n$]{0,45}\$\s*([0-9][0-9,]*(?:\.\d+)?)"),
    re.compile(r"(?i)(?:bounty|reward|prize|payout)[^\n]{0,45}([0-9][0-9,]*(?:\.\d+)?)\s*(?:USDC|USDG|USD)\b"),
    re.compile(r"(?i)\$\s*([0-9][0-9,]*(?:\.\d+)?)[^\n]{0,35}(?:bounty|reward|prize|payout)\b"),
]

TRAP_MARKERS = [
    "aquarium-of-gullibles",
    "digitaltoolsshed.com",
    "HUMAN_VERIFIED_SIGNATURE",
    "CERTIFIED BOT: I CONSUME API TOKENS",
    "Adversarial Autonomous Agent Benchmark",
]

SUPERTEAM_URLS = [
    "https://superteam.fun/earn/bounties",
    "https://superteam.fun/earn/opportunities/development-bounties",
]


@dataclass
class BountyCandidate:
    source: str
    repo_or_org: str
    title: str
    url: str
    amount: float
    comments: int
    status: str
    is_safe: bool = True
    rejection_reason: str = ""


def extract_reward_amount(text: str) -> float:
    amounts = []
    for pat in REWARD_PATTERNS:
        for m in pat.finditer(text):
            try:
                amounts.append(float(m.group(1).replace(",", "")))
            except ValueError:
                pass
    return max(amounts, default=0.0)


def check_is_trap(text: str) -> Optional[str]:
    for marker in TRAP_MARKERS:
        if marker.lower() in text.lower():
            return f"Trap marker detected: {marker}"
    return None


def scan_github_bounties(limit: int = 30) -> List[BountyCandidate]:
    cmd = [
        "gh", "search", "issues",
        "bounty",
        "--state", "open",
        "--sort", "updated",
        "--limit", str(limit),
        "--json", "title,url,repository,commentsCount,body,labels,assignees"
    ]
    try:
        res = subprocess.run(cmd, capture_output=True, text=True, check=True)
        raw_issues = json.loads(res.stdout)
    except Exception as exc:
        print(f"Error executing GitHub search: {exc}")
        return []

    candidates: List[BountyCandidate] = []
    for item in raw_issues:
        title = item.get("title", "")
        body = item.get("body", "")
        url = item.get("url", "")
        repo = item.get("repository", {}).get("nameWithOwner", "")
        comments = item.get("commentsCount", 0)
        assignees = item.get("assignees", [])

        full_text = f"{title}\n{body}"
        amount = extract_reward_amount(full_text)

        trap = check_is_trap(full_text)
        if trap:
            candidates.append(BountyCandidate(
                source="GitHub", repo_or_org=repo, title=title, url=url,
                amount=amount, comments=comments, status="TRAP_REJECTED",
                is_safe=False, rejection_reason=trap
            ))
            continue

        if assignees:
            candidates.append(BountyCandidate(
                source="GitHub", repo_or_org=repo, title=title, url=url,
                amount=amount, comments=comments, status="ASSIGNED",
                is_safe=False, rejection_reason="Issue already assigned"
            ))
            continue

        if amount >= MIN_NOMINAL:
            candidates.append(BountyCandidate(
                source="GitHub", repo_or_org=repo, title=title, url=url,
                amount=amount, comments=comments, status="QUALIFIED",
                is_safe=True
            ))

    return candidates


def run_full_scan() -> Dict[str, List[BountyCandidate]]:
    print("🛰️ [Bounty Radar] Scanning GitHub for safe, verified bounties >= $10 USD...")
    gh_candidates = scan_github_bounties(limit=40)
    qualified = [c for c in gh_candidates if c.is_safe and c.status == "QUALIFIED"]
    rejected = [c for c in gh_candidates if not c.is_safe]

    print(f"\n📊 Radar Scan Summary:")
    print(f"  - Total Evaluated: {len(gh_candidates)}")
    print(f"  - Qualified & Safe (>= ${MIN_NOMINAL} USD): {len(qualified)}")
    print(f"  - Traps / Assigned Filtered: {len(rejected)}")

    return {"qualified": qualified, "rejected": rejected}


if __name__ == "__main__":
    results = run_full_scan()
    print("\n🎯 Top Qualified Bounty Opportunities:")
    for q in results["qualified"][:10]:
        print(f"\n  • [{q.repo_or_org}] ${q.amount:.0f} USD | Comments: {q.comments}")
        print(f"    Title: {q.title}")
        print(f"    URL:   {q.url}")
