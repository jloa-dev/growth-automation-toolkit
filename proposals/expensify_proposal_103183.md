Contributor details
Your Expensify account email: jloa.dev@gmail.com
Upwork Profile Link: https://www.upwork.com/freelancers/~0163955a2ba22190aa

## Proposal

### Please re-state the problem that we are trying to solve in this issue.
When a tag containing an escaped colon sequence like `Parent\: Child` (literal backslash followed by a colon) is selected on a transaction, the tag is erroneously truncated and saved as `Parent\\` instead of `Parent\: Child`.

### What is the root cause of that problem?

1. **Incomplete escaping in `escapeTagName` (`src/libs/PolicyUtils/tag.ts:259-261`)**:
   Currently, `escapeTagName` only escapes colons:
   ```typescript
   function escapeTagName(tag: string) {
       return tag?.replaceAll(CONST.COLON, '\\:');
   }
   ```
   When an admin inputs `Parent\: Child`:
   - `tag` contains a backslash followed by a colon (`\:`).
   - `escapeTagName` replaces the `:` with `\:`, producing `Parent\\: Child`.

2. **Colon-splitting interference in `getTagArrayFromName` (`src/libs/TransactionUtils/index.ts:882-905`)**:
   When parsing the tag string to determine multi-level parts, `getTagArrayFromName` runs:
   ```typescript
   const tagWithoutDoubleSlashes = tagName.replaceAll('\\\\', '☠');
   const tagWithoutEscapedColons = tagWithoutDoubleSlashes.replaceAll('\\:', '☢');
   const matches = tagWithoutEscapedColons.split(':');
   ```
   Tracing `Parent\\: Child`:
   - Step 1: `replaceAll('\\\\', '☠')` replaces the double backslash `\\` with placeholder `☠`. This results in `Parent☠: Child`.
   - Step 2: `replaceAll('\\:', '☢')` looks for `\:`. Because the preceding backslash was consumed into `☠`, the subsequent colon is left unescaped: `Parent☠: Child`.
   - Step 3: `split(':')` splits on the colon, incorrectly breaking the single tag into two parts: `['Parent☠', ' Child']`.
   - Step 4: Restoring `☠` $\to$ `\\\\` produces `['Parent\\\\', ' Child']`.
   On a single-tag policy or 1-level transaction, only the first part (`Parent\\`) is assigned to the transaction, causing the truncation bug.

3. **Incomplete unescaping in `getCleanedTagName` (`src/libs/PolicyUtils/tag.ts:202-204`)**:
   ```typescript
   function getCleanedTagName(tag: string) {
       return Str.htmlDecode(tag?.replaceAll('\\:', CONST.COLON) ?? '');
   }
   ```
   `getCleanedTagName` only unescapes `\:`, but does not unescape `\\`.

### What changes do you think we should make in order to solve the problem?

1. **Escape backslashes before colons in `escapeTagName`**:
   In `src/libs/PolicyUtils/tag.ts`:
   ```typescript
   function escapeTagName(tag: string) {
       return tag?.replaceAll('\\', '\\\\').replaceAll(CONST.COLON, '\\:');
   }
   ```
   With this change:
   - Input `Parent\: Child` becomes `Parent\\\: Child`.
   - In `getTagArrayFromName`:
     - `\\\\` $\to$ `☠` produces `Parent☠\: Child`.
     - `\:` $\to$ `☢` produces `Parent☠☢ Child`.
     - `split(':')` leaves it intact as a single token `['Parent☠☢ Child']`.
     - Restoring placeholders produces `['Parent\\\: Child']`.

2. **Unescape colons then backslashes in `getCleanedTagName`**:
   In `src/libs/PolicyUtils/tag.ts`:
   ```typescript
   function getCleanedTagName(tag: string) {
       return Str.htmlDecode(tag?.replaceAll('\\:', CONST.COLON).replaceAll('\\\\', '\\') ?? '');
   }
   ```
   *(Alternatively, using a single regex replacement: `tag?.replace(/\\([\\:])/g, '$1')`).*
   Unescaping `\:` before `\\` ensures that `Parent\\\: Child` correctly decodes back to the original `Parent\: Child`.

3. **Leave `getTagArrayFromName` unchanged**:
   `getTagArrayFromName` already follows `TransactionUtils.php` and correctly handles `\\\\` and `\\:`. Maintaining this ensures 100% parity with backend tag parsing and does not break existing unit tests.

### What alternative solutions did you explore? (Optional)

- **Swapping replacement order inside `getTagArrayFromName`**:
  Changing `getTagArrayFromName` to replace `\:` before `\\\\` breaks existing test case at `TransactionUtilsTest.ts:5403` (`tag1\\:name:tag2`) and causes divergence with backend `TransactionUtils.php`. Escaping backslashes at source in `escapeTagName` preserves parser invariants and solves the issue cleanly without regressions.

### What specific scenarios should we cover in automated tests?
In `tests/unit/PolicyUtilsTest.ts` and `tests/unit/TransactionUtilsTest.ts`:
1. `escapeTagName('Parent\\: Child')` returns `'Parent\\\\\\: Child'`.
2. `getTagArrayFromName('Parent\\\\\\: Child')` returns `['Parent\\\\\\: Child']` (does not split).
3. `getCleanedTagName('Parent\\\\\\: Child')` returns `'Parent\\: Child'`.
4. Multi-level tags with escaped colons (`Level1\\: A:Level2`) continue splitting into `['Level1\\: A', 'Level2']`.
