## Proposal

### Please re-state the problem that we are trying to solve in this issue.
In `tests/actions/SessionTest.ts`, tests inside `describe('SAML sign out')` fail flakily with `expect(mockedOpenAuthSessionAsync).toHaveBeenCalledWith(...)` receiving 0 calls (`Number of calls: 0`), specifically when executed in shuffled or repeated test runs.

### What is the root cause of that problem?
The failure stems from a combination of un-awaited asynchronous promise chains and unrestored spies leaking across test suites from `describe('SignOutAndRedirectToSignIn')` into `describe('SAML sign out')`:

1. **Unrestored Spies in `describe('SignOutAndRedirectToSignIn')` (lines 565–620)**:
   Tests for supportal restore spy on core session methods:
   ```ts
   jest.spyOn(SessionUtil, 'isSupportAuthToken').mockReturnValue(true);
   jest.spyOn(SessionUtil, 'hasStashedSession').mockReturnValue(true);
   jest.spyOn(SessionUtil, 'signOut').mockResolvedValue(undefined);
   const onyxClearSpy = jest.spyOn(Onyx, 'clear').mockResolvedValue(undefined);
   const onyxMultiSetSpy = jest.spyOn(Onyx, 'multiSet').mockResolvedValue(undefined);
   ```
   Neither test cleans up these spies with `.mockRestore()` or an `afterEach` hook. When subsequent test suites execute, `SessionUtil.signOut` remains stubbed to resolve to `undefined` without executing the actual implementation.

2. **Un-awaited Promise Execution**:
   In lines 581 and 615:
   `signOutAndRedirectToSignIn(false, false, true, true);`
   is called without awaiting its return promise. `signOutAndRedirectToSignIn` executes an asynchronous Onyx chain (`Onyx.clear(...).then(...)`). Because this promise is not awaited, background microtasks resolve during subsequent tests, clobbering Onyx keys (`SESSION`, `CREDENTIALS`).

3. **Flawed Band-Aid in `describe('SAML sign out')` (lines 687–689)**:
   To work around the lingering spy, a comment and hook were added:
   ```ts
   // The supportal test above spies on SessionUtil.signOut and mocks it.
   // We need to restore it so our tests call the real implementation.
   beforeEach(() => {
       jest.restoreAllMocks();
   });
   ```
   However, calling `jest.restoreAllMocks()` in `beforeEach` indiscriminately restores spies and module mocks initialized for test isolation (including `TestHelper.signInWithTestUser()`, `HttpUtils.xhr`, and platform mocks), corrupting mock state whenever tests run in different ordering or concurrency.

### What changes do you think we should make in order to solve the problem?

1. **Properly Scope and Restore Spies in `describe('SignOutAndRedirectToSignIn')`**:
   In `tests/actions/SessionTest.ts`, add a scoped `afterEach` in `describe('SignOutAndRedirectToSignIn')` to guarantee all local spies are restored at the suite boundary:
   ```ts
   describe('SignOutAndRedirectToSignIn', () => {
       afterEach(() => {
           jest.restoreAllMocks();
       });
       // ...
   });
   ```
   Additionally, explicitly await the returned promise from `signOutAndRedirectToSignIn`:
   ```diff
   - signOutAndRedirectToSignIn(false, false, true, true);
   + await signOutAndRedirectToSignIn(false, false, true, true);
   ```
   and
   ```diff
   - signOutAndRedirectToSignIn(true, false, true, true);
   + await signOutAndRedirectToSignIn(true, false, true, true);
   ```

2. **Remove Broad Band-Aid and Isolate `describe('SAML sign out')`**:
   - In `describe('SAML sign out')`, remove `beforeEach(() => { jest.restoreAllMocks(); })`.
   - Add scoped cleanup for mock instances:
     ```ts
     afterEach(() => {
         mockedGetPlatform.mockReset();
         mockedOpenAuthSessionAsync.mockClear();
     });
     ```
   - In each SAML test, cleanly restore local spies (`makeRequestSpy.mockRestore()`), preserving module-level mocks.

#### Why this completely fixes the issue:
- Eliminates spy leakage at the source in `describe('SignOutAndRedirectToSignIn')`.
- Awaiting the promise prevents dangling Onyx background operations from racing against SAML tests.
- Preserves file-level mock contracts and allows `SessionTest.ts` to execute cleanly in any order, in parallel, and with repeated iterations.

### What alternative solutions did you explore? (Optional)
Placing `jest.restoreAllMocks()` in a root-level `afterEach`. This was rejected because root-level `restoreAllMocks()` tears down persistent file mocks (like `HttpUtils.xhr`), breaking subsequent describe blocks. Scoping mock restoration strictly to the describe blocks creating those spies is clean, idiomatic Jest practice.

### Test Plan
1. Run `SessionTest.ts` with repeated runs to verify flake elimination:
   ```bash
   npm test tests/actions/SessionTest.ts -- --runInBand
   ```
2. Run with reverse or randomized execution order to ensure complete isolation.
3. Verify that all 48 tests in `SessionTest.ts` pass consistently on 10+ consecutive iterations.


Contributor details
Your Expensify account email: jloa.dev@gmail.com
Upwork Profile Link: https://www.upwork.com/freelancers/~0163955a2ba22190aa
