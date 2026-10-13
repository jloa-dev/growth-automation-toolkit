## Proposal

### Please re-state the problem that we are trying to solve in this issue.
When enabling Global Reimbursement on a second USD bank account in Wallet settings, the "Registration number" field (and preceding business verification inputs) is unexpectedly prefilled with data entered during the registration of the first bank account.

### What is the root cause of that problem?
1. **Unscoped Draft Form Key**:
   In `src/pages/settings/Wallet/EnableGlobalReimbursements/EnableGlobalReimbursementsBusinessPage/subPages/RegistrationNumber.tsx:32`:
   The default form values are loaded from `ONYXKEYS.FORMS.ENABLE_GLOBAL_REIMBURSEMENTS_DRAFT`. This draft key is a single global Onyx key that is not partitioned by `bankAccountID`.
2. **Missing Post-Success / Clean-up Action**:
   In `src/libs/actions/BankAccounts.ts:1255-1285` (`enableGlobalReimbursementsForUSDBankAccount`), the `successData` resets `isEnablingGlobalReimbursements: false` and `isSuccess: true` on `ONYXKEYS.FORMS.ENABLE_GLOBAL_REIMBURSEMENTS`, but omits resetting `ONYXKEYS.FORMS.ENABLE_GLOBAL_REIMBURSEMENTS_DRAFT`.
   Furthermore, `clearEnableGlobalReimbursementsForUSDBankAccount` does not invoke `clearDraftValues(ONYXKEYS.FORMS.ENABLE_GLOBAL_REIMBURSEMENTS)`. Consequently, the previous account's registration number and business credentials remain permanently stored in Onyx.

### What changes do you think we should make in order to solve the problem?

1. **Clear Draft in `successData` via `Onyx.METHOD.SET`**:
   In `src/libs/actions/BankAccounts.ts`:
   In `enableGlobalReimbursementsForUSDBankAccount`, reset the draft in `successData`.
   *(Note: Onyx requires `Onyx.METHOD.SET` with `value: null` to completely wipe a form draft object, as `METHOD.MERGE` with `null` will not purge existing draft properties)*:
   ```typescript
   successData: [
       {
           onyxMethod: Onyx.METHOD.MERGE,
           key: ONYXKEYS.FORMS.ENABLE_GLOBAL_REIMBURSEMENTS,
           value: {
               isEnablingGlobalReimbursements: false,
               isSuccess: true,
           },
       },
       {
           onyxMethod: Onyx.METHOD.SET,
           key: ONYXKEYS.FORMS.ENABLE_GLOBAL_REIMBURSEMENTS_DRAFT,
           value: null,
       },
   ],
   ```

2. **Invoke `clearDraftValues` in Action Cleanup**:
   In `src/libs/actions/BankAccounts.ts`:
   Update `clearEnableGlobalReimbursementsForUSDBankAccount` to call:
   ```typescript
   clearDraftValues(ONYXKEYS.FORMS.ENABLE_GLOBAL_REIMBURSEMENTS);
   ```

3. **Validate `bankAccountID` on Route Entry**:
   In `src/pages/settings/Wallet/EnableGlobalReimbursements/EnableGlobalReimbursementsBusinessPage/index.tsx`:
   Store `bankAccountID` alongside the draft values. On mount, if the draft belongs to a different `bankAccountID` than the current route parameter, call `clearDraftValues(ONYXKEYS.FORMS.ENABLE_GLOBAL_REIMBURSEMENTS)`. This guarantees clean inputs across bank account switches while preserving legitimate mid-form draft recovery for the same bank account.

### What alternative solutions did you explore? (Optional)
- Using `Onyx.METHOD.MERGE` with `value: null`: Defective in Onyx for deleting draft forms. `Onyx.METHOD.SET` is required.

### What specific scenarios should we cover in automated tests?
In `tests/unit/EnableGlobalReimbursementsTest.tsx`:
1. Completing the flow for Bank Account 1 clears `ENABLE_GLOBAL_REIMBURSEMENTS_DRAFT`.
2. Navigating to Bank Account 2 presents an empty registration number field.
3. Switching between different bank accounts in Wallet resets any cross-account draft contamination.
