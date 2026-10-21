import subprocess
import tempfile
import json
import csv
from pathlib import Path

# Create synthetic data
test_data = [
    {
        'id': 'act_live_1',
        'description': 'Prepare Q3 roadmap slides',
        'completed': False,
        'due_at': '2026-10-15T14:30:00Z',
        'created_at': '2026-10-01T10:00:00Z',
        'conversation_id': 'c1',
    },
    {
        'id': 'act_live_2',
        'description': '=1+2 potential formula injection',
        'completed': True,
        'due_at': None,
        'created_at': '2026-10-02T11:00:00Z',
        'conversation_id': 'c2',
    },
]

with tempfile.TemporaryDirectory() as td:
    in_json = Path(td) / 'input.json'
    out_csv = Path(td) / 'result.csv'
    in_json.write_text(json.dumps(test_data), encoding='utf-8')

    # Test file execution
    cmd = ['python', 'examples/action_items_to_csv.py', str(in_json), '-o', str(out_csv), '--excel']
    res = subprocess.run(cmd, capture_output=True, text=True, cwd='c:/Users/Loa/Downloads/GOAL/omi_repo/sdks/python-cli')
    assert res.returncode == 0, f'CLI failed: {res.stderr}'
    print('CLI Output:', res.stdout.strip())

    # Verify CSV content
    with open(out_csv, 'r', encoding='utf-8-sig', newline='') as f:
        reader = list(csv.DictReader(f))
        assert len(reader) == 2, f'Expected 2 rows, got {len(reader)}'
        assert reader[0]['id'] == 'act_live_1'
        assert reader[0]['completed'] == 'false'
        assert reader[0]['due_at'] == '2026-10-15 14:30:00'
        assert reader[1]['description'] == "'=1+2 potential formula injection", 'Formula injection not escaped!'
        print('Runtime verification 3: PASSED 100% SUCCESS!')
