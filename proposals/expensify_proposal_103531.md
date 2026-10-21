## Proposal

### Please re-state the problem that we are trying to solve in this issue.
On iOS, when viewing a password-protected PDF attachment, rotating the device from portrait to landscape closes the password input and soft keyboard, and the carousel resets or navigates unexpectedly to another attachment.

### What is the root cause of that problem?
In `src/components/Attachments/AttachmentCarousel/AttachmentCarouselView/index.native.tsx`, the native pager emits `onPageSelected` events during layout recomputation and orientation changes (SwiftUI `TabView` container re-render). 

`updatePage` unconditionally executes `Keyboard.dismiss()` and updates the page state:
```typescript
const updatePage = useCallback(
    (newPageIndex: number) => {
        Keyboard.dismiss();
        setShouldShowArrows(true);
        // ...
        setPage(newPageIndex);
    },
    [setShouldShowArrows, attachments, setPage, onNavigate],
);
```

Because `updatePage` did not check whether `newPageIndex === page`:
1. When the device rotates while viewing the protected PDF (at current `page`), the native layout pass emits `onPageSelected` (with position 0 or the current position).
2. `Keyboard.dismiss()` is immediately triggered, which dismisses the iOS software keyboard and closes the PDF password form modal.
3. If the pager emitted 0 unprompted during orientation re-measurement, `setPage(0)` switches the active attachment back to the first item in the report instead of preserving the currently viewed attachment.

### What changes do you think we should make in order to solve the problem?
1. In `src/components/Attachments/AttachmentCarousel/AttachmentCarouselView/index.native.tsx`, add an early return guard in `updatePage` so that when `newPageIndex === page`, no redundant page state transition occurs and `Keyboard.dismiss()` is never called:
```typescript
const updatePage = useCallback(
    (newPageIndex: number) => {
        if (newPageIndex === page) {
            return;
        }
        Keyboard.dismiss();
        setShouldShowArrows(true);

        const item = attachments.at(newPageIndex);

        setPage(newPageIndex);
        if (newPageIndex >= 0 && item) {
            setActiveAttachmentID(item.attachmentID ?? item.source);
            if (onNavigate) {
                onNavigate(item);
            }
        }
    },
    [setShouldShowArrows, attachments, setPage, onNavigate, page],
);
```

2. Additionally, in `AttachmentCarouselPager` (`src/components/Attachments/AttachmentCarousel/AttachmentCarouselView/index.native.tsx`), ensure `onPageSelected` only dispatches when `newPage !== page`:
```typescript
onPageSelected={({nativeEvent: {position: newPage}}) => {
    if (newPage !== page) {
        updatePage(newPage);
    }
}}
```

This prevents keyboard dismissal on device rotation and preserves the user's active password input screen seamlessly across orientations.

### What alternative solutions did you explore? (Optional)
- Dismissing keyboard only on manual touch gestures: Redundant since checking `newPageIndex === page` directly resolves both false-positive dismissal and unprompted navigation resets without complex touch event listeners.
- Patching `react-native-pager-view` directly: Unnecessary overhead since guarding the callback in JS cleanly handles native layout change events without maintaining extra native patches.

### Tests
1. Open a chat report containing multiple attachments including a password-protected PDF.
2. Tap on the protected PDF to open the attachment preview modal.
3. Tap on the password input field so the keyboard is focused.
4. Rotate the device from portrait to landscape and back.
5. Verify that the keyboard remains open, the password modal is intact, and the viewer stays on the current protected PDF.
6. Swipe left and right between attachments to confirm normal navigation still works and dismisses the keyboard as intended.

Contributor details
Your Expensify account email: jloa.dev@gmail.com
Upwork Profile Link: https://www.upwork.com/freelancers/~0163955a2ba22190aa
