Contributor details
Your Expensify account email: jloa.dev@gmail.com
Upwork Profile Link: https://www.upwork.com/freelancers/~0163955a2ba22190aa

## Proposal

### Please re-state the problem that we are trying to solve in this issue.
When an offline user creates a scan expense in self-DM, clicks "Submit it to someone", and views the expense confirmation page, the Amount field displays raw `"00"` instead of `"Scanning…"`.

### What is the root cause of that problem?
In `src/components/MoneyRequestConfirmationList/sections/AmountField.tsx`:
1. When moving an existing scan expense from self-DM via "Submit it to someone", `canEnterScanFieldsManually` is `false`.
2. `isAmountFieldDisabled` (line 95) currently only evaluates:
   ```ts
   const isAmountFieldDisabled = didConfirm || isReadOnly || shouldShowTimeRequestFields || isDistanceRequest;
   ```
   It does not account for an active scan where manual scan field entry is not enabled (`isScanning(transactionForHandlers) && !canEnterScanFieldsManually`).
3. Consequently, `isAmountFieldDisabled` remains `false`, rendering `<NumberWithSymbolForm>` as an editable text input instead of the read-only row (`ExpenseFieldRow` / `MenuItemWithTopDescription`).
4. In `shouldShowEmptyAmount` (lines 127–129), `iouRequestType` is `CONST.IOU.REQUEST_TYPE.SCAN` and `canEnterScanFieldsManually` is `false`, so `shouldShowEmptyAmount` evaluates to `false`. The unfinalized pending scan's default transaction amount (`0`) is formatted into frontend text via `convertToFrontendAmountAsString(0, decimals)`, displaying `"00"` (or `"0.00"`).
5. The read-only row already correctly computes and translates `"Scanning…"` via `useConfirmationAmount.ts` (`formattedAmount`), but was completely bypassed.

### What changes do you think we should make in order to solve the problem?
1. In `src/components/MoneyRequestConfirmationList/sections/AmountField.tsx`:
   - Extend `isAmountFieldDisabled` to include active scanning states when manual scan field editing is not enabled (`isScanning(transactionForHandlers) && !canEnterScanFieldsManually`).
   - Also add `isScanning(transactionForHandlers)` as a guard in `shouldShowEmptyAmount` to prevent converting raw zero amounts to text strings during any scanning step.

```diff
--- a/src/components/MoneyRequestConfirmationList/sections/AmountField.tsx
+++ b/src/components/MoneyRequestConfirmationList/sections/AmountField.tsx
@@ -16,7 +16,7 @@ import {calculateAmount, isMovingTransactionFromTrackExpense, isParticipantP2P}
 import {isConfirmationAmountMissing} from '@libs/MoneyRequestUtils';
 import Navigation from '@libs/Navigation/Navigation';
 import {shouldEnableNegative} from '@libs/ReportUtils';
-import {calculateTaxAmount, getTaxCode, getTaxValue, hasAnyManuallyEnteredScanField} from '@libs/TransactionUtils';
+import {calculateTaxAmount, getTaxCode, getTaxValue, hasAnyManuallyEnteredScanField, isScanning} from '@libs/TransactionUtils';
 
 import IOURequestStepCurrencyModal from '@pages/iou/request/step/IOURequestStepCurrencyModal';
 
@@ -92,7 +92,7 @@ function AmountField({
     const [isCurrencyPickerVisible, setIsCurrencyPickerVisible] = useState(false);
     const [isAmountInputFocused, setIsAmountInputFocused] = useState(false);
 
-    const isAmountFieldDisabled = didConfirm || isReadOnly || shouldShowTimeRequestFields || isDistanceRequest;
+    const isAmountFieldDisabled = didConfirm || isReadOnly || shouldShowTimeRequestFields || isDistanceRequest || (isScanning(transactionForHandlers) && !canEnterScanFieldsManually);
     // The read-only row only opens the amount page for a form whose amount the user could have typed in the first
     // place. A distance or time amount is computed from the fields below it, so its row has nothing to open and is
     // not offered as a control at all: no caret, no hover, no press.
@@ -126,6 +126,7 @@ function AmountField({
     // input doesn't retain the original "$0.00 with no error" bug.
     const shouldShowEmptyAmount =
         (!transactionSlice?.isAmountSet && (transactionSlice?.iouRequestType === CONST.IOU.REQUEST_TYPE.MANUAL || canEnterScanFieldsManually)) ||
+        isScanning(transactionForHandlers) ||
         !!transactionSlice?.isFailedScanAmountPlaceholder;
     const transactionAmount = shouldShowEmptyAmount ? '' : convertToFrontendAmountAsString(amount, decimals);
     // The hint says SmartScan will fill this in. It goes once the user takes the field over, by focusing it or by
```

- When `isAmountFieldDisabled` is true for this offline scan flow, `AmountField` correctly renders the read-only row showing `formattedAmount` (`translate('iou.receiptScanning')` -> `"Scanning…"`).
- `canOpenAmountPage` remains `true`, so if the user wishes to override the amount manually before SmartScan finishes, they can tap the row to enter an amount.

Pre-coded and tested in branch: `fix/104113-scan-amount-offline-scanning` (https://github.com/jloa-dev/App/tree/fix/104113-scan-amount-offline-scanning).

### What alternative solutions did you explore? (Optional)
Hiding the Amount field completely while receipt is scanning. However, users expect to see the Amount row with the clear `"Scanning…"` state and keep the ability to tap and manually override the amount.
