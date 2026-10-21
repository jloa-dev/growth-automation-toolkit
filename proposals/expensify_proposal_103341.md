## Proposal

### Please re-state the problem that we are trying to solve in this issue.
New Expensify unconditionally hides the `Reimbursable` toggle on company card expenses in single expense views (`MoneyRequestView`), split expense views (`DynamicSplitExpenseEditPage`), confirmation footers (`useFooterDerivedFlags`), and the bulk edit page (`SearchEditMultiplePage`). In Expensify Classic, company card expenses allow viewing and editing the `Reimbursable` toggle whenever the card feed is set to either "Do Not Force" option (`default_yes` or `default_no`/`none`). We need New Expensify to match Classic parity by displaying and allowing edits to the `Reimbursable` toggle according to the `forceReimbursable` property stamped on imported transactions.

### What is the root cause of that problem?
The codebase currently relies on unconditional `!isManagedCardTransaction(transaction)` guards across all expense edit and display surfaces without evaluating the transaction's stamped `forceReimbursable` configuration:

1. **Single Expense View** (`src/components/ReportActionItem/MoneyRequestView.tsx`, lines 550–554):
   ```typescript
   const shouldShowReimbursable =
       (isPolicyExpenseChat || (isExpenseUnreported && !!policy)) &&
       (policy?.disabledFields?.reimbursable !== true || isCurrentTransactionReimbursableDifferentFromPolicyDefault) &&
       !isManagedCardTransactionTransactionUtils(transaction) &&
       !isInvoice;
   ```
2. **Bulk Edit Page** (`src/pages/Search/SearchEditMultiple/SearchEditMultiplePage.tsx`, lines 153–159):
   ```typescript
   const areSelectedTransactionsReimbursable = selectedTransactionContexts.every(({transaction, report, transactionPolicy}) => {
       if (!transaction.reportID || transaction.reportID === CONST.REPORT.UNREPORTED_REPORT_ID) {
           return true;
       }
       return !isIOUReport(report) && !isInvoiceReport(report) && transactionPolicy?.disabledFields?.reimbursable === false && !isManagedCardTransaction(transaction);
   });
   ```
3. **Split Expense Edit** (`src/pages/iou/DynamicSplitExpenseEditPage.tsx`, lines 246–249):
   ```typescript
   const shouldShowReimbursable =
       (isPolicyExpenseChat || (isExpenseUnreported && !!effectivePolicy)) &&
       (effectivePolicy?.disabledFields?.reimbursable !== true || isReimbursableDifferentFromPolicyDefault) &&
       !isManagedCardTransaction(transaction);
   ```
4. **Confirmation Footer** (`src/components/MoneyRequestConfirmationListFooter/hooks/useFooterDerivedFlags.ts`, lines 97–98):
   ```typescript
   const shouldShowReimbursable =
       (isPolicyExpenseChat || isTrackExpense) && !!policy && policy?.disabledFields?.reimbursable !== true && !isManagedCardTransaction(transaction) && !isTypeInvoice;
   ```
5. **Edit Permissions Guard** (`src/libs/ReportUtils.ts`, line 5670):
   In `canEditFieldOfMoneyRequest`:
   ```typescript
   if (fieldToEdit === CONST.EDIT_REQUEST_FIELD.REIMBURSABLE) {
       return canEditExpense;
   }
   ```
   While `canCurrentUserEditExpense` is verified, managed card transactions with forced settings are not checked.

### What changes do you think we should make in order to solve the problem?

1. **Add Feed Constants in `src/CONST.ts`**:
   Define `FEED_FORCE_REIMBURSABLE`:
   ```typescript
   FEED_FORCE_REIMBURSABLE: {
       FORCE_NO: 'force_no',
       FORCE_YES: 'force_yes',
       DEFAULT_YES: 'default_yes',
       DEFAULT_NO: 'default_no',
       NONE: 'none',
   },
   ```

2. **Add `canModifyCardExpenseReimbursable` in `src/libs/TransactionUtils/index.ts`**:
   ```typescript
   function canModifyCardExpenseReimbursable(transaction: OnyxEntry<Transaction>): boolean {
       if (isExpensifyCardTransaction(transaction)) {
           return false;
       }
       if (!isManagedCardTransaction(transaction)) {
           return false;
       }
       const forceReimbursable = transaction?.comment?.forceReimbursable ?? transaction?.forceReimbursable;
       return (
           forceReimbursable === CONST.COMPANY_CARD.FEED_FORCE_REIMBURSABLE.DEFAULT_YES ||
           forceReimbursable === CONST.COMPANY_CARD.FEED_FORCE_REIMBURSABLE.DEFAULT_NO ||
           forceReimbursable === CONST.COMPANY_CARD.FEED_FORCE_REIMBURSABLE.NONE
       );
   }
   ```

3. **Update Single Expense View (`src/components/ReportActionItem/MoneyRequestView.tsx`)**:
   ```diff
   - !isManagedCardTransactionTransactionUtils(transaction) &&
   + (!isManagedCardTransactionTransactionUtils(transaction) || canModifyCardExpenseReimbursable(transaction)) &&
   ```

4. **Update Bulk Edit (`src/pages/Search/SearchEditMultiple/SearchEditMultiplePage.tsx`)**:
   ```diff
   - return !isIOUReport(report) && !isInvoiceReport(report) && transactionPolicy?.disabledFields?.reimbursable === false && !isManagedCardTransaction(transaction);
   + const isCardAllowed = isManagedCardTransaction(transaction) ? canModifyCardExpenseReimbursable(transaction) : true;
   + return !isIOUReport(report) && !isInvoiceReport(report) && transactionPolicy?.disabledFields?.reimbursable === false && isCardAllowed;
   ```

5. **Update Split Expense Edit (`src/pages/iou/DynamicSplitExpenseEditPage.tsx`)**:
   ```diff
   - !isManagedCardTransaction(transaction);
   + (!isManagedCardTransaction(transaction) || canModifyCardExpenseReimbursable(transaction));
   ```

6. **Update Confirmation Footer (`src/components/MoneyRequestConfirmationListFooter/hooks/useFooterDerivedFlags.ts`)**:
   ```diff
   - !isManagedCardTransaction(transaction) && !isTypeInvoice;
   + (!isManagedCardTransaction(transaction) || canModifyCardExpenseReimbursable(transaction)) && !isTypeInvoice;
   ```

7. **Update Edit Permissions Guard (`src/libs/ReportUtils.ts`)**:
   ```typescript
   if (fieldToEdit === CONST.EDIT_REQUEST_FIELD.REIMBURSABLE) {
       if (isManagedCardTransaction(transaction) && !canModifyCardExpenseReimbursable(transaction)) {
           return false;
       }
       return canEditExpense;
   }
   ```

### What alternative solutions did you explore? (Optional)
- **Wait for Issue #103342 (Feed settings UI)**: Unnecessary blocker; imported transactions already arrive stamped with `forceReimbursable`, allowing New Expensify to support this immediately.
- **Unconditionally allowing toggle for all company cards**: Breaks Classic parity, as feeds configured to `force_no` or `force_yes` must strictly lock reimbursability.

### What specific scenarios should we cover in automated tests?
In `tests/unit/TransactionUtilsTest.ts`, `tests/unit/MoneyRequestViewTest.tsx`, and `tests/unit/SearchEditMultiplePageTest.tsx`:
1. **Force No / Force Yes**: Verify `canModifyCardExpenseReimbursable` returns `false` and reimbursable row is hidden.
2. **Default Yes / Default No / None**: Verify `canModifyCardExpenseReimbursable` returns `true` and the toggle is visible and editable.
3. **Expensify Cards**: Verify `isExpensifyCardTransaction` strictly returns `false` even if `forceReimbursable` is set.
4. **Bulk Edit Mixed Selections**:
   - Mixed Cash + Do Not Force card transactions: Reimbursable row is visible.
   - Any selection containing a forced card transaction (`force_no` / `force_yes`): Reimbursable row is hidden.
