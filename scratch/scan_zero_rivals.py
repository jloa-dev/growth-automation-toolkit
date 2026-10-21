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
    'tscircuit/infoplist-json',
    'tscircuit/graphics-debug'
]

results = []
for repo in repos:
    try:
        cmd = ['gh', 'issue', 'list', '--repo', repo, '--state', 'open', '--limit', '30', '--json', 'number,title,comments,labels,assignees,url']
        out = subprocess.check_output(cmd, encoding='utf-8')
        issues = json.loads(out)
        for iss in issues:
            if iss.get('assignees'):
                continue
            comments_count = len(iss.get('comments', []))
            labels = [l['name'] for l in iss.get('labels', [])]
            results.append({
                'repo': repo,
                'number': iss['number'],
                'title': iss['title'],
                'comments': comments_count,
                'labels': labels,
                'url': iss['url']
            })
    except Exception as e:
        pass

results.sort(key=lambda x: x['comments'])
print(f"Total candidate issues found: {len(results)}")
for r in results[:40]:
    repo = r['repo']
    num = r['number']
    comm = r['comments']
    title = r['title']
    print(f"[{repo}] #{num} ({comm} comments): {title}")
