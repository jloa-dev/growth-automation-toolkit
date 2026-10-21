Contributor details
Your Expensify account email: jloa.dev@gmail.com
Upwork Profile Link: https://www.upwork.com/freelancers/~0163955a2ba22190aa

## Proposal
### Please re-state the problem that we are trying to solve in this issue.
When searching for an expense using the search query `merchant:coffee` and clicking the search icon again, an asterisk (`*`) is automatically appended to the search query (becoming `merchant:coffee*`).

### What is the root cause of that problem?
In `src/libs/SearchQueryUtils.ts`:
When building the search query string from autocomplete suggestions or re-serializing the query for the search input bar, the query serializer checks if the merchant filter was matched via partial string matching. In `buildSearchQueryString`, wildcard asterisks are injected for partial matches. This logic was intended for background autocomplete calls to the backend, but it erroneously leaked into the user-facing search query input component, mutating the user's explicit input string upon subsequent clicks or focuses.

### What changes do you think we should make in order to solve the problem?
In `src/libs/SearchQueryUtils.ts`, ensure that user-entered search queries in the search input retain their literal string without automatically appending asterisks:
```typescript
function formatSearchQueryForDisplay(query: string): string {
    return query.replace(/(merchant:[^\s*]+)\*/g, '$1');
}
```
And in `SearchAutocompleteInput.tsx`, ensure the display text only displays the exact sanitized user value.

### What specific scenarios should we cover in automated tests?
In `tests/unit/SearchQueryUtilsTest.ts`:
- Verify that searching for `merchant:coffee` and re-rendering the search bar maintains `merchant:coffee` without appending `*`.
