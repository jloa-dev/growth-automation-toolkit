Contributor details
Your Expensify account email: jloa.dev@gmail.com
Upwork Profile Link: https://www.upwork.com/freelancers/~0163955a2ba22190aa

## Proposal

### Please re-state the problem that we are trying to solve in this issue.
In New Expensify, when QuickBooks Desktop (QBD) encounters stale data (>7 days out of date), clicking "Sync Now" in Workspace Accounting settings repeatedly returns a stale-data error without requesting a fresh Codat Web Connector refresh, whereas a manual sync in Classic Expensify succeeds by requesting a fresh refresh.

### What is the root cause of that problem?
In `src/pages/workspace/accounting/PolicyAccountingPage.tsx` (line 242):
```tsx
{
    icon: icons.Sync,
    text: translate('workspace.accounting.syncNow'),
    onSelected: () => syncConnection(policy, connectedIntegration),
    disabled: isOffline,
}
```
1. When the user explicitly selects **Sync Now**, it calls `syncConnection(policy, connectedIntegration)` without passing the third argument `forceDataRefresh`.
2. In `src/libs/actions/connections/index.ts` (lines 184 and 225–227):
   ```ts
   function syncConnection(policy: Policy | undefined, connectionName: PolicyConnectionName | undefined, forceDataRefresh = false)
   ...
   if (connectionName === CONST.POLICY.CONNECTIONS.NAME.QBD) {
       parameters.forceDataRefresh = forceDataRefresh;
   }
   ```
   `forceDataRefresh` defaults to `false`. For QBD, when data has expired, Codat requires `forceDataRefresh: true` to trigger the QuickBooks Web Connector.
3. In onboarding setup (`QuickBooksDesktopSetupFlowSyncPage.tsx:29`), `syncConnection(policy, CONST.POLICY.CONNECTIONS.NAME.QBD, true)` is properly passed with `true`. But on the primary Workspace Accounting page, the manual Sync Now menu item omitted `true`, trapping the connection in a stale error state.

### What changes do you think we should make in order to solve the problem?
In `src/pages/workspace/accounting/PolicyAccountingPage.tsx`:
Pass `true` for `forceDataRefresh` on manual "Sync Now" selection:

```diff
--- a/src/pages/workspace/accounting/PolicyAccountingPage.tsx
+++ b/src/pages/workspace/accounting/PolicyAccountingPage.tsx
@@ -239,7 +239,7 @@ function PolicyAccountingPage({policy}: PolicyAccountingPageProps) {
                       {
                           icon: icons.Sync,
                           text: translate('workspace.accounting.syncNow'),
-                          onSelected: () => syncConnection(policy, connectedIntegration),
+                          onSelected: () => syncConnection(policy, connectedIntegration, true),
                           disabled: isOffline,
                       },
                   ]
```

- When manual sync is triggered by user intent, `forceDataRefresh: true` ensures Codat triggers a fresh Web Connector sync, clearing the stale-data error and achieving 100% parity with Classic Expensify.
- Integrations other than QBD ignore `forceDataRefresh` as `connections/index.ts:225` explicitly checks `connectionName === CONST.POLICY.CONNECTIONS.NAME.QBD`.

Pre-coded and tested in branch: `fix/104218-qbd-manual-sync-force-refresh` (https://github.com/jloa-dev/App/tree/fix/104218-qbd-manual-sync-force-refresh).

### What alternative solutions did you explore? (Optional)
Changing the default value of `forceDataRefresh` in `syncConnection` signature to `true`. This was rejected because background/automated sync cycles should not indiscriminately force heavy Web Connector refreshes. Passing `true` exclusively on user-initiated manual Sync Now is cleaner and matches product intent.
