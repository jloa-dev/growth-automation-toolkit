"""
Automated GitHub Bounty Scanner & Quality Filter.
Finds active open bounty issues with low competition using GitHub CLI.
"""

from __future__ import annotations

import json
import subprocess
import sys
from typing import Dict, List


def run_gh_search(query: str, limit: int = 20) -> List[Dict]:
    cmd = [
        "gh", "search", "issues", query,
        "--state", "open",
        "--sort", "created",
        "--limit", str(limit),
        "--json", "title,url,repository,commentsCount,createdAt"
    ]
    try:
        res = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return json.loads(res.stdout)
    except Exception as exc:
        print(f"Error querying GitHub CLI: {exc}", file=sys.stderr)
        return []


def scan_uncontested_bounties() -> List[Dict]:
    print("🔍 [Bounty Scanner] Querying GitHub for active bounties with low competition...")
    raw_issues = run_gh_search("bounty", limit=30)
    viable = []

    for item in raw_issues:
        comments = item.get("commentsCount", 0)
        title = item.get("title", "")
        # Filter for low friction: 3 or fewer comments, clearly indicated bounty
        if comments <= 3:
            viable.append({
                "repo": item["repository"]["nameWithOwner"],
                "title": title,
                "url": item["url"],
                "comments": comments,
                "created_at": item["createdAt"],
            })

    return viable


def main() -> None:
    opportunities = scan_uncontested_bounties()
    print(f"\n🎯 Found {len(opportunities)} low-competition bounty opportunities:\n")
    for opp in opportunities[:10]:
        print(f"- [{opp['repo']}] {opp['title']}")
        print(f"  URL: {opp['url']} (Comments: {opp['comments']}, Created: {opp['created_at']})\n")


if __name__ == "__main__":
    main()
