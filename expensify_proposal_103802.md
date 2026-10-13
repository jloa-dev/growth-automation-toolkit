## Proposal

### Please re-state the problem that we are trying to solve in this issue.
When a user confirms the deletion of a split per-diem expense whose sibling split is in a submitted or approved report, the app redirects to the "Edit split" page instead of deleting the expense.

### What is the root cause of that problem?
In [`src/hooks/useDeleteTransactions.ts#L116-L136`](https://github.com/Expensify/App/blob/main/src/hooks/useDeleteTransactions.ts#L116-L136), `getSplitExpenseEditTransactionOnDelete` checks if the transaction being deleted is a split per diem expense:
```ts
if (!shouldRedirectDeleteToSplitExpenseEdit(transaction, originalTransaction)) {
    return undefined;
}
```
If the original transaction has more than one child split, it immediately returns the parent transaction to trigger redirection to the Edit Split flow (`navigateToEditSplitExpense`).

However, it fails to check whether any of the **remaining** sibling splits can actually be edited. If the sibling split is already in a submitted or approved report (`statusNum >= CONST.REPORT.STATUS_NUM.SUBMITTED`), the Edit Split page cannot modify or remove the split, leaving the user unable to delete their expense.

### What changes do you think we should make in order to solve the problem?
1. In `src/hooks/useDeleteTransactions.ts`, inside `getSplitExpenseEditTransactionOnDelete`, filter the sibling transactions to exclude the transaction being deleted:
```ts
const otherSplits = getChildTransactions(allTransactions, originalTransaction?.transactionID)
    .filter((child) => child.transactionID !== transaction.transactionID);
```
2. Verify if any remaining sibling is editable using the existing logic from `hasEditableSplitExpenseLeft` (checking if `statusNum < CONST.REPORT.STATUS_NUM.SUBMITTED`).
3. If no other editable split exists, return `undefined`, allowing `deleteTransactions` to proceed with the normal deletion flow and removing the expense cleanly.
4. Align `ReportSecondaryActionUtils` / `ContextMenuActions` so the delete action visibility matches the executable deletion state.
5. Add unit tests in `tests/unit/useDeleteTransactionsTest.ts` to assert that deleting a split per-diem expense whose only sibling is in an approved report results in a direct deletion (`deleted`) rather than a redirect (`redirected`).

### What alternative solutions did you explore? (Optional)
- Disabling the Delete option entirely when a sibling split is approved: rejected because it prevents users from deleting legitimate orphan expenses on open reports.
