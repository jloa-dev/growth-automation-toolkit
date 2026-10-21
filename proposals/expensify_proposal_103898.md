## Proposal

### Please re-state the problem that we are trying to solve in this issue.
In the Per Diem expense creation flow (`DynamicIOURequestStepDestination`), the empty list screen displays a static generic phrase (`"This workspace doesn't have any per diem rates..."`) instead of dynamically mentioning the specific workspace's name (`"${workspaceName} doesn't have any per diem rates..."`).

### What is the root cause of that problem?
1. In `src/languages/en.ts:5215-5217` (and corresponding locale files like `es.ts`):
   ```typescript
   requestEmptyList: {
       title: 'No rates found',
       subtitle: "This workspace doesn't have any per diem rates, ask your Admin to add some.",
       adminSubtitle: "This workspace doesn't have any per diem rates, add one to get started.",
   }
   ```
   Both `subtitle` and `adminSubtitle` are defined as static string literals without accepting the workspace/policy name as an interpolation argument.
2. In `src/pages/iou/request/step/DynamicIOURequestStepDestination.tsx:254-258`:
   ```typescript
   const subtitle = isAdmin
       ? translate('workspace.perDiem.requestEmptyList.adminSubtitle')
       : translate('workspace.perDiem.requestEmptyList.subtitle');
   ```
   The `translate()` calls do not pass `policy?.name`, even though `policy` is already resolved and present in the component scope.

### What changes do you think we should make in order to solve the problem?

1. **Update translation signatures across all locale files**:
   In `src/languages/en.ts` (and `es.ts`):
   ```typescript
   requestEmptyList: {
       title: 'No rates found',
       subtitle: (workspaceName: string) => `${workspaceName || 'This workspace'} doesn't have any per diem rates, ask your Admin to add some.`,
       adminSubtitle: (workspaceName: string) => `${workspaceName || 'This workspace'} doesn't have any per diem rates, add one to get started.`,
   }
   ```
   *(Providing the `'This workspace'` fallback ensures that if `policy?.name` is temporarily empty/undefined during initial Onyx hydration, the sentence remains grammatically correct without rendering `" doesn't have..."`)*.

2. **In `src/pages/iou/request/step/DynamicIOURequestStepDestination.tsx:254-258`**:
   Pass `policy?.name ?? ''`:
   ```typescript
   const workspaceName = policy?.name ?? '';
   const subtitle = isAdmin
       ? translate('workspace.perDiem.requestEmptyList.adminSubtitle', workspaceName)
       : translate('workspace.perDiem.requestEmptyList.subtitle', workspaceName);
   ```

### What alternative solutions did you explore? (Optional)
- Updating only the non-admin subtitle: Not recommended, because both admin and member empty states should share consistent design and naming conventions.

### What specific scenarios should we cover in automated tests?
In `tests/unit/DynamicIOURequestStepDestinationTest.tsx`:
1. Verify that when no per diem rates exist, the rendered empty state subtitle includes the policy's name for both admin and non-admin users.
2. Verify fallback behavior when `policy.name` is an empty string.
