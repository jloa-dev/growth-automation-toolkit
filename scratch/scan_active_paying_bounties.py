import subprocess
import json

cmd = ['gh', 'issue', 'list', '--repo', 'Expensify/App', '--state', 'open', '--limit', '100', '--json', 'number,title,labels,assignees,createdAt,comments']
res = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8')
issues = json.loads(res.stdout)

viable = []
for issue in issues:
    num = issue['number']
    title = issue['title']
    labels = [l['name'] for l in issue.get('labels', [])]
    assignees = [a['login'] for a in issue.get('assignees', [])]
    
    # Check if there's a PR linked or Melvin PR
    cmd_body = ['gh', 'issue', 'view', str(num), '--repo', 'Expensify/App', '--json', 'body,comments']
    res_b = subprocess.run(cmd_body, capture_output=True, text=True, encoding='utf-8')
    data = json.loads(res_b.stdout)
    body = data.get('body', '')
    comments = data.get('comments', [])
    
    # Upwork check
    if 'upwork.com' not in body:
        continue
    
    # Check if Melvin created a PR or someone was hired
    has_pr = False
    is_hired = False
    for c in comments:
        b = c.get('body', '').lower()
        if 'draft pr created' in b or 'hired on upwork' in b or 'assigned to contributor' in b:
            has_pr = True
            break
            
    if has_pr:
        continue
        
    # Count proposals
    proposals = []
    for c in comments:
        b = c.get('body', '').lower()
        author = c.get('author', {}).get('login', '')
        if ('## proposal' in b or '# proposal' in b) and author not in ['melvin-bot', 'MelvinBot', 'github-actions', 'applause-bot']:
            proposals.append(author)
            
    # Upwork URL
    upwork_url = ""
    for line in body.splitlines():
        if 'upwork.com' in line:
            upwork_url = line.strip()
            break
            
    viable.append({
        'number': num,
        'title': title,
        'proposals': len(set(proposals)),
        'proposal_authors': list(set(proposals)),
        'labels': labels,
        'upwork_url': upwork_url,
        'createdAt': issue['createdAt']
    })

print(f"Total viable: {len(viable)}")
for v in viable[:15]:
    print(f"#{v['number']} ({v['proposals']} props) - {v['title'][:60]}")
    print(f"   URL: {v['upwork_url']}")
with open('scratch/active_paying_bounties.json', 'w') as f:
    json.dump(viable, f, indent=2)
