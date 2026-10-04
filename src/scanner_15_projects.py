import subprocess
import json
import re

queries = [
    'label:bounty state:open sort:updated',
    'is:issue is:open "bounty" sort:updated',
    'is:issue is:open label:"help wanted" sort:updated',
]

seen_repos = set()
results = []
bad_markers = ['bounty-plaza', 'gullibles', 'bountyscout', 'relayhop', 'test-']

for q in queries:
    cmd = ['gh', 'search', 'issues', q, '--limit', '40', '--json', 'number,title,repository,url,body,labels,commentsCount']
    try:
        res = subprocess.run(cmd, capture_output=True, text=True, check=True)
        items = json.loads(res.stdout)
        for it in items:
            repo = it.get('repository', {}).get('nameWithOwner', '')
            if not repo or repo in seen_repos:
                continue
            if any(m in repo.lower() for m in bad_markers):
                continue
            title = it.get('title', '')
            url = it.get('url', '')
            comments = it.get('commentsCount', 0)
            body = it.get('body', '')[:300].replace('\n', ' ')
            
            seen_repos.add(repo)
            results.append({
                'repo': repo,
                'number': it.get('number'),
                'title': title,
                'url': url,
                'comments': comments,
                'summary': body[:120]
            })
            if len(results) >= 20:
                break
    except Exception as e:
        print(f"Error on query {q}: {e}")
    if len(results) >= 20:
        break

print(f"Total qualified distinct projects found: {len(results)}\n")
for i, r in enumerate(results[:15], 1):
    print(f"{i}. [{r['repo']}] #{r['number']}: {r['title']}")
    print(f"   URL: {r['url']}")
    print(f"   Summary: {r['summary']}\n")
