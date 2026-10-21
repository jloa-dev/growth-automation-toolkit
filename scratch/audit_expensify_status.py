import json

with open('scratch/expensify_scan_results.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

deployed_competitors = []
active_open = []
closed = []

for d in data:
    st = d.get('state')
    title = d.get('title', '')
    if st == 'CLOSED':
        closed.append(d)
    elif 'due for payment' in title.lower():
        deployed_competitors.append(d)
    else:
        active_open.append(d)

print(f'Total issues: {len(data)}')
print(f'1. Cerrados definitivamente: {len(closed)}')
print(f'2. En fase final de 7 dias (desplegados por terceros): {len(deployed_competitors)}')
print(f'3. Abiertos en proceso de revision / triage: {len(active_open)}')

print('\n=== EN FASE FINAL DE 7 DIAS (Desplegados / Próximos a Cobro de Terceros) ===')
for d in deployed_competitors:
    print(f"#{d['num']} | Asignados: {d['assignees']} | {d['title']}")

# Let's inspect the active_open to find which ones have our proposals and who is currently favored
print('\n=== ABIERTOS CON CANDIDATURA / DISCUSIÓN ACTIVA ===')
shortlist = []
for d in active_open:
    # Check if there is a C+ reviewer
    c_rev = d.get('c_plus_reviewers', [])
    assignees = d.get('assignees', [])
    num = d.get('num')
    note = (d.get('c_plus_selected') or '').replace('\n', ' ')[:80]
    if c_rev or len(assignees) >= 2:
        shortlist.append(d)
        print(f"#{num} | Assignees: {assignees} | C+: {c_rev}")
        if note:
            print(f"    Note: {note}")

print(f'\nTotal con revisión o C+ activo: {len(shortlist)}')
