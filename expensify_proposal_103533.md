## Proposal

### Please re-state the problem that we are trying to solve in this issue.
On wide desktop viewports, an image attachment message preview displayed inside the Concierge Right Hand Panel (RHP) side panel overflows the message column width and appears cut off on the right edge.

### What is the root cause of that problem?
In `src/hooks/useThumbnailDimensions.ts:19-20`, image thumbnail dimensions are chosen based solely on `shouldUseNarrowLayout`:
```typescript
const {shouldUseNarrowLayout} = useResponsiveLayout();
const fixedDimension = shouldUseNarrowLayout ? CONST.THUMBNAIL_IMAGE.SMALL_SCREEN.SIZE : CONST.THUMBNAIL_IMAGE.WIDE_SCREEN.SIZE;
```
1. On desktop screens, `shouldUseNarrowLayout` evaluates to `false`.
2. Consequently, `fixedDimension` is assigned `CONST.THUMBNAIL_IMAGE.WIDE_SCREEN.SIZE` (350px).
3. However, the side panel (`SidePanelReport`) has a fixed container width of 375px (`variables.sidePanelWidth`). Accounting for the chat item padding (20px horizontal) and avatar column spacing, the available message content width is under 300px.
4. Because the thumbnail width is fixed to 350px, the image container overflows its parent boundary and is clipped by the panel border.

### What changes do you think we should make in order to solve the problem?
The Concierge side panel wraps its inner `ReportScreen` inside `IsInSidePanelContext`. We can consume this existing context via `useIsInSidePanel` inside `useThumbnailDimensions`:

In `src/hooks/useThumbnailDimensions.ts`:
```typescript
import useIsInSidePanel from './useIsInSidePanel';
import useResponsiveLayout from './useResponsiveLayout';

export default function useThumbnailDimensions(width: number, height: number): ThumbnailDimensions {
    const {shouldUseNarrowLayout} = useResponsiveLayout();
    const isInSidePanel = useIsInSidePanel();
    const fixedDimension = shouldUseNarrowLayout || isInSidePanel ? CONST.THUMBNAIL_IMAGE.SMALL_SCREEN.SIZE : CONST.THUMBNAIL_IMAGE.WIDE_SCREEN.SIZE;
```

1. When rendered inside the Concierge side panel, `isInSidePanel` is `true`, so `fixedDimension` adopts `CONST.THUMBNAIL_IMAGE.SMALL_SCREEN.SIZE` (250px), matching the narrow phone column layout.
2. In the main desktop chat pane, `isInSidePanel` is `false`, so wide desktop attachments remain rendered at full 350px width as expected.
3. This also automatically protects video preview thumbnails and image renderers that share `useThumbnailDimensions`.

### What alternative solutions did you explore? (Optional)
- Setting CSS `maxWidth: '100%'` on the inner image: Doesn't scale the aspect-ratio sized container correctly, causing letterboxing or parent overflow since the inner wrapper retains fixed 350px width.
- Forcing `shouldUseNarrowLayout` globally in `SidePanelReport`: Undesirable because it alters other responsive behaviors (such as header action menus) across the side panel.

### Tests
1. On desktop web or desktop app, open a chat with Concierge in the side panel (RHP).
2. Send or view an image attachment (landscape and portrait).
3. Verify that the image preview stays neatly within the message column without overflowing or cutting off.
4. Open the same chat in the main viewport and verify the image expands to standard desktop size (350px).

Contributor details
Your Expensify account email: jloa.dev@gmail.com
Upwork Profile Link: https://www.upwork.com/freelancers/~0163955a2ba22190aa
