Contributor details
Your Expensify account email: jloa.dev@gmail.com
Upwork Profile Link: https://www.upwork.com/freelancers/~0163955a2ba22190aa

## Proposal

### Please re-state the problem that we are trying to solve in this issue.
In Android/iOS, after an expense is deleted while offline, opening an adjacent expense from the carousel and waiting for the offline delete to sync causes the navigation arrows in the header (`MoneyRequestReportTransactionsNavigation`) to disappear.

### What is the root cause of that problem?
1. **Unnecessary Component Remounting in `ReportNotFoundGuard.tsx`**:
   In `src/pages/inbox/ReportNotFoundGuard.tsx:127-131`:
   ```typescript
   if (!deleteTransactionNavigateBackUrl && isReportTransactionThread(report)) {
       return <ReportNotFoundInnerGuard reportIDFromPath={routeParams?.reportID}>{children}</ReportNotFoundInnerGuard>;
   }

   return children;
   ```
   When an expense is deleted offline, `deleteTransactionNavigateBackUrl` is set in Onyx (`ONYXKEYS.NVP_DELETE_TRANSACTION_NAVIGATE_BACK_URL`). While it is set, `ReportNotFoundGuard` renders `{children}` directly. When the delete syncs and `DeleteTransactionNavigateBackHandler` clears `deleteTransactionNavigateBackUrl`, `ReportNotFoundGuard` switches from bare `{children}` to `<ReportNotFoundInnerGuard>{children}</ReportNotFoundInnerGuard>`. Because the element type changes at the guard root, React unmounts the entire children tree (including `MoneyRequestHeader` and `MoneyRequestReportTransactionsNavigation`) and mounts a new one.

2. **Premature Clearing in `MoneyRequestReportTransactionsNavigation.tsx`**:
   In `src/components/MoneyRequestReportView/MoneyRequestReportTransactionsNavigation.tsx:209-217`:
   ```typescript
   useEffect(() => {
       return () => {
           const focusedRoute = findFocusedRoute(navigationRef.getRootState());
           if (focusedRoute?.name && (CAROUSEL_PRESERVING_SCREENS as readonly string[]).includes(focusedRoute.name)) {
               return;
           }
           clearActiveTransactionIDs();
       };
   }, []);
   ```
   When the unmount cleanup fires:
   - If the user has opened the Test Tools modal to toggle offline mode, `findFocusedRoute` returns `TEST_TOOLS_MODAL.ROOT` (or `SCREENS.RIGHT_MODAL.TEST_TOOLS`), which is not in `CAROUSEL_PRESERVING_SCREENS`.
   - Checking only `focusedRoute.name` fails to distinguish between the user actually navigating away from the screen versus a modal being focused or an internal remount where the screen route is still intact in the navigation state.
   - Consequently, `clearActiveTransactionIDs()` is called, wiping `ONYXKEYS.TRANSACTION_THREAD_NAVIGATION_TRANSACTION_IDS`. When the re-mounted `MoneyRequestReportTransactionsNavigation` evaluates `useCarouselTransactionIDs()`, `transactionIDsList` is empty, causing lines 426-429 to return early and hide the arrows.

### What changes do you think we should make in order to solve the problem?
1. **Stabilize `ReportNotFoundGuard.tsx` to prevent tree remounts**:
   Instead of conditionally swapping between `{children}` and `<ReportNotFoundInnerGuard>{children}</ReportNotFoundInnerGuard>`, always render `<ReportNotFoundInnerGuard>` for transaction threads and pass a condition (or check `!deleteTransactionNavigateBackUrl` internally in `ReportNotFoundInnerGuard` before determining `shouldShowNotFoundPage`):
   ```diff
   diff --git a/src/pages/inbox/ReportNotFoundGuard.tsx b/src/pages/inbox/ReportNotFoundGuard.tsx
   --- a/src/pages/inbox/ReportNotFoundGuard.tsx
   +++ b/src/pages/inbox/ReportNotFoundGuard.tsx
   @@ -127,5 +127,9 @@ function ReportNotFoundGuard({children}: ReportNotFoundGuardProps) {
   -    if (!deleteTransactionNavigateBackUrl && isReportTransactionThread(report)) {
   -        return <ReportNotFoundInnerGuard reportIDFromPath={routeParams?.reportID}>{children}</ReportNotFoundInnerGuard>;
   +    if (isReportTransactionThread(report)) {
   +        return (
   +            <ReportNotFoundInnerGuard
   +                reportIDFromPath={routeParams?.reportID}
   +                shouldCheckParent={!deleteTransactionNavigateBackUrl}
   +            >
   +                {children}
   +            </ReportNotFoundInnerGuard>
   +        );
        }
   ```
   In `ReportNotFoundInnerGuard`, if `shouldCheckParent` is `false`, set `shouldShowNotFoundPage = false`. This guarantees the component tree never unmounts due to `deleteTransactionNavigateBackUrl` updates.

2. **Harden `MoneyRequestReportTransactionsNavigation.tsx` unmount cleanup**:
   In `src/components/MoneyRequestReportView/MoneyRequestReportTransactionsNavigation.tsx`, check whether the component's route key (`useRoute().key`) is still in the navigation state before clearing:
   ```typescript
   const route = useRoute();
   useEffect(() => {
       return () => {
           const rootState = navigationRef.getRootState();
           const activeKeys = extractNavigationKeys(rootState);
           if (activeKeys.includes(route.key)) {
               return;
           }
           const focusedRoute = findFocusedRoute(rootState);
           if (focusedRoute?.name && (CAROUSEL_PRESERVING_SCREENS as readonly string[]).includes(focusedRoute.name)) {
               return;
           }
           clearActiveTransactionIDs();
       };
   }, [route.key]);
   ```
   Additionally, include `SCREENS.RIGHT_MODAL.TEST_TOOLS` in `CAROUSEL_PRESERVING_SCREENS`.

### What alternative solutions did you explore? (Optional)
- Only updating `CAROUSEL_PRESERVING_SCREENS`: Does not solve cases where other overlays or transient state transitions cause a remount while the screen route remains alive. Combining route key verification with `ReportNotFoundGuard` stabilization provides complete stability across both native and web platforms.

### What specific scenarios should we cover in automated tests?
1. In `tests/unit/components/MoneyRequestReportTransactionsNavigation.test.tsx`:
   - Verify that when `MoneyRequestReportTransactionsNavigation` unmounts while its route key is still in navigation state (or while a modal is focused), `clearActiveTransactionIDs` is not called.
2. In `tests/unit/ReportNotFoundGuardTest.tsx`:
   - Verify that toggling `deleteTransactionNavigateBackUrl` does not cause children to unmount and remount.
