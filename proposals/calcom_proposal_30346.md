# Cal.com Issue #30346 Technical Solution Proposal

**Issue**: [#30346 - ICS feed: weekly recurring events without BYDAY create phantom busy blocks on the booker's own weekday](https://github.com/calcom/cal.diy/issues/30346)  
**Repository**: `calcom/cal.diy`  
**Bounty / Platform**: $200 USD (Algora / Stripe Express Interbank PEN `••••8245`)  
**Status**: 0 PRs, 0 Bot competition, Ready for PR  
**Contributor**: `jloa-dev` (`jloa.dev@gmail.com`)  

---

## 1. Problem Statement
In external ICS calendar feeds (such as Proton Calendar, Nextcloud, Apple iCloud, Fastmail, or generic CalDAV exports), weekly recurring events without an explicit `BYDAY` parameter (e.g. `RRULE:FREQ=WEEKLY;INTERVAL=1`) derive their recurring weekday exclusively from the event's original start date (`DTSTART`).

However, in Cal.com's ICS feed calendar integration (`packages/app-store/ics-feedcalendar/lib/CalendarService.ts`), the recurrence iterator is seeded with the queried availability window's start date (`dateFrom`), rather than the event's canonical `DTSTART`.

This leads to two critical bugs:
1. **Weekday Shift (Phantom Busy Slots)**: The recurrence series shifts to the weekday of the booker's queried window (e.g., if a user views availability on a Wednesday, an event occurring every Monday is evaluated on Wednesday instead, blocking free slots).
2. **COUNT Expiration Leak**: For rules with `COUNT=N`, recurrence count is evaluated starting from the window seed instead of the original series beginning, resurrecting past events whose count has already expired.

---

## 2. Root Cause Analysis
In `packages/app-store/ics-feedcalendar/lib/CalendarService.ts`, lines 225-229:
```ts
const start = dayjs(dateFrom);
const end = dayjs(dateTo);
const startDate = ICAL.Time.fromDateTimeString(startISOString);
startDate.hour = event.startDate.hour;
startDate.minute = event.startDate.minute;
startDate.second = event.startDate.second;
const iterator = event.iterator(startDate);
```
Per the `ical.js` specification:
- `event.iterator(time)` treats the supplied `time` argument as the rule's initial anchor.
- For `RRULE:FREQ=WEEKLY` without `BYDAY`, `ical.js` reads the day of the week directly from the seed anchor.
- When `startDate` is instantiated with `startISOString` (representing `dateFrom`), the day of the week is replaced by `dateFrom.getDay()`, detaching the event from its real recurring day.
- Furthermore, `event.iterator()` without arguments already starts at `event.startDate` (`DTSTART`).

---

## 3. Surgical Implementation
Modify `packages/app-store/ics-feedcalendar/lib/CalendarService.ts` to instantiate the iterator from the event's true `event.startDate` and fast-forward past occurrences preceding the query window:

```diff
--- a/packages/app-store/ics-feedcalendar/lib/CalendarService.ts
+++ b/packages/app-store/ics-feedcalendar/lib/CalendarService.ts
@@ -222,11 +222,8 @@ export default class CalendarService implements Calendar {
 
           const start = dayjs(dateFrom);
           const end = dayjs(dateTo);
-          const startDate = ICAL.Time.fromDateTimeString(startISOString);
-          startDate.hour = event.startDate.hour;
-          startDate.minute = event.startDate.minute;
-          startDate.second = event.startDate.second;
-          const iterator = event.iterator(startDate);
+          // Initialize iterator from true event.startDate so DTSTART weekday and COUNT are preserved
+          const iterator = event.iterator();
           let current: ICAL.Time;
           let currentEvent;
           let currentStart = null;
@@ -253,6 +250,13 @@ export default class CalendarService implements Calendar {
             // do not mix up caldav and icalendar! For the recurring events here, the timezone
             // provided is relevant, not as pointed out in https://datatracker.ietf.org/doc/html/rfc4791#section-9.6.5
             // where recurring events are always in utc (in caldav!). Thus, apply the time zone here.
+            const occurrenceStart = dayjs(current.toJSDate());
+            const occurrenceEnd = dayjs(currentEvent.endDate.toJSDate());
+
+            // Skip occurrences strictly before the requested window
+            if (occurrenceEnd.isBefore(start)) {
+              continue;
+            }
```

---

## 4. Verification & Test Plan
- **Unit Test Coverage**: Created `packages/app-store/ics-feedcalendar/test/recurring-byday.test.ts`:
  1. Test weekly recurring event on Monday without `BYDAY` (`DTSTART:20261005T100000Z; RRULE:FREQ=WEEKLY`).
  2. Query availability window starting on a Wednesday (`2026-10-14`).
  3. Verify Wednesday has NO busy slots generated.
  4. Verify the busy slot correctly falls only on Monday (`2026-10-19`).
  5. Test `COUNT=5` expiring before query window; verify 0 occurrences generated.
