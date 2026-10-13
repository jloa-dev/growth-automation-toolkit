## Proposal

### Please re-state the problem that we are trying to solve in this issue.
When a workspace already has custom approval workflows configured (e.g. multiple approvers or custom rules) and Gusto is connected via Workspace Settings > More features > HR, the Gusto approval mode is displayed and defaulted to "Manager approval" instead of preserving "Custom approval".

### What is the root cause of that problem?
In PR #102750, support was added to keep approval workflow rules working with HR integrations (`hasApprovalWorkflowRules`). However:
1. In `src/pages/workspace/hr/utils.ts` and `src/pages/workspace/hr/HRApprovalModePageBase.tsx`:
   - `getCurrentApprovalMode` reads `policy?.connections?.gusto?.config?.approvalMode`.
   - When Gusto is newly connected, `approvalMode` is not yet explicitly set in the connection config.
   - `getHRApprovalMode` in `src/libs/merge/HRUtils.ts` falls back to `null`, and `getApprovalModeLabel` or default selection fails to inspect whether the workspace already has custom approval workflow rules.
   - As a result, the UI falls back to the default HR provider behavior, showing "Manager approval", which risks deleting existing custom workflow rules upon saving.

### What changes do you think we should make in order to solve the problem?

1. **Update `getHRApprovalMode` in `src/libs/merge/HRUtils.ts`**:
   Accept `rulesCollection?: OnyxCollection<Rule>` (or policyID) and default unconfigured HR connections to `CUSTOM` if the workspace has active approval workflow rules:
   ```typescript
   function getHRApprovalMode(
       policy?: OnyxEntry<Policy>,
       connectionName?: HRConnectionName,
       rules?: OnyxCollection<Rule>,
   ): ValueOf<typeof CONST.GUSTO.APPROVAL_MODE> | ValueOf<typeof CONST.ZENEFITS.APPROVAL_MODE> | MergeApprovalMode | null {
       if (!connectionName || !policy?.connections) {
           return null;
       }
       const configuredMode = policy.connections[connectionName]?.config?.approvalMode;
       if (configuredMode) {
           return configuredMode;
       }
       // If the workspace already has custom approval workflow rules, default to CUSTOM approval
       if (hasApprovalWorkflowRules(rules, policy?.id)) {
           return CONST.GUSTO.APPROVAL_MODE.CUSTOM;
       }
       return null;
   }
   ```

2. **In `src/pages/workspace/hr/HRApprovalModePageBase.tsx`**:
   Pass `rules` to derive `currentApprovalMode` so that if no approval mode was explicitly stored yet on the connection, it correctly preselects `CUSTOM`:
   ```typescript
   const currentApprovalMode = config.getCurrentApprovalMode(policy, rules) ?? (hasApprovalWorkflowRules(rules, policyID) ? config.approvalModes.CUSTOM : config.approvalModes.MANAGER);
   ```

3. **In `src/pages/workspace/hr/gusto/GustoApprovalModePage.tsx`**:
   Update `getCurrentApprovalMode` config signature to support rule detection:
   ```typescript
   getCurrentApprovalMode: (policy, rules) => policy?.connections?.gusto?.config?.approvalMode ?? (hasApprovalWorkflowRules(rules, policyID) ? CONST.GUSTO.APPROVAL_MODE.CUSTOM : undefined),
   ```

### What alternative solutions did you explore? (Optional)
- Only changing the display label in `utils.ts`: Insufficient because `HRApprovalModePageBase` would still stage `MANAGER` mode upon save, triggering the prompt to delete workflow rules.

### What specific scenarios should we cover in automated tests?
In `tests/unit/WorkflowUtilsTest.ts` and `tests/unit/HRConnectionActionTest.ts`:
1. Workspace with 2+ approvers (custom workflow rules) connecting Gusto defaults to `CUSTOM` approval mode.
2. Workspace with default/single approver without custom rules defaults to standard manager or basic mode.
3. Verify that saving in custom mode does not delete approval workflow rules in Onyx.
