Contributor details
Your Expensify account email: jloa.dev@gmail.com
Upwork Profile Link: https://www.upwork.com/freelancers/~01584ea0bc208b0a94

## Proposal

### Please re-state the problem that we are trying to solve in this issue.
When an Expensify Card feed is shared to a workspace, no activity message is posted in the `#admins` room, leaving other workspace admins unaware of who added the card feed.

### What is the root cause of that problem?
When company-card feeds are shared (`src/libs/actions/CompanyCards.ts`), a system activity action (`CONST.REPORT.ACTIONS.TYPE.COMPANY_CARD_FEED_ADDED`) is optimistically created and pushed to the `#admins` room. However, the Expensify Card sharing flow (`src/libs/actions/Card.ts`) executes the sharing request without creating the corresponding system activity message in the target workspace's `#admins` report.

### What changes do you think we should make in order to solve the problem?
1. In `src/libs/actions/Card.ts` (inside the function responsible for linking/sharing an Expensify Card feed to a workspace), create an optimistic system report action in the workspace `#admins` room mirroring `CompanyCards`:
   - Message text: `added "[feed name]" Expensify Card feed` (localized).
   - Feed name resolved using the display label from the Expensify Card selector.
2. Ensure the message is only created on newly shared feeds, not on retries or already-linked feeds.

### What alternative solutions did you explore? (Optional)
Relying on an email notification, but in-app `#admins` activity is the standard pattern for workspace audit trails.

### Tests
1. As a workspace admin, navigate to Settings > Workflows > Cards.
2. Share an existing Expensify Card feed to another workspace.
3. Navigate to the `#admins` room of the destination workspace.
4. Verify the activity message `[Admin] added "[feed name]" Expensify Card feed` is posted and styled correctly.
