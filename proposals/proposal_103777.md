Contributor details
Your Expensify account email: jloa.dev@gmail.com
Upwork Profile Link: https://www.upwork.com/freelancers/~0163955a2ba22190aa

## Proposal

### Please re-state the problem that we are trying to solve in this issue.
The application experiences an unhandled Sentry crash: `Cannot read properties of undefined (reading 'filter')` inside React Navigation's `StackRouter.getStateForRouteNamesChange` when custom navigators (such as RightModalNavigator / SearchReport in the RHP, SearchFullscreenNavigator, SplitNavigator, or WorkspaceNavigator) mount or change route names.

### What is the root cause of that problem?
In `RightModalRouter.ts`, `SearchFullscreenRouter.ts`, `SplitRouter.ts`, and `WorkspaceRouter.ts`:
1. When custom navigators initialize, they restore snapshots using `getPreservedNavigatorState(options.parentRoute.key)`.
2. When a preserved state is found, it is currently returned raw directly from `getInitialState`:
   ```ts
   const preservedState = getPreservedNavigatorState(options.parentRoute.key);
   return preservedState ?? stackRouter.getInitialState(configOptions);
   ```
3. Returning `preservedState` directly without validating or rehydrating it causes two critical failures:
   - If `preservedState` does not have a valid `routes` array (e.g. partial snapshot, or state preserved across a route key change or tab switch), `state.routes` is undefined or malformed.
   - Preserved states carry `stale: false`. When a navigator mounts with a different route set than the saved snapshot, `useNavigationBuilder` invokes `router.getStateForRouteNamesChange(state, {routeNames})`.
   - Upstream `@react-navigation/routers` calls `state.routes.filter(...)` and `state.preloadedRoutes ? state.preloadedRoutes.filter(...) : undefined`. Because the raw preserved state was never validated and never passed through `stackRouter.getRehydratedState`, `state.routes` (or `preloadedRoutes`) is undefined, throwing:
     `TypeError: Cannot read properties of undefined (reading 'filter')`.

### What changes do you think we should make in order to solve the problem?
In our custom routers:
- `src/libs/Navigation/AppNavigator/createRightModalNavigator/RightModalRouter.ts`
- `src/libs/Navigation/AppNavigator/createSearchFullscreenNavigator/SearchFullscreenRouter.ts`
- `src/libs/Navigation/AppNavigator/createSplitNavigator/SplitRouter.ts`
- `src/libs/Navigation/AppNavigator/createWorkspaceNavigator/WorkspaceRouter.ts`

Validate that `preservedState` has a non-empty `routes` array, and crucially pass it through `stackRouter.getRehydratedState(preservedState, configOptions)` before returning it. `getRehydratedState` is React Navigation's official contract for rehydrating state snapshots against the current route config, which safely synchronizes `routeNames`, populates all expected keys, and filters obsolete routes:

```diff
--- a/src/libs/Navigation/AppNavigator/createRightModalNavigator/RightModalRouter.ts
+++ b/src/libs/Navigation/AppNavigator/createRightModalNavigator/RightModalRouter.ts
@@ -11,9 +11,12 @@ function RightModalRouter(options: RightModalNavigatorRouterOptions) {
 
     return {
         ...stackRouter,
-        getInitialState({routeNames, routeParamList, routeGetIdList}: RouterConfigOptions) {
+        getInitialState(configOptions: RouterConfigOptions) {
             const preservedState = getPreservedNavigatorState(options.parentRoute.key);
-            return preservedState ?? stackRouter.getInitialState({routeNames, routeParamList, routeGetIdList});
+            if (preservedState && Array.isArray(preservedState.routes) && preservedState.routes.length > 0) {
+                return stackRouter.getRehydratedState(preservedState, configOptions);
+            }
+            return stackRouter.getInitialState(configOptions);
         },
     };
 }
```
(Identical safeguard applied to `SearchFullscreenRouter.ts`, `SplitRouter.ts`, and `WorkspaceRouter.ts`).

Pre-coded and tested in branch: `fix/103777-sentry-navigation-crash-filter` (https://github.com/jloa-dev/App/tree/fix/103777-sentry-navigation-crash-filter).

### What alternative solutions did you explore? (Optional)
Patching `node_modules/@react-navigation/routers` with an inline optional chaining null-check. While patching third-party packages is possible, fixing the custom router rehydration directly in application code is far cleaner, adheres to React Navigation router design, and completely avoids maintaining additional node_modules patches.
