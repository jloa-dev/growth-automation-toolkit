## What changed

Adds the `action-items -> Excel workbook (.xlsx)` recipe to `sdks/python-cli/examples/`:
- `sdks/python-cli/examples/action_items_xlsx.md`: step-by-step recipe guide for exporting action items to an Excel workbook with native cell types.
- `sdks/python-cli/examples/action_items_to_xlsx.py`: converter script using `openpyxl` with native UTC datetime formatting, formula injection defense, auto-fit columns, and freeze panes.
- `sdks/python-cli/tests/test_action_items_to_xlsx.py`: 7 focused hermetic unit tests.
- `sdks/python-cli/examples/README.md`: discovery index entry (+2 lines).

## Product Invariants & Security
- **Native Excel Types**: `due_at`, `created_at`, and `updated_at` are converted to naive UTC datetimes with format `yyyy-mm-dd hh:mm:ss`.
- **Formula Injection Mitigation**: Text cells explicitly set `cell.data_type = 's'`, ensuring that values starting with `=`, `+`, `-`, or `@` remain literal strings and cannot be evaluated as spreadsheet formulas.
- **Atomic File Writing**: Writes via `.partial` file before calling `os.replace`, with automatic cleanup on failure.
- **Path Traversal Protection**: Rejects paths containing `..`.
- **Auto-fit Columns & Usability**: Computes column width dynamically with padding up to 60 characters and locks the top header row with `freeze_panes = "A2"`.

## Triple Validation
1. **Unit Tests**: `python -m unittest tests.test_action_items_to_xlsx -v` -> 7/7 tests pass (0.132s).
2. **Static Compilation**: `python -m py_compile examples/action_items_to_xlsx.py tests/test_action_items_to_xlsx.py` -> clean.
3. **Runtime Simulation**: Verified end-to-end with synthetic JSON payloads, validating sheet title, explicit string types, and datetime formatting.

**Bounty Proposal**: $25 developer recipe bounty via Algora.
**PayPal**: `jloa.dev@gmail.com`
