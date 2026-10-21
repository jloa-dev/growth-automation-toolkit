import subprocess
import json

repos = [
    'tscircuit/core',
    'tscircuit/circuit-json-to-gerber',
    'tscircuit/circuit-json-to-kicad',
    'tscircuit/tscircuit-autorouter',
    'tscircuit/footprinter',
    'tscircuit/math-utils',
    'tscircuit/schematic-symbols',
    'tscircuit/props',
    'tscircuit/soup',
    'tscircuit/pcb-viewer',
    'tscircuit/circuit-to-svg',
    'tscircuit/circuit-json',
    'tscircuit/tscircuit',
    'tscircuit/calculate-cell-boundaries',
    'tscircuit/soup-util',
    'tscircuit/graphics-debug'
]

uncontested = []

for repo in repos:
    try:
        cmd = ['gh', 'issue', 'list', '--repo', repo, '--state', 'open', '--limit', '40', '--json', 'number,title,comments,labels,assignees,url']
        issues = json.loads(subprocess.check_output(cmd, encoding='utf-8'))
        for iss in issues:
            if iss.get('assignees'):
                continue
            num = iss['number']
            title = iss['title']
            
            # Check PRs
            pr_cmd = ['gh', 'pr', 'list', '--repo', repo, '--search', str(num), '--json', 'number,state']
            prs = json.loads(subprocess.check_output(pr_cmd, encoding='utf-8'))
            open_prs = [p for p in prs if p.get('state') == 'OPEN']
            if len(open_prs) == 0:
                print(f"FOUND 0-PR ISSUE: [{repo}] #{num}: {title}")
                uncontested.append({
                    'repo': repo,
                    'number': num,
                    'title': title,
                    'url': iss['url'],
                    'comments': len(iss.get('comments', []))
                })
                if len(uncontested) >= 20:
                    break
        if len(uncontested) >= 20:
            break
    except Exception as e:
        print(f"Error checking {repo}: {e}")

print("\n--- FINAL UNCONTESTED 0-PR CANDIDATES ---")
for u in uncontested:
    print(f"[{u['repo']}] #{u['number']} ({u['comments']} comm): {u['title']}")
