Contributor details
Your Expensify account email: jloa.dev@gmail.com
Upwork Profile Link: https://www.upwork.com/freelancers/~0163955a2ba22190aa

## Proposal

### Please re-state the problem that we are trying to solve in this issue.
When adding a US bank account and entering an address that includes Address Line 2 (`addressStreet2`), the address is not properly stored by the backend, resulting in a persistent "Review" badge on the added bank account.

### What is the root cause of that problem?
In `src/libs/actions/BankAccounts.ts` (`addPersonalBankAccount`), line 564 constructs the API payload by merging `addressStreet` and `addressStreet2` into a single string with a newline:
```ts
addressStreet: getFormattedStreet(account?.addressStreet, account?.addressStreet2),
```
1. `AddPersonalBankAccountParams.ts` does not define `addressStreet2`, so `addressStreet2` is omitted from the API payload.
2. The backend `AddPersonalBankAccount` handler expects `addressStreet` and `addressStreet2` as distinct parameters (mirroring the contract in `UpdatePersonalBankAccountInfo` established in PR #90350) and rejects street values containing embedded newline (`\n`) characters.
3. Because the street validation fails on the backend, `additionalData.addressStreet` remains missing, and `isPersonalBankAccountMissingInfo` evaluates to `true`, displaying the "Review" indicator on the bank account row in Wallet.
4. Additionally, `ConfirmationStep.tsx` only renders `bankAccountPersonalDetails?.addressStreet`, omitting `addressStreet2` from the review preview when present.

### What changes do you think we should make in order to solve the problem?

1. In `src/libs/API/parameters/AddPersonalBankAccountParams.ts`:
Add optional `addressStreet2?: string;`:
```diff
--- a/src/libs/API/parameters/AddPersonalBankAccountParams.ts
+++ b/src/libs/API/parameters/AddPersonalBankAccountParams.ts
@@ -13,6 +13,7 @@ type AddPersonalBankAccountParams = {
     legalFirstName?: string;
     legalLastName?: string;
     addressStreet?: string;
+    addressStreet2?: string;
     addressCity?: string;
     addressState?: string;
     addressZip?: string;
```

2. In `src/libs/actions/BankAccounts.ts` (`addPersonalBankAccount`):
Pass `addressStreet` and `addressStreet2` as separate fields instead of concatenating them with a newline:
```diff
--- a/src/libs/actions/BankAccounts.ts
+++ b/src/libs/actions/BankAccounts.ts
@@ -561,7 +561,8 @@ function addPersonalBankAccount(
         phoneNumber: account?.phoneNumber,
         legalFirstName: account?.legalFirstName,
         legalLastName: account?.legalLastName,
-        addressStreet: getFormattedStreet(account?.addressStreet, account?.addressStreet2),
+        addressStreet: account?.addressStreet,
+        addressStreet2: account?.addressStreet2 ?? '',
         addressCity: account?.addressCity,
         addressState: account?.addressState,
         addressZip: account?.addressZipCode,
```

3. In `src/pages/AddPersonalBankAccountPage/substeps/ConfirmationStep.tsx`:
Display both street lines in the address preview if `addressStreet2` is present:
```diff
--- a/src/pages/AddPersonalBankAccountPage/substeps/ConfirmationStep.tsx
+++ b/src/pages/AddPersonalBankAccountPage/substeps/ConfirmationStep.tsx
@@ -41,7 +41,9 @@ function ConfirmationStep({onNext, onMove, isEditing}: SubPageProps) {
             phoneNumber: (phone && formatE164PhoneNumber(phone, countryCode)) ?? '',
             legalFirstName: bankAccountPersonalDetails?.legalFirstName ?? privatePersonalDetails?.legalFirstName ?? '',
             legalLastName: bankAccountPersonalDetails?.legalLastName ?? privatePersonalDetails?.legalLastName ?? '',
-            addressStreet: bankAccountPersonalDetails?.addressStreet ?? currentAddress?.street ?? '',
+            addressStreet: bankAccountPersonalDetails?.addressStreet2
+                ? `${bankAccountPersonalDetails.addressStreet}, ${bankAccountPersonalDetails.addressStreet2}`
+                : (bankAccountPersonalDetails?.addressStreet ?? currentAddress?.street ?? ''),
             addressCity: bankAccountPersonalDetails?.addressCity ?? currentAddress?.city ?? '',
             addressState: bankAccountPersonalDetails?.addressState ?? currentAddress?.state ?? '',
             addressZip: bankAccountPersonalDetails?.addressZipCode ?? currentAddress?.zip ?? '',
```

### What alternative solutions did you explore? (Optional)
Concatenating with comma on client side (`${street1}, ${street2}`): Rejected because the backend database schema stores Address Line 1 and Line 2 in distinct database columns. Sending them as separate API parameters matches the convention used across all other bank account endpoints (such as `UpdatePersonalBankAccountInfo`).
