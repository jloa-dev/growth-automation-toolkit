Contributor details
Your Expensify account email: jloa.dev@gmail.com
Upwork Profile Link: https://www.upwork.com/freelancers/~0163955a2ba22190aa

## Proposal

### Please re-state the problem that we are trying to solve in this issue.
When opening a split expense preview from Search results (Spend > Expenses > Filters > Type > Chat), the application fails to resolve the route and renders the "Hmm... it's not here" (NotFound) screen.

### What is the root cause of that problem?
In `src/pages/inbox/report/actionContents/ChatTransactionPreview.tsx` (lines 70–74):
```tsx
onPreviewPressed={() => {
    if (shouldShowSplitPreview) {
        Navigation.navigate(createDynamicRoute(DYNAMIC_ROUTES.SPLIT_BILL_DETAILS.getRoute(action.reportActionID)));
        return;
    }
```
1. `createDynamicRoute` was called without a `basePath` parameter. When omitted, `createDynamicRoute` falls back to `getActiveRoute()`. When opening the preview from Search, `getActiveRoute()` resolves to `/search`.
2. This generates `/search/split/:reportActionID`.
3. In `DYNAMIC_ROUTES.SPLIT_BILL_DETAILS.entryScreens`:
   ```ts
   entryScreens: [SCREENS.REPORT, SCREENS.RIGHT_MODAL.SEARCH_REPORT, SCREENS.RIGHT_MODAL.EXPENSE_REPORT, SCREENS.RIGHT_MODAL.SEARCH_MONEY_REQUEST_REPORT]
   ```
   `SCREENS.SEARCH.ROOT` (`/search`) is not an allowed entry screen and has no `reportID` parameter. Consequently, `getStateFromPath` fails to match the dynamic route candidate and falls back to `SCREENS.NOT_FOUND`.
4. While lines 90 and 96 in `ChatTransactionPreview.tsx` were already updated to use `getReportRouteForCurrentContext({reportID: ...})` to properly contextualize transaction thread routes for Search, the split bill branch was omitted.

### What changes do you think we should make in order to solve the problem?
In `src/pages/inbox/report/actionContents/ChatTransactionPreview.tsx`:
Supply `baseReportRoute` computed via `getReportRouteForCurrentContext({reportID})` as the second argument to `createDynamicRoute`:

```diff
--- a/src/pages/inbox/report/actionContents/ChatTransactionPreview.tsx
+++ b/src/pages/inbox/report/actionContents/ChatTransactionPreview.tsx
@@ -69,7 +69,8 @@ function ChatTransactionPreview({action, reportID, chatReport, iouReport, should
                 transactionPreviewWidth={reportPreviewStyles.transactionPreviewStandaloneStyle.width}
                 onPreviewPressed={() => {
                     if (shouldShowSplitPreview) {
-                        Navigation.navigate(createDynamicRoute(DYNAMIC_ROUTES.SPLIT_BILL_DETAILS.getRoute(action.reportActionID)));
+                        const baseReportRoute = reportID ? getReportRouteForCurrentContext({reportID}) : undefined;
+                        Navigation.navigate(createDynamicRoute(DYNAMIC_ROUTES.SPLIT_BILL_DETAILS.getRoute(action.reportActionID), baseReportRoute));
                         return;
                     }
```

- When clicked inside Search (`isSearchTopmostFullScreenRoute()`), `getReportRouteForCurrentContext` returns `ROUTES.SEARCH_REPORT.getRoute({reportID, backTo})`. The route resolves cleanly as a child of SearchReport with `backTo` preserved, allowing the user to dismiss split bill details and return directly to their filtered Search state.
- When clicked inside standard Chat reports, `getReportRouteForCurrentContext` returns `ROUTES.REPORT_WITH_ID.getRoute({reportID})`, retaining 100% normal behavior.

Pre-coded and tested in branch: `fix/104161-split-bill-details-search-base-route` (https://github.com/jloa-dev/App/tree/fix/104161-split-bill-details-search-base-route).

### What alternative solutions did you explore? (Optional)
Directly passing `ROUTES.SEARCH_REPORT.getRoute({reportID})`. However, that omits the active `backTo` query parameter provided automatically by `getReportRouteForCurrentContext`, which would cause users to lose their Search filters upon navigating back.
