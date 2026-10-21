## Proposal

### Please re-state the problem that we are trying to solve in this issue.
When navigating to a newly created Held Expense report and tapping Search, the contextual suggestion "Search in #report" is missing from the search router suggestions list.

### What is the root cause of that problem?
In `src/components/Search/SearchRouter/SearchRouter.tsx` (lines 235–241):
1. When an expense is submitted on hold, `buildOptimisticExpenseReport` (`src/libs/actions/IOU/Hold.ts:810–824`) initializes the newly created expense report with `notificationPreference: CONST.REPORT.NOTIFICATION_PREFERENCE.HIDDEN` for the submitter (`src/libs/ReportUtils.ts:8150–8154`). This is standard Expensify behavior to keep submitted expense reports from cluttering the LHN sidebar.
2. In `SearchRouter.tsx`, the router attempts to find the report in `recentReports` (`recentReports.find((option) => option.reportID === contextualReportID)`). Because `recentReports` excludes hidden reports (`excludeHidden: true` in `OptionsListUtils/index.ts:2469–2471`), `reportForContextualSearch` is `undefined`.
3. The fallback path executes lines 238–241:
   ```typescript
   if (!reportForContextualSearch) {
       if (!contextualReport || isHiddenForCurrentUser(contextualReport)) {
           return undefined;
       }
   ```
4. `isHiddenForCurrentUser(contextualReport)` evaluates to `true` because of the `hidden` notification preference. As a result, the router returns `undefined` and completely omits the contextual suggestion ("Search in #report"), even though the user is actively viewing that report.

### What changes do you think we should make in order to solve the problem?
In `src/components/Search/SearchRouter/SearchRouter.tsx` (line 239), do not allow `isHiddenForCurrentUser` to suppress contextual search for money request reports:

```diff
             if (!reportForContextualSearch) {
-                if (!contextualReport || isHiddenForCurrentUser(contextualReport)) {
+                if (!contextualReport || (isHiddenForCurrentUser(contextualReport) && !ReportUtils.isMoneyRequestReport(contextualReport))) {
                     return undefined;
                 }
```

**Why this is optimal:**
1. A money request report is created with `hidden` notification preference by design for its submitter. Suppressing contextual search for a report the user is currently viewing conflates LHN sidebar filtering with active search context.
2. Checking `!ReportUtils.isMoneyRequestReport(contextualReport)` ensures that active expense reports, held reports, and IOU reports always generate their contextual search suggestion when viewed, without altering `OptionsListUtils.getRecentReports` or affecting general chat filtering.

### What specific scenarios should we cover in automated tests?
In `tests/unit/SearchRouterTest.tsx`:
1. Render `SearchRouter` with `contextualReport` set to an expense report whose `notificationPreference` is `'hidden'`.
2. Verify `reportForContextualSearch` is not in `recentReports`.
3. Assert that the returned suggestions list contains the contextual suggestion `"Search in #report"`.
4. Regression test: Verify that a genuinely hidden standard chat report (non-money request report) that is not in `recentReports` still returns `undefined` when `isHiddenForCurrentUser` is true.

Contributor details
Your Expensify account email: jloa.dev@gmail.com
Upwork Profile Link: https://www.upwork.com/freelancers/~0163955a2ba221e513
