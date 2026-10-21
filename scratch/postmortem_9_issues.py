import json
import subprocess

issues = ['103671', '103593', '103488', '103726', '103898', '103944', '103345', '103764', '103775']

for num in issues:
    res = subprocess.run(['gh', 'issue', 'view', num, '--repo', 'Expensify/App', '--json', 'title,createdAt,assignees,comments'], capture_output=True, text=True)
    if res.returncode == 0:
        d = json.loads(res.stdout)
        created_at = d.get('createdAt')
        assignees = [a.get('login') for a in d.get('assignees', [])]
        comments = d.get('comments', [])
        
        jloa_comments = [c for c in comments if any(k in c.get('author', {}).get('login', '').lower() for k in ['jloa', 'loa464'])]
        c_plus_comments = [c for c in comments if '🎀' in c.get('body', '') and 'C+' in c.get('body', '')]
        
        print('=============================================')
        print(f"ISSUE #{num}: {d.get('title')}")
        print(f"Created: {created_at} | Assignees: {assignees}")
        print(f"jloa-dev comments: {len(jloa_comments)}")
        for jc in jloa_comments:
            print(f"  jloa-dev at {jc.get('createdAt')}")
        print(f"C+ comments: {len(c_plus_comments)}")
        for cpc in c_plus_comments:
            author = cpc.get('author', {}).get('login')
            dt = cpc.get('createdAt')
            body = cpc.get('body', '').strip().replace('\n', ' ')[:250]
            print(f"  C+ [{author}] at {dt}: {body}")
        
        # Check when the winner posted proposal
        # Find comments by the assignee who is not staff
        for c in comments:
            auth = c.get('author', {}).get('login', '')
            if auth in assignees and '## Proposal' in c.get('body', ''):
                print(f"  Winner [{auth}] proposal at: {c.get('createdAt')}")
