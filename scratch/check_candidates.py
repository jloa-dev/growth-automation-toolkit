import subprocess
import json

issues = [104501, 104502, 104505, 104503, 104461, 104515, 104388, 104494, 104396, 104425, 104390]
for num in issues:
    cmd = ['gh', 'issue', 'view', str(num), '--repo', 'Expensify/App', '--json', 'title,state,assignees,labels,body,comments']
    res = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8')
    if res.returncode == 0:
        data = json.loads(res.stdout)
        title = data.get('title')
        state = data.get('state')
        body = data.get('body', '')
        labels = [l['name'] for l in data.get('labels', [])]
        assignees = [a['login'] for a in data.get('assignees', [])]
        comments = data.get('comments', [])
        
        # Check proposals
        proposal_authors = set()
        for c in comments:
            b = c.get('body', '').lower()
            author = c.get('author', {}).get('login', '')
            if '## proposal' in b or '# proposal' in b:
                proposal_authors.add(author)
                
        has_upwork = 'upwork.com' in body
        # Extract Upwork URL
        upwork_url = ""
        for line in body.splitlines():
            if 'upwork.com' in line:
                upwork_url = line.strip()
                break
                
        print(f"#{num} | state={state} | upwork={has_upwork} | proposals={len(proposal_authors)} authors={list(proposal_authors)} | assignees={assignees} | help_wanted={'Help Wanted' in labels}")
        if upwork_url:
            print(f"   URL: {upwork_url}")
