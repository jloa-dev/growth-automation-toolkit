import subprocess
import json

issue_nums = [
    103898, 103876, 103875, 103863, 103838, 103831, 103824, 103822,
    103726, 103721, 103624, 103622, 103619, 103578, 103576, 103560,
    103514, 103491, 103480, 103478
]

results = []

for num in issue_nums:
    cmd = ['gh', 'issue', 'view', str(num), '--repo', 'Expensify/App', '--json', 'number,title,comments,labels,state']
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode == 0:
        data = json.loads(res.stdout)
        comments = data.get('comments', [])
        labels = [l.get('name') for l in data.get('labels', [])]
        props = []
        has_jloa = False
        for c in comments:
            author = c.get('author', {}).get('login', '')
            body = c.get('body', '').lower()
            if author == 'jloa-dev':
                has_jloa = True
            if ('## proposal' in body or 'proposal\n' in body or 'root cause' in body) and author not in ['melvin-bot', 'github-actions', 'MelvinBot', 'OSBotify', 'applause-bot']:
                props.append(author)
        unique_props = list(set([p for p in props if p != 'jloa-dev']))
        results.append({
            'num': num,
            'title': data.get('title'),
            'comp_count': len(unique_props),
            'competitors': unique_props,
            'has_jloa': has_jloa,
            'labels': labels,
            'state': data.get('state')
        })

print("=== COMPETITION AUDIT OF CANDIDATES ===")
# Sort by comp_count ascending
results.sort(key=lambda x: (x['has_jloa'], x['comp_count']))
for r in results:
    jloa_str = "[YA ENVIADO]" if r['has_jloa'] else "[DISPONIBLE]"
    print(f"#{r['num']}: {jloa_str} Comp: {r['comp_count']} ({', '.join(r['competitors']) if r['competitors'] else '0 rivales'}) | {r['title']}")
