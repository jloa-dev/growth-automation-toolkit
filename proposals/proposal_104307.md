Contributor details
Your Expensify account email: jloa.dev@gmail.com
Upwork Profile Link: https://www.upwork.com/freelancers/~0163955a2ba22190aa

## Proposal
### Please re-state the problem that we are trying to solve in this issue.
When two splits of an expense are deleted, arrow navigation remains displayed on the report showing '1 of 2' despite only one expense existing, and clicking the arrow navigates to an 'It's not here' error page.

### What is the root cause of that problem?
In `src/components/MoneyRequestReportView/MoneyRequestReportTransactionsNavigation.tsx`:
The component caches the list of active transaction IDs (`activeTransactionIDs`) in component state.
When child split expenses are deleted, the parent Onyx report updates optimistically, but `activeTransactionIDs` is not re-synchronized against the remaining active, non-pending-deletion transactions. Because `activeTransactionIDs.length` still evaluates to 2, the navigation header continues to render the arrows (`1 of 2`), and clicking 'Next' attempts to navigate to the deleted transaction's ID.

### What changes do you think we should make in order to solve the problem?
In `src/components/MoneyRequestReportView/MoneyRequestReportTransactionsNavigation.tsx`:
Add a filter to reconcile `activeTransactionIDs` against the current transaction collection, omitting deleted or pending-delete transactions:
```typescript
const visibleTransactionIDs = useMemo(() => {
    return activeTransactionIDs.filter(id => {
        const transaction = transactions?.[id];
        return transaction && !TransactionUtils.isPendingDelete(transaction);
    });
}, [activeTransactionIDs, transactions]);
```
Use `visibleTransactionIDs` to determine arrow visibility (`visibleTransactionIDs.length > 1`) and page indexing.

### What specific scenarios should we cover in automated tests?
In `tests/unit/components/MoneyRequestReportTransactionsNavigation.test.tsx`:
- Add a test verifying that when transaction IDs in a report are reduced to 1 following deletions, the navigation arrows automatically unmount.
