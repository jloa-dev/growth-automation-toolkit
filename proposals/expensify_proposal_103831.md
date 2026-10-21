## Proposal

### Please re-state the problem that we are trying to solve in this issue.
When connecting a workspace to NetSuite using OAuth, entering an invalid or non-existent NetSuite Account ID causes the browser on Web to navigate to a broken page ("This site can’t be reached") and the native app on iOS/Android to display a generic OS WebView failure ("Error loading page"), without validating the account ID format or providing a way to correct the credentials.

### What is the root cause of that problem?
Under PR #96677 and PR #102240, REST + OAuth 2.0 became the default connection mechanism for NetSuite:
1. **Missing Account ID Format Validation**:
   In `src/pages/workspace/accounting/netsuite/NetSuiteTokenInput/subPages/NetSuiteTokenInputForm.tsx:41-54`, `validate` only checks whether `formValues[INPUT_IDS.NETSUITE_ACCOUNT_ID]` is empty (`translate('common.error.fieldRequired')`). Any arbitrary non-empty string passes validation.
2. **Premature Modal Dismissal on Web**:
   In `src/pages/workspace/accounting/netsuite/NetSuiteTokenInput/subPages/connectToNetSuiteOAuthSetup.ts:13-16`:
   ```typescript
   function connectToNetSuiteOAuthSetup(policyID: string, accountID: string, environmentURL: string) {
       openLink(getNetSuiteSetupLink(policyID, accountID), environmentURL);
       Navigation.dismissModal();
   }
   ```
   On Web, `openLink` immediately opens a new browser tab with the invalid NetSuite host URL and calls `Navigation.dismissModal()`, unmounting the credentials form. NetSuite fails to resolve the malformed account endpoint, resulting in the browser's "This site can't be reached" error.
3. **No Native WebView Error Boundary**:
   In `src/pages/workspace/accounting/AccountingSetupWebViewPage.tsx:103-114`, `<WebView>` is mounted without an `onError` or `renderError` handler. When native DNS or NetSuite HTTP requests fail on an invalid account ID, `react-native-webview` renders its internal unstyled OS error page ("Error loading page") and pressing Back exits to the main accounting page rather than returning to the credentials step.

### What changes do you think we should make in order to solve the problem?

1. **Client-Side Account ID Validation & Sanitization**:
   In `src/pages/workspace/accounting/netsuite/NetSuiteTokenInput/subPages/NetSuiteTokenInputForm.tsx`:
   - NetSuite Account IDs follow an established format: numbers followed by an optional sandbox suffix (e.g. `1234567`, `1234567_SB1`), or test drives (`TSTDRV1234567`). Hyphens used by administrators (e.g. `1234567-sb1`) should be normalized to underscores.
   - Define validation regex:
     ```typescript
     const NETSUITE_ACCOUNT_ID_REGEX = /^((TSTDRV)?[0-9]+(_[a-zA-Z0-9]+)?|[0-9]+-[a-zA-Z0-9]+)$/i;
     ```
   - In `validate`:
     ```typescript
     if (isOAuthFlow) {
         const accountID = formValues[INPUT_IDS.NETSUITE_ACCOUNT_ID]?.trim();
         if (!accountID) {
             addErrorMessage(errors, INPUT_IDS.NETSUITE_ACCOUNT_ID, translate('common.error.fieldRequired'));
         } else if (!NETSUITE_ACCOUNT_ID_REGEX.test(accountID)) {
             addErrorMessage(errors, INPUT_IDS.NETSUITE_ACCOUNT_ID, translate('workspace.accounting.netsuite.errors.invalidAccountId'));
         }
         return errors;
     }
     ```
   - In `connectPolicy`, sanitize input: `accountID.replace('-', '_').toUpperCase()`.
   - Add translation key `workspace.accounting.netsuite.errors.invalidAccountId` across all translation files.

2. **Native WebView Error Boundary (`renderError`)**:
   In `src/pages/workspace/accounting/AccountingSetupWebViewPage.tsx`:
   - Implement `renderError` on `<WebView>`:
     ```tsx
     <WebView
         source={{uri: webViewUri, headers: {Cookie: `authToken=${authToken}`}}}
         userAgent={getUAForWebView()}
         incognito
         startInLoadingState
         renderLoading={renderLoading}
         renderError={() => (
             <FullPageOfflineBlockingView>
                 <EmptyStateContent
                     title={translate('workspace.accounting.netsuite.errors.failedToConnectTitle')}
                     subtitle={translate('workspace.accounting.netsuite.errors.failedToConnectSubtitle')}
                     buttonText={translate('workspace.accounting.netsuite.reEnterCredentials')}
                     onButtonPress={() => Navigation.goBack()}
                 />
             </FullPageOfflineBlockingView>
         )}
     />
     ```

### What alternative solutions did you explore? (Optional)
Attempting an asynchronous backend handshake before launching OAuth was explored. However, NetSuite OAuth initiates on NetSuite's domain, so client-side format validation combined with native `renderError` recovery provides immediate UX protection without creating new backend roundtrips.

### Test Plan
#### Manual QA Steps:
1. Log in to an account with an existing workspace policy and Accounting enabled.
2. Navigate to Workspace Settings > Accounting > NetSuite and tap Connect.
3. Proceed to the "Enter your NetSuite credentials" step.
4. Enter an invalid/malformed Account ID (e.g. `abc!@#` or `123`).
5. Tap Connect.
6. **Verify:** An inline validation error appears immediately (`Please enter a valid NetSuite Account ID`), no popup opens, and the form remains visible.
7. Enter a valid formatted sandbox ID with a hyphen (e.g. `1234567-sb1`).
8. Tap Connect.
9. **Verify:** The ID normalizes to `1234567_SB1` and opens the authorization flow.
10. On iOS/Android: if network fails or NetSuite endpoint drops, verify that the in-app error view is rendered with a button to return to the credentials step, rather than a raw OS WebView error page.
