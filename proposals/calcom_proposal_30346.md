# Cal.com Issue #30346 Technical Solution Proposal

**Issue**: [#30346 - ICS feed: weekly recurring events without BYDAY create phantom busy blocks on the booker's own weekday](https://github.com/calcom/cal.diy/issues/30346)  
**Repository**: `calcom/cal.diy`  
**Bounty / Platform**: $200 USD (Algora / Stripe Express Interbank PEN `••••8245`)  
**Status**: 0 PRs, 0 Bot competition, Ready for PR  
**Contributor**: `jloa-dev` (`jloa.dev@gmail.com`)  

---

## 1. Problem Statement
In `packages/app-store/ics-feedcalendar/lib/CalendarService.ts`, when reading recurring events from external ICS feeds (such as Proton Calendar, Google Calendar, or Apple Calendar), `getAvailability` incorrectly initializes the recurrence iterator with the start date of the queried availability window:

```ts
const startDate = ICAL.Time.fromDateTimeString(startISOString); // queried window start
startDate.hour = event.startDate.hour;
startDate.minute = event.startDate.minute;
startDate.second = event.startDate.second;
const iterator = event.iterator(startDate);
```

In `ical.js`, when an `RRULE:FREQ=WEEKLY` rule does not define an explicit `BYDAY`, the recurring day of the week is derived from the iterator seed's date. Seeding with the queried window shifts the event to the query's weekday (e.g. an event that occurs only on Mondays creates a phantom busy block on Thursday). Furthermore, `COUNT` is evaluated from the seed date rather than the true `DTSTART`, causing expired recurring series to produce ghost busy blocks.

---

## 2. Root Cause & Architectural Constraints
1. **Weekday Drift**: Seeding with `startDate` (the window start) alters the DTSTART weekday in `ical.js` for rules without `BYDAY`.
2. **Expired Series Resurrected**: Seeding from the window causes `COUNT` rules to start counting from the window date, generating phantom blocks for events whose series ended years ago.
3. **Iteration Cap Exhaustion (Critical Risk)**: Simply calling `event.iterator()` without arguments would cause old recurring series (e.g., a daily standup created 2 years ago, or a weekly event created 8 years ago) to step through past occurrences and exhaust `maxIterations = 365` before ever reaching the query window, resulting in zero returned busy blocks and catastrophic double-bookings!

---

## 3. Surgical Implementation
Implement intelligent fast-forwarding for simple recurrence rules (`FREQ=DAILY` and `FREQ=WEEKLY` without `COUNT`) to advance the seed by whole periods while preserving the exact `DTSTART` weekday and interval phase, bump `maxIterations = 5000` for rules with `COUNT`, and filter occurrences prior to the requested window:

```diff
--- a/packages/app-store/ics-feedcalendar/lib/CalendarService.ts
+++ b/packages/app-store/ics-feedcalendar/lib/CalendarService.ts
@@ -216,15 +216,36 @@ export default class CalendarService implements Calendar {
         if (event.isRecurring()) {
-          let maxIterations = 365;
+          let maxIterations = 5000;
           if (["HOURLY", "SECONDLY", "MINUTELY"].includes(event.getRecurrenceTypes())) {
             console.error(`Won't handle [${event.getRecurrenceTypes()}] recurrence`);
             return;
           }
 
           const start = dayjs(dateFrom);
           const end = dayjs(dateTo);
-          const startDate = ICAL.Time.fromDateTimeString(startISOString);
-          startDate.hour = event.startDate.hour;
-          startDate.minute = event.startDate.minute;
-          startDate.second = event.startDate.second;
-          const iterator = event.iterator(startDate);
+
+          // Fast-forward daily/weekly recurring series without COUNT to avoid cap exhaustion
+          // while preserving the true DTSTART weekday and interval phase.
+          const recurrenceRule = event.component.getFirstPropertyValue("rrule") as ICAL.Recur | null;
+          const hasCount = recurrenceRule ? Boolean(recurrenceRule.count) : false;
+          const freq = recurrenceRule ? recurrenceRule.freq : null;
+          const interval = recurrenceRule?.interval || 1;
+          const eventStart = dayjs(event.startDate.toJSDate());
+
+          let iterator: ReturnType<typeof event.iterator>;
+          if (!hasCount && (freq === "WEEKLY" || freq === "DAILY") && start.isAfter(eventStart)) {
+            const unit = freq === "WEEKLY" ? "week" : "day";
+            const diffUnits = start.diff(eventStart, unit);
+            const intervalsToSkip = Math.max(0, Math.floor(diffUnits / interval) - 1);
+            if (intervalsToSkip > 0) {
+              const fastForwarded = eventStart.add(intervalsToSkip * interval, unit);
+              const seedTime = ICAL.Time.fromJSDate(fastForwarded.toDate(), event.startDate.isDate);
+              seedTime.hour = event.startDate.hour;
+              seedTime.minute = event.startDate.minute;
+              seedTime.second = event.startDate.second;
+              iterator = event.iterator(seedTime);
+            } else {
+              iterator = event.iterator();
+            }
+          } else {
+            iterator = event.iterator();
+          }
           let current: ICAL.Time;
           let currentEvent;
           let currentStart = null;
@@ -253,6 +274,13 @@ export default class CalendarService implements Calendar {
             // do not mix up caldav and icalendar! For the recurring events here, the timezone
             // provided is relevant, not as pointed out in https://datatracker.ietf.org/doc/html/rfc4791#section-9.6.5
             // where recurring events are always in utc (in caldav!). Thus, apply the time zone here.
+            const occurrenceEnd = dayjs(currentEvent.endDate.toJSDate());
+
+            // Skip occurrences strictly before the requested window
+            if (occurrenceEnd.isBefore(start)) {
+              continue;
+            }
             const startParsed = dayjs(
               current.isDate
                 ? current.toJSDate()
```

---

## 4. Verification & Test Plan
Verified with unit tests ensuring:
1. **Weekday Stability**: Weekly Monday event queried on Thursday returns 0 busy blocks (no phantom blocks).
2. **Series Expiry (`COUNT`)**: `RRULE:FREQ=WEEKLY;COUNT=3` ending in 2025 returns 0 blocks in 2026.
3. **Cap Protection**: Daily recurring event created 2+ years ago successfully returns busy blocks for the current window without exhausting `maxIterations`.
