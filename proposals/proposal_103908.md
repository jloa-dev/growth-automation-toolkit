Contributor details
Your Expensify account email: jloa.dev@gmail.com
Upwork Profile Link: https://www.upwork.com/freelancers/~0163955a2ba22190aa

## Proposal

### Please re-state the problem that we are trying to solve in this issue.
When a workspace member submits an expense to a manager other than the workspace owner, clicking the expense report preview card from the workspace chat traps the app in an infinite loading spinner or renders a "Not here" error page.

### What is the root cause of that problem?
1. In `src/components/ReportActionItem/MoneyRequestReportPreview/MoneyRequestReportPreviewProvider.tsx` (line 141):
   ```ts
   const shouldShowAccessPlaceHolder = !iouReport && !shouldShowLoading;
   ```
   When the viewer lacks access to the underlying IOU report, `shouldShowAccessPlaceHolder` evaluates to `true`, and `AccessMoneyRequestReportPreviewPlaceHolder` is displayed inside the card.
2. However, in `src/components/ReportActionItem/MoneyRequestReportPreview/MoneyRequestReportPreviewBody.tsx` (lines 102–104):
   ```tsx
   <PressableWithoutFeedback
       onPress={onPress}
       role={CONST.ROLE.BUTTON}
   ```
   The card remains fully pressable and clickable with a pointer cursor. Clicking it executes `onPress` (`openReportFromPreview`).
3. In `openReportFromPreview` (line 210 of `MoneyRequestReportPreviewProvider.tsx`), it unconditionally navigates to `ROUTES.REPORT_WITH_ID.getRoute(iouReportID)` without verifying if `shouldShowAccessPlaceHolder` is `true`.
4. Navigating to `/r/<iouReportID>` mounts `ReportNotFoundGuard`. Because the backend returns no data for an unauthorized user, `isLoading` hangs indefinitely (infinite spinner) or renders `shouldShowNotFoundPage` ("Hmm... it's not here").

### What changes do you think we should make in order to solve the problem?
1. In `src/components/ReportActionItem/MoneyRequestReportPreview/MoneyRequestReportPreviewProvider.tsx`:
   - Guard `openReportFromPreview` against `shouldShowAccessPlaceHolder`:
   ```ts
   const openReportFromPreview = useCallback(() => {
       if (!iouReportID || shouldShowAccessPlaceHolder) {
           return;
       }
   ```
2. In `src/components/ReportActionItem/MoneyRequestReportPreview/MoneyRequestReportPreviewBody.tsx`:
   - Extract `shouldShowAccessPlaceHolder` from `useReportPreviewUIState()`.
   - Disable `onPress`, selection blocking, and button accessibility role when `shouldShowAccessPlaceHolder` is `true`:
   ```diff
   --- a/src/components/ReportActionItem/MoneyRequestReportPreview/MoneyRequestReportPreviewBody.tsx
   +++ b/src/components/ReportActionItem/MoneyRequestReportPreview/MoneyRequestReportPreviewBody.tsx
   @@ -76,7 +76,7 @@ function MoneyRequestReportPreviewBody({
        const {checkIfContextMenuActive} = useShowContextMenuActions();
    
        const {action, iouReport, chatReportID} = useReportPreviewData();
   -    const {isTransitionPending, isScanning, reportPreviewStyles} = useReportPreviewUIState();
   +    const {isTransitionPending, isScanning, reportPreviewStyles, shouldShowAccessPlaceHolder} = useReportPreviewUIState();
    
        const isReportDeleted = action?.pendingAction === CONST.RED_BRICK_ROAD_PENDING_ACTION.DELETE;
        const isRejectedReport = iouReport?.stateNum === CONST.REPORT.STATE_NUM.OPEN && iouReport?.nextStep?.messageKey === CONST.NEXT_STEP.MESSAGE_KEY.REJECTED_REPORT;
   @@ -100,8 +100,8 @@ function MoneyRequestReportPreviewBody({
                        testID="carouselWidthSetter"
                    >
                        <PressableWithoutFeedback
   -                        onPress={onPress}
   -                        onPressIn={() => canUseTouchScreen() && ControlSelection.block()}
   +                        onPress={shouldShowAccessPlaceHolder ? undefined : onPress}
   +                        onPressIn={() => !shouldShowAccessPlaceHolder && canUseTouchScreen() && ControlSelection.block()}
                            onPressOut={() => ControlSelection.unblock()}
                            onLongPress={(event) => {
                                if (!shouldDisplayContextMenu) {
   @@ -115,9 +115,10 @@ function MoneyRequestReportPreviewBody({
                                styles.justifyContentBetween,
                                StyleUtils.getBackgroundColorStyle(theme.cardBG),
                                shouldShowBorder ? styles.borderedContentCardLarge : styles.reportContainerBorderRadius,
   +                            (isReportDeleted || shouldShowAccessPlaceHolder) && styles.cursorDefault,
                                isReportDeleted && styles.pointerEventsNone,
                            ]}
   -                        role={CONST.ROLE.BUTTON}
   +                        role={shouldShowAccessPlaceHolder ? undefined : CONST.ROLE.BUTTON}
                            isNested
                            accessibilityLabel={translate('iou.viewDetails')}
                            sentryLabel={CONST.SENTRY_LABEL.REPORT_PREVIEW.CARD}
   ```

- Unauthorized users seeing the access placeholder card cannot click into a dead route, avoiding infinite spinners and 404 pages.
- Standard authorized previews remain 100% interactive as before.

Pre-coded and tested in branch: `fix/103908-inaccessible-preview-navigation` (https://github.com/jloa-dev/App/tree/fix/103908-inaccessible-preview-navigation).

### What alternative solutions did you explore? (Optional)
Hiding the preview card completely. However, keeping the preview visible with `AccessMoneyRequestReportPreviewPlaceHolder` is Expensify's intentional design pattern to notify chat participants of the transaction without exposing private amounts. Disabling click navigation when the placeholder is active is the clean and direct resolution.
