## Proposal

### Please re-state the problem that we are trying to solve in this issue.
In Workspace Settings > Rules (under "Set field requirements" or "Flag for review"), when using the AI "Describe" rule assistant (`DescribeRuleModal`), if a user generates a rule for a category that already has an existing rule of that type, the category is accepted into the draft. Upon attempting to save, the user is presented with a confusing validation error ("Please select at least one field") because no differences from the existing rule are found, unlike the manual category picker which prevents re-selecting already configured categories.

### What is the root cause of that problem?
1. **Unfiltered AI Category Matching in `DescribeRuleModal.tsx`**:
   In `src/pages/workspace/rules/DescribeRuleModal.tsx`, `withPolicyCategory` only checks if the category exists and is enabled (`candidate.enabled`). It does not verify category availability for rule creation:
   - For `RequireFieldsRules`: `RequireFieldsRuleCategoryPageBase.tsx` filters categories with `!categoryHasAnyRequireFieldsRule(category)`, but `RequireFieldsRulePageBase.tsx:applyGeneratedRule` writes the category into `draftRequireFieldsRule` without checking if a rule already exists.
   - For `FlagForReviewRules`: `FlagForReviewRuleCategoryPageBase.tsx` filters categories with `!hasExplicitFlagAmount(category.maxExpenseAmount)`, but `FlagForReviewRulePageBase.tsx` passes `setDraftFlagForReviewRule` directly.
2. **Generic Validation Failure on Save**:
   When an already assigned category is saved, `hasRequireFieldsRuleChanges` returns `false`, causing `RequireFieldsRulesUtils.ts:534` to fall back to `confirmErrorDoNotRequireField` ("Please select at least one field") instead of highlighting that the category is already assigned.

### What changes do you think we should make in order to solve the problem?

1. **Category Eligibility Validator in `DescribeRuleModal.tsx`**:
   Add an `isCategoryEligible` predicate to `DescribeRuleModalProps` and `withPolicyCategory`:
   ```typescript
   function withPolicyCategory(
       values: GeneratedRuleValues,
       policyCategories: OnyxEntry<PolicyCategories>,
       isCategoryEligible?: (category: PolicyCategory) => boolean,
   ): {values: GeneratedRuleValues; isCategoryIneligible?: boolean} {
       const {category, ...rest} = values;
       if (!category) {
           return {values};
       }
       const policyCategory = Object.values(policyCategories ?? {}).find(
           (candidate) => candidate.enabled && getDecodedCategoryName(candidate.name) === getDecodedCategoryName(category),
       );
       if (!policyCategory) {
           return {values: rest};
       }
       if (isCategoryEligible && !isCategoryEligible(policyCategory)) {
           return {values: rest, isCategoryIneligible: true};
       }
       return {values: {...rest, category: policyCategory.name}};
   }
   ```

2. **Pass Filter Predicate from Rule Page Bases**:
   - In `src/pages/workspace/rules/RequireFieldsRules/RequireFieldsRulePageBase.tsx`:
     Pass `isCategoryEligible={(category) => !categoryHasAnyRequireFieldsRule(category)}` to `DescribeRuleButton`.
   - In `src/pages/workspace/rules/FlagForReviewRules/FlagForReviewRulePageBase.tsx`:
     Pass `isCategoryEligible={(category) => !hasExplicitFlagAmount(category.maxExpenseAmount)}` to `DescribeRuleButton`.

3. **Explicit Feedback in `DescribeRuleModal`**:
   If `isCategoryIneligible` is detected, display an inline notice or toast notifying the user that a rule for this category already exists and leaving the category selector open for an eligible category, preventing any cryptic save failure.

### What alternative solutions did you explore? (Optional)
- Silently omitting the category without notifying the user: Frustrating for users who explicitly asked for that category in their AI prompt. Giving explicit feedback or highlighting the Category field is significantly better UX.

### What specific scenarios should we cover in automated tests?
In `tests/unit/DescribeRuleModalTest.tsx` and `tests/unit/RequireFieldsRulesUtilsTest.ts`:
1. Verify that describing a rule for a category with an existing require-fields rule rejects the category assignment and directs the user to select an available category.
2. Verify that describing a rule for an available category successfully populates all rule fields.
