Contributor details
Your Expensify account email: jloa.dev@gmail.com
Upwork Profile Link: https://www.upwork.com/freelancers/~01584ea0bc208b0a94

## Proposal

### Please re-state the problem that we are trying to solve in this issue.
On mWeb, a "New message" indicator displays in a chat when opening the chat across multiple concurrent sessions, even for messages sent by the user themselves.

### What is the root cause of that problem?
In `src/libs/ReportActionsUtils.ts` (`isReportActionUnread`), the unread status checks whether the action's `created` timestamp is newer than `report.lastReadTime`. In multi-session scenarios (e.g. Hybrid App + mWeb Chrome + mWeb Safari), optimistic message actions sent from one session arrive in other sessions before the remote `lastReadTime` is updated. Because `isReportActionUnread` does not filter out messages authored by the current user (`actorAccountID === currentAccountID`), the self-authored message triggers the unread marker.

### What changes do you think we should make in order to solve the problem?
1. In `src/libs/ReportActionsUtils.ts` inside `isReportActionUnread`, add an explicit check: if `ReportActionsUtils.isCurrentUserTheAuthor(action)` or `action.actorAccountID === currentAccountID`, return `false`.
2. Self-messages must never be considered unread to the sender regardless of session timestamps.

### What alternative solutions did you explore? (Optional)
Synchronizing `lastReadTime` via immediate polling, which causes redundant network traffic.

### Tests
1. Log into the same account on two sessions (e.g. Mobile app and mWeb Chrome).
2. Send a message from the mobile app.
3. Open mWeb Chrome and navigate to the chat.
4. Verify the message appears without an erroneous "New message" indicator.
