Contributor details
Your Expensify account email: jloa.dev@gmail.com
Upwork Profile Link: https://www.upwork.com/freelancers/~0163955a2ba22190aa

## Proposal

### Please re-state the problem that we are trying to solve in this issue.
When navigating to the "Verify Domain" page while offline or after a transient network failure, the page shows a "Couldn't fetch verification code" error. Once internet connection is restored, returning to the page or staying on it leaves the error stuck on screen, preventing the user from ever loading the DNS verification code.

### What is the root cause of that problem?
1. When opening the verification page without internet connectivity, `getDomainValidationCode` calls `API.read(READ_COMMANDS.GET_DOMAIN_VALIDATE_CODE)`. When this fails, Onyx receives and persists `validateCodeError` on the domain collection (`ONYXKEYS.COLLECTION.DOMAIN${accountID}`).
2. In `src/pages/domain/BaseVerifyDomainPage.tsx:95-100`:
   ```typescript
   useFocusEffect(() => {
       if (isVerifiedDomainAdmin || !domainName || domain?.validateCode || domain?.isValidateCodeLoading || domain?.validateCodeError) {
           return;
       }
       getDomainValidationCode(domainAccountID, domainName);
   });
   ```
   `useFocusEffect` explicitly checks `domain?.validateCodeError`. If it is truthy, it returns immediately without fetching.
3. On mount, `BaseVerifyDomainPage.tsx:102-107` executes:
   ```typescript
   useEffect(() => {
       if (!doesDomainExist) {
           return;
       }
       resetDomainValidationError(domainAccountID);
   }, [domainAccountID, doesDomainExist]);
   ```
   However, in `src/libs/actions/Domain.ts:125-127`:
   ```typescript
   function resetDomainValidationError(accountID: number) {
       Onyx.merge(`${ONYXKEYS.COLLECTION.DOMAIN}${accountID}`, {domainValidationError: null});
   }
   ```
   `resetDomainValidationError` only resets `domainValidationError: null`. It fails to clear `validateCodeError: null` and `isValidateCodeLoading: null`.
4. Because `validateCodeError` is never cleared on mount or focus, subsequent navigations to the page are perpetually blocked by the `useFocusEffect` guard.
5. In addition, `BaseVerifyDomainPage` does not subscribe to network reconnections via `useNetwork({onReconnect})`, meaning a user who remains on the page while reconnecting is never automatically retried.

### What changes do you think we should make in order to solve the problem?
1. **Extend `resetDomainValidationError` to clear validation code state**:
   In `src/libs/actions/Domain.ts`, update `resetDomainValidationError` to clear both `validateCodeError` and `isValidateCodeLoading`:
   ```diff
   diff --git a/src/libs/actions/Domain.ts b/src/libs/actions/Domain.ts
   --- a/src/libs/actions/Domain.ts
   +++ b/src/libs/actions/Domain.ts
   @@ -125,3 +125,7 @@ function resetDomainValidationError(accountID: number) {
   -    Onyx.merge(`${ONYXKEYS.COLLECTION.DOMAIN}${accountID}`, {domainValidationError: null});
   +    Onyx.merge(`${ONYXKEYS.COLLECTION.DOMAIN}${accountID}`, {
   +        domainValidationError: null,
   +        validateCodeError: null,
   +        isValidateCodeLoading: null,
   +    });
    }
   ```
2. **Add Network Reconnect Hook in `BaseVerifyDomainPage.tsx`**:
   In `src/pages/domain/BaseVerifyDomainPage.tsx`, wire `useNetwork({onReconnect})` to re-trigger code fetching when connectivity is restored:
   ```typescript
   const fetchValidationCode = useCallback(() => {
       if (isVerifiedDomainAdmin || !domainName || domain?.validateCode || domain?.isValidateCodeLoading) {
           return;
       }
       getDomainValidationCode(domainAccountID, domainName);
   }, [domainAccountID, domainName, domain?.validateCode, domain?.isValidateCodeLoading, isVerifiedDomainAdmin]);

   useNetwork({onReconnect: fetchValidationCode});
   ```

### What alternative solutions did you explore? (Optional)
- **Only clearing `validateCodeError` when unmounting**:
  Rejected because if the app is killed or refreshed while on the page, the unmount cleanup never fires, leaving the error permanently stored in Onyx. Resetting on mount in `resetDomainValidationError` ensures consistency across fresh launches and page re-entries.

### What specific scenarios should we cover in automated tests?
In `tests/ui/BaseVerifyDomainPageTest.tsx`:
1. Verify that when `BaseVerifyDomainPage` mounts with existing `validateCodeError` in Onyx, `resetDomainValidationError` resets the error and initiates `getDomainValidationCode`.
2. Verify that when online connectivity resumes (`onReconnect`), `getDomainValidationCode` is called if the code was not yet populated.
