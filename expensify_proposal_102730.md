## Proposal

### Please re-state the problem that we are trying to solve in this issue.
When User B has a workspace with a non-supported currency and User A removes User B's admin permission on the workspace that has the Expensify Card configured, User B still sees the Expensify Card feed selector list instead of displaying the empty illustration (Telescope blocking view) indicating no cards are available.

### What is the root cause of that problem?
In `src/libs/ExpensifyCardFeedSelectorUtils.ts`, inside `isExpensifyCardFeedVisibleToAdmin`:
```typescript
// Source 2: the user is an admin of a non-deleted policy whose policyAccountID matches the fundID.
return Object.values(policies ?? {}).some(
    (policy) => policy?.policyAccountID === fundID && isPolicyAdmin(policy) && policy?.pendingAction !== CONST.RED_BRICK_ROAD_PENDING_ACTION.DELETE,
);
```
Notice that `isPolicyAdmin(policy)` is called without passing the current user's login.
In `src/libs/PolicyUtils/index.ts`:
```typescript
const isPolicyAdmin = (policy: OnyxInputOrEntry<Policy>, login?: string, shouldCheckGlobalPolicyRole = true): boolean => ...
```
When `login` is omitted, `isPolicyAdmin` checks `policy?.role === CONST.POLICY.ROLE.ADMIN`.
When User A removes User B from the admin role in the employee list, `policy.role` on the cached policy object may still reflect admin status unless the specific user's login is evaluated against `policy.employeeList`.
Because `login` is not passed, `isExpensifyCardFeedVisibleToAdmin` continues to return `true`, keeping the other workspace's feed in `otherFeeds`.
In `WorkspaceExpensifyCardFeedSelectorPage.tsx`, since `otherFeeds.length > 0`, the page renders the feed list instead of the empty `BlockingView` (Telescope).

### What changes do you think we should make in order to solve the problem?

1. **In `src/libs/ExpensifyCardFeedSelectorUtils.ts`**:
   Update `getAdminExpensifyCardFeedEntries` and `isExpensifyCardFeedVisibleToAdmin` to pass `currentUserLogin`:
   ```diff
   --- a/src/libs/ExpensifyCardFeedSelectorUtils.ts
   +++ b/src/libs/ExpensifyCardFeedSelectorUtils.ts
   @@ -79,6 +79,7 @@ function isExpensifyCardFeedVisibleToAdmin(
        domains: OnyxCollection<Domain>,
        currentUserAccountID: number,
   +    currentUserLogin: string,
        programs: ExpensifyCardFeedProgram[],
    ): boolean {
   @@ -92,7 +93,7 @@ function isExpensifyCardFeedVisibleToAdmin(
        // Source 2: the user is an admin of a non-deleted policy whose policyAccountID matches the fundID.
        return Object.values(policies ?? {}).some(
   -        (policy) => policy?.policyAccountID === fundID && isPolicyAdmin(policy) && policy?.pendingAction !== CONST.RED_BRICK_ROAD_PENDING_ACTION.DELETE,
   +        (policy) => policy?.policyAccountID === fundID && isPolicyAdmin(policy, currentUserLogin) && policy?.pendingAction !== CONST.RED_BRICK_ROAD_PENDING_ACTION.DELETE,
        );
    }
   ```

2. **In `src/hooks/useExpensifyCardFeedsForFeedSelector.ts`**:
   Pass `currentUserLogin` from `useCurrentUserPersonalDetails` to `getAdminExpensifyCardFeedEntries`.

3. **In `WorkspaceExpensifyCardFeedSelectorPage.tsx`**:
   When `primaryFeeds.length === 0` and `otherFeeds.length === 0`, `renderFeedListContent` cleanly falls through to render `BlockingView` with the Telescope illustration.

### What alternative solutions did you explore? (Optional)
- Wiping all card settings from Onyx on any policy role update: Overly aggressive and causes data thrashing. Validating user identity via `isPolicyAdmin(policy, currentUserLogin)` directly addresses the permission boundary.

### What specific scenarios should we cover in automated tests?
In `tests/ui/WorkspaceExpensifyCardFeedSelectorPageTest.tsx`:
1. When a user is removed as admin from the feed-owning workspace, `useExpensifyCardFeedsForFeedSelector` returns empty `primaryFeeds` and `otherFeeds`.
2. The page renders the empty `BlockingView` with `illustrations.Telescope` and appropriate empty state messaging.
