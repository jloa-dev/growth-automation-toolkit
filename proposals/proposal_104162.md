Contributor details
Your Expensify account email: jloa.dev@gmail.com
Upwork Profile Link: https://www.upwork.com/freelancers/~0163955a2ba22190aa

## Proposal

### Please re-state the problem that we are trying to solve in this issue.
On the expense confirmation page, the Report field remains interactive/clickable even when all outstanding reports for the workspace contain only non-reimbursable expenses (and cannot accept new transactions), leading to an interactive field that cannot attach to those reports.

### What is the root cause of that problem?
In `src/components/MoneyRequestConfirmationList/sections/ReportField.tsx` (lines 113–116):
```tsx
const outstandingReports = useOutstandingReports(undefined, isFromGlobalCreate && !isPerDiemRequest ? undefined : policyID, ownerAccountID, false);
const shouldReportBeEditable = (isUnreported ? outstandingReports.length >= 1 : outstandingReports.length > 1) && !isMoneyRequestReport(reportID);
```
- `useOutstandingReports` returns all outstanding reports by checking open status, but it does NOT verify whether the user/expense is eligible to add transactions to those reports.
- Under workspaces with instant submission and submit & close (or where existing reports contain only non-reimbursable expenses), `ReportUtils.canAddTransaction(report, rules, undefined, true)` returns `false` (lines 3102–3108 of `ReportUtils.ts`).
- Consequently, while `outstandingReports.length > 1` evaluates to `true`, none of those reports can actually accept the expense. `ReportField` incorrectly sets `shouldReportBeEditable = true`, leaving the field interactive when it should be disabled / read-only.

### What changes do you think we should make in order to solve the problem?
1. In `src/components/MoneyRequestConfirmationList/sections/ReportField.tsx`:
   - Filter `outstandingReports` using `canAddTransaction(report, rules, undefined, true)` to obtain `eligibleOutstandingReports`.
   - Update `shouldReportBeEditable` to base its threshold on `eligibleOutstandingReports`:
```diff
--- a/src/components/MoneyRequestConfirmationList/sections/ReportField.tsx
+++ b/src/components/MoneyRequestConfirmationList/sections/ReportField.tsx
@@ -9,7 +9,7 @@ import createDynamicRoute from '@libs/Navigation/helpers/dynamicRoutesUtils/crea
 import Navigation from '@libs/Navigation/Navigation';
 import Parser from '@libs/Parser';
 import {getReportName} from '@libs/ReportNameUtils';
-import {generateReportID, getOutstandingReportsForUser, isMoneyRequestReport, isReportOutstanding, sortOutstandingReportsBySelected} from '@libs/ReportUtils';
+import {canAddTransaction, generateReportID, getOutstandingReportsForUser, isMoneyRequestReport, isReportOutstanding, sortOutstandingReportsBySelected} from '@libs/ReportUtils';
 
 import CONST from '@src/CONST';
 import type {IOUAction, IOUType} from '@src/CONST';
@@ -21,7 +21,7 @@ import type {Participant} from '@src/types/onyx/IOU';
 import type {OnyxEntry} from 'react-native-onyx';
 
 import {createOutstandingReportsForPolicySelector} from '@selectors/Report';
-import React from 'react';
+import React, {useMemo} from 'react';
 
 import ExpenseFieldRow from './ExpenseFieldRow';
 import {useExpenseFormLayout} from './ExpenseFormLayoutContext';
@@ -111,9 +111,13 @@ function ReportField({selectedParticipants, iouType, reportID, reportActionID, a
     })();
 
     const outstandingReports = useOutstandingReports(undefined, isFromGlobalCreate && !isPerDiemRequest ? undefined : policyID, ownerAccountID, false);
+    const eligibleOutstandingReports = useMemo(() => {
+        return outstandingReports.filter((report) => canAddTransaction(report, rules, undefined, true));
+    }, [outstandingReports, rules]);
+
     // When creating an expense in an individual report, the report field becomes read-only
     // since the destination is already determined and there's no need to show a selectable list.
-    const shouldReportBeEditable = (isUnreported ? outstandingReports.length >= 1 : outstandingReports.length > 1) && !isMoneyRequestReport(reportID);
+    const shouldReportBeEditable = (isUnreported ? eligibleOutstandingReports.length >= 1 : eligibleOutstandingReports.length > 1) && !isMoneyRequestReport(reportID);
 
     const openReportPage = () => {
         if (!transactionID || !selectedReportID) {
```

Pre-coded and tested in branch: `fix/104162-report-field-non-reimbursable` (https://github.com/jloa-dev/App/tree/fix/104162-report-field-non-reimbursable).

### What alternative solutions did you explore? (Optional)
Filtering out non-reimbursable reports inside `useOutstandingReports` hook globally. However, that hook is shared by other flows (including search and workspace overview) where open reports need to be listed regardless of transaction eligibility. Filtering at the field level where interactivity is determined is cleaner and avoids side-effects.
