import json
import subprocess

issues = ['103671', '103593', '103488', '103726', '103898', '103944', '103345', '103764', '103775']

for num in issues:
    res = subprocess.run(['gh', 'issue', 'view', num, '--repo', 'Expensify/App', '--json', 'assignees,comments'], capture_output=True, text=True)
    if res.returncode == 0:
        d = json.loads(res.stdout)
        assignees = [a.get('login') for a in d.get('assignees', [])]
        comments = d.get('comments', [])
        
        print(f"=================== #{num} ===================")
        print(f"Assignees: {assignees}")
        
        # Look for the comment that assigned or decided the winner
        for c in comments:
            b = c.get('body', '')
            author = c.get('author', {}).get('login')
            if any(k in b.lower() for k in ['assigned to', 'trigger assignment', 'proposal lgtm', '🎀', 'hire', 'contract', 'approved']):
                print(f"Decision/Review comment by {author} at {c.get('createdAt')}:")
                print(b[:250].replace('\n', ' '))
                print('---')
