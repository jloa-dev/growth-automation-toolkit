import json

with open("scratch/viable_candidates.json", "r") as f:
    cand = json.load(f)

for i, c in enumerate(cand):
    print(f"{i+1}. #{c['number']} [${c['price']}] (Props: {c['proposals']}) | {c['title'][:75]}")
