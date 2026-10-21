import subprocess
import json

candidates = [
    ("tscircuit/circuit-json-to-kicad", 401),
    ("tscircuit/circuit-json-to-kicad", 533),
    ("tscircuit/circuit-json-to-kicad", 403),
    ("tscircuit/circuit-json-to-kicad", 585),
    ("tscircuit/circuit-json-to-gerber", 155),
    ("tscircuit/circuit-json-to-gerber", 169),
    ("tscircuit/core", 3982),
    ("tscircuit/core", 3732),
    ("tscircuit/core", 4154),
    ("tscircuit/footprinter", 871), # already fixed or open?
    ("tscircuit/circuit-json-to-kicad", 506),
]

for repo, num in candidates:
    try:
        out = subprocess.check_output(["gh", "issue", "view", str(num), "--repo", repo, "--json", "title,comments,state"], encoding="utf-8")
        data = json.loads(out)
        comm_count = len(data.get("comments", []))
        print(f"[{repo} #{num}] state={data['state']} comments={comm_count} title={data['title']}")
        if comm_count > 0:
            for c in data['comments']:
                print(f"   -> by {c['author']['login']}: {c['body'][:80].replace(chr(10), ' ')}")
    except Exception as e:
        print(f"Error {repo} #{num}: {e}")
