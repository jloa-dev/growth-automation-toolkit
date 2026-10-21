Contributor details
Your Expensify account email: jloa.dev@gmail.com
Upwork Profile Link: https://www.upwork.com/freelancers/~0163955a2ba22190aa

## Proposal
### Please re-state the problem that we are trying to solve in this issue.
On Android, enabling the 'InsightsPage' beta override in Troubleshoot, navigating back, and then disabling it causes the application to crash.

### What is the root cause of that problem?
In `src/libs/Navigation/AppNavigator/index.tsx` and `src/pages/home/sidebar/SidebarScreen/index.tsx`:
When the `InsightsPage` beta override is enabled, the Insights tab is dynamically registered in the bottom tab navigator and drawer routes. When the beta is toggled off, `Permissions.canUseInsights(betas)` immediately evaluates to `false`. 
However, React Navigation's state tree still holds the active or previous route reference to `SCREENS.INSIGHTS`. When the user taps the back button, the navigator attempts to resolve the previous navigation state for a screen that has been unmounted from the route configuration, throwing an unhandled navigation exception (`Route 'Insights' not found in navigator`) and crashing the app.

### What changes do you think we should make in order to solve the problem?
1. In `src/pages/settings/Troubleshoot/BetaOverridesPage.tsx`, when disabling a feature flag that modifies top-level navigation routes (like `InsightsPage`), reset or sanitize the navigation history to point to `SCREENS.HOME`:
```typescript
function handleBetaToggle(betaKey: string, isEnabled: boolean) {
    if (betaKey === CONST.BETAS.INSIGHTS_PAGE && !isEnabled) {
        Navigation.resetToHome();
    }
    User.updateBetaOverrides(betaKey, isEnabled);
}
```
2. In `src/libs/Navigation/AppNavigator/createCustomStackNavigator.tsx`, add a fallback guard in `getStateForRouteNamesChange` to prevent crashing when a route name disappears from the descriptor tree after a beta toggle.

### What specific scenarios should we cover in automated tests?
In `tests/unit/PermissionsTest.ts` and navigation unit tests:
- Test that toggling `canUseInsights` dynamically from true to false does not leave orphaned route keys in navigation state.
