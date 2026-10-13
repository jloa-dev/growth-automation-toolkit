Contributor details
Your Expensify account email: jloa.dev@gmail.com
Upwork Profile Link: https://www.upwork.com/freelancers/~0163955a2ba22190aa

## Proposal

### Please re-state the problem that we are trying to solve in this issue.
When editing an expense's merchant name, the change is saved on the transaction, but the Reports / Search tab list continues to display the old merchant name until an un-cached refresh occurs.

### What is the root cause of that problem?
In the Reports / Search tab, rows are populated from the active search snapshot collection (`snapshot_${hash}`).

In `src/libs/actions/IOU/UpdateMoneyRequest.ts` (lines 2418–2433), `getUpdateMoneyRequestParams` updates the search snapshot via `getSearchSnapshotUpdates` only when `hash` is provided:
```typescript
if (hash) {
    const snapshotUpdates = getSearchSnapshotUpdates({
        hash,
        transactionID,
        updatedTransaction,
        pendingFields,
        clearedPendingFields,
        transaction,
        optimisticViolations: Array.isArray(violationsOnyxData.value) ? violationsOnyxData.value : [],
        currentTransactionViolations,
    });
    optimisticData.push(...snapshotUpdates.optimisticData);
    successData.push(...snapshotUpdates.successData);
    failureData.push(...snapshotUpdates.failureData);
}
```
However, in `src/pages/iou/request/step/DynamicIOURequestStepMerchant.tsx` (lines 151–173), `updateMoneyRequestMerchant` is called without passing `hash`. As a result, only `TRANSACTION_${transactionID}` and `REPORT_ACTIONS_${reportID}` are updated optimistically, while `snapshot_${hash}` continues holding the stale merchant name. (By contrast, `DynamicIOURequestStepTag.tsx` and `DynamicIOURequestStepCategoryCreate.tsx` already read and pass `hash: currentSearchHash`).

### What changes do you think we should make in order to solve the problem?
1. In `src/pages/iou/request/step/DynamicIOURequestStepMerchant.tsx`:
   - Import `useSearchQueryContext` from `@components/Search/SearchQueryContext`.
   - Read `const {currentSearchHash} = useSearchQueryContext();`.
   - Pass `hash: currentSearchHash` in the `updateMoneyRequestMerchant({...})` call inside `updateMerchant`.
2. Add unit test coverage in `tests/actions/UpdateMoneyRequestTest.ts`:
   - Verify that calling `updateMoneyRequestMerchant` with `hash` updates `snapshot_${hash}.data.transactions_${transactionID}.merchant` in `optimisticData`.
   - Verify that failure rollback restores the previous merchant in `failureData`.

### What alternative solutions did you explore? (Optional)
Reading the current search hash from Onyx inside `UpdateMoneyRequest.ts`. Rejected because caller-driven parameter propagation follows NewDot's architectural standard (as implemented in `DynamicIOURequestStepTag.tsx`).
