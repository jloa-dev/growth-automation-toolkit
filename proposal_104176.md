Contributor details
Your Expensify account email: jloa.dev@gmail.com
Upwork Profile Link: https://www.upwork.com/freelancers/~01584ea0bc208b0a94

## Proposal

### Please re-state the problem that we are trying to solve in this issue.
The "Vendor" option is missing from the filter list in Search > Expenses for workspaces with accounting connections (such as QBO) where non-reimbursable expenses have vendors assigned.

### What is the root cause of that problem?
In `src/libs/SearchUIUtils.ts` and `src/pages/Search/SearchAdvancedFiltersPage.tsx`, the search filter configuration defines the visible filter fields via `FILTER_VIEW_MAP`. The key `CONST.SEARCH.SYNTAX_FILTER_KEYS.VENDOR` is missing from the filter list mapping for the `EXPENSES` search type, preventing users from filtering expenses by vendor even when vendor data exists on transactions.

### What changes do you think we should make in order to solve the problem?
1. In `src/libs/SearchUIUtils.ts`, include `CONST.SEARCH.SYNTAX_FILTER_KEYS.VENDOR` in `FILTER_VIEW_MAP` and ensure `getFilterMenuItems` returns the Vendor option when the search type is `EXPENSES`.
2. Ensure the Vendor filter navigates to the vendor selection page (`ROUTES.SEARCH_ADVANCED_FILTERS_VENDOR.getRoute()`) and serializes to the `vendor:` search query parameter.

### What alternative solutions did you explore? (Optional)
Relying solely on free-text search in the search bar, which does not provide structured vendor autocompletion or exact matching.

### Tests
1. Log in as an admin of a workspace connected to QBO with non-reimbursable expenses.
2. Navigate to Search > Expenses.
3. Click "Filters".
4. Verify "Vendor" appears in the filter list options.
5. Select a vendor and verify the search results are filtered correctly by `vendor:"..."`.
