Contributor details
Your Expensify account email: jloa.dev@gmail.com
Upwork Profile Link: https://www.upwork.com/freelancers/~01584ea0bc208b0a94

## Proposal

### Please re-state the problem that we are trying to solve in this issue.
On Web/Desktop, clicking the browser back button after opening multiple reports navigates to Home or a previous action instead of the previously viewed report.

### What is the root cause of that problem?
In PR #103346, history delta reconciliation was patched in `@react-navigation/native` (`patches/react-navigation/@react-navigation+native+*.patch`). When the user navigates between reports on Web, `historyDelta === 0` state reconciliations in `useLinking.js` trigger `getStaleHistoryDiff` inappropriately, resetting the report stack state or focusing the default Home action instead of popping the topmost report from the navigation state stack.

### What changes do you think we should make in order to solve the problem?
1. In the React Navigation patch / `src/libs/Navigation/AppNavigator/index.tsx`, ensure that popstate navigation events preserve the sequential report hierarchy in navigation state.
2. Ensure `historyDelta` correctly computes the index difference between report routes rather than falling back to action-level reconciliation.

### What alternative solutions did you explore? (Optional)
Using `window.history.back()` overrides, but native React Navigation state reconciliation is the proper architecture for web deep linking.

### Tests
1. On Web (Chrome/Safari), open Expensify.
2. Open Report A from Inbox, then Report B, then Report C.
3. Click the browser Back button.
4. Verify navigation returns to Report B, then click Back again to return to Report A.
