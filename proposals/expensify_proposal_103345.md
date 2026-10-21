Contributor details
Your Expensify account email: jloa.dev@gmail.com
Upwork Profile Link: https://www.upwork.com/freelancers/~0163955a2ba22190aa

## Proposal

### Please re-state the problem that we are trying to solve in this issue.
The app crashes with an unhandled `URIError: URI malformed` when adding or navigating to a contact method containing a `%` symbol in the email address (e.g. `test%alias@gmail.com`), preventing the user from viewing or managing their contact methods.

### What is the root cause of that problem?
1. In `src/ROUTES.ts`, `DYNAMIC_ROUTES.CONTACT_METHOD_DETAILS.getRoute(contactMethod)` encodes the contact method once with `encodeURIComponent(contactMethod)`.
2. When navigating to the route, React Navigation's path matcher (`getStateFromPath` / `linkingConfig`) parses the `:contactMethod` path parameter and executes `decodeURIComponent` once on the segment. Consequently, `route.params.contactMethod` is delivered to screen components as the fully decoded string (e.g., `test%alias@gmail.com`).
3. In `DynamicContactMethodDetailsPage.tsx:91` and `SetDefaultContactMethodConfirmValidateCodePage.tsx:21`, the param is passed to `getDecodedContactMethodFromUriParam(route.params.contactMethod)`.
4. In `src/pages/settings/Profile/Contacts/utils.ts:8-23`:
   ```typescript
   function getDecodedContactMethodFromUriParam(contactMethodParam: string) {
       const lastPercentIndex = contactMethodParam.lastIndexOf('%');
       const encodePercents = contactMethodParam.substring(lastPercentIndex).match(/25/g);
       ...
       return addSMSDomainIfPhoneNumber(decodeURIComponent(beforeAtSign + afterAtSign));
   }
   ```
   `getDecodedContactMethodFromUriParam` attempts to run `decodeURIComponent` a second time on the already-decoded string.
5. In an email such as `test%alias@gmail.com`, `%al` is not a valid two-digit hex escape sequence (`%HH`). Passing this to `decodeURIComponent` causes the JavaScript runtime to throw `URIError: URI malformed`. Because this executes during component rendering inside `useMemo`, it crashes the screen and hits the error boundary.
6. Furthermore, running a redundant second `decodeURIComponent` corrupts valid email addresses containing hex-like sequences (e.g. `user%40domain@example.com` would mutate to `user@domain@example.com`, causing `loginList[contactMethod]` lookups to fail).

### What changes do you think we should make in order to solve the problem?
1. **Clean up `getDecodedContactMethodFromUriParam`**:
   In `src/pages/settings/Profile/Contacts/utils.ts`, remove the redundant second `decodeURIComponent` and percent-counting string replacement logic. Delegate directly to `addSMSDomainIfPhoneNumber(contactMethodParam)`:
   ```typescript
   import {addSMSDomainIfPhoneNumber} from '@libs/PhoneNumber';

   /**
    * Decodes the contact method from the route params
    */
   function getDecodedContactMethodFromUriParam(contactMethodParam: string) {
       return addSMSDomainIfPhoneNumber(contactMethodParam);
   }

   export default getDecodedContactMethodFromUriParam;
   ```
2. **Remove Orphaned Regex in `CONST`**:
   In `src/CONST/index.ts`, remove `ENCODE_PERCENT_CHARACTER: /%(25)+/g`, as it is not used anywhere else in the codebase.
3. **Automated Unit Tests**:
   Create a dedicated unit test suite in `tests/unit/ContactUtilsTest.ts` to lock in behavior and prevent future regressions.

### What alternative solutions did you explore? (Optional)
- Wrapping `decodeURIComponent` in a `try/catch` fallback:
  Rejected because a `try/catch` would still silently corrupt valid emails containing legitimate hex escapes (such as `user%20name@test.com` or `user%40tag@test.com`), converting them to spaces or `@` and desyncing the contact method key from Onyx `loginList`. Because React Navigation guarantees route params are already decoded once, stripping the duplicate decode is the clean, idempotent solution.

### What specific scenarios should we cover in automated tests?
In `tests/unit/ContactUtilsTest.ts`:
1. **Emails with non-hex `%` characters**: `user%alias@gmail.com` decodes safely without throwing `URIError`.
2. **Emails with hex-like escapes**: `user%40tag@gmail.com` preserves literal characters intact and does not get double-decoded to `user@tag@gmail.com`.
3. **Standard email addresses**: `john@gmail.com` remains unchanged.
4. **Phone numbers**: `+15551234567` correctly appends the `@expensify.sms` domain.
5. **Phone numbers already with SMS domain**: `+15551234567@expensify.sms` remains unchanged.
