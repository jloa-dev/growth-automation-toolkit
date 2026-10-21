## Proposal

### Please re-state the problem that we are trying to solve in this issue.
After successfully reconnecting a direct company card feed (such as American Express or Chase) in Workspace Settings > Company Cards, the "Connection error" banner remains displayed on the cards table until the user manually triggers "Update card" on individual cards.

### What is the root cause of that problem?
There are two coupled root causes:

1. **Disconnect between Reconnect Lifecycle and Card Scrape Sync**:
   In `src/pages/workspace/companyCards/RefreshCardFeedConnectionPage.tsx:57-71`, the OAuth flow monitors `feed?.expiration` changing and directly calls `closeRHPFlow()`. It closes the side panel without triggering an automatic scrape/sync on the newly re-authenticated feed or clearing the stale error state.
   Because `lastScrapeResult` on the card object remains in its failed state (e.g. 434 or authentication failure) until a scrape occurs, `getShouldShowBrokenConnectionError.ts:14-17` continues to evaluate to `true`.

2. **Incomplete Coverage in `useUpdateFeedBrokenConnection.ts`**:
   In `src/hooks/useUpdateFeedBrokenConnection.ts:28-34`, post-reconnect syncing only inspects `cardsWithBrokenFeedConnection`, completely ignoring cards with status 434 or general connection issues (`hasCardConnectionIssue(card)`).
   Furthermore, `clearCompanyCardFeedErrors` is not optimistically invoked upon completing the re-authentication flow, allowing stale feed-level error banners to linger in Onyx.

### What changes do you think we should make in order to solve the problem?

1. **Trigger Feed & Card Re-Sync on Reconnect Completion in `RefreshCardFeedConnectionPage.tsx`**:
   In `src/pages/workspace/companyCards/RefreshCardFeedConnectionPage.tsx`, when `expiration` updates (OAuth) or `isRefreshing` clears without errors:
   - Call `clearCompanyCardFeedErrors(workspaceAccountID, feed)` to optimistically clear stale feed errors.
   - Dispatch `updateWorkspaceCompanyCard` across all assigned cards on the feed that have connection issues (`hasCardConnectionIssue(card)`) prior to calling `closeRHPFlow()`.

2. **Align Sync Scope in `useUpdateFeedBrokenConnection.ts`**:
   Update `useUpdateFeedBrokenConnection` to include all cards matching `hasCardConnectionIssue(card) || isFeedConnectionBroken`, ensuring 434 and feed-level broken states are fully resolved upon reconnect.

3. **Prevent Premature Mount Triggers in `BankConnection`**:
   Guard the mount effect in `BankConnection/index.tsx` so it does not prematurely close or trigger redundant syncs while a refresh is in flight (`isRefreshing === true`), centralizing the lifecycle in `RefreshCardFeedConnectionPage`.

### What alternative solutions did you explore? (Optional)
- Waiting solely on backend webhook to push card updates: Flawed because webhook latency can take up to several minutes, during which the user is left looking at an alarming broken connection banner after just successfully re-authenticating.

### What specific scenarios should we cover in automated tests?
In `tests/unit/RefreshCardFeedConnectionPageTest.tsx` and `tests/unit/useUpdateFeedBrokenConnectionTest.ts`:
1. Reconnecting an Amex feed with cards in error state 434 triggers `SyncCard` and clears the connection error banner.
2. Ensure feed-level errors are optimistically cleared when `expiration` changes.
