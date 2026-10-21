Contributor details
Your Expensify account email: jloa.dev@gmail.com
Upwork Profile Link: https://www.upwork.com/freelancers/~0163955a2ba221e513

## Proposal

### Please re-state the problem that we are trying to solve in this issue.
In the Collect Deposit Account flow (adding a Bank Account to Wallet as a non-admin workspace member), after reviewing and confirming bank account information, the RHP fails to dismiss. Instead, an empty "Check your info" page appears and tapping Confirm results in an unexpected error.

### What is the root cause of that problem?
1. In `src/pages/settings/Wallet/CollectDepositAccount/index.tsx`, `useSubPage` configures the sub-page navigation:
   - By default, `shouldReplaceRoute` is `false`, so each step (`Country` -> `Details` -> `Confirmation` -> `Success`) pushes a new screen instance onto the modal navigation stack via `Navigation.navigate()`.
   - When the user confirms their information on `Confirmation.tsx`, `personalBankAccount.shouldShowSuccess` becomes true. `Confirmation.tsx` calls `onNext()` (which advances to `Success`) and immediately calls `clearDraftValues(ONYXKEYS.FORMS.COLLECT_DEPOSIT_ACCOUNT_FORM)` to clean up the draft data from Onyx.
2. On the `Success` screen, tapping "Continue" (or the back button) invokes `onFinished`, which triggers `goBack()` in `CollectDepositAccount/index.tsx`:
   ```ts
   const goBack = () => {
       clearDraftValues(ONYXKEYS.FORMS.COLLECT_DEPOSIT_ACCOUNT_FORM);
       Navigation.goBack();
   };
   ```
3. A single `Navigation.goBack()` only pops the `Success` screen off the navigation stack, exposing the `Confirmation` screen that is still sitting underneath it in the stack.
4. Because the draft values were already cleared upon advancing to `Success`, the exposed `Confirmation` screen renders with empty values (showing the blank "Check your info" header without any fields).
5. If the user taps "Confirm" again on this blank screen, it submits empty parameters, causing the backend to fail and display `walletPage.addBankAccountFailure`.

### What alternative solutions did you explore? (Optional)
None, ensuring modal dismissal via `Navigation.dismissModal()` and enabling route replacement via `shouldReplaceRoute: true` aligns this flow with standard Expensify RHP patterns.

### What changes do you think we should make in order to solve the problem?

In `src/pages/settings/Wallet/CollectDepositAccount/index.tsx`:
1. Use `Navigation.dismissModal()` when dismissing/finishing the flow instead of a single `Navigation.goBack()`.
2. Set `shouldReplaceRoute: true` in `useSubPage` options so intermediate subpages replace each other in place rather than stacking up in navigation history:

```diff
--- a/src/pages/settings/Wallet/CollectDepositAccount/index.tsx
+++ b/src/pages/settings/Wallet/CollectDepositAccount/index.tsx
@@ -58,7 +58,7 @@ function CollectDepositAccount() {
     const goBack = () => {
         clearDraftValues(ONYXKEYS.FORMS.COLLECT_DEPOSIT_ACCOUNT_FORM);
-        Navigation.goBack();
+        Navigation.dismissModal();
     };
 
     const {CurrentPage, isEditing, nextPage, prevPage, pageIndex, moveTo, isRedirecting} = useSubPage<CustomSubPageProps>({
@@ -66,6 +66,7 @@ function CollectDepositAccount() {
         startFrom: STEP_INDEXES.COUNTRY_SELECTOR,
         onFinished: goBack,
+        shouldReplaceRoute: true,
         buildRoute: (pageName, action) => ROUTES.SETTINGS_COLLECT_DEPOSIT_ACCOUNT.getRoute(pageName, action),
     });
```

### What automated tests can you add to prevent this from re-occurring?
Add a unit test in `tests/unit/pages/CollectDepositAccountTest.tsx` verifying that:
1. Advancing through `CollectDepositAccount` replaces subpage routes without stacking multiple instances.
2. Invoking `onFinished` on the `Success` page invokes `Navigation.dismissModal()`, cleanly closing the entire RHP.
