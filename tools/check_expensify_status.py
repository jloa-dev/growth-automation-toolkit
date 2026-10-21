import subprocess
import json

issues = [102525, 103345, 103349, 103324]
for num in issues:
    cmd = ['gh', 'issue', 'view', str(num), '-R', 'Expensify/App', '--json', 'title,state,assignees,comments']
    res = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8')
    if res.returncode == 0:
        data = json.loads(res.stdout)
        comms = data.get('comments', [])
        assignees = [a.get('login') for a in data.get('assignees', [])]
        latest = comms[-1] if comms else {}
        print(f"=== Issue #{num}: {data.get('title')} ===")
        print(f"State: {data.get('state')} | Assignees: {assignees} | Total comments: {len(comms)}")
        if latest:
            print(f"Latest comment by @{latest.get('author', {}).get('login')} at {latest.get('createdAt')}:")
            snippet = latest.get('body', '')[:200].replace('\n', ' ')
            print(f"  {snippet}")
        print()
    else:
        print(f"Error viewing #{num}:", res.stderr)
