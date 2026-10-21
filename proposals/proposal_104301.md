Contributor details
Your Expensify account email: jloa.dev@gmail.com
Upwork Profile Link: https://www.upwork.com/freelancers/~0163955a2ba22190aa

## Proposal
### Please re-state the problem that we are trying to solve in this issue.
On mWeb (mobile web), when opening Concierge Help from the header icon in a chat, swiping back does not close the Concierge Right Hand Panel (RHP).

### What is the root cause of that problem?
In `src/libs/Navigation/AppNavigator/Navigators/RightModalNavigator.tsx`:
Concierge RHP is opened as a modal screen within the right modal stack. On mobile web (`Browser.isMobileChrome()` / `Browser.isMobileSafari()`), screen swipe gestures are handled by `react-navigation`'s pan responder.
In the screen options for `SCREENS.RIGHT_MODAL.CONCIERGE`:
`gestureEnabled` is either overridden by modal wrapper styles or the nested web scrollview intercepts horizontal drag events before the modal dismissal gesture recognizer can evaluate swipe velocity and distance.

### What changes do you think we should make in order to solve the problem?
1. In `src/libs/Navigation/AppNavigator/Navigators/RightModalNavigator.tsx`:
Explicitly configure `gestureEnabled: true` and `gestureDirection: 'horizontal'` for Concierge modal routes on mWeb:
```typescript
const defaultSubRouteOptions = {
    gestureEnabled: true,
    gestureDirection: 'horizontal',
    gestureResponseDistance: 100,
};
```
2. In `ConciergePage.tsx`, ensure the root container uses `touch-action: pan-y` so horizontal swipe gestures propagate cleanly to the navigation dismissal handler.

### What specific scenarios should we cover in automated tests?
In navigation modal unit tests:
- Verify that Concierge RHP screen options evaluate `gestureEnabled: true` on mobile web environments.
