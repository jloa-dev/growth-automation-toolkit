Contributor details
Your Expensify account email: jloa.dev@gmail.com
Upwork Profile Link: https://www.upwork.com/freelancers/~0163955a2ba22190aa

## Proposal

### Please re-state the problem that we are trying to solve in this issue.
In a shared Expensify Card program linked across multiple workspaces, an admin of Workspace X can view card transactions originating from Workspace Y by clicking "View transactions" under Current balance, even if they are not an admin or member of Workspace Y.

### What is the root cause of that problem?
In `src/pages/workspace/expensifyCard/WorkspaceCardsListLabel.tsx` (lines 185–194):
```tsx
const handleViewTransactionsPress = () => {
    const fundIDForFeedKey = defaultFundID === CONST.DEFAULT_NUMBER_ID ? undefined : String(defaultFundID);
    const feedKey = fundIDForFeedKey ? `${fundIDForFeedKey}_${CONST.EXPENSIFY_CARD.BANK}` : CONST.EXPENSIFY_CARD.BANK;
    const query = buildQueryStringFromFilterFormValues({
        type: CONST.SEARCH.DATA_TYPES.EXPENSE,
        feed: [feedKey],
        withdrawalStatus: [CONST.SEARCH.SETTLEMENT_STATUS.NEVER, CONST.SEARCH.SETTLEMENT_STATUS.PENDING],
    });
    Navigation.navigate(ROUTES.SEARCH_ROOT.getRoute({query, searchKey: CONST.SEARCH.SEARCH_KEYS.EXPENSES}));
};
```
1. When an Expensify Card program is shared across workspaces, all linked workspaces share the same underlying `fundID`.
2. When the admin clicks "View transactions", `buildQueryStringFromFilterFormValues` specifies `feed: [feedKey]` and `withdrawalStatus`, but **omits `policyID`**.
3. While the card list itself in `WorkspaceExpensifyCardListPage.tsx` scopes displayed cards to the current workspace's members via `CardUtils.getCardsByCardholderName`, omitting `policyID` in `buildQueryStringFromFilterFormValues` causes Search to query all transactions across the entire shared feed without workspace boundaries, displaying transactions from Workspace Y to Workspace X admins.

### What changes do you think we should make in order to solve the problem?
In `src/pages/workspace/expensifyCard/WorkspaceCardsListLabel.tsx`:
Add `policyID: [policyID]` (already extracted from route params at line 61) to `buildQueryStringFromFilterFormValues`:

```diff
--- a/src/pages/workspace/expensifyCard/WorkspaceCardsListLabel.tsx
+++ b/src/pages/workspace/expensifyCard/WorkspaceCardsListLabel.tsx
@@ -187,6 +187,7 @@ function WorkspaceCardsListLabel({type, value, style}: WorkspaceCardsListLabelPr
         const feedKey = fundIDForFeedKey ? `${fundIDForFeedKey}_${CONST.EXPENSIFY_CARD.BANK}` : CONST.EXPENSIFY_CARD.BANK;
         const query = buildQueryStringFromFilterFormValues({
             type: CONST.SEARCH.DATA_TYPES.EXPENSE,
+            policyID: [policyID],
             feed: [feedKey],
             withdrawalStatus: [CONST.SEARCH.SETTLEMENT_STATUS.NEVER, CONST.SEARCH.SETTLEMENT_STATUS.PENDING],
         });
```

- This ensures that the generated Search query includes `policyID:<policyID>` (or `workspace:<policyID>`), restricting results strictly to card expenses belonging to the workspace currently being viewed.
- Admins of Workspace X will only see transactions belonging to Workspace X, cleanly enforcing workspace data isolation.

Pre-coded and tested in branch: `fix/104221-workspace-card-view-transactions-scope` (https://github.com/jloa-dev/App/tree/fix/104221-workspace-card-view-transactions-scope).

### What alternative solutions did you explore? (Optional)
Constructing raw query strings manually. Using `buildQueryStringFromFilterFormValues({ policyID: [policyID], ... })` is the official, type-safe API used by the component and guarantees consistent URL formatting, encoding, and filter preservation across Search views.
