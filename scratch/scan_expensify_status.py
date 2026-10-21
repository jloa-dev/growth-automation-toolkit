import re
import json
import subprocess
from concurrent.futures import ThreadPoolExecutor

with open('TASK_LEDGER.md', 'r', encoding='utf-8') as f:
    text = f.read()

issues = sorted(list(set(re.findall(r'https://github\.com/Expensify/App/issues/(\d+)', text))), key=lambda x: int(x))
print(f'Total Expensify issues in TASK_LEDGER: {len(issues)}')

def check_issue(iss):
    res = subprocess.run(['gh', 'issue', 'view', iss, '--repo', 'Expensify/App', '--json', 'state,assignees,title,labels,comments'], capture_output=True, text=True)
    if res.returncode == 0:
        d = json.loads(res.stdout)
        comments = d.get('comments', [])
        
        # Check C+ review
        c_plus_reviewers = []
        c_plus_selected = None
        has_jloa = False
        last_comment = comments[-1] if comments else {}
        
        for c in comments:
            author = c.get('author', {}).get('login', '')
            body = c.get('body', '')
            if 'jloa-dev' in author or 'loa464' in author or 'jloa' in body:
                has_jloa = True
            if '🎀' in body and 'C+ reviewed' in body:
                c_plus_reviewers.append(author)
                # Check who is referenced in this comment
                c_plus_selected = body[:200]
                
        return {
            'num': iss,
            'state': d.get('state'),
            'assignees': [a.get('login') for a in d.get('assignees', [])],
            'title': d.get('title'),
            'has_jloa': has_jloa,
            'c_plus_reviewers': c_plus_reviewers,
            'c_plus_selected': c_plus_selected,
            'comments_count': len(comments),
            'last_comment_author': last_comment.get('author', {}).get('login', ''),
            'last_comment_date': last_comment.get('createdAt', '')
        }
    return None

results = []
with ThreadPoolExecutor(max_workers=10) as executor:
    for r in executor.map(check_issue, issues):
        if r:
            results.append(r)

results.sort(key=lambda x: int(x['num']))

with open('scratch/expensify_scan_results.json', 'w', encoding='utf-8') as f:
    json.dump(results, f, indent=2)

print(f'Successfully analyzed {len(results)} issues.')
