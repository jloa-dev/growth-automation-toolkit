Contributor details
Your Expensify account email: jloa.dev@gmail.com
Upwork Profile Link: https://www.upwork.com/freelancers/~0163955a2ba22190aa

## Proposal
### Please re-state the problem that we are trying to solve in this issue.
In a Control workspace with approval workflows configured with an approval limit on the initial approver and an over-limit approver, submitting an expense report exceeding the limit skips the first approver and routes directly to the over-limit approver.

### What is the root cause of that problem?
In `src/libs/WorkflowUtils.ts` (inside `getInitialApproverForReport`):
When evaluating multi-level approval rules, the logic checks if `report.total > approvalRule.limit`. 
If true, it immediately returns `approvalRule.overLimitApprover` as the initial approver, skipping the sequential workflow requirement where reports must first be approved by the primary approver before escalating to the over-limit approver.

### What changes do you think we should make in order to solve the problem?
In `src/libs/WorkflowUtils.ts`:
Modify approval routing so that reports exceeding the threshold still route to `approvalRule.primaryApprover` for initial review. The over-limit approver should only become active in the approval chain once the primary approver has approved the report:
```typescript
function getNextApprover(report: OnyxEntry<Report>, rule: ApprovalRule): string {
    const isOverLimit = (report?.total ?? 0) > rule.limit;
    if (!report?.isApprovedByPrimary && rule.primaryApprover) {
        return rule.primaryApprover;
    }
    return isOverLimit ? rule.overLimitApprover : rule.primaryApprover;
}
```

### What specific scenarios should we cover in automated tests?
In `tests/unit/WorkflowUtilsTest.ts`:
- Add a test verifying that submitting a report exceeding the approval limit assigns the primary approver first, not the over-limit approver.
