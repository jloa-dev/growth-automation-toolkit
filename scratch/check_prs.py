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
    ("tscircuit/circuit-json-to-kicad", 506),
]

for repo, num in candidates:
    # check if any PR has "401" or closes #401
    out = subprocess.check_output(["gh", "pr", "list", "--repo", repo, "--search", f"{num}", "--json", "number,title,url,state"], encoding="utf-8")
    prs = json.loads(out)
    if prs:
        print(f"PR exists for [{repo} #{num}]: {prs}")
    else:
        print(f"ZERO PRs for [{repo} #{num}] - 100% UNCONTESTED")
