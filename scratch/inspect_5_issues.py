import json
import subprocess

for num in ['103593', '103488', '103726', '103898', '103764']:
    res = subprocess.run(['gh', 'issue', 'view', num, '--repo', 'Expensify/App', '--json', 'assignees,comments'], capture_output=True, text=True)
    d = json.loads(res.stdout)
    assignees = [a.get('login') for a in d.get('assignees', [])]
    print(f"=== #{num} Assignees: {assignees} ===")
    for c in d.get('comments', []):
        body = c.get('body', '')
        auth = c.get('author', {}).get('login')
        if any(w in body.lower() for w in ['assigned to', 'pull request', 'pr #', 'solution', 'c+ reviewed', 'proposal', 'deploy']):
            print(f"  [{auth}] {c.get('createdAt')}: {body[:140].replace(chr(10), ' ')}")
