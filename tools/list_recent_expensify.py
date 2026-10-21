import subprocess
import json

cmd = ['gh', 'issue', 'list', '-R', 'Expensify/App', '--limit', '50', '--json', 'number,title,createdAt,labels,comments']
res = subprocess.run(cmd, capture_output=True, text=True)
issues = json.loads(res.stdout)
for it in issues:
    labels = [l['name'] for l in it['labels']]
    c = it['comments']
    c_count = c if isinstance(c, int) else (len(c) if isinstance(c, list) else 0)
    print(f"#{it['number']} | {it['createdAt'][:10]} | Comms: {c_count} | {labels} | {it['title']}")
