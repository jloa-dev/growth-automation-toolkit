import subprocess
import tempfile
import json
import sqlite3
from pathlib import Path

# Create synthetic data
test_memories = [
    {
        'id': 'mem_live_101',
        'content': 'Discussed deploying autonomous agents with supervisor patterns and strict budget constraints',
        'category': 'work',
        'tags': ['ai', 'deployment', 'agents'],
        'created_at': '2026-10-04T18:00:00Z',
    },
    {
        'id': 'mem_live_102',
        'content': 'Need to buy specialized ceramic coffee filters and light roast beans',
        'category': 'lifestyle',
        'tags': ['shopping', 'coffee'],
        'created_at': '2026-10-04T19:30:00Z',
    },
]

with tempfile.TemporaryDirectory() as td:
    in_json = Path(td) / 'memories.json'
    out_db = Path(td) / 'test_vault.sqlite'
    in_json.write_text(json.dumps(test_memories), encoding='utf-8')

    # Execute CLI script
    cmd = ['python', 'examples/memories_to_sqlite.py', str(in_json), '--db', str(out_db)]
    res = subprocess.run(cmd, capture_output=True, text=True, cwd='c:/Users/Loa/Downloads/GOAL/omi_repo/sdks/python-cli')
    assert res.returncode == 0, f'CLI failed: {res.stderr}'
    print('CLI Output:', res.stdout.strip())

    # Verify SQLite DB
    conn = sqlite3.connect(str(out_db))
    cur = conn.cursor()

    cur.execute("SELECT count(*) FROM memories")
    assert cur.fetchone()[0] == 2, 'Row count mismatch!'

    # Verify FTS5 query
    cur.execute("SELECT m.id, m.content FROM memories m JOIN memories_fts f ON m.rowid = f.rowid WHERE memories_fts MATCH 'autonomous'")
    row = cur.fetchone()
    assert row is not None and row[0] == 'mem_live_101', 'FTS5 match failed!'
    print(f"FTS5 Query Match Verified: {row[0]} -> '{row[1][:40]}...'")

    conn.close()
    print('Task 2 Validation 3: PASSED 100% SUCCESS!')
