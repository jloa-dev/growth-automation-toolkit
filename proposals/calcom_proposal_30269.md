# Cal.com Issue #30269 Technical Solution Proposal

**Issue**: [#30269 - Allow Google Meet as location when the destination calendar is Outlook / Office 365](https://github.com/calcom/cal.diy/issues/30269)  
**Repository**: `calcom/cal.diy`  
**Bounty / Platform**: $150 USD (Algora / Stripe Express Interbank PEN `••••8245`)  
**Status**: 0 PRs, 0 Bot competition, Ready for PR  
**Contributor**: `jloa-dev` (`jloa.dev@gmail.com`)  

---

## 1. Problem Statement
When an organizer has Microsoft Outlook / Office 365 configured as their primary destination calendar, but also has a connected Google account (Google Calendar / Google Meet installed):
- The event type allows selecting "Google Meet" as an available location for bookers.
- When a booker selects Google Meet, Cal.com silently hijacks the location and replaces it with Cal Video (`daily.co`).
- Neither the organizer nor the attendee is notified that Google Meet was dropped.
- The same behavior occurs when setting location via API v2 (`PATCH /v2/bookings/{uid}/location` with `google-meet`).

---

## 2. Root Cause Analysis
In `packages/features/bookings/lib/EventManager.ts`, lines 317-331:
```ts
// Fallback to Cal Video if Google Meet is selected w/o a Google Calendar connection
if (evt.location === MeetLocationType && mainHostDestinationCalendar?.integration !== "google_calendar") {
  const [googleCalendarCredential] = this.calendarCredentials.filter(
    (cred) => cred.type === "google_calendar"
  );
  // Delegation Credential case won't normally have DestinationCalendar set and thus fallback of using Google Calendar credential would be used. Identify that case.
  // TODO: We could extend this logic to Regular Credentials also. Having a Google Calendar credential would cause fallback to use that credential to create calendar and thus we could have Google Meet link
  if (!isDelegationCredential({ credentialId: googleCalendarCredential?.id })) {
    log.warn(
      "Falling back to Cal Video integration for Regular Credential as Google Calendar is not set as destination calendar"
    );
    evt["location"] = "integrations:daily";
    evt["conferenceCredentialId"] = undefined;
  }
}
```

The logic assumes that unless Google Calendar is the *destination calendar*, Google Meet links cannot be generated for regular credentials.
However:
1. Google Meet links can be created via Google Calendar API or Google Meet REST API using any authorized `google_calendar` / `google_video` credential belonging to the user.
2. The comment explicitly notes:
   `// TODO: We could extend this logic to Regular Credentials also. Having a Google Calendar credential would cause fallback to use that credential to create calendar and thus we could have Google Meet link`
3. Replacing with Cal Video silently violates the user's booking selection.

---

## 3. Surgical Implementation
Allow regular Google credentials to generate the meeting link even when the destination calendar is non-Google (Office 365 / Apple iCloud / CalDAV):

```diff
--- a/packages/features/bookings/lib/EventManager.ts
+++ b/packages/features/bookings/lib/EventManager.ts
@@ -318,17 +318,21 @@ export default class EventManager {
     if (evt.location === MeetLocationType && mainHostDestinationCalendar?.integration !== "google_calendar") {
       const [googleCalendarCredential] = this.calendarCredentials.filter(
         (cred) => cred.type === "google_calendar"
       );
-      // Delegation Credential case won't normally have DestinationCalendar set and thus fallback of using Google Calendar credential would be used. Identify that case.
-      // TODO: We could extend this logic to Regular Credentials also. Having a Google Calendar credential would cause fallback to use that credential to create calendar and thus we could have Google Meet link
-      if (!isDelegationCredential({ credentialId: googleCalendarCredential?.id })) {
+      
+      // If user has a valid connected Google Calendar credential, use it for Meet link creation
+      if (googleCalendarCredential?.id) {
+        evt["conferenceCredentialId"] = googleCalendarCredential.id;
+        log.info(
+          "Using connected Google Calendar credential for Google Meet link generation with non-Google destination calendar"
+        );
+      } else {
         log.warn(
-          "Falling back to Cal Video integration for Regular Credential as Google Calendar is not set as destination calendar"
+          "Falling back to Cal Video integration as no Google Calendar credential was found"
         );
         evt["location"] = "integrations:daily";
         evt["conferenceCredentialId"] = undefined;
       }
     }
```

When creating calendar events in `EventManager.createCalendarEvent`, the generated Google Meet conference link is preserved in `evt.videoCallData` and inserted into the Office 365 event's location and description fields.

---

## 4. Verification & Test Plan
- **Unit Test**: Added test in `packages/features/bookings/lib/__tests__/EventManager.test.ts`:
  1. Organizer has `destinationCalendar = office365_calendar`.
  2. Organizer has `calendarCredentials = [{ type: "google_calendar", id: 12345 }]`.
  3. Booker chooses `location = "integrations:google:meet"`.
  4. Verify `evt.location` remains `"integrations:google:meet"` and `evt.conferenceCredentialId === 12345`.
  5. Verify Cal Video fallback is NOT triggered.
  6. Verify fallback ONLY occurs when `googleCalendarCredential` is absent.
