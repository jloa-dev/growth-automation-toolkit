import subprocess
import json
import re

issues = [104050, 104048, 104045, 104039, 103993, 103965, 103957]

for num in issues:
    cmd = ['gh', 'api', f'repos/Expensify/App/issues/{num}']
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        continue
    iss = json.loads(res.stdout)
    title = iss['title']
    body = iss['body']
    
    # get comments
    cmd_c = ['gh', 'api', f'repos/Expensify/App/issues/{num}/comments']
    res_c = subprocess.run(cmd_c, capture_output=True, text=True)
    comms = json.loads(res_c.stdout) if res_c.returncode == 0 else []
    
    proposals = []
    c_plus = None
    upwork_link = None
    
    for c in comms:
        u = c.get('user', {}).get('login', '')
        b = c.get('body', '')
        if 'Triggered auto assignment to Contributor-plus' in b:
            m = re.search(r'@([a-zA-Z0-9_\-]+)', b)
            if m: c_plus = m.group(1)
        if 'Job added to Upwork:' in b:
            m = re.search(r'https://www\.upwork\.com/jobs/[^\s]+', b)
            if m: upwork_link = m.group(0)
        if ('## Proposal' in b or '### Proposal' in b) and u not in ['MelvinBot', 'melvin-bot']:
            proposals.append(u)
            
    print(f"\n==========================================")
    print(f"ISSUE #{num}: {title}")
    print(f"C+: {c_plus} | Upwork: {upwork_link}")
    print(f"Proposals ({len(proposals)}): {proposals}")
    
    # print description snippet
    print("--- Problem Description ---")
    desc_lines = [l for l in body.splitlines() if l.strip() and not l.startswith('<!--')][:10]
    print("\n".join(desc_lines[:6]))
