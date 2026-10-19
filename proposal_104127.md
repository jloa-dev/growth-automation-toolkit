Contributor details
Your Expensify account email: jloa.dev@gmail.com
Upwork Profile Link: https://www.upwork.com/freelancers/~01584ea0bc208b0a94

## Proposal

### Please re-state the problem that we are trying to solve in this issue.
On Android, Concierge does not update the expense category when requested in natural language within a report chat (e.g. "Update all transactions in this report to have category Car").

### What is the root cause of that problem?
In the mobile agent tool execution pipeline (`src/libs/actions/Report.ts` and the AI command parser integration), natural language intent handlers map report update instructions to backend action parameters. On Android, the report parameter resolution fails to bind the active `reportID` to the category update payload when executed from within an IOU/Expense report thread, resulting in the agent failing silently or executing a no-op instead of dispatching `updateMoneyRequestCategory`.

### What changes do you think we should make in order to solve the problem?
1. In `src/libs/actions/Report.ts` (or the relevant Concierge agent action dispatcher), ensure that when an AI prompt requests a batch category update within a report, the current `reportID` and child transaction IDs (`transactionIDList`) are correctly resolved from Onyx `reportActions` and passed to the batch category update routine.
2. Ensure proper error handling and fallback UI feedback in the Concierge thread if an invalid category name is provided.

### What alternative solutions did you explore? (Optional)
Handling category updates purely through manual dropdowns, but this breaks the intended natural language concierge automation on mobile.

### Tests
1. Open the New Expensify app on Android.
2. Navigate to a workspace expense report containing 1 or more expenses.
3. In the report compose box, type: "Update all transactions in this report to have category Car" and send.
4. Verify Concierge successfully updates all transactions in the report to category "Car".
