Contributor details
Your Expensify account email: jloa.dev@gmail.com
Upwork Profile Link: https://www.upwork.com/freelancers/~0163955a2ba221e513

## Proposal

### Please re-state the problem that we are trying to solve in this issue.
On iOS HybridApp (Hermes / Fabric), scrolling a FlashList (e.g. on native screen `Workspaces_List` or during screen transitions) crashes the application with a fatal error:
`Error: LayoutManager is not initialized, window size is unavailable`
thrown from `@shopify/flash-list/dist/recyclerview/RecyclerViewManager.js` -> `getWindowSize()`, called via `recyclerViewManager.recordInteraction()` from `RecyclerView.js:269`'s `onScroll` handler.

### What is the root cause of that problem?
1. On iOS Fabric, native scroll momentum events (`onScroll`) can be dispatched asynchronously from the native UI thread while React Native's layout pass has not yet completed (e.g., during navigation push/pop, or when the screen is hidden via `display: none` where our patch `@shopify+flash-list+2.3.2+002+skip-layout-when-hidden.patch` intentionally skips layout measurement).
2. When the native scroll event fires, `RecyclerView.js`'s `onScroll` handler invokes:
   ```javascript
   recyclerViewManager.recordInteraction();
   ```
3. Inside `RecyclerViewManager.js`, `recordInteraction()` directly delegates to:
   ```javascript
   this.itemViewabilityManager.recordInteraction();
   ```
   which triggers `updateViewableItems()` and calls `this.recyclerViewManager.getWindowSize()`.
4. `getWindowSize()` requires an active `layoutManager`:
   ```javascript
   getWindowSize() {
       if (!this.layoutManager) {
           throw new Error("LayoutManager is not initialized, window size is unavailable");
       }
       return this.layoutManager.getWindowSize();
   }
   ```
   Because `layoutManager` is `undefined` before the first measurement or after the list is hidden/dirtied, calling `recordInteraction()` causes an unhandled exception that crashes the hybrid app.

### What alternative solutions did you explore? (Optional)
Catching the error with `try / catch` inside `ExternalScrollFlashListTable.tsx` only protects the synthetic scroll path of MoneyRequestReportView, but does not protect native FlashLists throughout the app (such as `Workspaces_List` or `SearchRouter`). Fixing this at the FlashList patch level protects all lists globally.

### What changes do you think we should make in order to solve the problem?
Add a patch in `patches/@shopify/flash-list/` (or update patch `002` / create patch `017+fix-record-interaction-without-layout.patch`):

1. **In `node_modules/@shopify/flash-list/dist/recyclerview/RecyclerViewManager.js` (and src counterpart):**
   Guard `recordInteraction()` using `hasLayout()`:
   ```diff
   --- a/node_modules/@shopify/flash-list/dist/recyclerview/RecyclerViewManager.js
   +++ b/node_modules/@shopify/flash-list/dist/recyclerview/RecyclerViewManager.js
   @@ -215,6 +215,9 @@ export class RecyclerViewManager {
        }
        recordInteraction() {
   +        if (!this.hasLayout()) {
   +            return;
   +        }
            this.itemViewabilityManager.recordInteraction();
        }
   ```

2. **In `node_modules/@shopify/flash-list/dist/recyclerview/RecyclerView.js` (and src counterpart):**
   Also add a safeguard in the `onScroll` callback:
   ```diff
   --- a/node_modules/@shopify/flash-list/dist/recyclerview/RecyclerView.js
   +++ b/node_modules/@shopify/flash-list/dist/recyclerview/RecyclerView.js
   @@ -266,7 +266,9 @@ const RecyclerViewComponent = (props, ref) => {
            if (isInitialScrollComplete) {
   -            recyclerViewManager.recordInteraction();
   +            if (recyclerViewManager.hasLayout()) {
   +                recyclerViewManager.recordInteraction();
   +            }
            }
   ```

3. Update `patches/@shopify/flash-list/details.md` documenting this safeguard alongside the existing `scrollToIndex` guard in patch `002`.

### What automated tests can you add to prevent this from re-occurring?
Add a test in `tests/unit/FlashListTest.tsx` (or a unit test verifying `RecyclerViewManager`) that triggers `recordInteraction()` on a newly instantiated `RecyclerViewManager` whose `layoutManager` is undefined, verifying that it safely early-returns without throwing `"LayoutManager is not initialized, window size is unavailable"`.
