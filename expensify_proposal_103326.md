## Proposal

### Please re-state the problem that we are trying to solve in this issue.
When the user goes offline and attaches a file to a chat that already contains text in the composer, on Android native the comment does not display the expected pending/greyed-out indicator or the optimistic action fails to appear.

### What is the root cause of that problem?
There are two coupled root causes:

1. **Premature `clearComposer` Worklet Retries on Native Resume**:
   In `src/pages/inbox/report/ReportActionCompose/useAttachmentPicker.ts:50-56`:
   ```typescript
   if (isNative) {
       if (exceededMaxLength) {
           return;
       }
       addAttachment(files);
       return;
   }
   ```
   When the Android system document/image picker returns, the React Native Activity resumes. `addAttachment` immediately calls `clearComposer()` (`src/pages/inbox/report/ReportActionCompose/ComposerProvider.tsx:124-149`).
   At this exact instant, the composer ref or its `clearWorklet` has often not finished re-attaching. Because `CONST.COMPOSER.CLEAR_WORKLET_MAX_RETRIES` (3 retries via `requestAnimationFrame`) is exhausted in <50ms before the native input is ready, `clearComposer` logs:
   `[ComposerProvider] Skipping clearComposer because composerRef.clearWorklet never re-attached`
   and sets `attachmentFileRef.current = null`. As a result, `validateAndSubmitDraft` is never triggered and the optimistic comment is silently dropped.

2. **Optimistic Translation Key & Rendering in Combined Messages**:
   In `src/libs/ReportUtils.ts:7235-7265` (`buildOptimisticAddCommentReportAction`):
   ```typescript
   const isAttachmentOnly = file && !text;
   const isAttachmentWithText = !!text && file !== undefined;
   // ...
   translationKey: isAttachmentOnly ? CONST.TRANSLATION_KEYS.ATTACHMENT : '',
   ```
   When text is present, `translationKey` is intentionally empty. The pending grey status in NewDot is driven by `OfflineWithFeedback` (`pendingAction: CONST.RED_BRICK_ROAD_PENDING_ACTION.ADD`) applying `opacity: 0.5`. However, in `ReportActionItemFragment.tsx:117-130`, because `isReportMessageAttachment` returns `false` when text is present (`hasOtherContent === true`), it renders `TextCommentFragment`. In `TextCommentFragment`, if the optimistic image HTML tag has local file URI without an established cached thumbnail dimension while offline, the image container collapses or fails to show the pending dimmed container properly.

### What changes do you think we should make in order to solve the problem?

1. **Robust Native Worklet Re-attachment in `ComposerProvider.tsx`**:
   Increase retry tolerance and handle post-system-picker re-attachment on native platforms so `clearComposer` does not discard `attachmentFileRef`:
   ```typescript
   const maxRetries = isNative ? CONST.COMPOSER.CLEAR_WORKLET_NATIVE_MAX_RETRIES : CONST.COMPOSER.CLEAR_WORKLET_MAX_RETRIES;
   ```
   Or allow `clearComposer` to fallback to direct programmatic clearing and submit trigger if `clearWorklet` is unavailable.

2. **Ensure Optimistic Offline Attachment Container Renders Consistently**:
   In `src/libs/ReportUtils.ts`, ensure `getUploadingAttachmentHtml` provides explicit initial fallback bounding styles for offline local URIs so `RenderCommentHTML` inside `TextCommentFragment` displays the dimmed local file preview and text with `OfflineWithFeedback` styling intact.

3. **Update Test Case Guidance**:
   Clarify in Applause test documentation that NewDot replaces the legacy OldDot literal string `"Uploading Attachment"` with an optimistic dimmed card/message showing the text + attachment preview at 50% opacity.

### What alternative solutions did you explore? (Optional)
- Forcing a modal preview on Android (reverting PR #98528): Not recommended as skipping the preview modal on native improves mobile UX and was a deliberate product decision.

### What specific scenarios should we cover in automated tests?
In `tests/unit/ComposerProviderTest.tsx` and `tests/unit/ReportActionComposeTest.tsx`:
1. Simulate picking an attachment with pre-filled text while offline on Android, verifying that `addAttachmentWithComment` is called and `attachmentFileRef` is not dropped prematurely.
2. Assert that the resulting optimistic `reportAction` contains both the text and the attachment with `pendingAction: 'add'` and is rendered with dimmed pending opacity.
