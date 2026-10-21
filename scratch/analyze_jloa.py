import json

with open('scratch/expensify_scan_results.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

jloa_issues = [d for d in data if d.get('has_jloa')]
print(f'Total issues scanned: {len(data)}')
print(f'Issues where jloa-dev is present: {len(jloa_issues)}')

open_jloa = [d for d in jloa_issues if d['state'] == 'OPEN']
closed_jloa = [d for d in jloa_issues if d['state'] == 'CLOSED']

print(f'\n--- OPEN ISSUES ({len(open_jloa)}) ---')
for d in open_jloa:
    c_note = (d.get('c_plus_selected') or '').strip().replace('\n', ' ')[:100]
    print(f"#{d['num']} | Assignees: {d['assignees']} | C+: {d['c_plus_reviewers']} | Title: {d['title'][:60]}")
    if c_note:
        print(f"   Note: {c_note}")

print(f'\n--- CLOSED ISSUES ({len(closed_jloa)}) ---')
for d in closed_jloa:
    print(f"#{d['num']} | Assignees: {d['assignees']} | Title: {d['title'][:60]}")
