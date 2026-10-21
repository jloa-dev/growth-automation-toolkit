## Proposal

### Please re-state the problem that we are trying to solve in this issue.
The Export to-do in New Expensify (Home To-do tab) omits eligible reports that Search correctly returns for `action:export`. On accounts with accounting connections (such as QuickBooks Online) where the user is configured as the connection's exporter, Search returns reports needing export while the Home Export to-do shows 0.

### What is the root cause of that problem?
Rule discrepancies between `TodosUtils.ts` and the rest of the application:
1. **Exporter check in `TodosUtils.ts` (line 169)**:
   ```typescript
   case CONST.SEARCH.SEARCH_KEYS.EXPORT: {
       const reportActions = Object.values(allReportActions?.[`${ONYXKEYS.COLLECTION.REPORT_ACTIONS}${report.reportID}`] ?? []);
       return isExportAction(report, login, policy, reportActions) && policy?.exporter === login;
   }
   ```
   `TodosUtils.ts` strictly checks `policy?.exporter === login`.
   However, on QuickBooks (and other direct accounting integration) workspaces, `policy.exporter` is often empty while the specific connection exporter is set to the user.
2. In contrast, `ReportPrimaryActionUtils.ts`, `ReportSecondaryActionUtils.ts`, and `ReportPreviewActionUtils.ts` all use `isPreferredExporter(policy, currentUserLogin)` from `src/libs/PolicyUtils/index.ts`, which inspects both `policy.exporter` and all connection-specific exporter configurations (`policy.connections.quickbooksOnline.config.export.exporter`, etc.).
3. Furthermore, `isExportAction` already enforces `isReportExporter` via `isPreferredExporter`. The extra `&& policy?.exporter === login` check in `TodosUtils.ts` artificially suppresses valid export to-dos.

### What changes do you think we should make in order to solve the problem?

1. **In `src/libs/TodosUtils.ts`**:
   Remove the restrictive `&& policy?.exporter === login` condition and align with `isPreferredExporter`:
   ```diff
   --- a/src/libs/TodosUtils.ts
   +++ b/src/libs/TodosUtils.ts
   @@ -166,7 +166,7 @@ function doesReportRequireAction(
                );
            case CONST.SEARCH.SEARCH_KEYS.EXPORT: {
                const reportActions = Object.values(allReportActions?.[`${ONYXKEYS.COLLECTION.REPORT_ACTIONS}${report.reportID}`] ?? []);
   -            return isExportAction(report, login, policy, reportActions) && policy?.exporter === login;
   +            return isExportAction(report, login, policy, reportActions);
            }
            default:
                return false;
   ```

2. **In `src/libs/ReportPrimaryActionUtils.ts`**:
   Ensure `isExportAction` consistently handles auto-sync and export errors across both To-dos and Search query evaluations.

3. **Verify parity across all 4 export touchpoints**:
   - Home to-do count (`createTodosReportsAndTransactions`)
   - Search sidebar item & badge (`action:export`)
   - Search row primary action
   - Report page secondary action

### What alternative solutions did you explore? (Optional)
- Duplicating connection exporter lookups inside `TodosUtils.ts`: Antipattern; `isExportAction` already calls `isPreferredExporter` which centrally handles all connection exporters.

### What specific scenarios should we cover in automated tests?
In `tests/unit/TodosUtilsTest.ts`:
1. `policy.exporter` set to user $\to$ report classified in Export to-do.
2. `policy.exporter` empty, but QuickBooks connection exporter set to user $\to$ report classified in Export to-do.
3. User is admin but not exporter $\to$ report classified correctly according to admin permissions.
4. Already exported reports (`isExported`) or reports with export errors handled consistently between `isExportAction` and `TodosUtils`.
5. Parity test asserting that `TodosUtils.doesReportRequireAction(report, login, policy, CONST.SEARCH.SEARCH_KEYS.EXPORT)` returns `true` for all reports returned by `action:export`.
