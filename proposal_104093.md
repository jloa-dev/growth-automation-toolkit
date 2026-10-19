Contributor details
Your Expensify account email: jloa.dev@gmail.com
Upwork Profile Link: https://www.upwork.com/freelancers/~01584ea0bc208b0a94

## Proposal

### Please re-state the problem that we are trying to solve in this issue.
When a user signs up and joins a workspace using the "Join my company workspace" onboarding intent, the `#admins` room unexpectedly opens in the Right Hand Panel (RHP).

### What is the root cause of that problem?
In `src/pages/OnboardingWorkspaces/BaseOnboardingWorkspaces.tsx` inside `finishOnboarding`, the navigation logic checks whether the workspace utilizes the Submit flow (`shouldUseSubmitFlow`). If true, it invokes `navigateToSubmitWorkspaceAfterOnboardingWithMicrotaskQueue`, which defaults to opening the workspace `#admins` room in the RHP. It fails to distinguish between creating a brand-new workspace vs joining an existing company workspace (`isJoiningCompanyWorkspace` / `CONST.ONBOARDING_CHOICES.JOIN_WORKSPACE`), where the new joiner is typically a member (not necessarily an admin needing immediate room setup).

### What changes do you think we should make in order to solve the problem?
1. In `src/pages/OnboardingWorkspaces/BaseOnboardingWorkspaces.tsx`, check `isJoiningCompanyWorkspace` in `finishOnboarding`.
2. When joining an existing workspace, navigate directly to the workspace default report/chat or home without opening the `#admins` room in RHP.

### What alternative solutions did you explore? (Optional)
Closing RHP on unmount, which causes a visual flicker of the admin panel before dismissing.

### Tests
1. Sign up with a private-domain email that has an existing joinable workspace.
2. Select "Join my company workspace", validate account, and join.
3. Verify the user lands on the workspace default chat/Inbox and the `#admins` room does NOT open in the RHP.
