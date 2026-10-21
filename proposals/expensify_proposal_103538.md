## Proposal

### Please re-state the problem that we are trying to solve in this issue.
In Account > Wallet, when a user edits the nickname of a business bank account and saves it, refreshing the page reverts the displayed bank account name back to the default bank name.

### What is the root cause of that problem?
When `updateBankAccountName` is called in `src/libs/actions/BankAccounts.ts`, it sends the `UpdateBankAccount` API request with `{bankAccountID, addressName: newName}`. The backend successfully persists the nickname in `addressName` and returns the bank account object on subsequent `OpenPaymentsPage` fetches (such as on page refresh) with `accountData.addressName` set to the nickname, while `title` is set to the masked account number (containing `CONST.MASKED_PAN_PREFIX`, e.g. `XXXXX1111`).

However, in `src/pages/settings/Wallet/PaymentMethodList.tsx:624`:
```typescript
title: paymentMethod.title?.includes(CONST.MASKED_PAN_PREFIX) ? paymentMethod.accountData?.additionalData?.bankName : paymentMethod.title,
```
and in `src/pages/settings/Wallet/EditBankAccountNicknamePage.tsx:39`:
```typescript
const defaultValue = bankAccount?.title?.includes(CONST.MASKED_PAN_PREFIX) ? bankAccount?.accountData?.additionalData?.bankName : bankAccount?.title;
```
Both places check whether `title` includes `CONST.MASKED_PAN_PREFIX` and immediately fall back to `additionalData.bankName` (the default bank name, e.g. "Chase"), without ever reading `accountData.addressName`. 

Because `accountData.addressName` is ignored, whenever the page is refreshed and the server sends down the bank account data, the presence of the masked account prefix in `title` causes the frontend to overwrite the name with `additionalData.bankName`, reverting the nickname back to the default bank name.

### What changes do you think we should make in order to solve the problem?
1. In `src/pages/settings/Wallet/PaymentMethodList.tsx:624`:
Prioritize `paymentMethod.accountData?.addressName` before checking the masked title fallback:
```typescript
title: paymentMethod.accountData?.addressName || (paymentMethod.title?.includes(CONST.MASKED_PAN_PREFIX) ? paymentMethod.accountData?.additionalData?.bankName : paymentMethod.title),
```

2. In `src/pages/settings/Wallet/EditBankAccountNicknamePage.tsx:39`:
Similarly prioritize `accountData.addressName`:
```typescript
const defaultValue = bankAccount?.accountData?.addressName || (bankAccount?.title?.includes(CONST.MASKED_PAN_PREFIX) ? bankAccount?.accountData?.additionalData?.bankName : bankAccount?.title);
```

3. Update the unit tests in `tests/ui/EditBankAccountNicknamePageTest.tsx` and `tests/actions/BankAccountsTest.ts` to assert that when `title` is a masked PAN and `accountData.addressName` is set, `accountData.addressName` is used as the display name and form default value.

### What alternative solutions did you consider?
Reverting the PR: as noted by MelvinBot, reverting the entire feature loses the functionality for users. The fix is a one-line resolution reading `accountData.addressName` which is already saved by the backend.
