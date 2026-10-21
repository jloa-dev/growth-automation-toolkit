## What changed

Adds the `action-items -> CSV` conversion recipe to `sdks/python-cli/examples/`:
- `sdks/python-cli/examples/action_items_csv.md`: step-by-step recipe guide for exporting open or all tasks to spreadsheet-ready CSV.
- `sdks/python-cli/examples/action_items_to_csv.py`: standalone converter script using only Python standard library (`csv`, `json`, `datetime`, `tempfile`, `pathlib`).
- `sdks/python-cli/tests/test_action_items_to_csv.py`: 9 focused hermetic unit tests.
- `sdks/python-cli/examples/README.md`: discovery index entry (+2 lines).

## Product Invariants & Security
- **No external dependencies**: Pure Python 3.10+ stdlib.
- **Formula Injection Defense**: Escapes values prefixed with `=`, `+`, `-`, `@`, `\t`, `\r` with a leading single quote (`'`) to guard against DDE execution in Excel and Google Sheets.
- **Atomic write**: Writes to a temporary file before `os.replace`, preventing partially written files.
- **Path Traversal Protection**: Rejects output paths containing `..`.
- **RFC 4180 compliant**: Standard Windows CRLF (`\r\n`) row terminators and optional UTF-8 BOM (`--excel`).

## Triple Validation
1. **Unit Tests**: `python -m unittest tests.test_action_items_to_csv -v` -> 9/9 tests pass (0.055s).
2. **Static Compilation**: `python -m py_compile examples/action_items_to_csv.py tests/test_action_items_to_csv.py` -> clean.
3. **Runtime Simulation**: Verified end-to-end with synthetic JSON payloads, validating output columns and formula sanitization.

**Bounty Proposal**: $25 developer recipe bounty via Algora.
**PayPal**: `jloa.dev@gmail.com`
