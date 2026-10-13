## Proposal

### Please re-state the problem that we are trying to solve in this issue.
When inviting a new (non-existing Expensify) member to a workspace, navigating into the member row and clicking on "Role" quickly triggers a "Not Found" error / blocking screen instead of displaying the role options.

### What is the root cause of that problem?
When an admin invites a new user, NewDot assigns an optimistic `accountID` (generated via `generateAccountID(login)`).
When the backend `AddMembersToWorkspace` call finishes:
1. The backend provides the permanent `accountID`, removing the temporary personal details entry.
2. In `src/pages/workspace/members/WorkspaceMemberDetailsRolePage.tsx` (line 40):
   ```typescript
   const memberLogin = personalDetails?.[accountID]?.login ?? '';
   const member = policy?.employeeList?.[memberLogin];
   const canManageSelectedMemberRole = canMemberAssignRole(policy, currentUserLogin, member?.role);
   ```
   `WorkspaceMemberDetailsRolePage` looks up `personalDetails?.[accountID]`. Since `accountID` in route params is the optimistic ID, `personalDetails?.[accountID]` is `undefined`.
3. `memberLogin` falls back to `''`, so `member` is `undefined`, and `canMemberAssignRole` evaluates to `false`.
4. `AccessOrNotFoundWrapper` has `shouldBeBlocked={!canManageSelectedMemberRole}`, immediately blocking the screen with an error.

While `WorkspaceMemberDetailsPage.tsx` already addressed this in PR #96449 using `getMemberLoginByOptimisticAccountID`, this helper was not exported nor used in `WorkspaceMemberDetailsRolePage.tsx`.

### What changes do you think we should make in order to solve the problem?

1. **Export `getMemberLoginByOptimisticAccountID` in `src/libs/PolicyUtils/index.ts`** (or `src/libs/PolicyMemberRoleUtils.ts`):
   ```typescript
   function getMemberLoginByOptimisticAccountID(policy: OnyxEntry<Policy>, accountID: number): string {
       const matchesOptimisticAccountID = (login: string) => generateAccountID(login) === accountID || generateAccountID(Str.removeSMSDomain(login)) === accountID;
       const primaryLoginOfInvitedSecondary = Object.entries(policy?.primaryLoginsInvited ?? {}).find(([secondaryLogin]) => matchesOptimisticAccountID(secondaryLogin))?.[1];
       if (primaryLoginOfInvitedSecondary) {
           return primaryLoginOfInvitedSecondary;
       }
       return Object.keys(policy?.employeeList ?? {}).find(matchesOptimisticAccountID) ?? '';
   }
   ```

2. **Update `src/pages/workspace/members/WorkspaceMemberDetailsRolePage.tsx`**:
   - Recover member login and resolved accountID using `getMemberLoginByOptimisticAccountID`:
   ```typescript
   const routeAccountID = Number(route.params.accountID);
   const memberLogin = personalDetails?.[routeAccountID]?.login ?? getMemberLoginByOptimisticAccountID(policy, routeAccountID);
   const member = policy?.employeeList?.[memberLogin];
   const resolvedAccountID = personalDetailByLogin?.[memberLogin]?.accountID ?? routeAccountID;
   ```
   - Use `resolvedAccountID` for role updates and back navigation:
   ```typescript
   updateWorkspaceMembersRole(policy, [memberLogin], [resolvedAccountID], value);
   Navigation.goBack(ROUTES.WORKSPACE_MEMBER_DETAILS.getRoute(policyID, resolvedAccountID));
   ```

3. **In `src/pages/workspace/members/WorkspaceMemberDetailsPage.tsx`**:
   Import `getMemberLoginByOptimisticAccountID` from `@libs/PolicyUtils` instead of inlining it.

### What alternative solutions did you explore? (Optional)
- Forcing a blocking modal until `AddMembersToWorkspace` finishes: Poor UX; optimism is a core principle in New Expensify. Recovering the member login preserves instant responsiveness.

### What specific scenarios should we cover in automated tests?
In `tests/ui/WorkspaceMemberDetailsRolePageTest.tsx`:
1. Navigating to `WorkspaceMemberDetailsRolePage` with an optimistic `accountID` successfully resolves the member from `policy.employeeList` and renders the role list.
2. Changing role with an optimistic ID dispatches `updateWorkspaceMembersRole` with the resolved ID and navigates back cleanly without errors.
