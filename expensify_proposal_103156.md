## Proposal

### Please re-state the problem that we are trying to solve in this issue.
When attempting to unlock a locked bank account while offline in Workspace settings > Workflows > Payment, Concierge does not open. Instead, an alert stating "Request already submitted" is displayed, creating a dead-end without navigating to Concierge.

### What is the root cause of that problem?
There are two distinct root causes contributing to this issue:

1. **Persistent NVP Guard and Dead-End Modal on Retest**:
   In `src/pages/workspace/workflows/tabs/WorkflowsPaymentsTab.tsx:225-233`:
   ```typescript
   if (state === CONST.BANK_ACCOUNT.STATE.LOCKED && bankAccountID && isUserReimburser) {
       if (unlockRequestedAt) {
           showUnlockAlreadyRequestedModal(showConfirmModal, translate);
           return;
       }
       pressLockedBankAccount(bankAccountID, translate, conciergeReportID ?? undefined, delegateAccountID, initiatingBankAccountUnlock);
       navigateToConciergeChat({conciergeReportID: conciergeReportID ?? undefined, introSelected, currentUserAccountID, isSelfTourViewed, conciergePersonalDetails});
       return;
   }
   ```
   When an unlock request has been initiated previously (e.g. on shared test accounts like `applausetester+lockedba@applause.expensifail.com`), `unlockRequestedAt` (`nvp_expensify_vbaUnlockRequested_<bankAccountID>`) is already populated in Onyx.
   `showUnlockAlreadyRequestedModal` in `src/libs/BankAccountUtils.ts:291-298` renders a single-button modal (`common.buttonConfirm`) and immediately returns without offering navigation to Concierge.

2. **Offline Navigation Block in `navigateToConciergeChat`**:
   In `src/libs/actions/Report/index.ts:4491-4494`:
   ```typescript
   if (!conciergeReportID) {
       return onServerDataReady().then(() => {
           // ...
       });
   }
   ```
   If `conciergeReportID` is undefined when offline, `navigateToConciergeChat` waits for `onServerDataReady()`, which hangs indefinitely while disconnected from the internet, preventing the app from opening Concierge.

### What changes do you think we should make in order to solve the problem?

1. **Allow Direct Navigation to Concierge from `showUnlockAlreadyRequestedModal`**:
   In `src/libs/BankAccountUtils.ts`, update `showUnlockAlreadyRequestedModal` to accept an `onNavigateToConcierge` callback:
   ```typescript
   function showUnlockAlreadyRequestedModal(
       showConfirmModal: ReturnType<typeof useConfirmModal>['showConfirmModal'],
       translate: LocaleContextProps['translate'],
       onConfirm?: () => void,
   ) {
       showConfirmModal({
           title: translate('bankAccount.unlockAlreadyRequestedTitle'),
           prompt: translate('bankAccount.unlockAlreadyRequestedDescription'),
           confirmText: translate('bankAccount.viewConciergeChat'),
           cancelText: translate('common.cancel'),
           shouldShowCancelButton: true,
           onConfirm,
       });
   }
   ```
   In `WorkflowsPaymentsTab.tsx`:
   ```typescript
   if (unlockRequestedAt) {
       showUnlockAlreadyRequestedModal(showConfirmModal, translate, () => {
           navigateToConciergeChat({conciergeReportID: conciergeReportID ?? undefined, introSelected, currentUserAccountID, isSelfTourViewed, conciergePersonalDetails});
       });
       return;
   }
   ```

2. **Offline Resilient Concierge Routing**:
   In `navigateToConciergeChat`, if offline and `conciergeReportID` is undefined, check for any cached Concierge report in `allReports` by matching `CONST.EMAIL.CONCIERGE` / `CONST.ACCOUNT_ID.CONCIERGE` instead of stalling on `onServerDataReady()`.

3. **QA Environment Step Clarification**:
   Document in the test instructions that fresh account verification requires either a bank account without prior unlock NVP or clearing `nvp_expensify_vbaUnlockRequested_<bankAccountID>`.

### What alternative solutions did you explore? (Optional)
- Silently bypassing `unlockRequestedAt`: Not recommended, because duplicate backend unlock tickets should not be generated for the same bank account.

### What specific scenarios should we cover in automated tests?
In `tests/unit/WorkflowsPaymentsTabTest.tsx` and `tests/unit/BankAccountsTest.ts`:
1. When `unlockRequestedAt` is present, clicking Unlock shows the modal with the option to navigate to Concierge.
2. When offline and clicking Unlock for the first time, `pressLockedBankAccount` optimistically creates the concierge report action and triggers navigation to Concierge.
