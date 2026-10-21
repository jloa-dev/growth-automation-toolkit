## Proposal

### Please re-state the problem that we are trying to solve in this issue.
The Inbox displays a red brick road (RBR) and a **Fix** to-do badge for violations on expense reports that have already been submitted by the employee (e.g. `receiptRequired` or `itemizedReceiptRequired`). In contrast, Home and Spend correctly show nothing to do because the submitter cannot fix violations once a report is submitted. This leaves an un-clearable RBR on the Inbox.

### What is the root cause of that problem?
The rule defining actionable violations is fragmented across the app:
1. **Inbox Check (`src/libs/ReportUtils.ts`, line 10206)**:
   ```typescript
   // Allow both open and processing reports to show RBR for violations
   if (!isOpenOrProcessingReport(potentialReport)) {
       return false;
   }
   ```
   `ReportUtils` treats both `OPEN` and `PROCESSING` reports as actionable for violations, excluding only specific names (`companyCardRequired` and `modifiedAmount`). Other violations like `receiptRequired` and `itemizedReceiptRequired` continue to flag the Inbox after submission.
2. **Home Check (`src/pages/home/ForYouSection/useReviewFlaggedExpenses.ts`, lines 48–58)**:
   ```typescript
   return report.stateNum === CONST.REPORT.STATE_NUM.OPEN && report.statusNum === CONST.REPORT.STATUS_NUM.OPEN;
   ```
   Home strictly requires the report to be `OPEN` (draft), correctly ignoring submitted/processing reports.

### What changes do you think we should make in order to solve the problem?

1. **Centralize Actionable Violation Check in `src/libs/TodosUtils.ts`**:
   Introduce a shared helper `shouldShowViolationFixForReport`:
   ```typescript
   function shouldShowViolationFixForReport(report: OnyxEntry<Report>, canEditExpense = false): boolean {
       if (!report) {
           return false;
       }
       // If the report is in draft (OPEN) state, submitter can fix violations
       if (isOpenReport(report)) {
           return true;
       }
       // For submitted/processing reports, only allow if the expense remains explicitly editable (e.g. instant submit policies before approval)
       return isProcessingReport(report) && canEditExpense;
   }
   ```

2. **In `src/libs/ReportUtils.ts`**:
   Replace `isOpenOrProcessingReport` in `hasViolatingReport` / LHN RBR check with the centralized actionability check:
   ```diff
   - if (!isOpenOrProcessingReport(potentialReport)) {
   + if (!isOpenReport(potentialReport)) {
         return false;
     }
   ```

3. **In `src/pages/home/ForYouSection/useReviewFlaggedExpenses.ts`**:
   Use the shared helper to ensure 100% parity between Home "Review flagged expenses" and Inbox LHN RBR.

### What alternative solutions did you explore? (Optional)
- Adding more individual exclusions (e.g. excluding `receiptRequired`, `itemizedReceiptRequired` one by one): Fragile band-aid that perpetuates regression risk when new violation types are introduced. Restricting "Fix" to editable/open reports solves the underlying architectural discrepancy.

### What specific scenarios should we cover in automated tests?
In `tests/unit/ReportUtilsTest.ts` and `tests/unit/useTodoCountsTest.tsx`:
1. Open report with `receiptRequired` violation $\to$ RBR and Fix badge displayed.
2. Submitted (processing) report with `receiptRequired` violation $\to$ RBR and Fix badge suppressed.
3. Cross-page parity test verifying that whenever Inbox shows an RBR for a violation, Home "Review flagged expenses" matches it, and vice versa.
