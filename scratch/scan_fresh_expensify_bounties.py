import json
import subprocess
import re
from datetime import datetime, timezone, timedelta

pet_offset = timezone(timedelta(hours=-5))

print("Fetching recent open issues from Expensify/App...")
cmd = [
    'gh', 'issue', 'list',
    '--repo', 'Expensify/App',
    '--state', 'open',
    '--limit', '100',
    '--json', 'number,title,createdAt,labels,assignees,url,comments'
]

res = subprocess.run(cmd, capture_output=True, text=True)
if res.returncode != 0:
    print("Error:", res.stderr)
    exit(1)

data = json.loads(res.stdout)
print(f"Total open issues retrieved: {len(data)}")

candidates = []

for item in data:
    num = item['number']
    title = item['title']
    assignees = [a.get('login') for a in item.get('assignees', [])]
    comments = item.get('comments', [])
    
    # 1. Must have a dollar bounty in title
    m_price = re.search(r'\$(\d+)', title)
    if not m_price:
        continue
    price = int(m_price.group(1))
    
    # Ignore payment summary / due for payment issues
    if any(k in title.lower() for k in ['due for payment', 'payment issue', 'deploy checklist', 'retest & close', 'deploy blocker']):
        continue
        
    # Check if jloa-dev already commented
    has_jloa = any('jloa' in c.get('author', {}).get('login', '').lower() for c in comments)
    if has_jloa:
        continue
        
    # Check if already assigned to a contributor (more than 1 assignee where one is a contributor with a PR)
    # Usually assignees has [Staff, C+] or [Staff, C+, Contributor]. If 3 assignees, it's often assigned.
    # Check if there is already a C+ approval "🎀" in comments
    c_plus_approved = any('🎀' in c.get('body', '') and 'c+ reviewed' in c.get('body', '').lower() for c in comments)
    if c_plus_approved:
        continue
        
    # Count proposals
    proposals = [c for c in comments if '## proposal' in c.get('body', '').lower()]
    prop_count = len(proposals)
    
    if prop_count > 4:
        # competition too high
        continue
        
    dt_utc = datetime.fromisoformat(item['createdAt'].replace('Z', '+00:00'))
    dt_pet = dt_utc.astimezone(pet_offset)
    
    candidates.append({
        'number': num,
        'title': title,
        'price': price,
        'proposals': prop_count,
        'assignees': assignees,
        'createdAt': dt_pet.strftime('%Y-%m-%d %H:%M'),
        'url': item['url']
    })

candidates.sort(key=lambda x: (x['proposals'], -x['number']))

print(f"\nFound {len(candidates)} high-potential viable issues with verified escrow:")
for c in candidates[:15]:
    print(f"#{c['number']} [${c['price']}] (Props: {c['proposals']}) | {c['createdAt']} | {c['title'][:70]}")

with open('scratch/viable_candidates.json', 'w', encoding='utf-8') as f:
    json.dump(candidates, f, indent=2)
