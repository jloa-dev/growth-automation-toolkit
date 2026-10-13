## Proposal

### Please re-state the problem that we are trying to solve in this issue.
When an approver or member receives an email notification for a submitted expense and clicks the "View" button, the app opens the workspace chat root at the newest messages, rather than navigating to the specific expense report or scrolling to and highlighting the expense action.

### What is the root cause of that problem?
The root cause is a discrepancy in how the email notification links are constructed between the "Approve" and "View" CTAs:

1. **Email Link Parameter Mismatch in Notification Generation**:
   - The email's **Approve** button correctly builds the deep link target as:
     `https://new.expensify.com/r/<workspaceChatID>/<reportActionID>`
     When clicked, the route parameters contain both `reportID` and `reportActionID`. `LinkedActionNotFoundGuard.tsx` passes `reportActionID` to `useReportActionsScroll`, which locates the `REPORT_PREVIEW` action, scrolls to it, and applies the highlight animation.
   - The email's **View** button is incorrectly constructed as:
     `https://new.expensify.com/r/<workspaceChatID>`
     It passes only the `workspaceChatID` (`parentReportID`), omitting both the `reportActionID` and the child `expenseReportID` (`iouReportID`).
   
2. **App Deep Link Resolution**:
   In `src/ROUTES.ts:2720`:
   ```typescript
   REPORT_WITH_ID: {
       route: 'r/:reportID?/:reportActionID?',
   }
   ```
   Because no `reportActionID` is provided in the URL, `ReportScreen` mounts without `LinkedActionNotFoundGuard` action parameters. `useReportActionsScroll.ts` initializes with default scroll behavior (`scrollOffsetRef.current = 0`), landing the user at the bottom of the workspace chat at the latest conversation messages.

### What changes do you think we should make in order to solve the problem?

1. **Fix Email Notification CTA Link Builder (Backend / Web-E)**:
   In the email notification template service that formats expense notification emails:
   - For the **"View"** CTA: Construct the link using the target expense report ID:
     `https://new.expensify.com/r/<expenseReportID>`
     (or `https://new.expensify.com/r/<workspaceChatID>/<reportActionID>`).
   - This ensures clicking "View" directly opens the expense report screen with the transaction breakdown, receipts, and category details, matching the behavior of clicking an expense preview inside the app.

2. **App Deep-Link Resiliency (Frontend)**:
   In `src/libs/ReportUtils.ts` and `src/pages/inbox/ReportScreen.tsx`:
   - If an email or notification URL passes an optional `transactionID` or `iouReportID` query parameter (e.g. `?transactionID=...`), resolve and navigate to the corresponding `expenseReportID` automatically via `Navigation.navigate(ROUTES.REPORT_WITH_ID.getRoute(expenseReportID))`.

### What alternative solutions did you explore? (Optional)
- Guessing the newest expense action in `ReportScreen` when no `reportActionID` is passed: Not recommended, as the user may have multiple unapproved expenses in the same workspace chat, and guessing could navigate to the wrong transaction.

### What specific scenarios should we cover in automated tests?
In `tests/unit/ReportScreenTest.tsx` and deep-link routing unit tests:
1. Verify navigating to `r/<workspaceChatID>/<reportActionID>` highlights the target expense action.
2. Verify navigating to `r/<expenseReportID>` opens the expense report with all transaction fields displayed.
3. Verify that URLs without `reportActionID` preserve standard chat scroll behavior without regression.
