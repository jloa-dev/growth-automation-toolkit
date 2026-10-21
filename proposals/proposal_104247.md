Contributor details
Your Expensify account email: jloa.dev@gmail.com
Upwork Profile Link: https://www.upwork.com/freelancers/~0163955a2ba22190aa

## Proposal
### Please re-state the problem that we are trying to solve in this issue.
In Spend > Filter, selecting only the workspace owner account in the `From` filter causes the `From` column to disappear from the results table. When an additional user account is selected, the `From` column reappears.

### What is the root cause of that problem?
In `src/libs/SearchUIUtils.ts` (inside `getColumnsForSearchQuery`):
There is an optimization rule that conditionally hides the `From` column if all filtered expenses belong to the currently logged-in user:
```typescript
if (isFilteringOnlyCurrentUser(searchQuery)) {
    columns = columns.filter(col => col !== CONST.SEARCH.COLUMNS.FROM);
}
```
In a workspace or spend view, even when filtering exclusively by the owner's account, table context requires the `From` column to distinguish member expenses from owner expenses. Hiding it selectively creates an inconsistent layout.

### What changes do you think we should make in order to solve the problem?
In `src/libs/SearchUIUtils.ts`:
Do not hide the `From` column in Workspace/Spend search contexts:
```typescript
function shouldShowFromColumn(searchQuery: SearchQueryJSON, isWorkspaceContext: boolean): boolean {
    if (isWorkspaceContext) return true;
    return !isFilteringOnlyCurrentUser(searchQuery);
}
```

### What specific scenarios should we cover in automated tests?
In `tests/unit/SearchUIUtilsTest.ts`:
- Verify that the `From` column remains present in Spend results when the filter is set to the owner account.
