import subprocess
import json

cmd = ['gh', 'search', 'prs', 'bounty in:title is:merged', '--limit', '25', '--sort', 'updated', '--json', 'title,url,repository,closedAt,author']
res = subprocess.run(cmd, capture_output=True, text=True)
if res.returncode == 0:
    items = json.loads(res.stdout)
    print(f"Found {len(items)} merged bounty PRs:")
    for it in items:
        print(f"[{it['repository']['nameWithOwner']}] #{it['url'].split('/')[-1]} - {it['title']} (closed: {it['closedAt']}, by: {it['author']['login']})")
else:
    print("Error:", res.stderr)
