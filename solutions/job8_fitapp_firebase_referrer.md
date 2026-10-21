# Solution for Issue #30 (nick-transition/fitapp):
# Security: Add HTTP referrer restrictions to Firebase API keys
# Bounty: $100 - $200 USD (Size S)

## Implementation Guide & Cloud Setup

To prevent unauthorized quota consumption and quota depletion from external domains, the Google Cloud Console API Key restrictions must be updated:

1. Navigate to Google Cloud Console > APIs & Services > Credentials.
2. Select the Firebase Web API Key (`AIza...`).
3. Under **Application restrictions**, select **Web sites**.
4. Add the allowed HTTP referrers:
   - `https://fitapp.web.app/*`
   - `https://fitapp.firebaseapp.com/*`
   - `http://localhost:*/*` (local development only)
   - `http://127.0.0.1:*/*` (emulator runner)
5. Under **API restrictions**, restrict key usage strictly to:
   - Identity Toolkit API
   - Cloud Firestore API
   - Firebase App Check API

### Documentation Patch for README / Deployment Guide:
Update `docs/security/api_keys.md` to document key restrictions policy.
