## Proposal

### Please re-state the problem that we are trying to solve in this issue.
Dragging and dropping a receipt file onto an existing receipt of an expense in Draft, Outstanding, or Approved status behaves inconsistently: sometimes it replaces the receipt, sometimes only "Add attachments" appears, and other times (especially on Approved expenses) dropping prompts the user to create a new expense instead of replacing the existing receipt.

### What is the root cause of that problem?
There are two root causes that combine to cause all three observed behaviors:

1. **Approved expenses fail `canEditFieldOfMoneyRequest` because `policy` and `report` are not passed in `useShouldAddOrReplaceReceipt`:**
In `src/pages/inbox/report/ReportActionCompose/useShouldAddOrReplaceReceipt.ts`:
```typescript
const canEditReceipt =
    canUserPerformWriteAction &&
    canEditFieldOfMoneyRequest({reportAction: effectiveParentReportAction, fieldToEdit: CONST.EDIT_REQUEST_FIELD.RECEIPT, transaction, rules, reportNameValuePairs: undefined}) &&
    !transaction?.receipt?.isTestDriveReceipt;
```
Notice that `canEditFieldOfMoneyRequest` is invoked without passing `policy` or `report`.
Inside `canEditFieldOfMoneyRequest` (`src/libs/ReportUtils.ts:5647-5655`):
```typescript
const reportPolicy = policy ?? getPolicy(moneyRequestReport?.policyID);
const isAdmin = isExpenseReport(moneyRequestReport) && reportPolicy?.role === CONST.POLICY.ROLE.ADMIN;
const isAdminChangingReceiptOnApprovedReport = isAdmin && fieldToEdit === CONST.EDIT_REQUEST_FIELD.RECEIPT && !isDeleteAction && !isSettled(moneyRequestReport);

if (!isAdminChangingReceiptOnApprovedReport && (isSettled(moneyRequestReport) || isReportApproved({report: moneyRequestReport}))) {
    return false;
}
```
Because `policy` is not passed, `reportPolicy` falls back to `getPolicy(...)` using deprecated Onyx collection data which may be undefined. As a consequence, `isAdmin` evaluates to `false`. When the report is Approved (`isReportApproved`), the check fails and returns `false`, causing `canEditReceipt` and `shouldAddOrReplaceReceipt` to become `false`.

2. **When `shouldAddOrReplaceReceipt` is false, `RichDropZone` falls back to creating a new expense or showing only "Add attachments":**
In `src/pages/inbox/report/ReportActionCompose/ComposerDropZone.tsx:84-85`:
```typescript
const canModifyReceipt = shouldAddOrReplaceReceipt && !isSettledReport;
const shouldDisplayDualDropZone = canModifyReceipt || hasMoneyRequestOptions;
```
- If `hasMoneyRequestOptions` is `false`, `shouldDisplayDualDropZone` is `false`, falling back to `SimpleDropZone`, which only displays "Add attachments" (reproducing the second observed behavior).
- If `hasMoneyRequestOptions` is `true`, `DualDropZone` is displayed, but because `shouldAddOrReplaceReceipt` is `false`, dropping onto the receipt drop zone hits `useReceiptDrop.ts:86`:
```typescript
if (shouldAddOrReplaceReceipt && transactionID) {
    replaceReceipt(...);
    return;
}
const initialTransaction = initMoneyRequest(...);
```
which initiates `initMoneyRequest` and navigates the user to create a new expense instead of replacing the receipt (reproducing the third observed behavior).

### What changes do you think we should make in order to solve the problem?
1. In `src/pages/inbox/report/ReportActionCompose/useShouldAddOrReplaceReceipt.ts`:
Fetch `policy` for `report?.policyID` via `useOnyx` and pass `report` and `policy` to `canEditFieldOfMoneyRequest`:
```typescript
const [policy] = useOnyx(`${ONYXKEYS.COLLECTION.POLICY}${report?.policyID}`);

// ...
const canEditReceipt =
    canUserPerformWriteAction &&
    canEditFieldOfMoneyRequest({
        reportAction: effectiveParentReportAction,
        fieldToEdit: CONST.EDIT_REQUEST_FIELD.RECEIPT,
        transaction,
        report,
        policy,
        rules,
        reportNameValuePairs: undefined,
    }) &&
    !transaction?.receipt?.isTestDriveReceipt;
```

2. Additionally, ensure that when the user is viewing an expense report (where `report` is the expense report itself), `effectiveParentReportAction` is properly resolved from `reportActionValues` if `report.parentReportActionID` is not present on the report itself.

### What alternative solutions did you consider?
Bypassing `canEditFieldOfMoneyRequest` entirely in `useShouldAddOrReplaceReceipt`: this would risk allowing receipt edits on settled/paid expenses where receipt replacements must remain disallowed. Passing `policy` and `report` preserves all existing business validation (including admin overrides on approved expenses) correctly.
