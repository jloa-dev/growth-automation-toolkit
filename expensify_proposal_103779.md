## Proposal

### Please re-state the problem that we are trying to solve in this issue.
In a TriNet-connected workspace, the **Final approver** configuration row disappears from the HR TriNet settings card when the workspace approval mode is switched to **Custom approval**.

### What is the root cause of that problem?
In [`src/pages/workspace/hr/utils.ts#L214-L227`](https://github.com/Expensify/App/blob/main/src/pages/workspace/hr/utils.ts#L214-L227), `getHRCards` builds the configuration rows for connected HR providers. It deliberately restricts `finalApproverRows` so they are only included when `!isCustomApproval`:

```ts
const finalApproverRows: MergeProviderConfigRow[] = !isCustomApproval && provider.finalApproverRoute
    ? [{
        field: 'finalApprover',
        description: translate('workspace.merge.finalApprover'),
        title: getMergeFinalApproverDisplayName(config?.finalApprover, policyEmployeePersonalDetails, translate, formatPhoneNumber),
        route: provider.finalApproverRoute.getRoute(policyID),
        pendingAction: config?.pendingFields?.finalApprover,
        errors: config?.errorFields?.finalApprover,
    }]
    : [];
```
The exact same condition exists in the Merge HR loop ([lines 263–276](https://github.com/Expensify/App/blob/main/src/pages/workspace/hr/utils.ts#L263-L276)). 

However, `config.finalApprover` remains persisted in Onyx, and the underlying backend and final approver pages continue to operate normally. Hiding the row completely prevents administrators from inspecting, configuring, or updating their TriNet final approver while on Custom approval mode.

### What changes do you think we should make in order to solve the problem?
1. In `src/pages/workspace/hr/utils.ts` within `getHRCards`, remove the `!isCustomApproval` restriction so that `finalApproverRows` is always created when `provider.finalApproverRoute` is available.
2. Deduplicate the row builder by extracting a shared helper function `getFinalApproverConfigRow(...)` used by both the static HR provider block and the dynamic Merge HR provider loop.
3. Update unit tests in `tests/unit/HrUtilsTest.ts` to verify that `finalApprover` row is included in the returned config rows for Gusto, TriNet, and Merge HR cards even when `isCustomApproval` is true.

### What alternative solutions did you explore? (Optional)
- Making the row visible but disabled in Custom mode: unnecessary since updating the final approver on the destination page is valid and doesn't conflict with custom rules.
