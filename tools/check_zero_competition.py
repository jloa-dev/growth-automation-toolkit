import subprocess
import json

cmd = ['gh', 'issue', 'list', '--repo', 'Expensify/App', '--state', 'open', '--limit', '100', '--search', 'is:issue is:open label:External', '--json', 'number,title,comments,labels,createdAt']
res = subprocess.run(cmd, capture_output=True, text=True)
if res.returncode == 0:
    issues = json.loads(res.stdout)
    zero_proposals = []
    for iss in issues:
        comments = iss.get('comments', [])
        props = []
        for c in comments:
            b = c.get('body', '').lower()
            author = c.get('author', {}).get('login', '')
            if ('proposal' in b or 'root cause' in b) and author not in ['melvin-bot', 'github-actions', 'MelvinBot', 'OSBotify']:
                props.append(author)
        props = list(set([p for p in props if p != 'jloa-dev']))
        labels = [l.get('name', '') for l in iss.get('labels', [])]
        num = iss.get('number')
        title = iss.get('title')
        dt = iss.get('createdAt')
        
        # Check if already assigned or under review or closed
        is_assigned = any('Reviewing' in l for l in labels)
        is_help_wanted = any('Help Wanted' in l for l in labels)
        
        item = {
            'number': num,
            'title': title,
            'props': props,
            'count': len(props),
            'labels': labels,
            'date': dt[:10],
            'is_help_wanted': is_help_wanted,
            'is_assigned': is_assigned
        }
        if len(props) == 0:
            zero_proposals.append(item)

    print(f"=== TOTAL OPEN EXTERNAL ISSUES CON 0 RIVALES: {len(zero_proposals)} ===")
    for x in zero_proposals:
        stat = "HELP WANTED" if x['is_help_wanted'] else ("REVIEWING" if x['is_assigned'] else "PENDING TRIAGE")
        print(f"#{x['number']} [{x['date']}] [{stat}]: {x['title']}")
