## Proposal

### Please re-state the problem that we are trying to solve in this issue.
When a list-type report field has all of its options disabled on a workspace, it is correctly hidden on unsettled expense reports. However, once the report field is deleted from the workspace settings, the disabled field unexpectedly reappears on the unsettled report with an empty value.

### What is the root cause of that problem?
The root cause lies in how `src/libs/ReportUtils.ts:getAvailableReportFields` reconciles policy field definitions with the report's snapshot:

1. **Option Disabling Updates Policy Only**:
   When an admin disables all list options in Workspace Settings > Report Fields, Onyx updates `policy.fieldList[fieldKey].disabledOptions` to `[true, true, ...]`. Existing report snapshots (`report.fieldList`) are not mutated, so `report.fieldList[fieldKey].disabledOptions` remains `undefined`.

2. **Snapshot Overlay in `getAvailableReportFields` (lines 5190–5203)**:
   ```typescript
   if (field) {
       return {
           ...field,
           ...(policyReportField
               ? {
                     disabledOptions: policyReportField.disabledOptions,
                     values: policyReportField.values,
                 }
               : {}),
       };
   }
   ```
   - While the field still exists on the policy, `policyReportField` is present, so `disabledOptions` is overlaid onto `field`.
   - In `hasEnabledListValue(reportField)` (lines 14424–14426):
     ```typescript
     function hasEnabledListValue(reportField: PolicyReportField): boolean {
         return reportField.values.some((_, index) => !reportField.disabledOptions.at(index));
     }
     ```
     Because all options in `policyReportField.disabledOptions` are `true`, `hasEnabledListValue` returns `false`. `shouldHideSingleReportField` evaluates `!hasEnableOption` to `true` and hides the field.

3. **Regression Upon Deletion**:
   - When the field is deleted from the workspace, `policyReportFields` no longer contains the field (`policyReportField === undefined`).
   - In `getAvailableReportFields`, the spread `...(policyReportField ? ... : {})` evaluates to `{}`.
   - Consequently, `field.disabledOptions` reverts to the report snapshot's local value (`undefined`).
   - In `hasEnabledListValue`, `!reportField.disabledOptions.at(index)` evaluates `!undefined` to `true`, mistakenly considering every option enabled.
   - `shouldHideSingleReportField` now returns `false` (do not hide), causing the deleted, unselectable list field to resurrect on the unsettled report.

### What changes do you think we should make in order to solve the problem?

In `src/libs/ReportUtils.ts`:

1. **Cleanly Filter Unpopulated Deleted Fields in `getAvailableReportFields`**:
   For unsettled reports, a report field that was completely deleted from the workspace policy (`!policyReportField`) and has no entered value (`!field.value?.trim()`) cannot have options selected or edited, and should not be displayed:
   ```typescript
   const fields = mergedFieldIds.map((id) => {
       const field = report?.fieldList?.[getReportFieldKey(id)] ?? report?.fieldList?.[id];
       const policyReportField = policyReportFields.find(({fieldID}) => fieldID === id);

       if (field) {
           // If a field has been deleted from the policy and has no entered value on an unsettled report,
           // it cannot be filled and should remain hidden.
           if (!policyReportField && !field.value) {
               return null;
           }

           return {
               ...field,
               ...(policyReportField
                   ? {
                         disabledOptions: policyReportField.disabledOptions,
                         values: policyReportField.values,
                     }
                   : {}),
           };
       }

       if (policyReportField) {
           return policyReportField;
       }

       return null;
   });
   ```

2. **Preserve Historical Values on Settled / Populated Reports**:
   - If a field was previously populated by the user before deletion (`field.value` is present), `!field.value` is `false`, so the field is preserved in the list for auditability and historical record.
   - If the report is settled (`reportIsSettled === true`), lines 5181–5183 already return `reportFields` directly.
   - Only unpopulated, deleted fields on unsettled reports are omitted, matching expected design behavior.

### What alternative solutions did you explore? (Optional)
- Prop-drilling `policyFieldList` into `shouldHideSingleReportField`: Requires changing signatures across `MoneyRequestViewReportFields.tsx`, `MoneyReportView.tsx`, and `ReportUtils.ts`. Resolving it centrally at the source in `getAvailableReportFields` adheres to DRY principles and eliminates redundant prop forwarding.
- Mutating all active reports on the backend upon policy deletion: Expensive and out of scope for frontend state reconciliation.

### Test Plan
#### Automated Unit Tests (`tests/unit/ReportUtilsTest.ts`):
1. Create an unsettled report with a list field in `report.fieldList` that is missing from `policyReportFields`.
2. When `field.value` is empty, assert that `getAvailableReportFields` returns an array excluding the deleted field.
3. When `field.value` is `'Option 1'`, assert that `getAvailableReportFields` retains the deleted field with its value intact.
4. When `reportIsSettled` is `true`, assert that all snapshot fields continue to be returned.

#### Manual QA Steps:
1. Navigate to Workspace Settings > Report Fields and create a list type report field with options.
2. Open workspace chat and create a new expense report.
3. In Workspace Settings > Report Fields, disable all options for that list field.
4. Return to the expense report and verify the list field is hidden.
5. In Workspace Settings > Report Fields, delete the list field.
6. Return to the expense report.
7. **Verify:** The deleted list field remains hidden and does not reappear on the report.
8. Create another expense report and select a value for a list report field. Delete the field from workspace settings.
9. **Verify:** The entered value is still displayed on the expense report historically.

Contributor details
Your Expensify account email: jloa.dev@gmail.com
Upwork Profile Link: https://www.upwork.com/freelancers/~0163955a2ba22190aa
