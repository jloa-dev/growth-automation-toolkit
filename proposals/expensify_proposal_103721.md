## Proposal

### Please re-state the problem that we are trying to solve in this issue.
In the Per Diem flow, after selecting a workspace while offline and subsequently regaining network connection, navigating to the Destination step flashes or permanently renders the "Not here" (404) page instead of loading the per diem rates and destinations.

### What is the root cause of that problem?
There are two primary causes interacting between the workspace selection and destination steps:

1. **Workspace Policy Dropped in Track Flow**:
   In `src/pages/iou/request/step/IOURequestStepPerDiemWorkspace.tsx:78-90`:
   ```typescript
   if (targetIouType === CONST.IOU.TYPE.TRACK) {
       setMoneyRequestParticipantsFromReport(transactionID, targetReport, accountID, false);
   } else {
       setMoneyRequestParticipants(transactionID, [
           {
               selected: true,
               accountID: 0,
               isPolicyExpenseChat: true,
               reportID: targetReport.reportID,
               policyID: policy?.id,
           },
       ]);
   }
   ```
   In the `TRACK` branch (such as within a self-DM), `setMoneyRequestParticipantsFromReport` sets `policyID: undefined` on the draft transaction participants. Consequently, when `DynamicIOURequestStepDestination.tsx` attempts to resolve the policy via `getIOURequestPolicyID(transaction, report)`, it falls back to `report.policyID` (`CONST.POLICY.ID_FAKE`).

2. **Premature 404 Render without Loading Guards**:
   In `src/pages/iou/request/step/DynamicIOURequestStepDestination.tsx:121`:
   ```typescript
   const shouldShowNotFoundPage = isEmptyObject(policy);
   ```
   When the destination mounts or transitions online, `policy` is temporarily undefined before Onyx finishes resolving the collection key `${ONYXKEYS.COLLECTION.POLICY}${policyID}`. Because `shouldShowNotFoundPage` is not guarded by `isLoadingOnyxValue(policyMetadata)` or `isOffline`, the component immediately trips to `NotFoundPage`.

### What changes do you think we should make in order to solve the problem?

1. **Preserve `policyID` in `IOURequestStepPerDiemWorkspace.tsx`**:
   In `selectWorkspace`, ensure the selected workspace `policyID` is persisted on the draft transaction participant in the `TRACK` branch as well:
   ```typescript
   if (targetIouType === CONST.IOU.TYPE.TRACK) {
       setMoneyRequestParticipantsFromReport(transactionID, targetReport, accountID, false);
       setMoneyRequestParticipants(transactionID, [
           {
               accountID,
               policyID: policy?.id,
               reportID: targetReport.reportID,
           },
       ]);
   }
   ```

2. **Guard `shouldShowNotFoundPage` in `DynamicIOURequestStepDestination.tsx`**:
   Ensure `NotFoundPage` does not render while Onyx is actively loading or while disconnected:
   ```diff
   -const shouldShowNotFoundPage = isEmptyObject(policy);
   +const shouldShowNotFoundPage = isEmptyObject(policy) && !isLoadingOnyxValue(policyMetadata) && !isOffline;
   ```

3. **Auto-Retry Per Diem Rates on Reconnection**:
   In `IOURequestStepPerDiemWorkspace.tsx`, register `onReconnect` via `useNetwork` so that if `pendingPolicyID` was waiting for rates while offline, `fetchPerDiemRates(pendingPolicyID)` re-triggers as soon as the client comes back online.

### What alternative solutions did you explore? (Optional)
- Passing `policyID` solely through route params: Not ideal, as draft transaction state in Onyx should remain the source of truth across step navigations.

### What specific scenarios should we cover in automated tests?
In `tests/unit/DynamicIOURequestStepDestinationTest.tsx` and `tests/unit/IOURequestStepPerDiemWorkspaceTest.tsx`:
1. When selecting a workspace offline in the Track flow, assert `policyID` is preserved on the draft participants.
2. When navigating to `DynamicIOURequestStepDestination` with unloaded policy metadata, assert `NotFoundPage` does not render.
