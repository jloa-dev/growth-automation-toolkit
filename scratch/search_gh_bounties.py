import subprocess
import json

queries = [
    'label:bounty is:open state:open sort:created-desc',
    'bounty in:title is:open state:open sort:created-desc',
    '"$100" OR "$50" OR "$200" OR "$500" in:title is:open state:open label:bounty sort:created-desc',
    'algora in:comments is:open state:open sort:created-desc',
    'opire in:comments is:open state:open sort:created-desc',
]

for q in queries:
    print(f"=== Query: {q} ===")
    cmd = ['gh', 'search', 'issues', q, '--limit', '10', '--json', 'title,url,repository,commentsCount,createdAt']
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode == 0:
        try:
            items = json.loads(res.stdout)
            for it in items:
                print(f"[{it['repository']['nameWithOwner']}] #{it['url'].split('/')[-1]} (comments: {it['commentsCount']}, created: {it['createdAt']})")
                print(f"  Title: {it['title']}")
                print(f"  URL: {it['url']}")
        except Exception as e:
            print("Error parsing json:", e)
    else:
        print("Error:", res.stderr)
