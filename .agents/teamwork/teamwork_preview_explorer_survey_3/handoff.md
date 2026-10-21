# Handoff Report: Codebase & Test Infrastructure Assessment

## 1. Observation

### 1.1 Local Expensify/App Repository Location and Git State
- **Filesystem Path**: `c:\Users\Loa\Downloads\GOAL\expensify_app`
- **Working Tree Cleanliness**:
  Command executed: `git status` in `c:\Users\Loa\Downloads\GOAL\expensify_app`
  Verbatim output:
  ```
  On branch fix/104500-agent-fallback-avatar-in-thread
  nothing to commit, working tree clean
  ```
- **Current Branch**: `fix/104500-agent-fallback-avatar-in-thread`
- **Current HEAD Commit**: `4c358bdd3ee` ("fix: sanitize childOldestFourAccountIDs so thread preview displays processing agent avatar")
- **Merge Base Commit**: `1712396aeb4` ("Merge pull request #104369 from software-mansion-labs/@OlGierd03/Insights-Wrong-Tooltip-Position-After-Rotating")
- **Configured Remotes**:
  Command executed: `git remote -v`
  Verbatim output:
  ```
  origin	https://github.com/jloa-dev/App.git (fetch)
  origin	https://github.com/jloa-dev/App.git (push)
  upstream	https://github.com/Expensify/App.git (fetch)
  upstream	https://github.com/Expensify/App.git (push)
  ```
- **Local Feature Branches**: Over 45 active branches tracking historical and recent issues, including:
  `fix/102683-company-card-nicknames-spend-filter`, `fix/102730-ecard-feed-selector-admin-check`, `fix/102734-member-security-unlock-pending-ui`, `fix/102792-submitted-report-violation-rbr`, `fix/102868-export-todo-connection-exporter`, `fix/103058-member-role-optimistic-account-id`, `fix/103183-tag-escaping`, `fix/103198-unassign-card-warning-clarification`, `fix/103240-duplicate-key-search-filter`, `fix/103245-agent-page-copilot-loading`, `fix/103307-gusto-custom-approval-mode`, `fix/103341-company-card-reimbursable-toggle`, `fix/103345-contact-method-percent-crash`, `fix/103355-expense-members-filter-threshold`, `fix/103403-offline-nav-arrows`, `fix/103406-archived-cards`, `fix/103488-gps-distance-intl`, `fix/103492-archived-workspace-rbr`, `fix/103497-composer-empty-height`, `fix/103531-ios-carousel-rotation`, `fix/103533-concierge-preview-rhp-dimensions`, `fix/103538-bank-nickname-refresh`, `fix/103648-pinch-zoom-max-clamp`, `fix/103662-native-share-oversized-file`, `fix/103663-negative-tax-amount-field`, `fix/103664-create-negative-tax-amount`, `fix/103671-merge-offline-negative-tax`, `fix/103775-search-bulk-actions-undefined-data`, `fix/103777-sentry-navigation-crash-filter`, `fix/103908-inaccessible-preview-navigation`, `fix/104113-scan-amount-offline-scanning`, `fix/104138-receipt-preview-resize-mode`, `fix/104147-optimistic-search-filter-match`, `fix/104161-split-bill-details-search-base-route`, `fix/104162-report-field-non-reimbursable`, `fix/104165-bank-account-address-street2`, `fix/104218-qbd-manual-sync-force-refresh`, `fix/104221-workspace-card-view-transactions-scope`, `fix/104500-agent-fallback-avatar-in-thread`, `main`.

### 1.2 Local Verification Tools & Environment State
- **Runtimes & Package Managers**:
  - Node.js: `v24.16.0` (`C:\Program Files\nodejs\node.exe`)
  - npm: `11.13.0` (`C:\Program Files\nodejs\npm.ps1`)
  - Bun: `1.4.2` (`C:\Users\Loa\AppData\Roaming\npm\bun.ps1`)
  - Python: `3.12.15` (`C:\Program Files\Python312\python.exe`)
  - Git: `2.51.1.1` (`C:\Program Files\Git\cmd\git.exe`)
  - Yarn: Not installed / Not in PATH (`Get-Command yarn` returned not found).
  - Global `tsc`: Not installed / Not in PATH.
- **Node Modules & Package Lock**:
  - `expensify_app/package.json` version: `9.5.15-1`.
  - `expensify_app/package-lock.json`: Exists.
  - `expensify_app/node_modules`: **Does not exist** (`Test-Path node_modules` returned `False`).
  - Bun package cache: `C:\Users\Loa\.bun\install\cache` contains ~2.9 GB of cached packages.
- **Verification Tool Execution Tests**:
  - Running `bun test ./tests/unit/StringUtilsTest.ts`:
    Verbatim output:
    ```
    error: Cannot find package 'expensify-common' from 'C:\Users\Loa\Downloads\GOAL\expensify_app\src\libs\StringUtils\index.ts'
    0 pass, 1 fail, 1 error
    ```
  - Running `bun scripts/typecheck.ts`:
    Requires `node_modules/typescript/bin/tsc` (line 26 of `scripts/typecheck.ts`: `const tsc = \`${projectRoot}/node_modules/typescript/bin/tsc\`;`) and `import CLI from 'expensify-common/CLI'` (line 17). Cannot run without `node_modules`.
  - Running `npm test` (Jest):
    `package.json` line 47 defines `"test": "TZ=utc NODE_OPTIONS=\"--experimental-vm-modules --max_old_space_size=8192\" jest"`, which resolves to local `node_modules/.bin/jest` and is unavailable without `node_modules`.
  - Python Verification Suite:
    Python 3.12.15 scripts in root `c:\Users\Loa\Downloads\GOAL` (`test_tag_escaping.py`, `analyze_competitors.py`, `audit_*.py`, `check_*.py`) execute directly and reliably without external dependencies.

### 1.3 Key Architectural Modules Touched by Open Issues
Inspection of `c:\Users\Loa\Downloads\GOAL\expensify_app\src` revealed the following core architecture:
1. **Onyx State & Reactive Hooks**:
   - `src/ONYXKEYS.ts` (120,214 bytes, 1,328+ lines) defines all key namespaces.
   - `src/hooks/useOnyx.ts` (lines 1-109) wraps `react-native-onyx` with search snapshot resolution (`getKeyData`, `getDataByPath`) and handles OXC React Compiler constraints (lines 50-57: "OXC's React Compiler currently fails to compile a hook when a generic type cast referencing the hook's own type parameters appears inside a nested closure").
   - `src/libs/actions/OnyxUpdates.ts`, `src/libs/actions/OnyxDerived/`, `src/libs/actions/QueuedOnyxUpdates.ts`: Manage optimistic state writes, server rollbacks, and offline update queues.
2. **Report Actions & IOU Life Cycle**:
   - `src/libs/actions/Report/index.ts` (388,859 bytes): Core engine for report creation, message posting, optimistic updates, and thread hierarchy.
   - `src/libs/ReportUtils.ts`, `src/libs/IOUUtils.ts`: Contain Red Brick Road (RBR) violation evaluation (`hasReportViolations`, `getReportRBRStatus`), invoice vs expense handling, and currency formatting.
3. **Navigation & Deep Linking**:
   - `src/libs/Navigation/Navigation.ts` (58,210 bytes), `NavigationRoot.tsx`, `OnyxTabNavigator.tsx`.
   - `src/ROUTES.ts` (317,283 bytes), `src/SCREENS.ts` (83,668 bytes).
   - Right Hand Panel (RHP) stack transitions and search base route contexts (`shouldSkipDeepLinkNavigation.ts`, `saveLastRoute/`, `processReportIDDeeplink/`).
4. **Virtualized Lists & Performance**:
   - `src/components/SelectionList/`: The primary list abstraction.
   - `src/components/FlashList/` & `src/components/LegendList/`: High-performance list wrappers built over `@shopify/flash-list` and `@legendapp/list`.
   - `src/libs/memoize/`: Centralized caching and memoization layer (`cache/`, `const.ts`, `stats.ts`, `types.ts`).
5. **Search Query Engine**:
   - `src/libs/SearchParser/searchParser.peggy`, `autocompleteParser.peggy`: Grammars compiled to JS for query parsing (`group-by:`, `status:`, `merchant:`, `type:`).
   - `src/libs/actions/Search.ts` (120,973 bytes): Handles client-side and server-side search querying, table column structures, and filter state.
6. **Policy, Workspaces & Cards**:
   - `src/libs/actions/Policy/`, `src/libs/actions/CompanyCards.ts` (58,058 bytes), `src/libs/CardUtils.ts` (117,150 bytes): Workspace administration, feed assignment checks (`isPolicyAdmin`), company card spend filters, and bank account setups.

### 1.4 Verification Script Examples
- `c:\Users\Loa\Downloads\GOAL\test_tag_escaping.py`: Tests tag escaping (`\:` vs `\\`) demonstrating current flaw vs fixed behavior for issue #103183.
- `c:\Users\Loa\Downloads\GOAL\analyze_competitors.py`: Extracts C+ reviews and human proposals via GitHub CLI (`gh issue view ...`).

---

## 2. Logic Chain

1. **Local Repository Identification**:
   - Observation 1.1 confirms that `c:\Users\Loa\Downloads\GOAL\expensify_app` is a complete Git clone of Expensify/App, containing valid remotes for `origin` (`jloa-dev/App`) and `upstream` (`Expensify/App`).
   - The working tree is clean and positioned at commit `4c358bdd3ee` on branch `fix/104500-agent-fallback-avatar-in-thread`.

2. **Verification Tooling Constraints**:
   - Observation 1.2 shows that Node.js 24, npm 11, Bun 1.4.2, and Python 3.12 are installed on the host.
   - However, `expensify_app/node_modules` does not exist on disk.
   - Attempting to invoke `bun test` fails immediately with module resolution errors (`Cannot find package 'expensify-common'`), and `bun scripts/typecheck.ts` depends directly on `node_modules/typescript/bin/tsc`.
   - Under the read-only exploration boundary ("Do NOT modify source code or run destructive commands"), running `npm install` or `bun install` is impermissible because it downloads gigabytes of packages, modifies lockfiles, and triggers postinstall build scripts.
   - Therefore, automated regression checks cannot rely on running `npm test` or `bun scripts/typecheck.ts` directly within `expensify_app` during this exploration phase.

3. **Viable Methodology for Checking Competitor Proposals**:
   - Step 2 rules out full in-tree Jest runs, but does NOT prevent rigorous verification.
   - As demonstrated by `test_tag_escaping.py` (Observation 1.4), core logic algorithms (parsing, validation, data transformation, regex, string manipulation, formatting) can be extracted and verified hermetically via standalone Python or Bun scripts with zero side effects.
   - For UI/architectural proposals, exact source inspection against `src/` (e.g. `useOnyx.ts`, `ReportUtils.ts`, `Navigation.ts`) enables verification of competitor edge cases:
     - Missing null/undefined guards on Onyx collections.
     - FlashList memoization breaks or React Compiler bails.
     - Incomplete navigation route hierarchies causing 404/"It's not here" screens.
     - Missing Red Brick Road (RBR) badge updates for unhandled report statuses.
   - For syntax and patch validity, `git apply --check <patch>` provides an in-memory, zero-side-effect test to prove whether a rival's diff is stale or corrupted against HEAD.

---

## 3. Caveats

1. **`node_modules` Absence**: Full Jest test suites and TypeScript project-wide checks (`tsc --build`) cannot be run until `npm install` is executed in an authorized implementation step.
2. **Platform-Specific Runtimes**: Native iOS/Android builds cannot be executed locally without Android SDK / Xcode toolchains, meaning native bridge behavior must be analyzed via TypeScript/Java/Kotlin source inspection and documented Expensify platform conventions.
3. **No Code Modification Undertaken**: In strict compliance with read-only exploration rules, no files in `expensify_app` were altered.

---

## 4. Conclusion

1. **Repository Readiness**: `c:\Users\Loa\Downloads\GOAL\expensify_app` is fully ready for deep code inspection. It is on branch `fix/104500-agent-fallback-avatar-in-thread` at commit `4c358bdd3ee` with a clean working tree and access to all upstream master/main changes.
2. **Adversary Verification Strategy**:
   - **Primary**: Direct source cross-examination against the 6 core architectural modules (`useOnyx`, `ReportActions`, `Navigation`, `FlashList/SelectionList`, `SearchParser`, `Policy/CardUtils`).
   - **Secondary**: Standalone hermetic reproduction scripts (Python / isolated Bun) to test and expose algorithmic, regex, and edge-case flaws in competitor proposals (matching the proven pattern of `test_tag_escaping.py`).
   - **Tertiary**: `git apply --check` for non-destructive patch integrity verification.
3. **Zero Risk of Side Effects**: By using read-only source inspection, standalone test scripts in `c:\Users\Loa\Downloads\GOAL`, and non-modifying git checks, competitor proposals can be audited with zero pollution to the repository or git history.

---

## 5. Verification Method

To independently reproduce and verify this assessment:
1. Verify git path, commit, and branch:
   ```powershell
   cd c:\Users\Loa\Downloads\GOAL\expensify_app
   git status
   git log -n 1 --oneline
   git remote -v
   ```
2. Verify missing node_modules:
   ```powershell
   Test-Path c:\Users\Loa\Downloads\GOAL\expensify_app\node_modules
   ```
   (Expected result: `False`)
3. Verify installed runtimes:
   ```powershell
   node -v
   npm -v
   bun -v
   python --version
   ```
4. Verify hermetic test script execution capability:
   ```powershell
   cd c:\Users\Loa\Downloads\GOAL
   python test_tag_escaping.py
   ```
   (Expected result: Clean execution demonstrating current vs fixed tag parsing)
