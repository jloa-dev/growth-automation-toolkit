## Proposal

### Please re-state the problem that we are trying to solve in this issue.
On Android, a Sentry crash (APP-M66) occurs with `java.lang.IllegalStateException: dialog must exist when we call updateProperties` inside `ReactModalHostView.updateSystemAppearance`.

### What is the root cause of that problem?
In our React Native patch [`patches/react-native/react-native+0.86.0+019+fix-modal-transparent-navigation-bar.patch#L18`](https://github.com/Expensify/App/blob/main/patches/react-native/react-native+0.86.0+019+fix-modal-transparent-navigation-bar.patch#L18), we schedule a deferred UI tick to update system bar appearances:
```kotlin
window.decorView.post { updateSystemAppearance() }
```
When a modal is rapidly closed or unmounted immediately after opening, `dismiss()` runs before the posted runnable executes on the looper queue, setting `dialog = null`. When the posted runnable subsequently runs, `updateSystemAppearance()` executes:
```kotlin
checkNotNull(dialog) { "dialog must exist when we call updateProperties" }
```
which throws an `IllegalStateException` and crashes the application because `dialog` is null.

### What changes do you think we should make in order to solve the problem?
1. In `patches/react-native/react-native+0.86.0+019+fix-modal-transparent-navigation-bar.patch`, safeguard the deferred runnable by verifying that `dialog` still exists and is currently showing:
```kotlin
window.decorView.post {
    val currentDialog = dialog
    if (currentDialog != null && currentDialog.isShowing) {
        updateSystemAppearance()
    }
}
```
2. Re-apply and verify the patch with `npx patch-package react-native`.
3. Update `patches/react-native/details.md` with the null-safety rationale for patch 019.

### What alternative solutions did you explore? (Optional)
- Wrapping `updateSystemAppearance()` in a `try-catch` block: rejected because silently swallowing exceptions is defensive anti-pattern compared to explicit null/lifecycle checks.
- Cancelling the runnable via `removeCallbacks`: adds unnecessary runnable reference tracking when a simple guard check achieves the exact same protection cleanly.
