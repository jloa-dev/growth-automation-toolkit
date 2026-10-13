## Proposal

### Please re-state the problem that we are trying to solve in this issue.
When selecting a workspace on the Per Diem tab where per diem rates have not yet loaded, the app navigates immediately to a separate Destination screen that displays a full-screen spinner with a header back arrow, completely hiding the tab bar.

### What is the root cause of that problem?
In `src/pages/iou/request/step/IOURequestStepPerDiemWorkspace.tsx:70-75`:
```typescript
const canDestinationResolvePolicy = !!perDiemUnit || (!!targetReport.policyID && targetReport.policyID !== CONST.POLICY.ID_FAKE);
if (!canDestinationResolvePolicy) {
    setPendingPolicyID(policy?.id);
    return;
}
```
1. **Premature Navigation via Short-Circuiting**:
   For any standard policy expense chat, `targetReport.policyID` is valid (not `CONST.POLICY.ID_FAKE`). Therefore, `canDestinationResolvePolicy` evaluates to `true` even when `perDiemUnit` is completely `undefined` and its rates have not arrived yet.
   As a result, `selectWorkspace` skips the in-tab pending state (`pendingPolicyID`) and immediately calls:
   ```typescript
   Navigation.navigate(
       createDynamicRoute(DYNAMIC_ROUTES.MONEY_REQUEST_STEP_DESTINATION.path, ROUTES.MONEY_REQUEST_CREATE.getRoute(action, targetIouType, transactionID, targetReport.reportID)),
   );
   ```

2. **Destination Step Full-Screen Loading**:
   Once navigated to `DynamicIOURequestStepDestination.tsx`, because per diem rates are still missing, `DynamicIOURequestStepDestination` renders its own `FullScreenLoadingIndicator` inside a pushed `StepScreenWrapper`. This pushed screen has its own header back button (`<`) and is outside the tab navigator, causing the tab bar to disappear while loading.

### What changes do you think we should make in order to solve the problem?

1. **Gate Destination Navigation on Per Diem Unit / Rates Resolution**:
   In `src/pages/iou/request/step/IOURequestStepPerDiemWorkspace.tsx`:
   Require the per diem custom unit to be loaded before navigating away from the workspace selection step:
   ```diff
   -const canDestinationResolvePolicy = !!perDiemUnit || (!!targetReport.policyID && targetReport.policyID !== CONST.POLICY.ID_FAKE);
   +const canDestinationResolvePolicy = !!perDiemUnit && (!!targetReport.policyID && targetReport.policyID !== CONST.POLICY.ID_FAKE);
    if (!canDestinationResolvePolicy) {
        setPendingPolicyID(policy?.id);
        return;
    }
   ```
   Or explicitly check `if (!perDiemUnit) { setPendingPolicyID(policy?.id); return; }`.

2. **In-Tab Loading Indicator**:
   When `pendingPolicyID` is set, render the in-tab activity indicator within the tab container (preserving the tab bar and header) rather than pushing a new screen.
   The existing `useEffect` in lines 99-106 will then cleanly fire `selectWorkspace(pendingPolicy)` once `pendingPolicy` receives `perDiemUnit` via Onyx, smoothly transitioning to Destination with rates already available.

### What alternative solutions did you explore? (Optional)
- Gating inside `DynamicIOURequestStepDestination.tsx`: Not recommended, because navigating to a pushed screen only to show a spinner defeats the purpose of keeping tab navigation visible.

### What specific scenarios should we cover in automated tests?
In `tests/unit/IOURequestStepPerDiemWorkspaceTest.tsx`:
1. Render `IOURequestStepPerDiemWorkspace` with multiple workspaces where the selected workspace has not yet cached per diem custom units.
2. Verify that clicking the workspace sets `pendingPolicyID` and keeps the user on the workspace step without firing navigation.
3. Simulate Onyx updating with the policy's per diem custom unit and assert navigation to `MONEY_REQUEST_STEP_DESTINATION` is triggered with the tab bar preserved up until navigation.
