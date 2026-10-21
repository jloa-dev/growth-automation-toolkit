Contributor details
Your Expensify account email: jloa.dev@gmail.com
Upwork Profile Link: https://www.upwork.com/freelancers/~0163955a2ba221e513

## Proposal

### Please re-state the problem that we are trying to solve in this issue.
On Web, accessing "Add existing expenses" (`/search/r/:reportID/add-existing-expense`) or navigating and scrolling lists under `/search` crashes with:
`Error: Maximum update depth exceeded (React #185)`
at `@shopify/flash-list/dist/recyclerview/ViewHolderCollection.js:116 commitLayout -> setRenderId((prev) => prev + 1)`
called from `@shopify/flash-list/dist/recyclerview/RecyclerView.js:213 layout effect -> viewHolderCollectionRef.current.commitLayout()`.

### What is the root cause of that problem?
There are two coupled root causes that trigger an infinite re-render loop between React and FlashList's `RecyclerView`:

1. **Unstable Prop References passed to `FlashList` on every render:**
   - In `src/components/Table/TableBody.tsx`, line 477 passes `maintainVisibleContentPosition={{disabled: true}}` as an inline object literal. Because `{disabled: true} !== {disabled: true}`, FlashList's `RecyclerView` treats `maintainVisibleContentPosition` as updated on every render cycle.
   - In `src/components/Table/TableBody.tsx`, line 395 computes `const listData = buildTableListData(...)` without `useMemo`. A new array reference is supplied to `<FlashList data={listData}>` on each render.
   - In `src/components/Table/TableBody.tsx`, lines 471-474 pass an inline arrow function as `ref`:
     ```tsx
     ref={(instance) => {
         listRef.current = instance;
         measureScrollbarRef(instance);
     }}
     ```
     An inline ref callback identity change causes React to invoke it with `null` then the new instance, invalidating layout hooks.
   - In `src/components/Tables/AddExistingExpenseTable/index.tsx`, line 147 also passes `maintainVisibleContentPosition={{disabled: true}}` inline, and `columns`, `filters`, `compareItems`, and `renderExpenseTableRow` are recreated on every render.
   - In `src/pages/AddExistingExpense.tsx`, line 96: `const unreportedExpenses = createUnreportedExpenses(transactions).map(...)` creates a fresh array instance on every parent render without `useMemo`.

2. **FlashList `commitLayout` re-trigger cycle:**
   In `@shopify/flash-list`, when `maintainVisibleContentPosition` or `data` changes reference while a layout effect mounts, `RecyclerView.js` invokes `viewHolderCollectionRef.current.commitLayout()`, which calls `setRenderId((prev) => prev + 1)`. Because the parent component (`TableBody`) receives a new render from this state update, it recreates `listData`, `maintainVisibleContentPosition`, and the inline `ref`, triggering `commitLayout()` again on the next layout effect tick until React's max update depth (50) is exceeded.

### What alternative solutions did you explore? (Optional)
None, fixing reference stability across `TableBody`, `AddExistingExpenseTable`, and `AddExistingExpense` directly eliminates the re-render cascades.

### What changes do you think we should make in order to solve the problem?

1. **In `src/components/Table/TableBody.tsx`**:
   - Define a static module-level constant for disabled MVCP:
     ```tsx
     const FLASH_LIST_MVCP_DISABLED = {disabled: true} as const;
     ```
   - Memoize `listData`:
     ```tsx
     const listData = useMemo(() => buildTableListData<TableData>(filteredAndSortedData, tableListMetadata), [filteredAndSortedData, tableListMetadata]);
     ```
   - Memoize the list ref callback:
     ```tsx
     const setFlashListRef = useCallback((instance: FlashList<TableData> | null) => {
         listRef.current = instance;
         measureScrollbarRef(instance);
     }, [measureScrollbarRef]);
     ```
   - Pass `maintainVisibleContentPosition={FLASH_LIST_MVCP_DISABLED}` and `ref={setFlashListRef}` to `<FlashList>`.

2. **In `src/components/Tables/AddExistingExpenseTable/index.tsx`**:
   - Define a module-level constant `MVCP_DISABLED = {disabled: true} as const;` and pass it to `<Table maintainVisibleContentPosition={MVCP_DISABLED}>`.
   - Memoize `columns`, `filters`, `compareItems`, and `renderExpenseTableRow` using `useMemo` and `useCallback`.

3. **In `src/pages/AddExistingExpense.tsx`**:
   - Wrap `unreportedExpenses` in `useMemo`:
     ```tsx
     const unreportedExpenses: UnreportedExpenseTableRowData[] = useMemo(
         () =>
             createUnreportedExpenses(transactions).map((item) => ({
                 ...item,
                 disabled: item.isDisabled,
             })),
         [transactions],
     );
     ```

### What automated tests can you add to prevent this from re-occurring?
Add a unit test in `tests/unit/AddExistingExpenseTest.tsx` and `tests/unit/TableBodyTest.tsx` verifying that:
1. Re-rendering `TableBody` with identical data rows does not re-instantiate `listData` or re-fire `RecyclerView.commitLayout()`.
2. Rendering `AddExistingExpense` with 50+ transactions does not trigger `Maximum update depth exceeded`.
