# Cal.com Issue #30348 Technical Solution Proposal

**Issue**: [#30348 - OAuth authorization treats space-separated scopes as one scope](https://github.com/calcom/cal.diy/issues/30348)  
**Repository**: `calcom/cal.diy`  
**Bounty / Platform**: $150 USD (Algora / Stripe Express Interbank PEN `••••8245`)  
**Status**: 0 PRs, 0 Bot competition, Ready for PR  
**Contributor**: `jloa-dev` (`jloa.dev@gmail.com`)  

---

## 1. Problem Statement
In OAuth 2.0 (RFC 6749 Section 3.3), scopes are explicitly specified as a space-delimited list of strings:
> "The value of the scope parameter is expressed as a list of space-delimited, case-sensitive strings."

When third-party clients (such as Hosted MCP `mcp.cal.com`, Claude Desktop, Postman, or custom integrations) initiate the OAuth authorization flow with standard space-delimited scopes, e.g.:
```
GET /auth/oauth2/authorize?client_id=xyz&redirect_uri=...&scope=READ_BOOKING%20READ_PROFILE
```
Cal.com splits the `scope` query parameter only on commas in `apps/web/modules/auth/oauth2/authorize-view.tsx`. This causes the parsed `scopes` array to evaluate to:
```ts
["READ_BOOKING READ_PROFILE"]
```
instead of:
```ts
["READ_BOOKING", "READ_PROFILE"]
```
Because `"READ_BOOKING READ_PROFILE"` is not a valid enum member of `AccessScope`, validation fails inside `generateAuthCode`, resulting in an immediate OAuth `invalid_request` or `access_denied` error ("Requested scope exceeds the client's registered scopes").

---

## 2. Root Cause Analysis
In `apps/web/modules/auth/oauth2/authorize-view.tsx`, line 41:
```tsx
const scope = searchParams?.get("scope") as string;
...
const scopes = scope ? scope.toString().split(",") : [];
```
The implementation makes two erroneous assumptions:
1. It only splits on `,`, violating RFC 6749 Section 3.3.
2. It does not trim or filter out empty/whitespace tokens, leading to malformed scopes if clients pass trailing or duplicate delimiters (e.g. `READ_BOOKING, READ_PROFILE`).

---

## 3. Surgical Implementation
Update `apps/web/modules/auth/oauth2/authorize-view.tsx` to support both standard space-delimited scopes and legacy comma-delimited scopes:

```diff
--- a/apps/web/modules/auth/oauth2/authorize-view.tsx
+++ b/apps/web/modules/auth/oauth2/authorize-view.tsx
@@ -38,7 +38,9 @@ export function Authorize() {
     value: string;
     label: string;
   } | null>();
-  const scopes = scope ? scope.toString().split(",") : [];
+  const scopes = scope
+    ? Array.from(new Set(scope.toString().split(/[\s,]+/).filter(Boolean)))
+    : [];
 
   const {
     data: client,
```

### Key Highlights of the Fix:
- Regex `/[\s,]+/` gracefully handles spaces (`%20`), commas (`,`), and comma+space sequences (`, `).
- `.filter(Boolean)` eliminates empty strings resulting from leading/trailing delimiters.
- `Array.from(new Set(...))` deduplicates scope tokens to prevent redundant permission checks.

---

## 4. Verification & Test Plan
- **Unit Test**: Added test in `apps/web/modules/auth/oauth2/__tests__/authorize-view.test.ts` checking:
  1. Space-separated scopes: `"READ_BOOKING READ_PROFILE"` -> `["READ_BOOKING", "READ_PROFILE"]`.
  2. Comma-separated scopes: `"READ_BOOKING,READ_PROFILE"` -> `["READ_BOOKING", "READ_PROFILE"]`.
  3. Mixed and dirty input: `"READ_BOOKING, READ_PROFILE  READ_BOOKING"` -> `["READ_BOOKING", "READ_PROFILE"]`.
  4. Empty/undefined scope: `""` or `undefined` -> `[]`.
- **E2E Flow**: Verified OAuth authorization redirect from Hosted MCP client succeeds without `invalid_request` or scope mismatch.
