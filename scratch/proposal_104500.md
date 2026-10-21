## Proposal

### Please re-state the problem that we are trying to solve in this issue.
While a custom agent is processing a request in a thread (before comments or replies have landed), the thread preview under the parent action in the chat displays a generic fallback avatar instead of the agent's real avatar.

### What is the root cause of that problem?
In `src/pages/inbox/report/ReportActionItemThread.tsx` (lines 61-66):
```ts
const childAccountIDs =
    reportAction.childOldestFourAccountIDs
        ?.split(',')
        .map((accountID) => Number(accountID))
        .filter((accountID): accountID is number => typeof accountID === 'number') ?? [];
const accountIDs = childAccountIDs.length === 0 && processingAgentIDs ? processingAgentIDs : childAccountIDs;
```
When a thread has no comments yet, `reportAction.childOldestFourAccountIDs` is initialized or sent as an empty string `''` (e.g. in `ReportUtils.updateOptimisticParentReportAction` line 7339: `childOldestFourAccountIDs = ''`, as well as from backend responses).

Because `''` is not nullish (`null` or `undefined`), optional chaining `?.` executes:
1. `''.split(',')` returns `['']`.
2. `[''].map((accountID) => Number(accountID))` converts `Number('')` into `0`.
3. `.filter((accountID): accountID is number => typeof accountID === 'number')` keeps `0` because `typeof 0 === 'number'` is `true`.

Consequently, `childAccountIDs` evaluates to `[0]` (array with length 1), so the fallback check `childAccountIDs.length === 0 && processingAgentIDs` evaluates to `false`. `accountIDs` is set to `[0]` instead of using `processingAgentIDs`.

When `accountIDs = [0]` is passed to `MultiAccountAvatar`, account `0` (`CONST.DEFAULT_NUMBER_ID`) has no personal details in Onyx and represents an invalid account ID, causing `MultiAccountAvatar` to render the generic fallback placeholder avatar instead of the agent's avatar.

### What changes do you think we should make in order to solve the problem?
In `src/pages/inbox/report/ReportActionItemThread.tsx`, sanitize `childOldestFourAccountIDs` when parsing by filtering out empty strings and invalid/zero account IDs (`CONST.DEFAULT_NUMBER_ID`):

```diff
-    const childAccountIDs =
-        reportAction.childOldestFourAccountIDs
-            ?.split(',')
-            .map((accountID) => Number(accountID))
-            .filter((accountID): accountID is number => typeof accountID === 'number') ?? [];
-    const accountIDs = childAccountIDs.length === 0 && processingAgentIDs ? processingAgentIDs : childAccountIDs;
+    const childAccountIDs =
+        reportAction.childOldestFourAccountIDs
+            ?.split(',')
+            .filter(Boolean)
+            .map((accountID) => Number(accountID))
+            .filter((accountID): accountID is number => !Number.isNaN(accountID) && accountID !== CONST.DEFAULT_NUMBER_ID) ?? [];
+    const accountIDs = childAccountIDs.length === 0 && processingAgentIDs?.length ? processingAgentIDs : childAccountIDs;
```

This guarantees:
1. When `childOldestFourAccountIDs` is `''` or contains empty tokens, `childAccountIDs` evaluates to `[]`.
2. `accountIDs` cleanly falls back to `processingAgentIDs`, displaying the custom agent's avatar from Onyx personal details while it is processing.
3. Once real replies land and valid `accountIDs` exist, `childAccountIDs` continues to take precedence as expected.

### What specific scenarios should we cover in automated tests?
Add unit tests in `tests/unit/components/ReportActionItemThreadTest.tsx`:
1. Render `ReportActionItemThread` with `childOldestFourAccountIDs: ''` and `processingAgentIDs: [agentAccountID]`, with agent personal details populated in Onyx. Assert that the rendered `MultiAccountAvatar` receives `accountIDs: [agentAccountID]` and renders the agent's avatar instead of the fallback icon.
2. Render `ReportActionItemThread` with `childOldestFourAccountIDs: '111,222'` and `processingAgentIDs: [agentAccountID]`. Assert that `childAccountIDs` `[111, 222]` takes precedence.
3. Render `ReportActionItemThread` with `childOldestFourAccountIDs: undefined` and verify consistent fallback handling.

### What alternative solutions did you explore? (Optional)
Handling this at the backend or in `updateOptimisticParentReportAction` by setting `childOldestFourAccountIDs: undefined` instead of `''`. However, defensive parsing in `ReportActionItemThread.tsx` is required because historical Onyx data and API responses may still deliver empty strings or malformed comma-separated IDs.

Contributor details
Your Expensify account email: jloa.dev@gmail.com
Upwork Profile Link: https://www.upwork.com/freelancers/~0163955a2ba221e513
