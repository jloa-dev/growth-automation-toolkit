# Cal.com Issue #30271 Technical Solution Proposal

**Issue**: [#30271 - Date overrides split into duplicate days, and today's override disappears, when the server TZ is not UTC](https://github.com/calcom/cal.diy/issues/30271)  
**Repository**: `calcom/cal.diy`  
**Bounty / Platform**: $250 USD (Algora / Stripe Express Interbank PEN `••••8245`)  
**Status**: 0 PRs, 0 Bot competition, Ready for PR  
**Contributor**: `jloa-dev` (`jloa.dev@gmail.com`)  

---

## 1. Problem Statement
When Cal.com server instances run on hosts with non-UTC system timezones (e.g. `TZ=America/New_York`, `TZ=Europe/Berlin`, or `TZ=Asia/Tokyo`):
1. **Duplicate Day Overrides**: A date override containing multiple time ranges (e.g. 09:00-12:00 and 14:00-17:00 UTC on 2026-10-10) is split into two separate entries in the output schedule array rather than a single day entry containing two ranges.
2. **Current Day Override Drop**: Date overrides scheduled for "today" in the user's schedule timezone are erroneously dropped as "past" dates if the server's local midnight has not caught up or is ahead of the schedule timezone.

This affects `ScheduleRepository`, the availability management page (`schedule/get` tRPC), and API v2 schedules (`/v2/schedules`).

---

## 2. Root Cause Analysis
In `packages/lib/schedules/transformers/for-atom.ts` (`transformDateOverridesForAtom`):
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

Two distinct defects cause this behavior:
1. `dayjs(override.date)` creates a dayjs instance in the NodeJS server's local timezone (`process.env.TZ`), whereas `currentTimeInTz` is manually shifted with minute arithmetic. In negative UTC offset timezones (e.g. EDT -04:00), `override.date` parses into the previous calendar day, causing `.isBefore(..., "day")` to incorrectly discard valid today overrides.
2. In the grouping lookup `yyyymmdd(item.ranges[0].start) === yyyymmdd(override.date)`, `yyyymmdd` formats the `Date` object using local server time (`YYYY-MM-DD`). If a UTC range starts at 01:00 UTC, a server in `America/New_York` (UTC-4) formats `item.ranges[0].start` as the previous day, causing `dayRangeIndex === -1` and appending a duplicate date bucket.

---

## 3. Surgical Implementation
Anchor date conversions strictly to the schedule's `timeZone` or UTC:

```diff
--- a/packages/lib/schedules/transformers/for-atom.ts
+++ b/packages/lib/schedules/transformers/for-atom.ts
@@ -28,10 +28,8 @@ export function transformDateOverridesForAtom(
 ) {
   const acc = schedule.availability.reduce(
     (acc, override) => {
-      // only if future date override
-      const currentUtcOffset = dayjs().tz(timeZone).utcOffset();
-      const currentTimeInTz = dayjs().utc().add(currentUtcOffset, "minute");
-
-      if (!override.date || dayjs(override.date).isBefore(currentTimeInTz, "day")) {
+      // Invariant to server TZ: evaluate 'today' in schedule's timezone
+      const todayInScheduleTz = dayjs().tz(timeZone).startOf("day");
+      const overrideDateInScheduleTz = dayjs(override.date).tz(timeZone);
+
+      if (!override.date || overrideDateInScheduleTz.isBefore(todayInScheduleTz, "day")) {
         return acc;
       }
       const newValue = {
@@ -47,9 +45,15 @@ export function transformDateOverridesForAtom(
           .minute(override.endTime.getUTCMinutes())
           .toDate(),
       };
+
+      const overrideKey = dayjs.utc(override.date).format("YYYY-MM-DD");
       const dayRangeIndex = acc.findIndex(
-        // early return prevents override.date from ever being empty.
-        (item) => override.date && yyyymmdd(item.ranges[0].start) === yyyymmdd(override.date)
+        (item) => dayjs.utc(item.ranges[0].start).format("YYYY-MM-DD") === overrideKey
       );
       if (dayRangeIndex === -1) {
         acc.push({ ranges: [newValue] });
```

---

## 4. Verification & Test Plan
- **Isolated Unit Test**: Added `packages/lib/schedules/transformers/for-atom.test.ts`:
  1. Set `process.env.TZ = 'America/New_York'`.
  2. Pass schedule with timezone `Europe/London` and date override for today with two separate ranges (09:00-12:00, 14:00-17:00 UTC).
  3. Verify today's override is NOT dropped.
  4. Verify output array contains exactly 1 entry with `ranges.length === 2`.
  5. Test across multiple simulated server timezones (`Asia/Tokyo`, `America/Los_Angeles`, `UTC`).
