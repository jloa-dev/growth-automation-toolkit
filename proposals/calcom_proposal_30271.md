# Cal.com Issue #30271 Technical Solution Proposal

**Issue**: [#30271 - Date overrides split into duplicate days, and today's override disappears, when the server TZ is not UTC](https://github.com/calcom/cal.diy/issues/30271)  
**Repository**: `calcom/cal.diy`  
**Bounty / Platform**: $250 USD (Algora / Stripe Express Interbank PEN `••••8245`)  
**Status**: 0 Bot competition, Ready for PR  
**Contributor**: `jloa-dev` (`jloa.dev@gmail.com`)  

---

## 1. Problem Statement
When the server process runs in a timezone other than UTC (e.g. `TZ=America/New_York` or `TZ=America/Lima`):
1. **Duplicate Entries**: A date override containing multiple time ranges (e.g. 09:00-12:00 and 14:00-17:00 UTC) is split into separate single-range entries instead of being grouped into one entry.
2. **Dropped "Today" Overrides**: A date override for today is filtered out as if it were in the past.

---

## 2. Root Cause Analysis
In `packages/lib/schedules/transformers/for-atom.ts`:
```ts
const currentUtcOffset = dayjs().tz(timeZone).utcOffset();
const currentTimeInTz = dayjs().utc().add(currentUtcOffset, "minute");

if (!override.date || dayjs(override.date).isBefore(currentTimeInTz, "day")) {
  return acc;
}
...
const dayRangeIndex = acc.findIndex(
  (item) => override.date && yyyymmdd(item.ranges[0].start) === yyyymmdd(override.date)
);
```

1. **Storage Format**: Override dates in the database are stored as UTC midnight (e.g., `2026-10-10T00:00:00.000Z`).
2. **Grouping Failure**: `yyyymmdd` formats in the server's local process timezone. On a server in `America/New_York` (UTC-4), `override.date` evaluates to `2026-10-09 20:00:00`, formatting as `"2026-10-09"`. However, `item.ranges[0].start` (which starts at 09:00 UTC = 05:00 EDT) formats as `"2026-10-10"`. Because `"2026-10-10" !== "2026-10-09"`, the ranges never match and are split into duplicate days.
3. **Filtering Failure**: `dayjs(override.date).isBefore(currentTimeInTz, "day")` uses local server time for `dayjs(override.date)`. Shifting UTC midnight into negative timezones puts it into the previous day, causing today's override to be dropped.
4. **Subtle Flaw in Naive Fixes**: Attempting to fix this via `dayjs(override.date).tz(timeZone)` also shifts the UTC midnight date backwards in Western timezones (America/New_York is UTC-4, turning `2026-10-10T00:00Z` into `2026-10-09 20:00`). The correct representation is to treat `override.date` as a calendar date in UTC.

---

## 3. Surgical Implementation
Use `dayjs.utc(override.date)` for both filtering and range grouping:

```diff
--- a/packages/lib/schedules/transformers/for-atom.ts
+++ b/packages/lib/schedules/transformers/for-atom.ts
@@ -1,6 +1,5 @@
 import dayjs from "@calcom/dayjs";
 import { getWorkingHours } from "@calcom/lib/availability";
-import { yyyymmdd } from "@calcom/lib/dayjs";
 import type { Availability } from "@calcom/prisma/client";
 import type { Schedule, TimeRange } from "@calcom/types/schedule";
 
@@ -36,7 +35,7 @@ export function transformDateOverridesForAtom(
       const currentUtcOffset = dayjs().tz(timeZone).utcOffset();
       const currentTimeInTz = dayjs().utc().add(currentUtcOffset, "minute");
 
-      if (!override.date || dayjs(override.date).isBefore(currentTimeInTz, "day")) {
+      if (!override.date || dayjs.utc(override.date).isBefore(currentTimeInTz, "day")) {
         return acc;
       }
       const newValue = {
@@ -53,7 +52,10 @@ export function transformDateOverridesForAtom(
       };
       const dayRangeIndex = acc.findIndex(
         // early return prevents override.date from ever being empty.
-        (item) => override.date && yyyymmdd(item.ranges[0].start) === yyyymmdd(override.date)
+        (item) =>
+          override.date &&
+          dayjs.utc(item.ranges[0].start).format("YYYY-MM-DD") ===
+            dayjs.utc(override.date).format("YYYY-MM-DD")
       );
       if (dayRangeIndex === -1) {
         acc.push({ ranges: [newValue] });
```

---

## 4. Verification & Test Plan
Verified across multiple simulated process timezones (`TZ=America/New_York`, `TZ=America/Lima`, `TZ=UTC`):
1. **Grouping Invariance**: Multiple ranges for the same date are grouped into a single entry with multiple ranges.
2. **Today Preservation**: An override for today in the schedule timezone is retained and never dropped.
3. **Past Exclusions**: Overrides strictly before today are accurately excluded.
