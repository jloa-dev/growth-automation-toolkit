Contributor details
Your Expensify account email: jloa.dev@gmail.com
Upwork Profile Link: https://www.upwork.com/freelancers/~0163955a2ba22190aa

## Proposal

### Please re-state the problem that we are trying to solve in this issue.
The GPS distance counter builds its label by manually joining separate pieces in JSX instead of using localized number and unit formatting:
- `common.distance` field name
- the rounded distance number, styled bold
- a hard-coded space, then the raw `unit` string (`mi` / `km`), styled muted
In `src/pages/iou/request/step/IOURequestStepDistanceGPS/Waypoints/DistanceCounter.tsx:36-40`.

This breaks across locales where:
1. The unit is placed before the amount or without an ASCII space.
2. The unit is displayed as raw English symbols rather than localized.
3. Number formatting (decimals/group separators) does not respect user locale.

### What is the root cause of that problem?
In `DistanceCounter.tsx:37-42`:
```typescript
titleComponent={
    <Text style={[styles.iouAmountTextInput, styles.textXLarge, styles.colorMuted, styles.ml3]}>
        <Text style={[styles.iouAmountTextInput, styles.textXLarge]}>{distance}</Text>
        {` ${unit}`}
    </Text>
}
```
The component manually concatenates `{distance}` and `{` ${unit}`}` inside a styled text container, bypassing the locale-aware formatting pipeline.

### What changes do you think we should make in order to solve the problem?
1. **Leverage `Intl.NumberFormat` with `formatToParts` in `DistanceCounter.tsx`**:
   In `src/pages/iou/request/step/IOURequestStepDistanceGPS/Waypoints/DistanceCounter.tsx`:
   - Map policy `unit` to standard Unicode unit identifiers (`CONST.POLICY.UNIT.MI -> 'mile'`, `CONST.POLICY.UNIT.KM -> 'kilometer'`).
   - Use `preferredLocale` from `useLocalize` to format using `Intl.NumberFormat(preferredLocale, { style: 'unit', unit: unitIdentifier, unitDisplay: 'short' })`.
   - Call `.formatToParts(distance)` to decompose the localized string into individual tokens:
     - Numeric parts (`integer`, `decimal`, `fraction`, `group`) rendered with `[styles.iouAmountTextInput, styles.textXLarge]`.
     - Non-numeric parts (`literal`, `unit`) rendered with `[styles.iouAmountTextInput, styles.textXLarge, styles.colorMuted]`.
   - This automatically respects the exact grammatical ordering, spacing, and translation of every locale while strictly preserving the visual distinction between the bold value and the muted unit.

2. **Automated Unit Tests**:
   Add unit tests in `tests/unit/DistanceCounterTest.tsx` validating:
   - English (`en`) locale: formats distance and short unit (e.g., `12.5 mi`).
   - Spanish (`es`) locale: formats distance with comma and localized unit (`12,5 km`).
   - Token-based styling correctly styles numeric parts with bold text and unit/literal parts with muted text.

### What alternative solutions did you explore? (Optional)
- HTML template string parsed via `RenderHTML`: Heavier runtime footprint and unnecessary parsing overhead for numeric metrics compared to the native `Intl.NumberFormat.formatToParts` standard.
