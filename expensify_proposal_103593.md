Contributor details
Your Expensify account email: jloa.dev@gmail.com
Upwork Profile Link: https://www.upwork.com/freelancers/~0163955a2ba22190aa

## Proposal

### Please re-state the problem that we are trying to solve in this issue.
On Android and iOS, taking a photo via Create (+) > Attachment > Take photo sends the photo directly into chat without showing a preview screen where the user can inspect or retake it.

### What is the root cause of that problem?
In `src/pages/inbox/report/ReportActionCompose/useAttachmentPicker.ts` (lines 50–57), PR #98528 bypassed the attachment preview modal on native platforms (`if (isNative) { addAttachment(files); return; }`) under the assumption that the system camera already provided its own native "Use Photo / Retake" review screen.

However, PR #96458 introduced the in-app `AttachmentCamera` (VisionCamera). When capturing a photo, `handleCameraCapture` in `src/components/AttachmentPicker/index.native.tsx` invokes `pickAttachment(assets)`, which flows through `onFilesValidated`. Because `isNative` is true, it immediately calls `addAttachment(files)` and sends the photo without ever opening the `REPORT_ADD_ATTACHMENT` preview modal or offering a retake step.

### What changes do you think we should make in order to solve the problem?
We should pass an optional flag (`shouldShowPreview?: boolean`) specifically for in-app camera captures so that camera captures open the preview modal while gallery and document pickers keep their direct-send native behavior:

1. In `src/components/AttachmentPicker/types.ts`, update `PickerOptions` to accept `onPicked: (files: FileObject[], options?: {shouldShowPreview?: boolean}) => void`.
2. In `src/components/AttachmentPicker/index.native.tsx`, pass `{shouldShowPreview: true}` inside `handleCameraCapture` when calling `pickAttachment(assets)`.
3. In `AttachmentPickerWithMenuItems.tsx` and `ComposerActionMenu.tsx`, propagate `shouldShowPreview` through `onAttachmentPicked` to `pickAttachments`.
4. In `src/pages/inbox/report/ReportActionCompose/useAttachmentPicker.ts`, update `onFilesValidated` so that `isNative` only bypasses preview when `!shouldShowPreview`:
   - If `shouldShowPreview` is true (in-app camera capture), set the attachment in `reportAttachmentsContext` and navigate to `ROUTES.REPORT_ADD_ATTACHMENT.getRoute(reportID)`.
   - Gallery and file uploads (`!shouldShowPreview`) continue to call `addAttachment(files)` directly.

### What alternative solutions did you explore? (Optional)
Adding custom "Retake" / "Send" buttons directly inside `AttachmentCamera`. While possible, leveraging the established `REPORT_ADD_ATTACHMENT` preview screen is simpler, fully localized, consistent with web/desktop, and does not require duplicate UI components.
