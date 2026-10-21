# Cal.com Issue #30269 Technical Solution Proposal

**Issue**: [#30269 - Allow Google Meet as location when the destination calendar is Outlook / Office 365](https://github.com/calcom/cal.diy/issues/30269)  
**Repository**: `calcom/cal.diy`  
**Bounty / Platform**: $150 USD (Algora / Stripe Express Interbank PEN `••••8245`)  
**Status**: 0 Bot competition, Ready for PR  
**Contributor**: `jloa-dev` (`jloa.dev@gmail.com`)  

---

## 1. Problem Statement
When an organizer configures Microsoft Outlook / Office 365 as their destination calendar, but also has a connected Google account (Google Calendar / Google Meet):
- The event type allows offering "Google Meet" as an available meeting location.
- When a booker selects Google Meet, Cal.com silently falls back to Cal Video (`daily.co`).
- Neither the organizer nor the attendee is warned that Google Meet was replaced.
- The same behavior occurs when updating location via API v2 (`PATCH /v2/bookings/{uid}/location` with `google-meet`).

---

## 2. Root Cause Analysis
In `packages/features/bookings/lib/EventManager.ts`:
```ts
// Fallback to Cal Video if Google Meet is selected w/o a Google Calendar connection
if (evt.location === MeetLocationType && mainHostDestinationCalendar?.integration !== "google_calendar") {
  const [googleCalendarCredential] = this.calendarCredentials.filter(
    (cred) => cred.type === "google_calendar"
  );
  if (!isDelegationCredential({ credentialId: googleCalendarCredential?.id })) {
    log.warn(
      "Falling back to Cal Video integration for Regular Credential as Google Calendar is not set as destination calendar"
    );
    evt["location"] = "integrations:daily";
    evt["conferenceCredentialId"] = undefined;
  }
}
```
The architecture currently couples Google Meet video conferencing directly to the destination calendar. Because Google Meet conference links in Cal.com are generated through Google Calendar's API, selecting an Outlook destination calendar caused Cal.com to drop Google Meet and fall back to Cal Video.

---

## 3. Surgical Implementation
Implement proper conferencing decoupling in `EventManager.ts` and ensure Google Meet URLs are recognized across locations:

1. **Conference Generation in `EventManager.ts`**:
   When `evt.location === MeetLocationType` and the destination calendar is non-Google, invoke `createEvent` on the organizer's connected `googleCalendarCredential` to generate the Google Meet conference link, attach `createdEvent` to `evt.videoCallData`, update `evt.location = meetingUrl`, and push the result. When `createAllCalendarEvents` subsequently executes for Outlook / Office 365, the Outlook booking includes the actual Google Meet link.

2. **URL Matching in `packages/app-store/locations.ts` & `_metadata.ts`**:
   Add `urlRegExp: "^https?:\\/\\/(?:www\\.)?meet\\.google\\.com\\/[a-zA-Z0-9-_]+"` to `packages/app-store/googlevideo/_metadata.ts` and permit matching in `getStaticLinkLocationByValue`.

```diff
--- a/packages/app-store/googlevideo/_metadata.ts
+++ b/packages/app-store/googlevideo/_metadata.ts
@@ -23,6 +23,7 @@ export const metadata = {
       linkType: "dynamic",
       type: "integrations:google:meet",
       label: "Google Meet",
+      urlRegExp: "^https?:\/\/(?:www\.)?meet\.google\.com\/[a-zA-Z0-9-_]+",
     },
   },
   dirName: "googlevideo",
--- a/packages/app-store/locations.ts
+++ b/packages/app-store/locations.ts
@@ -288,8 +288,8 @@ const getStaticLinkLocationByValue = (value: string | undefined | null) => {
     return null;
   }
   return locations.find((l) => {
-    if (l.default || l.linkType == "dynamic" || !l.urlRegExp) {
-      return;
+    if (l.default || !l.urlRegExp) {
+      return false;
     }
     return new RegExp(l.urlRegExp).test(value);
   });
--- a/packages/features/bookings/lib/EventManager.ts
+++ b/packages/features/bookings/lib/EventManager.ts
@@ -319,11 +319,26 @@ export default class EventManager {
       const [googleCalendarCredential] = this.calendarCredentials.filter(
         (cred) => cred.type === "google_calendar"
       );
-      // Delegation Credential case won't normally have DestinationCalendar set and thus fallback of using Google Calendar credential would be used. Identify that case.
-      // TODO: We could extend this logic to Regular Credentials also. Having a Google Calendar credential would cause fallback to use that credential to create calendar and thus we could have Google Meet link
-      if (!isDelegationCredential({ credentialId: googleCalendarCredential?.id })) {
+      if (googleCalendarCredential) {
+        log.info(
+          "Creating Google Meet conference using connected Google Calendar credential for non-Google destination calendar"
+        );
+        const clonedCalEvent = cloneDeep(event);
+        const gcalResult = await createEvent(googleCalendarCredential, clonedCalEvent);
+        if (gcalResult?.createdEvent) {
+          const meetingUrl =
+            typeof gcalResult.createdEvent === "string"
+              ? JSON.parse(gcalResult.createdEvent)?.onlineMeetingUrl || JSON.parse(gcalResult.createdEvent)?.url
+              : gcalResult.createdEvent?.url;
+          if (meetingUrl) {
+            evt.videoCallData = gcalResult.createdEvent;
+            evt.location = meetingUrl;
+            results.push(gcalResult);
+          }
+        }
+      } else {
         log.warn(
-          "Falling back to Cal Video integration for Regular Credential as Google Calendar is not set as destination calendar"
+          "Falling back to Cal Video integration as no Google Calendar credential was found for Google Meet"
         );
         evt["location"] = "integrations:daily";
         evt["conferenceCredentialId"] = undefined;
```

---

## 4. Verification & Test Plan
1. **Conference Link Creation**: When `destinationCalendar` is `office365_calendar` and host has `google_calendar` credential, Google Meet conference link is generated and attached to `evt.videoCallData`.
2. **Fallback Safety**: When host has no Google credential connected, gracefully falls back to Cal Video (`integrations:daily`).
3. **URL Recognition**: `https://meet.google.com/abc-defg-hij` is recognized as `Google Meet` instead of a generic bare URL.
