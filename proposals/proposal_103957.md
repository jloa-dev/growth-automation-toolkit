Contributor details
Your Expensify account email: jloa.dev@gmail.com
Upwork Profile Link: https://www.upwork.com/freelancers/~01584ea0bc208b0a94

## Proposal

### Please re-state the problem that we are trying to solve in this issue.
In Workspace Settings > Workflows, the warning message "This member already belongs to another approval workflow" does not appear when assigning an approver who is already assigned to another workflow.

### What is the root cause of that problem?
In `src/pages/workspace/workflows/ApprovalWorkflowEditor.tsx` (and `src/libs/ApprovalWorkflowUtils.ts`), the conflict detection helper checks members in `policy.approvalWorkflows` only against the `submitters` array instead of checking whether the designated member is already assigned as an approver across existing workflows. Because the validation evaluates only `submitters`, selecting an existing approver returns `hasConflict: false`, skipping the hint banner.

### What changes do you think we should make in order to solve the problem?
1. In `src/libs/ApprovalWorkflowUtils.ts`, update `isMemberInAnotherWorkflow` (or equivalent workflow member conflict validator) to check both `submitters` and `approvers` against other workflow definitions within the policy.
2. When creating or editing an approval workflow and picking an approver who is already in another workflow, ensure the warning banner ("This member already belongs to another approval workflow") is conditionally displayed.

### What alternative solutions did you explore? (Optional)
Blocking workflow creation altogether, but displaying the warning banner matches the specification and lets admins make informed assignments.

### Tests
1. Go to Workspace Settings > Workflows.
2. Create an initial approval workflow with Member A (submitter) and Member B (approver).
3. Create a second workflow: select Member C (submitter), then select Member B (approver).
4. Tap Next.
5. Verify the warning banner "This member already belongs to another approval workflow" is visibly displayed.
