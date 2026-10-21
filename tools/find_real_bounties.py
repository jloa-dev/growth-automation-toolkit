import subprocess
import json
import urllib.parse

def search_issues(query, per_page=15):
    encoded_query = urllib.parse.quote(query)
    cmd = ["gh", "api", f"search/issues?q={encoded_query}&sort=created&order=desc&per_page={per_page}"]
    res = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8")
    if res.returncode == 0:
        try:
            return json.loads(res.stdout).get("items", [])
        except Exception as e:
            return []
    return []

queries = [
    ("💎 Bounty Label", 'is:issue is:open label:"💎 Bounty"'),
    ("Bounty Label Open", 'is:issue is:open label:bounty comments:<5 -org:SecureBananaLabs -org:Faizal97 -org:Ikalus1988'),
    ("Polar Bounties Open", 'is:issue is:open "polar.sh" comments:<5'),
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
