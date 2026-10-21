Contributor details
Your Expensify account email: jloa.dev@gmail.com
Upwork Profile Link: https://www.upwork.com/freelancers/~0163955a2ba221e513

## Proposal

### Please re-state the problem that we are trying to solve in this issue.
On Android HybridApp, navigating between screens (e.g., visiting `Settings_Troubleshoot` or during screen transitions inside a ScreenStack) crashes fatally with:
`IllegalArgumentException: Maximum number of items supported by CustomBottomNavigationView is 6`
thrown from:
```
com.swmansion.rnscreens.ScreenStack.onUpdate (ScreenStack.kt:323)
com.swmansion.rnscreens.gamma.tabs.container.TabsContainer.onAttachedToWindow (TabsContainer.kt:311)
com.swmansion.rnscreens.gamma.tabs.container.TabsContainer.flushPendingUpdates (TabsContainer.kt:212)
com.swmansion.rnscreens.gamma.tabs.container.TabsContainer.updateNavigationMenuStructure (TabsContainer.kt:545)
com.swmansion.rnscreens.gamma.tabs.container.MenuHelpersKt.getOrCreateMenuItemForFragment (MenuHelpers.kt:8)
androidx.appcompat.view.menu.MenuBuilder.add
```

### What is the root cause of that problem?
1. In `react-native-screens` (gamma tabs on Android), `TabsContainer` manages bottom navigation tabs using `CustomBottomNavigationView` (based on Android Material's `BottomNavigationView`). Android's bottom navigation menu enforces a strict hardware constraint:
   `MAX_ITEM_COUNT = 6` (or 5 standard, 6 custom). Adding a 7th item to `MenuBuilder` throws `IllegalArgumentException`.
2. In `ScreenStack.kt:286`, when screen fragments are updated or re-appended in stack order, the fragment containing the tab bar is detached and re-attached to the window (`transaction.remove(wrapper.fragment)` followed by `transaction.add(...)`).
3. When `TabsContainer.onAttachedToWindow()` executes, it calls `flushPendingUpdates()` -> `updateNavigationMenuStructure()`.
4. In `updateNavigationMenuStructure()`, `TabsContainer` iterates through its tab fragments and calls `getOrCreateMenuItemForFragment(fragment)` which delegates to `bottomNavigationView.menu.add(...)`.
5. However, `updateNavigationMenuStructure()` does not clear or synchronize the existing `bottomNavigationView.menu` prior to re-populating items. Because items from the initial layout pass are already present in the menu, re-adding the tabs appends duplicate menu items to the `MenuBuilder`. As soon as `menu.size()` reaches 7 (e.g. 4 tabs added twice = 8 items), Android throws `IllegalArgumentException: Maximum number of items supported by CustomBottomNavigationView is 6`.

### What alternative solutions did you explore? (Optional)
None, clearing existing menu items in `TabsContainer.updateNavigationMenuStructure` before adding items is the cleanest, idiomatic solution.

### What changes do you think we should make in order to solve the problem?
Add patch `patches/react-native-screens/react-native-screens+4.28.0+006+clear-tab-menu-before-update.patch`:

In `node_modules/react-native-screens/android/src/main/java/com/swmansion/rnscreens/gamma/tabs/container/TabsContainer.kt`:
Before populating fragments in `updateNavigationMenuStructure()`, clear the existing menu:

```diff
--- a/node_modules/react-native-screens/android/src/main/java/com/swmansion/rnscreens/gamma/tabs/container/TabsContainer.kt
+++ b/node_modules/react-native-screens/android/src/main/java/com/swmansion/rnscreens/gamma/tabs/container/TabsContainer.kt
@@ -542,6 +542,7 @@ class TabsContainer(
     }
 
     private fun updateNavigationMenuStructure() {
+        bottomNavigationView.menu.clear()
         fragments.forEachIndexed { index, fragment ->
             val menuItem = getOrCreateMenuItemForFragment(fragment)
```

### What automated tests can you add to prevent this from re-occurring?
Add an Android instrumented/unit test for `TabsContainer` verifying that calling `onAttachedToWindow()` and `flushPendingUpdates()` repeatedly on a `TabsContainer` with 4-5 tabs never causes `bottomNavigationView.menu.size()` to exceed the fragment count or throw `IllegalArgumentException`.
