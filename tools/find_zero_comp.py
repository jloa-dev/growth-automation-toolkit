import subprocess
import json

cmd = ['gh', 'issue', 'list', '--repo', 'Expensify/App', '--state', 'open', '--limit', '50', '--search', 'is:issue is:open label:External -label:Reviewing', '--json', 'number,title,comments,labels']
res = subprocess.run(cmd, capture_output=True, text=True)
if res.returncode == 0:
    issues = json.loads(res.stdout)
    zero_comp = []
    for iss in issues:
        comments = iss.get('comments', [])
        proposals = []
        for c in comments:
            b = c.get('body', '')
            author = c.get('author', {}).get('login', '')
            if 'proposal' in b.lower() and author not in ['melvin-bot', 'github-actions', 'MelvinBot']:
                proposals.append(author)
        unique_proposers = list(set([p for p in proposals if p != 'jloa-dev']))
        if len(unique_proposers) == 0:
            zero_comp.append({
                'number': iss.get('number'),
                'title': iss.get('title'),
                'comments_count': len(comments)
            })
    print(f"=== TOTAL CON 0 COMPETIDORES ENCONTRADOS: {len(zero_comp)} ===")
    for z in zero_comp:
        print(f"#{z['number']}: {z['title']} (Coms: {z['comments_count']})")
