Contributor details
Your Expensify account email: jloa.dev@gmail.com
Upwork Profile Link: https://www.upwork.com/freelancers/~0163955a2ba22190aa

## Proposal
### Please re-state the problem that we are trying to solve in this issue.
When duplicating a workspace that does not have Rules enabled, the 'Rules' checkbox option is still displayed and checked by default during the duplication flow, causing Rules to briefly flash in the LHN of the new workspace.

### What is the root cause of that problem?
In `src/pages/workspace/WorkspaceDuplicatePage.tsx`:
The list of duplicate feature options (`DUPLICATE_WORKSPACE_OPTIONS`) statically includes `CONST.WORKSPACE_OPTIONS.RULES` without checking if the source policy actually has the Rules feature enabled (`PolicyUtils.hasRulesEnabled(policy)`). Consequently, the checkbox is rendered for all policy types regardless of plan or configuration.

### What changes do you think we should make in order to solve the problem?
In `src/pages/workspace/WorkspaceDuplicatePage.tsx`:
Filter out the Rules option if the source workspace does not have Rules enabled:
```typescript
const duplicateOptions = useMemo(() => {
    return BASE_DUPLICATE_OPTIONS.filter(option => {
        if (option === CONST.WORKSPACE_OPTIONS.RULES) {
            return PolicyUtils.hasRulesEnabled(policy);
        }
        return true;
    });
}, [policy]);
```

### What specific scenarios should we cover in automated tests?
In `tests/unit/WorkspaceDuplicatePageTest.ts`:
- Test that duplicating a workspace with Rules disabled does not render the Rules checkbox option in the duplication step.
