## Proposal

### Please re-state the problem that we are trying to solve in this issue.
The Red Brick Road (RBR) error indicator remains permanently visible on the Workspaces tab (and on the workspace row in the workspaces list) after a workspace with an accounting sync error (such as bad credentials) is archived, and the user has no way to dismiss or clear it because archived workspaces are read-only.

### What is the root cause of that problem?
1. In `src/hooks/usePoliciesWithCardFeedErrors.ts`, `cleanPolicies` filters policies solely by whether they possess an `id`:
```typescript
const cleanPolicies = Object.values(policies ?? {}).filter((policy) => policy?.id);
```
It does not filter out archived policies using `isArchivedPolicy(policy)`.

2. When `usePolicyIndicatorChecks` iterates through `cleanPolicies` to evaluate `shouldShowSyncError` (along with `shouldShowPolicyError`, `shouldShowCustomUnitsError`, `shouldShowEmployeeListError`, etc.), the archived workspace is still evaluated:
```typescript
[
    CONST.INDICATOR_STATUS.HAS_SYNC_ERRORS,
    cleanPolicies.find((cleanPolicy) =>
        shouldShowSyncError(
            cleanPolicy,
            isConnectionInProgress(allConnectionSyncProgresses?.[`${ONYXKEYS.COLLECTION.POLICY_CONNECTION_SYNC_PROGRESS}${cleanPolicy?.id}`], cleanPolicy),
            CONST.POLICY.CONNECTIONS.ACCOUNTING_CONNECTION_NAMES,
        ),
    ),
]
```
Because neither `shouldShowSyncError` nor `cleanPolicies` checks if the policy is archived, the hook returns `HAS_SYNC_ERRORS`, keeping the red dot visible in `useWorkspacesTabIndicatorStatus`.

3. Similarly, in `src/libs/PolicyUtils/index.ts`, `getPolicyBrickRoadIndicatorStatus` lacks an early return check for `isArchivedPolicy(policy)`, which causes `WorkspaceRowBrickRoadIndicator.tsx` to continue displaying the red indicator on the row even when the workspace is archived.

### What changes do you think we should make in order to solve the problem?
1. In `src/hooks/usePoliciesWithCardFeedErrors.ts`:
Exclude archived policies when generating `cleanPolicies` so `usePolicyIndicatorChecks` suppresses error indicators originating from read-only archived workspaces:
```typescript
import {isArchivedPolicy, isPolicyAdmin} from '@libs/PolicyUtils';

// ...
const cleanPolicies = Object.values(policies ?? {}).filter((policy) => policy?.id && !isArchivedPolicy(policy));
```

2. In `src/libs/PolicyUtils/index.ts`:
In `getPolicyBrickRoadIndicatorStatus`, return `undefined` immediately when the policy is archived:
```typescript
function getPolicyBrickRoadIndicatorStatus(policy: OnyxEntry<Policy>, isConnectionInProgress: boolean): ValueOf<typeof CONST.BRICK_ROAD_INDICATOR_STATUS> | undefined {
    if (isArchivedPolicy(policy)) {
        return undefined;
    }

    if (
        shouldShowEmployeeListError(policy) ||
        shouldShowCustomUnitsError(policy) ||
        shouldShowPolicyErrorFields(policy) ||
        shouldShowSyncError(policy, isConnectionInProgress, getAccountingConnectionNames()) ||
        shouldShowQBOReimbursableExportDestinationAccountError(policy) ||
        shouldShowHRConnectionError(policy, isConnectionInProgress, isPolicyAdmin(policy))
    ) {
        return CONST.BRICK_ROAD_INDICATOR_STATUS.ERROR;
    }
    return undefined;
}
```

3. In `src/components/Tables/WorkspaceListTable/WorkspaceRowBrickRoadIndicator.tsx`:
Add an archived check to `createPolicyErrorsSelector`:
```typescript
const createPolicyErrorsSelector = (connectionSyncProgress: OnyxEntry<PolicyConnectionSyncProgress>) => (policy: OnyxEntry<Policy>) =>
    !isArchivedPolicy(policy) &&
    (getUberConnectionErrorDirectlyFromPolicy(policy) ||
        shouldShowEmployeeListError(policy) ||
        getPolicyBrickRoadIndicatorStatus(policy, isConnectionInProgress(connectionSyncProgress, policy)) === CONST.BRICK_ROAD_INDICATOR_STATUS.ERROR);
```

### What alternative solutions did you consider?
- Modifying each individual `shouldShow*Error` function to check `!isArchivedPolicy(policy)`: this adds redundant checks across multiple utility functions instead of handling it centrally in `cleanPolicies`, `getPolicyBrickRoadIndicatorStatus`, and row selector.
- Clearing error fields in Onyx when archiving a policy: this would be destructive and fragile if server responses or sync progress updates re-populate the error keys asynchronously.
