import subprocess
import json
import sys

def search_github(query, limit=20):
    cmd = [
        "gh", "search", "issues",
        query,
        "--state", "open",
        "--sort", "updated",
        "--limit", str(limit),
        "--json", "title,url,repository,body,commentsCount,updatedAt,labels"
    ]
    try:
        res = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return json.loads(res.stdout)
    except Exception as e:
        print(f"Error querying '{query}': {e}")
        return []

queries = [
    'bounty "algora.io" is:open',
    'bounty "polar.sh" is:open',
    'label:bounty is:open is:issue',
    '"bounty" "$" is:open is:issue'
]

print("Starting deep bounty search...")
found = {}
for q in queries:
    print(f"\n--- Query: {q} ---")
    results = search_github(q, limit=15)
    print(f"Found {len(results)} issues.")
    for item in results:
        url = item['url']
        if url not in found:
            found[url] = item

print(f"\nTotal unique issues found: {len(found)}")

# Analyze and print issues that have escrow or clear reward
for url, iss in found.items():
    repo = iss.get('repository', {}).get('nameWithOwner', '')
    title = iss.get('title', '')
    body = iss.get('body', '') or ''
    labels = [l.get('name', '') for l in iss.get('labels', [])]
    
    # Filter out discussions, bots, noise
    if any(k in repo.lower() for k in ['test', 'spam', 'bounty-plaza', 'demo']):
        continue
        
    print(f"\n[REPO] {repo}")
    print(f"[TITLE] {title}")
    print(f"[URL] {url}")
    print(f"[LABELS] {', '.join(labels)}")
    # Print snippet of body
    lines = [line.strip() for line in body.splitlines() if line.strip()]
    snippet = " | ".join(lines[:3])[:200]
    print(f"[BODY] {snippet}")
