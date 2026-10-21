## What changed

Adds the `memories -> SQLite` database recipe to `sdks/python-cli/examples/`:
- `sdks/python-cli/examples/memories_sqlite.md`: step-by-step recipe guide for importing memories, facts, and learnings into a local SQLite database with Full-Text Search (FTS5).
- `sdks/python-cli/examples/memories_to_sqlite.py`: standalone importer script using only Python standard library (`sqlite3`, `json`, `datetime`, `pathlib`).
- `sdks/python-cli/tests/test_memories_to_sqlite.py`: 8 focused hermetic unit tests.
- `sdks/python-cli/examples/README.md`: discovery index entry (+1 line).

## Features & Product Invariants
- **Full-Text Search (FTS5)**: Automatically configures an FTS5 virtual table and synchronization triggers (`AFTER INSERT`, `AFTER DELETE`, `AFTER UPDATE`) for fast keyword querying across personal memories.
- **Idempotent Merging**: Uses `INSERT OR REPLACE` so multi-page exports can be safely imported without duplicate entries.
- **Surrogate Pair Defense**: Sanitizes lone surrogate characters (`\ud800`) to prevent SQLite `UnicodeEncodeError`.
- **Path Traversal Protection**: Rejects destination paths containing `..`.
- **File Integrity Validation**: Confirms SQLite 3 magic byte header on existing databases.
- **No External Dependencies**: Pure Python 3.10+ standard library.

## Triple Validation
1. **Unit Tests**: `python -m unittest tests.test_memories_to_sqlite -v` -> 8/8 tests pass (0.150s).
2. **Static Compilation**: `python -m py_compile examples/memories_to_sqlite.py tests/test_memories_to_sqlite.py` -> clean.
3. **Runtime Simulation**: Verified end-to-end with real SQLite database creation, inserting memories, and executing FTS5 MATCH queries.

**Bounty Proposal**: $25 developer recipe bounty via Algora.
**PayPal**: `jloa.dev@gmail.com`
