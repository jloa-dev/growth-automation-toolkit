Contributor details
Your Expensify account email: jloa.dev@gmail.com
Upwork Profile Link: https://www.upwork.com/freelancers/~0163955a2ba22190aa

## Proposal

### Please re-state the problem that we are trying to solve in this issue.
When receipts are forwarded to `receipts@expensify.com` (such as tall, vertical order confirmations or invoice emails), the receipt preview in the expense details panel crops out the bottom half of the receipt. When tapping the receipt to open the full-screen modal, the complete receipt is visible.

### What is the root cause of that problem?
1. In `src/components/ReportActionItem/MoneyRequestReceiptView.tsx` (line 755), when `!fillSpace` (standard expense preview in RHP), the receipt image sits in a fixed 16:9 container (`styles.expenseViewImage` / `styles.expenseViewImageSmall`).
2. `MoneyRequestReceiptView` delegates rendering to `ReportActionItemImage`. However, `ReportActionItemImageProps` does not accept or pass a `resizeMode` prop.
3. In `src/components/ReportActionItem/ReportActionItemImage.tsx`, the constructed `propsObj` passed to `ReceiptImage` lacks `resizeMode`.
4. While `ReceiptImage` (`src/components/ReceiptImage/index.tsx`, lines 119, 151, 231) already accepts and forwards `resizeMode` to `ThumbnailImage` / `ImageWithSizeCalculation`, omitting `resizeMode` causes `ImageWithSizeCalculation.tsx` (line 88) to default to `'cover'`.
5. Because `resizeMode="cover"` is applied to tall vertical email receipts inside a 16:9 container, the top of the receipt expands to fit the full width, causing the entire bottom section (line items, taxes, and total amounts) to be cropped out of view.

### What changes do you think we should make in order to solve the problem?
1. In `src/components/ReportActionItem/ReportActionItemImage.tsx`:
   - Add optional `resizeMode?: ReceiptImageProps['resizeMode'];` to `ReportActionItemImageProps`.
   - Forward `resizeMode` into `propsObj` across the thumbnail/image branches.

2. In `src/components/ReportActionItem/MoneyRequestReceiptView.tsx`:
   - Pass `resizeMode={!fillSpace ? 'contain' : undefined}` to `<ReportActionItemImage />`.
   - When displayed inside the bounded 16:9 thumbnail frame (`!fillSpace`), the whole receipt fits cleanly via `contain` without cutting off bottom receipt details.
   - For `fillSpace` (wide desktop view), it preserves full dynamic height without letterboxing.

```diff
--- a/src/components/ReportActionItem/MoneyRequestReceiptView.tsx
+++ b/src/components/ReportActionItem/MoneyRequestReceiptView.tsx
@@ -753,6 +753,7 @@ function MoneyRequestReceiptView({
                                     {({isHovering}) => (
                                         <>
                                             <ReportActionItemImage
+                                                resizeMode={!fillSpace ? 'contain' : undefined}
                                                 shouldUseThumbnailImage={!fillSpace}
                                                 shouldUseFullHeight={fillSpace}
                                                 canZoomReceipt={canZoomReceipt}
--- a/src/components/ReportActionItem/ReportActionItemImage.tsx
+++ b/src/components/ReportActionItem/ReportActionItemImage.tsx
@@ -98,6 +98,9 @@ type ReportActionItemImageProps = {
     /** Whether the receipt can be hover-zoomed. When true, remote PDFs render the actual PDF on top of the thumbnail so magnification stays sharp (web only). */
     canZoomReceipt?: boolean;
 
+    /** Resize mode for the receipt image */
+    resizeMode?: ReceiptImageProps['resizeMode'];
+
     /** Callback to be called when the image loads */
     onLoad?: (event?: {nativeEvent: {width: number; height: number}}) => void;
@@ -130,6 +133,7 @@ function ReportActionItemImage({
     report: reportProp,
     shouldUseThumbnailImage,
     canZoomReceipt = false,
+    resizeMode,
     onLoad,
     onLoadFailure,
 }: ReportActionItemImageProps) {
@@ -198,6 +202,7 @@ function ReportActionItemImage({
 
             // If the image is full height, use initial position to make sure it will grow properly to fill the container
             shouldUseInitialObjectPosition: isMapDistanceRequest && !shouldUseFullHeight,
+            resizeMode,
         };
     } else if (effectiveIsLocalFile && isPDF && typeof originalImageSource === 'string') {
         propsObj = {isPDFThumbnail: true, source: originalImageSource};
@@ -214,6 +219,7 @@ function ReportActionItemImage({
             // If the image is full height, use initial position to make sure it will grow properly to fill the container
             shouldUseInitialObjectPosition: isMapDistanceRequest && !shouldUseFullHeight,
             isEmptyReceipt,
+            resizeMode,
             onPress,
         };
     }
```

Pre-coded and tested in branch: `fix/104138-receipt-preview-resize-mode` (https://github.com/jloa-dev/App/tree/fix/104138-receipt-preview-resize-mode).

### What alternative solutions did you explore? (Optional)
Expanding the preview container's height to match the receipt's native aspect ratio. However, long email receipts can be 3000px+ high, which would distort the expense details screen and push all expense fields far below the fold. Using `contain` within the standard preview bounds cleanly displays the entire receipt while preserving the layout.
