Contributor details
Your Expensify account email: jloa.dev@gmail.com
Upwork Profile Link: https://www.upwork.com/freelancers/~0163955a2ba221e513

## Proposal

### Please re-state the problem that we are trying to solve in this issue.
When adding a secondary contact method while offline and submitting the magic code, once the device reconnects to the internet and validation succeeds, the user is not navigated back to the contact methods list and remains on the contact method details screen (which transitions into its validated state).

### What is the root cause of that problem?
In `src/pages/settings/Profile/Contacts/DynamicContactMethodDetailsPage.tsx:133-161`:
1. **Unstable target route during reconnect batching:**
   The validation success navigation effect calls `Navigation.goBack(listPath)` where `listPath` is derived from `useDynamicBackPath(DYNAMIC_ROUTES.CONTACT_METHOD_DETAILS.path)`. `useDynamicBackPath` computes the path by serializing the global root navigation tree via `useRootNavigationState`. When the app reconnects to the network, `ReconnectApp` and queued API responses execute in the same tick. The router state is temporarily transitional, causing `Navigation.goBack(listPath)` to silently fail with `[Navigation] Unable to go up` or evaluate to an invalid dynamic path.
   Conversely, line 85 already defines `backTo = getPathWithoutDynamicSuffix(listPath, DYNAMIC_ROUTES.CONTACT_METHODS.path) || ROUTES.SETTINGS_PROFILE.route`, which provides a clean static fallback target.
2. **One-shot guard with `usePrevious` prevents retry on drop:**
   The effect is guarded by:
   ```ts
   if (prevValidatedDate || !loginData?.validatedDate) {
       return;
   }
   ```
   `usePrevious` updates its internal ref on each render cycle. Once `validatedDate` arrives in Onyx, `prevValidatedDate` becomes truthy on the immediate next render. If the `goBack` call fails or is dropped during the reconnect transition, the effect never re-runs, stranding the user on the contact method details view.

### What alternative solutions did you explore? (Optional)
None, ensuring route target stability via `backTo` and using an explicit navigation latch ref is the robust pattern.

### What changes do you think we should make in order to solve the problem?

In `src/pages/settings/Profile/Contacts/DynamicContactMethodDetailsPage.tsx`:
1. Use a ref latch (`hasNavigatedOnValidation`) instead of relying solely on `usePrevious`.
2. Target `backTo` (or `listPath` with `backTo` fallback) rather than bare `listPath`:

```diff
--- a/src/pages/settings/Profile/Contacts/DynamicContactMethodDetailsPage.tsx
+++ b/src/pages/settings/Profile/Contacts/DynamicContactMethodDetailsPage.tsx
@@ -134,18 +134,22 @@ function DynamicContactMethodDetailsPage({route}: DynamicContactMethodDetailsPage
     const isFocused = useIsFocused();
     const [shouldNavigateOnFocus, setShouldNavigateOnFocus] = useState(false);
+    const hasNavigatedOnValidation = useRef(false);
 
     useEffect(() => {
-        if (prevValidatedDate || !loginData?.validatedDate) {
+        if (hasNavigatedOnValidation.current || !loginData?.validatedDate) {
             return;
         }
 
         if (isFocused) {
+            hasNavigatedOnValidation.current = true;
             // Navigate to methods page on successful validateCode verification.
             // The validatedDate property indicates successful validateCode verification.
-            Navigation.goBack(listPath);
+            Navigation.goBack(backTo);
         } else {
             // Set flag to navigate when screen regains focus
             setShouldNavigateOnFocus(true);
         }
-    }, [prevValidatedDate, loginData?.validatedDate, isDefaultContactMethod, listPath]);
+    }, [loginData?.validatedDate, isFocused, backTo]);
 
     // Handle navigation when screen regains focus and flag is set
     useEffect(() => {
@@ -155,7 +159,8 @@ function DynamicContactMethodDetailsPage({route}: DynamicContactMethodDetailsPage
         }
         setShouldNavigateOnFocus(false);
-        Navigation.goBack(listPath);
+        hasNavigatedOnValidation.current = true;
+        Navigation.goBack(backTo);
     }, [isFocused, shouldNavigateOnFocus, backTo]);
```

### What automated tests can you add to prevent this from re-occurring?
Add a unit test in `tests/unit/pages/DynamicContactMethodDetailsPageTest.tsx` simulating:
1. Entering magic code offline (login marked pending).
2. Simulating reconnect batch updating `loginData.validatedDate` while `DynamicContactMethodDetailsPage` is mounted.
3. Asserting that `Navigation.goBack(backTo)` is called, returning the user to the contact methods list.
