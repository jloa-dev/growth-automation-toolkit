import subprocess
import json
import re

# Fetch open issues in Expensify/App with label External
cmd = ['gh', 'issue', 'list', '--repo', 'Expensify/App', '--state', 'open', '--limit', '100', '--search', 'is:issue is:open label:External', '--json', 'number,title,comments,labels,createdAt,body']
res = subprocess.run(cmd, capture_output=True, text=True)

candidates = []

if res.returncode == 0:
    issues = json.loads(res.stdout)
    for iss in issues:
        title = iss.get('title', '')
        num = iss.get('number')
        comments = iss.get('comments', [])
        labels = [l.get('name', '') for l in iss.get('labels', [])]
        body = iss.get('body', '')
        
        # Check if already resolved/closed
        if 'due for payment' in title.lower():
            continue
            
        # Check price tag
        price_match = re.search(r'\[\$(\d+)\]', title)
        price = price_match.group(1) if price_match else None
        
        # Check upwork job
        has_upwork = 'upwork.com/jobs' in body.lower() or any('upwork.com/jobs' in c.get('body', '').lower() for c in comments)
        
        # Count proposals
        proposals = []
        already_submitted = False
        for c in comments:
            b = c.get('body', '')
            author = c.get('author', {}).get('login', '')
            if author == 'jloa-dev':
                already_submitted = True
            if ('## proposal' in b.lower() or '### proposal' in b.lower() or 'proposal\n' in b.lower()) and author not in ['melvin-bot', 'github-actions', 'MelvinBot', 'OSBotify']:
                proposals.append(author)
                
        unique_proposers = list(set([p for p in proposals if p != 'jloa-dev']))
        comp_count = len(unique_proposers)
        
        if not already_submitted and price is not None:
            candidates.append({
                'number': num,
                'title': title,
                'price': price,
                'comp_count': comp_count,
                'competitors': unique_proposers,
                'has_upwork': has_upwork,
                'createdAt': iss.get('createdAt', '')[:10],
                'labels': labels
            })

# Sort by comp_count ascending, then by price descending, then by date descending
candidates.sort(key=lambda x: (x['comp_count'], -int(x['price']), x['createdAt']), reverse=False)

print(f"Total candidate issues without jloa-dev proposal: {len(candidates)}")
print("=== TOP 20 CANDIDATES ===")
for c in candidates[:20]:
    print(f"#{c['number']} [${c['price']}] [Comp: {c['comp_count']}] [{c['createdAt']}] Upwork: {c['has_upwork']} -> {c['title']}")
