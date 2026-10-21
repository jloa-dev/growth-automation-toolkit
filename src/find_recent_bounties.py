import subprocess
import json

cmd = [
    "gh", "search", "issues",
    "label:bounty is:issue is:open",
    "--sort", "created",
    "--limit", "30",
    "--json", "number,title,url,repository,labels,body,commentsCount,createdAt"
]

res = subprocess.run(cmd, capture_output=True, text=True)
data = json.loads(res.stdout)
print(f"Total found: {len(data)}")

for item in data:
    repo = item['repository']['nameWithOwner']
    labels = [l['name'] for l in item.get('labels', [])]
    # Filter out known spam / farming
    if any(s in repo.lower() for s in ['banana', 'bounty-plaza', 'spam', 'farm', 'test']):
        continue
    print(f"\n[{repo}] #{item['number']}: {item['title']}")
    print(f"URL: {item['url']}")
    print(f"Labels: {labels}")
    print(f"Created: {item.get('createdAt')}")
    body_first_line = (item.get('body') or '').splitlines()
    body_snippet = body_first_line[0] if body_first_line else ""
    print(f"Snippet: {body_snippet[:150]}")
