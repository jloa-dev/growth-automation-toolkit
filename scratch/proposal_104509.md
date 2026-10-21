## Proposal

### Please re-state the problem that we are trying to solve in this issue.
On the Issue Card "Set card rules" step, when the user turns on the "Add spend rule" toggle, clicks "Next" without selecting or configuring a rule (which triggers an error), and then turns off the toggle, the "Next" button remains permanently stuck in a disabled loading spinner state, preventing the user from continuing.

### What is the root cause of that problem?
In `src/pages/workspace/expensifyCard/issueNew/spendRules/SetSpendRulesStep.tsx`:
1. `FormProvider` sets `isPressed = true` inside `startWithLoading` by default when the submit button is clicked (`src/components/Form/FormProvider.tsx:156, 355`).
2. `submit` (lines 190–196) performs an ad-hoc validation check:
   ```typescript
   const formSpendRuleError = getSpendRuleErrorMessage();

   if (formSpendRuleError) {
       setSpendRuleErrorMessage(formSpendRuleError);
       return;
   }
   ```
3. Because this validation check is performed inside `submit` rather than inside the `validate` function (lines 221–242), `FormProvider` treats the form as valid and initiates the press loading state. When `submit` returns early, `isPressed` is never reset (it only resets on unmount, screen blur, thrown error, or external `isLoading` transition).
4. Turning off the toggle in `handleToggleSpendRules` (lines 111–117) calls `setSpendRuleErrorMessage('')`, but does not touch `FormProvider`'s internal `isPressed` state, leaving the button locked in a loading spinner.

### What changes do you think we should make in order to solve the problem?
1. In `src/pages/workspace/expensifyCard/issueNew/spendRules/SetSpendRulesStep.tsx`:
   Pass `shouldShowLoadingImmediatelyOnPress={false}` to `FormProvider` (lines 273–281):
   ```diff
               <FormProvider
                   style={[styles.flexGrow1, styles.ph5]}
                   formID={ONYXKEYS.FORMS.ISSUE_NEW_EXPENSIFY_CARD_FORM}
                   onSubmit={submit}
                   submitButtonText={isEditing ? translate('common.confirm') : translate('common.next')}
                   enabledWhenOffline
                   shouldHideFixErrorsAlert
                   validate={validate}
   +               shouldShowLoadingImmediatelyOnPress={false}
               >
   ```
   **Rationale:** Submitting this wizard step only updates local Onyx draft state (`setIssueNewCardStepAndData`) before navigating to the next wizard step. It requires zero network latency and should never trigger an unrecoverable blocking press spinner. This matches the established pattern in other wizard forms (`RulePageBase.tsx`, `ReportAddApproverPage.tsx`).

2. Integrate `getSpendRuleErrorMessage()` into `validate()` so `FormProvider`'s validation lifecycle natively stops submission before any loading state is initiated:
   ```diff
       const validate = (values: FormOnyxValues<typeof ONYXKEYS.FORMS.ISSUE_NEW_EXPENSIFY_CARD_FORM>) => {
           const errors: FormInputErrors<typeof ONYXKEYS.FORMS.ISSUE_NEW_EXPENSIFY_CARD_FORM> = {};
   +       const formSpendRuleError = getSpendRuleErrorMessage();
   +       if (formSpendRuleError) {
   +           setSpendRuleErrorMessage(formSpendRuleError);
   +           errors[INPUT_IDS.EXPIRATION_TOGGLED] = formSpendRuleError;
   +       }
           if (!expirationToggled) {
   -           return {};
   +           return errors;
           }
   ```

### What specific scenarios should we cover in automated tests?
In `tests/unit/SetSpendRulesStepTest.tsx`:
1. Render `SetSpendRulesStep` with "Add spend rule" enabled and no rules configured.
2. Click "Next", assert validation error appears and the submit button remains interactive (not locked in a spinner).
3. Toggle "Add spend rule" OFF, click "Next", assert navigation proceeds to `CARD_NAME` step.

Contributor details
Your Expensify account email: jloa.dev@gmail.com
Upwork Profile Link: https://www.upwork.com/freelancers/~0163955a2ba221e513
