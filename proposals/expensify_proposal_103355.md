## Proposal

### Please re-state the problem that we are trying to solve in this issue.
In the expense report details members view (More > View details > Members), the "Find a member" search input (`Table.FilterBar`) is unconditionally rendered even when the report only has 1 or a few members. It should only appear when there are 12 or more members (`CONST.STANDARD_LIST_ITEM_LIMIT`).

### What is the root cause of that problem?
During the migration of the members view to the unified `Table` architecture (PR #93963), `ReportParticipantsTable` unconditionally instantiates `Table.FilterBar` inside `composeTableListHeader`:
```typescript
// src/components/Tables/ReportParticipantsTable/index.tsx:109
const tableHeaderComponent = composeTableListHeader(headerComponent, <Table.FilterBar label={translate('selectionList.findMember')} />);
```
`TableFilterBar` only hides itself when the dataset has zero rows (`isEmpty`). For any non-empty list (even 1 member), it renders `TableSearchBar`. The previous threshold check `members.length >= CONST.STANDARD_LIST_ITEM_LIMIT` was inadvertently omitted.

### What changes do you think we should make in order to solve the problem?
In `src/components/Tables/ReportParticipantsTable/index.tsx`:
1. Import `CONST from '@src/CONST'`.
2. Compute `shouldShowSearchBar = members.length >= CONST.STANDARD_LIST_ITEM_LIMIT` and pass it to `composeTableListHeader`, matching the existing pattern in `DomainMembersTable`:
```typescript
const shouldShowSearchBar = members.length >= CONST.STANDARD_LIST_ITEM_LIMIT;
const tableHeaderComponent = composeTableListHeader(
    headerComponent, 
    shouldShowSearchBar ? <Table.FilterBar label={translate('selectionList.findMember')} /> : undefined
);
```

- When `members.length < 12`, `composeTableListHeader` receives `undefined` for the filter bar slot, preserving the header actions without mounting the search bar.
- When `members.length >= 12`, `Table.FilterBar` renders normally and filters active members.
- If members are filtered or deleted while searching, `TableSearchBar` properly unmounts and cleans up search strings.

### What alternative solutions did you explore? (Optional)
- Gating within `TableFilterBar` globally: This would inadvertently hide filters and column selectors on full-width tables (such as workspace settings and categories) where the filter bar is meant to remain visible regardless of item count.

### Tests
1. Open an expense report with fewer than 12 participants (e.g. 1 or 2 members) and go to More > View details > Members.
2. Verify that no "Find a member" search bar appears.
3. Open or create a report/workspace with 12 or more members.
4. Verify that the "Find a member" search bar is displayed and searches correctly.

Contributor details
Your Expensify account email: jloa.dev@gmail.com
Upwork Profile Link: https://www.upwork.com/freelancers/~0163955a2ba22190aa
