Contributor details
Your Expensify account email: jloa.dev@gmail.com
Upwork Profile Link: https://www.upwork.com/freelancers/~01584ea0bc208b0a94

## Proposal

### Please re-state the problem that we are trying to solve in this issue.
The "Import contacts" option does not appear when tapping "Start chat" from the Floating Action Button (FAB) on a fresh app installation.

### What is the root cause of that problem?
In PR #102928, the "Import contacts" button on `NewChatPage` (`src/pages/NewChatPage.tsx`) was introduced with conditional rendering dependent on `contactState?.pickContact` and contact permission state. On a fresh installation, permissions have neither been requested nor initialized in Onyx state, causing `contactState` to be undefined/null on initial mount. As a result, the button condition evaluates to false and fails to render the "Import contacts" entry point.

### What changes do you think we should make in order to solve the problem?
1. In `src/pages/NewChatPage.tsx`, update the condition for rendering the "Import contacts" item so that on supported native mobile platforms (iOS / Android), the button is rendered even if permissions have not yet been queried.
2. Trigger the native contact permission flow (`requestContactsPermission`) upon tapping the "Import contacts" item rather than requiring pre-granted permissions to simply display the option.

### What alternative solutions did you explore? (Optional)
Querying permissions synchronously on app start, which causes unwanted permission prompts before the user interacts with chat.

### Tests
1. Perform a clean install of the New Expensify app on iOS or Android.
2. Sign in with a new account.
3. Tap FAB > "Start chat".
4. Verify "Import contacts" is visibly displayed in the options list.
5. Tap "Import contacts" and verify the OS contact permission dialog appears as expected.
