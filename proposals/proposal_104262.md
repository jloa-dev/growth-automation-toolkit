Contributor details
Your Expensify account email: jloa.dev@gmail.com
Upwork Profile Link: https://www.upwork.com/freelancers/~0163955a2ba22190aa

## Proposal
### Please re-state the problem that we are trying to solve in this issue.
When inviting a new member with a non-existing account to an expense report, the invited member is not displayed in the members list immediately and only appears after manually refreshing the page.

### What is the root cause of that problem?
In `src/libs/actions/Report.ts` (inside `inviteToReport` / `inviteToRoom`):
When inviting an email that does not yet exist in Onyx `personalDetails`, the optimistic data writes the invitation notification but fails to add the temporary/optimistic account ID to `report.participantAccountIDs` in the optimistic Onyx payload. As a result, the members list component (which reads from `report.participantAccountIDs`) does not re-render until the backend command completes and returns the full report object on reload.

### What changes do you think we should make in order to solve the problem?
In `src/libs/actions/Report.ts`, include the invited account ID in the optimistic `report.participantAccountIDs`:
```typescript
const optimisticData: OnyxUpdate[] = [
    {
        onyxMethod: Onyx.METHOD.MERGE,
        key: `${ONYXKEYS.COLLECTION.REPORT}${reportID}`,
        value: {
            participantAccountIDs: [...(report?.participantAccountIDs ?? []), invitedAccountID],
        },
    },
];
```
This ensures the members list updates instantly without requiring a page refresh.

### What specific scenarios should we cover in automated tests?
In `tests/unit/ReportTest.ts`:
- Test that inviting a non-existing account ID updates `report.participantAccountIDs` optimistically before the network request resolves.
