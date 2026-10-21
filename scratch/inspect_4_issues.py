import subprocess
import json

for num in [104515, 104461, 104494, 104396]:
    cmd = ['gh', 'issue', 'view', str(num), '--repo', 'Expensify/App', '--json', 'title,labels,comments']
    res = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8')
    data = json.loads(res.stdout)
    labels = [l['name'] for l in data.get('labels', [])]
    comments = data.get('comments', [])
    print(f"=== #{num}: {data['title']} ===")
    print('Labels:', labels)
    print('Comments count:', len(comments))
    for c in comments[-3:]:
        print(f"  [{c['author']['login']}] {c['body'][:200]}...")
