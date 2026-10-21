import json
import subprocess

with open('scratch/viable_candidates.json', 'r', encoding='utf-8') as f:
    candidates = json.load(f)

for c in candidates[:10]:
    num = c['number']
    res = subprocess.run(['gh', 'issue', 'view', str(num), '--repo', 'Expensify/App', '--json', 'title,body,comments,url'], capture_output=True, text=True)
    if res.returncode == 0:
        d = json.loads(res.stdout)
        print(f"==================================================")
        print(f"ISSUE #{num}: {d['title']}")
        print(f"URL: {d['url']}")
        # print first 500 chars of body
        print("BODY PREVIEW:")
        print(d['body'][:600])
        print("COMMENTS COUNT:", len(d['comments']))
        for cm in d['comments']:
            author = cm.get('author', {}).get('login', '')
            print(f"  Comment by {author} at {cm.get('createdAt')}")
        print()
