Contributor details
Your Expensify account email: jloa.dev@gmail.com
Upwork Profile Link: https://www.upwork.com/freelancers/~0163955a2ba22190aa

## Proposal

### Please re-state the problem that we are trying to solve in this issue.
Android - On a fresh install, opening a public room deep link as an unauthenticated/anonymous user fails with "Auth OpenReport returned an error" and redirects to Concierge instead of opening the public room.

### What is the root cause of that problem?
On Android cold launch from an external intent/deep link, React Native triggers both `Linking.getInitialURL()` (lines 100–127 in `src/DeepLinkHandler.tsx`) and fires the native `'url'` listener (`Linking.addEventListener('url', ...)` at lines 167–196) with the exact same initial URL.

While `initialUrlProcessed.current` guards against re-running `getInitialURL()` on unauthenticated re-renders, the `Linking.addEventListener('url')` handler lacks a de-duplication check against the already-processed initial URL. Consequently, during cold start on Android, `openReportFromDeepLink` is invoked twice in rapid succession in an unauthenticated state:
1. The first call begins unauthenticated `openReport` and anonymous session creation.
2. The concurrent duplicate call races with the pending session, sending a conflicting unauthenticated `OpenReport` or triggering duplicate anonymous account creation.
3. When the conflicting request fails, `report.errorFields.notFound` is set in Onyx, activating the fallback in `src/libs/actions/Link.ts` (lines 606–616) which calls `navigateToConciergeChat()`.

### What changes do you think we should make in order to solve the problem?
1. In `src/DeepLinkHandler.tsx`, maintain a ref to track the last processed URL (`lastProcessedUrl = useRef<string | null>(null)`).
2. Set `lastProcessedUrl.current = url` when `Linking.getInitialURL()` successfully processes the initial URL.
3. In `Linking.addEventListener('url', (state) => { ... })`, check if `state.url === lastProcessedUrl.current`. If the URL matches the one already processed on cold start, ignore the duplicate event. Clear or update `lastProcessedUrl.current` only when a genuinely distinct deep link arrives or when navigating away.
4. Additionally in `src/libs/actions/Link.ts`, ensure `openReportFromDeepLink` de-duplicates concurrent in-flight requests for the same `reportID` when unauthenticated to prevent racing requests from clobbering Onyx state during cold boot.

### What alternative solutions did you explore? (Optional)
Handling de-duplication solely at the network request queue layer (`resolveOpenReportDuplicationConflictAction`). However, intercepting and preventing the duplicate deep-link event at `DeepLinkHandler.tsx` prevents redundant authentication, Onyx connections, and navigation side-effects entirely.
