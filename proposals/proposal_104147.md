Contributor details
Your Expensify account email: jloa.dev@gmail.com
Upwork Profile Link: https://www.upwork.com/freelancers/~0163955a2ba22190aa

## Proposal

### Please re-state the problem that we are trying to solve in this issue.
When a user has an active restrictive filter applied on Search/Spend (e.g. `merchant:I`), creating a new expense whose merchant does not match the active filter (e.g. merchant "Gj") causes the non-matching expense to appear in the filtered search results. Because the backend search snapshot excludes the non-matching expense, the optimistic row remains stuck in the search results until the view is reloaded.

### What is the root cause of that problem?
In `src/components/Search/hooks/useOptimisticSearchTracking.ts`:
Lines 146–164 unconditionally inject `optimisticTransaction` into `searchDataWithOptimisticTransaction`:
```ts
const nextSearchData = {
    ...searchData,
    [optimisticTransactionKey]: optimisticTransaction,
} as SearchResults['data'];
```
1. `searchDataWithOptimisticTransaction` only verifies `isTransactionSearchType(type)` and whether the tracking key exists. It never validates `optimisticTransaction` against the active query filters in `queryJSON.flatFilters` (such as `merchant`, `category`, `tag`, `currency`).
2. Calling `clearOptimisticTracking()` directly inside `searchDataWithOptimisticTransaction` during render (as proposed in earlier drafts) violates React rules and React Compiler invariants by triggering state updates (`setIsOptimisticTrackingCleared`, `setShowPendingExpensePlaceholder`, `setOptimisticWatchKey`) during render.
3. The clean place to guard insertion is:
   - Filter `searchDataWithOptimisticTransaction` so non-matching optimistic transactions are never injected into the data pipeline.
   - Clear optimistic tracking cleanly via `useEffect` without causing unmounted/re-render side effects.

### What changes do you think we should make in order to solve the problem?

1. Add a query matching helper `canOptimisticTransactionMatchQuery(transaction, queryJSON)` in `src/libs/SearchQueryUtils.ts` (or `SearchUIUtils.ts`):
```ts
function canOptimisticTransactionMatchQuery(transaction: OnyxEntry<Transaction>, queryJSON: SearchQueryJSON): boolean {
    if (!transaction) {
        return false;
    }

    const {flatFilters} = queryJSON;
    if (!flatFilters || flatFilters.length === 0) {
        return true;
    }

    const merchantFilter = flatFilters.find((f) => f.key === CONST.SEARCH.SYNTAX_FILTER_KEYS.MERCHANT);
    if (merchantFilter) {
        const transactionMerchant = (transaction.modifiedMerchant ?? transaction.merchant ?? '').toLowerCase();
        const matchesMerchant = merchantFilter.filters.some((filter) => {
            const filterValue = (filter.value ?? '').toLowerCase();
            if (filter.operator === CONST.SEARCH.OPERATOR_TYPES.EQUAL) {
                return transactionMerchant === filterValue;
            }
            return transactionMerchant.includes(filterValue);
        });
        if (!matchesMerchant) {
            return false;
        }
    }

    const categoryFilter = flatFilters.find((f) => f.key === CONST.SEARCH.SYNTAX_FILTER_KEYS.CATEGORY);
    if (categoryFilter) {
        const transactionCategory = (transaction.category ?? '').toLowerCase();
        const matchesCategory = categoryFilter.filters.some((filter) => (filter.value ?? '').toLowerCase() === transactionCategory);
        if (!matchesCategory) {
            return false;
        }
    }

    const currencyFilter = flatFilters.find((f) => f.key === CONST.SEARCH.SYNTAX_FILTER_KEYS.CURRENCY);
    if (currencyFilter) {
        const matchesCurrency = currencyFilter.filters.some((filter) => (filter.value ?? '').toUpperCase() === (transaction.currency ?? '').toUpperCase());
        if (!matchesCurrency) {
            return false;
        }
    }

    return true;
}
```

2. In `src/components/Search/hooks/useOptimisticSearchTracking.ts`:
- In `searchDataWithOptimisticTransaction`:
```diff
--- a/src/components/Search/hooks/useOptimisticSearchTracking.ts
+++ b/src/components/Search/hooks/useOptimisticSearchTracking.ts
@@ -156,7 +156,13 @@ function useOptimisticSearchTracking({searchResults, queryJSON, transactions, re
         if (!optimisticTransactionKey || !optimisticTransaction?.transactionID || searchData[optimisticTransactionKey] || optimisticTransaction.reportID === CONST.REPORT.SPLIT_REPORT_ID) {
             return searchData;
         }
 
+        if (!canOptimisticTransactionMatchQuery(optimisticTransaction, queryJSON)) {
+            return searchData;
+        }
+
         const nextSearchData = {
```
- In a reactive `useEffect` (cleanly disarming tracking when the created expense does not belong in this search without calling `setState` during render):
```ts
useEffect(() => {
    if (!optimisticTransactionKey || !optimisticTransaction || !isTransactionSearchType(type) || isOptimisticTrackingCleared) {
        return;
    }
    if (!canOptimisticTransactionMatchQuery(optimisticTransaction, queryJSON)) {
        clearOptimisticTracking();
    }
}, [optimisticTransactionKey, optimisticTransaction, queryJSON, type, isOptimisticTrackingCleared]);
```

### What alternative solutions did you explore? (Optional)
- Calling `clearOptimisticTracking()` inside the `searchDataWithOptimisticTransaction` IIFE: Rejected because setting state during render violates React rules and breaks React Compiler memoization.
- Subscribing to reports in `useOptimisticSearchTracking`: Rejected because `useOptimisticSearchTracking` deliberately avoids full report subscriptions to maintain 60 FPS performance on Search screens. Evaluating the transaction's own fields (`merchant`, `category`, `currency`) is fast, zero-overhead, and hermetic.
