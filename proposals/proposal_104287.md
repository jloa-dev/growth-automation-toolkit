Contributor details
Your Expensify account email: jloa.dev@gmail.com
Upwork Profile Link: https://www.upwork.com/freelancers/~0163955a2ba22190aa

## Proposal
### Please re-state the problem that we are trying to solve in this issue.
When a saved search containing an existing `From` filter is viewed, and the user enters `group-by: reports` in the search bar and submits, an error occurs and the `From` filter is unexpectedly dropped.

### What is the root cause of that problem?
In `src/libs/SearchQueryUtils.ts` (inside `buildSearchQueryString` and query normalization when handling `groupBy` modifiers):
When `group-by: reports` is appended to an existing query string of a saved search, `getSearchQueryJSON` parses the query tokens. During the transition from the flat expense view to the report grouped view, the search query normalizer checks filter compatibility with `groupBy`.
Specifically, the `from` filter parameter was using direct user account identification that the report-level group parser treats as non-groupable in saved queries if not explicitly retained in the sanitized query options (`SearchQueryUtils.ts:sanitizeSearchValue`). Because `group-by: reports` forces report-level aggregation, the query sanitizer strips filters not explicitly listed in the allowed grouped filter set, leading to the parameter being dropped and an undefined field error when fetching report-grouped results.

### What changes do you think we should make in order to solve the problem?
1. In `src/libs/SearchQueryUtils.ts`, ensure that when parsing and sanitizing `group-by: reports`, user-specified filters such as `from` and `to` are preserved across both flat and grouped search views:
```typescript
function sanitizeFiltersForGroupBy(queryJSON: SearchQueryJSON): SearchQueryJSON {
    return {
        ...queryJSON,
        filters: {
            ...queryJSON.filters,
        },
    };
}
```
2. In `src/libs/actions/Search.ts`, ensure saved search re-execution retains all active filter criteria before appending the `groupBy` parameter to the search URL.

### What specific scenarios should we cover in automated tests?
In `tests/unit/SearchQueryUtilsTest.ts`:
- Add a test verifying that adding `group-by: reports` to a search query containing `from:<accountID>` preserves the `from` filter without dropping it.
- Add a test verifying that no syntax or parser error is thrown on saved search report groupings.
