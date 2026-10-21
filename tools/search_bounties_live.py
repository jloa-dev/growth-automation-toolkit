import subprocess
import json
import urllib.parse
import sys

def search_issues(query, per_page=10):
    encoded_query = urllib.parse.quote(query)
    cmd = ["gh", "api", f"search/issues?q={encoded_query}&sort=created&order=desc&per_page={per_page}"]
    res = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8")
    if res.returncode == 0:
        try:
            return json.loads(res.stdout).get("items", [])
        except Exception as e:
            return []
    return []

if __name__ == "__main__":
    queries = [
        ("Algora Bot", 'is:issue is:open "bounty of $" "algora"'),
        ("Algora App", 'is:issue is:open "app/algora"'),
        ("Polar Bounties", 'is:issue is:open "polar.sh" "$/"'),
        ("Opire Rewards", 'is:issue is:open "opire/reward"'),
        ("Bounty label funded", 'is:issue is:open label:bounty "$"')
    ]

    for label, q in queries:
        print(f"\n=== {label} ===")
        items = search_issues(q, per_page=10)
        for it in items:
            repo = it.get("repository_url", "").replace("https://api.github.com/repos/", "")
            num = it.get("number")
            title = it.get("title")
            comments = it.get("comments")
            url = it.get("html_url")
            labels = [l.get("name") for l in it.get("labels", [])]
            print(f"- [{repo}#{num}] ({comments} comms): {title}")
            print(f"  URL: {url}")
            print(f"  Labels: {labels}")
