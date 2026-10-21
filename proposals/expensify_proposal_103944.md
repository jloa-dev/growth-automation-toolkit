## Proposal

### Please re-state the problem that we are trying to solve in this issue.
When an expense is removed from a multi-expense report (via "Remove from report") or moved to another report, the top-right navigation carousel arrows (e.g., "1 of 2") remain visible on the screen. Clicking the arrows attempts to resolve sibling transactions against the stale carousel, navigating the user to an unintended destination (such as the Self DM).

### What is the root cause of that problem?
Carousel navigation across sibling transactions is tracked in Onyx (`ONYXKEYS.TRANSACTION_THREAD_NAVIGATION_TRANSACTION_IDS`) and managed by `src/libs/actions/TransactionThreadNavigation.ts` via module state (`lastSetIDs`, `lastSetSource`).

1. **Seeding with Report Prefix**:
   When viewing a transaction opened from a report, the carousel is seeded with transaction IDs stamped with one of three report-scoped sources:
   - `CAROUSEL_SOURCE.report(reportID)` (`report:<reportID>`)
   - `CAROUSEL_SOURCE.reportRow(reportID)` (`reportRow:<reportID>`) when opening an expense from the transaction list (`MoneyRequestReportTransactionList.tsx:273`)
   - `CAROUSEL_SOURCE.reportPreview(reportID)` (`reportPreview:<reportID>`) when opening an expense from a chat preview.

2. **Unreporting Leaves Carousel Stale**:
   When the user clicks "Remove from report", `removeFromReport` calls `changeTransactionsReport` which changes the transaction's `reportID` to `CONST.REPORT.UNREPORTED_REPORT_ID` (unreported).
   - In `src/hooks/useCarouselTransactionIDs.ts`, `validTransactionIDsSelector` only filters out transactions marked as deleted (`isDeletedTransaction`) or pending delete (`isTransactionPendingDelete`). Since the detached transaction is not deleted, it remains in `validTransactionIDs`.
   - `TransactionThreadNavigation` is never notified that the transaction left the active report, so `lastSetIDs` retains the detached ID.

3. **Arrow Visibility Remains True**:
   In `src/components/MoneyRequestReportView/MoneyRequestReportTransactionsNavigation.tsx` (line 435):
   ```typescript
   if (transactionIDsList.length < 2 || currentTransactionIndex === -1) {
       return;
   }
   ```
   Because `transactionIDsList` still holds both IDs, `length < 2` is false.
   Clicking the arrows resolves the remaining sibling against the report which now has only 1 expense (`isOneTransactionReport`), while the detached transaction's thread is under the Self DM, resulting in broken navigation jumps to the Self DM.

### What changes do you think we should make in order to solve the problem?

#### 1. Add `removeActiveTransactionIDs` in `src/libs/actions/TransactionThreadNavigation.ts`:
Expose a helper to remove detached transaction IDs from the active carousel, safely validating against all report-scoped sources (`report:`, `reportRow:`, `reportPreview:`) so non-report carousels (e.g. Search, Spend) are never inadvertently altered:

```typescript
/**
 * Helper to determine whether an active carousel source belongs to a specific report.
 */
function isSourceMatchingReport(source: string | null, reportID: string): boolean {
    if (!source) {
        return false;
    }
    return (
        source === CAROUSEL_SOURCE.report(reportID) ||
        source === CAROUSEL_SOURCE.reportRow(reportID) ||
        source === CAROUSEL_SOURCE.reportPreview(reportID)
    );
}

/**
 * Removes one or more transaction IDs from the active carousel if the current carousel
 * belongs to the specified report.
 * If fewer than two IDs remain, clears the carousel completely so navigation arrows hide.
 */
function removeActiveTransactionIDs(transactionIDsToRemove: string[], fromReportID?: string) {
    if (!lastSetIDs?.length || !transactionIDsToRemove.length) {
        return Promise.resolve();
    }

    if (fromReportID && !isSourceMatchingReport(lastSetSource, fromReportID)) {
        return Promise.resolve();
    }

    const idsToRemoveSet = new Set(transactionIDsToRemove);
    const updatedIDs = lastSetIDs.filter((id) => !idsToRemoveSet.has(id));

    if (updatedIDs.length === lastSetIDs.length) {
        return Promise.resolve();
    }

    if (updatedIDs.length < 2) {
        return clearActiveTransactionIDs();
    }

    let updatedDescriptors = lastSetDescriptors ? {...lastSetDescriptors} : null;
    if (updatedDescriptors) {
        for (const id of transactionIDsToRemove) {
            delete updatedDescriptors[id];
        }
    }

    return setActiveTransactionIDs(updatedIDs, {
        source: lastSetSource ?? undefined,
        snapshotHash: lastSetSnapshotHash ?? undefined,
        descriptors: updatedDescriptors ?? undefined,
    });
}
```
Export `removeActiveTransactionIDs` from `TransactionThreadNavigation.ts`.

#### 2. Call `removeActiveTransactionIDs` when transactions leave a report:
- In `src/pages/iou/request/step/IOURequestStepReport/hooks/useReportSelectionActions.ts`:
  - In `removeFromReport`:
    ```typescript
    const removeFromReport = () => {
        if (!transaction) {
            return;
        }
        removeActiveTransactionIDs(targetTransactionIDs, transaction.reportID);
        Navigation.dismissToSuperWideRHP({ ... });
    };
    ```
  - In `handleRegularReportSelection` when `isEditing` is true (moving an expense to a different report):
    ```typescript
    if (isEditing) {
        removeActiveTransactionIDs(targetTransactionIDs, transaction.reportID);
        // ... call changeTransactionsReport
    }
    ```
- In `src/pages/iou/request/step/DynamicIOURequestEditReport.tsx`:
  - In `removeFromReport`:
    ```typescript
    removeActiveTransactionIDs(transactionIDs, selectedReport?.reportID);
    ```
  - In `setNavigationActionToMicrotaskQueue` when moving to `newReport`:
    ```typescript
    removeActiveTransactionIDs(transactionIDs, selectedReport?.reportID);
    ```

### What alternative solutions did you explore? (Optional)
1. **Filtering in `useCarouselTransactionIDs.ts` by `reportID`:**
   Filtering by `transaction.reportID` inside `useCarouselTransactionIDs` breaks Search and Spend page carousels where transactions intentionally span multiple reports.
2. **Matching only `CAROUSEL_SOURCE.report(reportID)`:**
   A naive equality check `lastSetSource === CAROUSEL_SOURCE.report(reportID)` fails whenever an expense is opened from a report's transaction list (which sets `CAROUSEL_SOURCE.reportRow(reportID)`) or from a chat report preview (`CAROUSEL_SOURCE.reportPreview(reportID)`). Supporting all three report prefix sources via `isSourceMatchingReport` is essential for consistent behavior.

### Test Plan
#### Automated Unit Tests (`tests/unit/libs/actions/TransactionThreadNavigationTest.ts`):
1. `removeActiveTransactionIDs` successfully removes IDs when source is `CAROUSEL_SOURCE.report(reportID)`, `CAROUSEL_SOURCE.reportRow(reportID)`, or `CAROUSEL_SOURCE.reportPreview(reportID)`.
2. `removeActiveTransactionIDs` clears the carousel completely when remaining IDs drop below 2 (`updatedIDs.length < 2`), asserting that `ONYXKEYS.TRANSACTION_THREAD_NAVIGATION_TRANSACTION_IDS` is cleared.
3. `removeActiveTransactionIDs` retains remaining IDs (e.g. 3 IDs -> 2 IDs) and updates Onyx when 2 or more IDs remain.
4. `removeActiveTransactionIDs` does nothing when `fromReportID` does not match the active carousel source (e.g., search or another report).

#### Manual QA Steps:
1. Go to workspace chat.
2. Create two expenses on a report.
3. Open the report.
4. Click on an expense to open the thread.
5. In the expense details, click Report > Remove from report.
6. **Verify:** The top-right carousel arrows ("1 of 2") are completely hidden.
7. Return to the report and verify only the remaining expense is displayed.
8. Create three expenses on a report, open the first expense, and remove it from the report.
9. **Verify:** The carousel updates to "1 of 2" for the two remaining expenses and pages smoothly between them without jumping to Self DM.

Contributor details
Your Expensify account email: jloa.dev@gmail.com
Upwork Profile Link: https://www.upwork.com/freelancers/~0163955a2ba22190aa
