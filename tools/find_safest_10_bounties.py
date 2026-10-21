import subprocess
import json
import re

def get_gh_json(cmd):
    res = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8")
    if res.returncode == 0 and res.stdout.strip():
        try:
            return json.loads(res.stdout)
        except Exception:
            return None
    return None

def scan_expensify_safe_bounties():
    print("=== SCANNING EXPENSIFY SAFE HELP WANTED ISSUES ===")
    # Search open issues with "Help Wanted" label and [$175] or [$250]
    query = 'repo:Expensify/App is:issue is:open label:"Help Wanted" -label:CFI -label:Internal'
    cmd = ['gh', 'issue', 'list', '-R', 'Expensify/App', '--search', query, '--limit', '40', '--json', 'number,title,createdAt,labels,comments']
    data = get_gh_json(cmd) or []
    print(f"Total Help Wanted issues returned: {len(data)}")

    safe_issues = []
    for it in data:
        num = it['number']
        title = it['title']
        created = it['createdAt'][:10]
        labels = [l['name'] for l in it.get('labels', [])]

        if 'CFI' in labels or 'Internal' in labels or 'Engineering' in labels:
            continue

        # fetch comments
        cmd_c = ['gh', 'api', f'repos/Expensify/App/issues/{num}/comments?per_page=100']
        comments = get_gh_json(cmd_c) or []

        has_upwork = False
        assigned_c_plus = None
        human_proposals = []
        is_assigned_to_someone = False

        for c in comments:
            u = c.get('user', {}).get('login', '')
            b = c.get('body', '')

            if 'Job added to Upwork:' in b:
                has_upwork = True
            if 'Triggered auto assignment to Contributor-plus' in b:
                m = re.search(r'@([a-zA-Z0-9_\-]+)', b)
                if m:
                    assigned_c_plus = m.group(1)
            if 'has been assigned to this issue' in b or 'Assigned to contributor' in b or 'assigned to @' in b:
                is_assigned_to_someone = True

            if ('## Proposal' in b or '### Proposal' in b) and u not in ['MelvinBot', 'melvin-bot']:
                human_proposals.append(u)

        # Check bounty amount
        m_amt = re.search(r'\[\$(\d+)\]', title)
        bounty_val = f"${m_amt.group(1)} USD" if m_amt else "Unknown"

        if has_upwork and not is_assigned_to_someone:
            safe_issues.append({
                'num': num,
                'title': title,
                'bounty': bounty_val,
                'created': created,
                'c_plus': assigned_c_plus,
                'proposals': human_proposals,
                'prop_count': len(human_proposals),
                'labels': labels
            })

    safe_issues.sort(key=lambda x: (x['prop_count'], x['created']), reverse=False)
    return safe_issues

def scan_tscircuit_issues():
    print("\n=== SCANNING TSCIRCUIT BOUNTIES / ISSUES ===")
    repos = ['tscircuit/core', 'tscircuit/footprinter', 'tscircuit/schematic-symbols', 'tscircuit/pcb-viewer', 'tscircuit/circuit-json']
    tsc_issues = []
    for r in repos:
        cmd = ['gh', 'issue', 'list', '-R', r, '--state', 'open', '--limit', '15', '--json', 'number,title,createdAt,labels,comments']
        data = get_gh_json(cmd) or []
        for it in data:
            num = it['number']
            title = it['title']
            created = it['createdAt'][:10]
            labels = [l['name'] for l in it.get('labels', [])]

            # Check if there is an open PR closing it
            cmd_pr = ['gh', 'api', f'repos/{r}/issues/{num}/timeline?per_page=30']
            timeline = get_gh_json(cmd_pr) or []
            has_pr = False
            for event in timeline:
                if event.get('event') == 'cross-referenced':
                    source = event.get('source', {}).get('issue', {})
                    if source.get('pull_request'):
                        has_pr = True
                        break

            if not has_pr:
                tsc_issues.append({
                    'repo': r,
                    'num': num,
                    'title': title,
                    'created': created,
                    'labels': labels
                })
    return tsc_issues

if __name__ == '__main__':
    exp = scan_expensify_safe_bounties()
    print(f"\nSafe Expensify issues ({len(exp)}):")
    for e in exp[:15]:
        print(f"#{e['num']} ({e['bounty']}) | C+: {e['c_plus']} | Props ({e['prop_count']}): {e['proposals']} | {e['title']}")

    tsc = scan_tscircuit_issues()
    print(f"\ntscircuit open issues with 0 PRs ({len(tsc)}):")
    for t in tsc[:15]:
        print(f"{t['repo']}#{t['num']} | {t['title']} | Labels: {t['labels']}")
