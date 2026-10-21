Contributor details
Your Expensify account email: jloa.dev@gmail.com
Upwork Profile Link: https://www.upwork.com/freelancers/~0163955a2ba221e513

## Proposal

### Please re-state the problem that we are trying to solve in this issue.
When an expense report contains multiple expenses and an expense is split and then held, choosing "Approve only the unheld expenses" causes the original approved report's total to display the sum of both approved and held expenses rather than only the unheld expenses.

### What is the root cause of that problem?
In `src/libs/actions/IOU/Hold.ts:971-981`:
When moving held transactions out into a new report during "Approve only the unheld expenses", the original report's optimistic total is updated by copying cached unheld properties:
```typescript
if (shouldUpdateOriginalReportTotals) {
    optimisticData.push({
        onyxMethod: Onyx.METHOD.MERGE,
        key: `${ONYXKEYS.COLLECTION.REPORT}${iouReport?.reportID}`,
        value: {
            total: iouReport?.unheldTotal ?? 0,
            nonReimbursableTotal: iouReport?.unheldNonReimbursableTotal ?? 0,
            reimbursableTotal: getUnheldReimbursableTotal(iouReport),
        },
    });
}
```
1. `iouReport.unheldTotal` and `iouReport.unheldReimbursableTotal` are server-computed fields that were cached when the report was originally fetched.
2. When an expense is split (Step 3: Open expense -> More -> Split) and then held (Step 4: Hold split expense), new optimistic transactions are created locally, but the server has not yet returned an updated `unheldTotal` for the report.
3. Because `iouReport.unheldTotal` is stale, lines 976-978 write stale totals onto the original report. Furthermore, in `src/libs/actions/IOU/Hold.ts:794-795`, `holdReimbursable` is calculated as `getReimbursableTotal(iouReport) - getUnheldReimbursableTotal(iouReport)`, which similarly produces an inaccurate delta when `unheldReimbursableTotal` is out of sync with optimistic client transactions.

### What alternative solutions did you explore? (Optional)
Re-fetching the entire report was explored, but optimistic updates should be calculated immediately on the client using the real list of held transactions.

### What changes do you think we should make in order to solve the problem?

In `src/libs/actions/IOU/Hold.ts`:
Calculate the held transactions' amounts directly from `holdTransactions` instead of subtracting cached unheld fields:

```typescript
let holdReimbursableAmount = 0;
let holdNonReimbursableAmount = 0;

for (const transaction of holdTransactions) {
    const amount = Math.abs(transaction.amount ?? 0);
    if (TransactionUtils.isReimbursable(transaction)) {
        holdReimbursableAmount += amount;
    } else {
        holdNonReimbursableAmount += amount;
    }
}
```

Then in the optimistic update for the original report:
```diff
--- a/src/libs/actions/IOU/Hold.ts
+++ b/src/libs/actions/IOU/Hold.ts
@@ -971,11 +971,11 @@
     if (shouldUpdateOriginalReportTotals) {
         optimisticData.push({
             onyxMethod: Onyx.METHOD.MERGE,
             key: `${ONYXKEYS.COLLECTION.REPORT}${iouReport?.reportID}`,
             value: {
-                total: iouReport?.unheldTotal ?? 0,
-                nonReimbursableTotal: iouReport?.unheldNonReimbursableTotal ?? 0,
-                reimbursableTotal: getUnheldReimbursableTotal(iouReport),
+                total: (iouReport?.total ?? 0) - (holdReimbursableAmount + holdNonReimbursableAmount) * coefficient,
+                nonReimbursableTotal: (iouReport?.nonReimbursableTotal ?? 0) - holdNonReimbursableAmount * coefficient,
+                reimbursableTotal: getReimbursableTotal(iouReport) - holdReimbursableAmount * coefficient,
             },
         });
     }
```

### What automated tests can you add to prevent this from re-occurring?
Add a unit test in `tests/actions/IOUTest/HoldTest.ts` verifying that:
1. When a report contains split transactions and a split transaction is held, approving only unheld expenses updates `iouReport.total` to reflect only the remaining unheld transactions.
2. The optimistic report total never includes the amount of held transactions even when `iouReport.unheldTotal` is missing or stale.
