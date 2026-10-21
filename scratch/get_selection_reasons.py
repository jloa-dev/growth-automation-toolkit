import json
import subprocess

issues = ['103671', '103593', '103488', '103726', '103898', '103944', '103345', '103764', '103775']

for num in issues:
    res = subprocess.run(['gh', 'issue', 'view', num, '--repo', 'Expensify/App', '--json', 'assignees,comments'], capture_output=True, text=True)
    if res.returncode == 0:
        d = json.loads(res.stdout)
        assignees = [a.get('login') for a in d.get('assignees', [])]
        comments = d.get('comments', [])
        print(f"\n=================== #{num} Assignees: {assignees} ===================")
        for c in comments:
            b = c.get('body', '')
            author = c.get('author', {}).get('login')
            if any(k in b.lower() for k in ['hired', 'assigned to @', 'assigning', 'selected', 'proposal is selected', '🎀']):
                print(f"[{author}] ({c.get('createdAt')}): {b[:200].replace(chr(10), ' ')}")
