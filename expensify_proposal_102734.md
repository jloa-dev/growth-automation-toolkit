## Proposal

### Please re-state the problem that we are trying to solve in this issue.
In Member Security (`DomainMemberDetailsPage`), after a domain member's account has been locked due to suspicious activity, clicking "Unlock account" and confirming in the dialog submits the request, but the UI provides no indicator that the unlock request was submitted. The button remains in its active "Unlock account" state, confusing admins into repeatedly clicking it.

### What is the root cause of that problem?
In `src/libs/actions/User.ts` (line 1534):
```typescript
function requestUnlockAccount(accountID: number) {
    const params: LockAccountParams = {
        accountID,
    };

    API.write(WRITE_COMMANDS.REQUEST_UNLOCK_ACCOUNT, params);
}
```
`requestUnlockAccount` dispatches `API.write` without providing `optimisticData`.
Consequently:
1. No pending action or optimistic state is written to Onyx for the domain member or user security setting.
2. `DomainMemberDetailsPage.tsx` checks `isAccountLocked` and renders the active `MenuItemAction` for `UnlockAccount`.
3. Because Onyx state is unchanged, closing the confirmation dialog leaves the UI in the exact same state as before the request.

### What changes do you think we should make in order to solve the problem?

1. **Add Optimistic and Success Data to `requestUnlockAccount` in `src/libs/actions/User.ts`**:
   ```typescript
   function requestUnlockAccount(domainAccountID: number, accountID: number) {
       const params: LockAccountParams = {
           accountID,
       };

       const optimisticData: OnyxUpdates = [
           {
               onyxMethod: Onyx.METHOD.MERGE,
               key: `${ONYXKEYS.COLLECTION.DOMAIN_PENDING_ACTIONS}${domainAccountID}`,
               value: {
                   memberPendingActions: {
                       [accountID]: {
                           unlockAccount: CONST.RED_BRICK_ROAD_PENDING_ACTION.UPDATE,
                       },
                   },
               },
           },
       ];

       const successData: OnyxUpdates = [
           {
               onyxMethod: Onyx.METHOD.MERGE,
               key: `${ONYXKEYS.COLLECTION.DOMAIN_PENDING_ACTIONS}${domainAccountID}`,
               value: {
                   memberPendingActions: {
                       [accountID]: {
                           unlockAccount: null,
                       },
                   },
               },
           },
       ];

       API.write(WRITE_COMMANDS.REQUEST_UNLOCK_ACCOUNT, params, {optimisticData, successData});
   }
   ```

2. **In `src/pages/domain/Members/DomainMemberDetailsPage.tsx`**:
   - Check if an unlock request is pending via `domainPendingActions?.memberPendingActions?.[accountID]?.unlockAccount`.
   - When pending:
     - Display title `translate('lockAccountPage.unlockRequested')` or render `OfflineWithFeedback` / disabled state with a pending indicator.
     - Prevent duplicate invocations.

### What alternative solutions did you explore? (Optional)
- Using local React state (`useState`): Discarded because navigating away from and back to `DomainMemberDetailsPage` while offline or in-flight would lose the pending feedback. Storing the pending action in Onyx ensures resilient feedback.

### What specific scenarios should we cover in automated tests?
In `tests/ui/DomainMemberDetailsPageTest.tsx`:
1. Clicking "Unlock account" and confirming in the modal sets the optimistic pending state in Onyx.
2. The UI reflects the pending state ("Unlock requested" / disabled with pending spinner).
3. Success response clears the pending action.
