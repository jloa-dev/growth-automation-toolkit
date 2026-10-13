Contributor details
Your Expensify account email: jloa.dev@gmail.com
Upwork Profile Link: https://www.upwork.com/freelancers/~0163955a2ba22190aa

## Proposal

### Please re-state the problem that we are trying to solve in this issue.
When an employee (User A) creates and submits a report with an expense and places a hold on it, the approver (User B) sees the single-expense report in their Inbox "To-dos" tab with a green "Approve" badge upon opening the app before clicking on the report.

### What is the root cause of that problem?
In `src/libs/ReportUtils.ts`, `isReportExcludedForHeldExpenses` determines whether a report whose expenses are on hold should be excluded from requiring action from the current user:
```typescript
function isReportExcludedForHeldExpenses(iouReport: OnyxEntry<Report>, transactions: Transaction[], reportActions: OnyxEntry<ReportActions>, currentUserAccountID?: number): boolean {
    if (!hasOnlyHeldExpenses(transactions)) {
        return false;
    }
    return isOpenExpenseReport(iouReport) || !didCurrentUserPlaceHoldOnReportExpense(reportActions, transactions, currentUserAccountID);
}
```
However, `hasOnlyHeldExpenses(transactions)` evaluates:
```typescript
function hasOnlyHeldExpenses(allReportTransactions: Transaction[]): boolean {
    return allReportTransactions.length > 0 && !allReportTransactions.some((transaction) => !isOnHoldTransactionUtils(transaction));
}
```
When User B (the approver) opens the app and navigates to the Inbox / To-dos tab without first opening User A's report, User A's transactions have not yet been fetched into the local Onyx store (`getReportTransactions(iouReportID)` returns an empty array `[]`).

Because `allReportTransactions.length === 0`:
1. `hasOnlyHeldExpenses([])` evaluates to `false`.
2. It fails to check the report's aggregate totals already present on `iouReport`: when `iouReport.unheldTotal === 0 && (iouReport.total ?? 0) !== 0` (or `iouReport.unheldReimbursableTotal === 0`), the report is entirely composed of held expenses.
3. Since `isReportExcludedForHeldExpenses` returns `false`, `getBadgeFromIOUReport` in `src/libs/actions/IOU/ReportWorkflow.ts` treats the report as actionable and assigns `CONST.REPORT.ACTION_BADGE.APPROVE`. This causes the report to be shown in User B's To-dos tab with an Approve badge, even though User B cannot approve a report where all expenses are held by the submitter.

### What changes do you think we should make in order to solve the problem?
1. In `src/libs/ReportUtils.ts`, update `isReportExcludedForHeldExpenses` (or `hasOnlyHeldExpenses`) to check the report's aggregate unheld metrics as a fallback when transactions are not yet populated in Onyx:
   - When `transactions.length === 0`, verify whether `iouReport?.unheldTotal === 0 && (iouReport?.total ?? 0) !== 0` (and `!didCurrentUserPlaceHoldOnReportExpense(...)`).
   - If all expenses are held and the current user was not the one who placed the hold, the report cannot proceed and must be excluded from demanding action.
2. Ensure `didCurrentUserPlaceHoldOnReportExpense` handles the cold-cache case gracefully when individual transaction objects are not yet loaded, defaulting to `false` for an approver who did not initiate the hold.
3. Add hermetic unit test in `tests/unit/ReportUtilsTest.ts` verifying that when a report has `unheldTotal: 0` and non-zero `total`, `isReportExcludedForHeldExpenses` correctly returns `true` (excluding the report from To-dos) even when `transactions` is empty `[]`.

### What alternative solutions did you explore? (Optional)
Eagerly fetching all child transactions for every report when loading the Inbox, but that introduces unnecessary network overhead and memory pressure on startup. Using the aggregate `unheldTotal` / `unheldReimbursableTotal` properties already provided by the backend on the report object is instantaneous and zero-cost.
