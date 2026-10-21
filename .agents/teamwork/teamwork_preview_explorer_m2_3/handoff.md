# Technical Adversarial Audit Report: Batch 3 (Tier 3 2-Rival Issues)

**Auditor:** M2 Explorer 3 (Adversarial Analyst - Batch 3: Tier 3 2-Rival Issues)  
**Target Space:** `Expensify/App`  
**Identity Context:** `jloa-dev <jloa.dev@gmail.com>`  
**Date:** 2026-10-21  

---

## 1. Observation

Direct inspection of GitHub issues via GitHub CLI (`gh issue view <issue> --repo Expensify/App --json ...`) and local repository codebase at `c:\Users\Loa\Downloads\GOAL\expensify_app\src\...` revealed the following verified factual states across the 17 assigned issues:

### 1.1 Issue #103183 — Tags: Transaction tag truncated when selecting tag with `\:`
- **Rivals:** `@camesenin`, `@bonnhatnguyen`
- **Observed Proposal Code:** Both rivals proposed escaping backslashes first in `src/libs/PolicyUtils/tag.ts`:
  `tagName.replaceAll('\\', '\\\\').replaceAll(':', '\\:')`
- **Maintainer Intervention:** On 2026-10-17, C+ `@bernhardoj` shared internal Slack confirmation:
  > *"Classic does escape it... Plain:Colon saves as Plain\\:Colon, and Parent\\: Child is left as is (the backend skips colons that are already escaped)... The NewDot bug is that escapeTagName escapes colons that are already escaped, which turns Parent\\: Child into Parent\\."*
- **Bot Interception:** On 2026-10-18, `@bernhardoj` issued `@MelvinBot implement this`. MelvinBot opened Draft PR [#104305](https://github.com/Expensify/App/pull/104305) using negative lookbehind `(?<!\\):`.

### 1.2 Issue #102683 — Spend: Card filter company card nickname search
- **Rivals:** `@bonnhatnguyen`, `@camesenin`
- **Observed Code Base:** In `src/libs/CardFeedUtils.ts` (lines 83–90):
  ```typescript
  let cardName = card?.nameValuePairs?.cardTitle;
  const text = personalDetails?.displayName ?? cardName;
  const plaidUrl = getPlaidInstitutionIconUrl(card?.bank);
  const isCSVImportCard = card?.bank === CONST.PERSONAL_CARDS.BANK_NAME.CSV;
  const isPersonal = isPersonalCard(card);
  if (isPersonal && !isCSVImportCard) {
      cardName = customCardNames?.[card?.cardID] ?? card?.cardName;
  }
  ```
- **Rival Flaw:** Both rivals proposed appending `else if (!isExpensifyCard(card)) { cardName = getCompanyCardCustomName(...); }` but left `const text = personalDetails?.displayName ?? cardName;` declared *before* `cardName` is updated. For unassigned cards or members missing from `personalDetailsList`, `text` falls back to the old `cardTitle` or `undefined`, failing to display the nickname in the primary row text.
- **jloa-dev Pre-coded State:** Branch `fix/102683-company-card-nicknames-spend-filter` relocates `const text = personalDetails?.displayName ?? cardName;` after custom name resolution, introduces `allSharedCompanyCardCustomNamesSelector`, and adds unit tests in `tests/unit/Search/buildCardFilterDataTest.ts`.

### 1.3 Issue #102730 — Ecard: Empty illustration not shown after removing user admin permission
- **Rivals:** `@yusufdeveloper2903`
- **C+ Review Verdict:** On 2026-10-19, C+ `@jayeshmangwani` observed:
  > *"filtering on the frontend only hides the leftover data. It also misses the case where User B is removed from the workspace entirely, because that workspace’s policy no longer exists in Onyx. I think this needs a backend fix: when an admin is demoted or removed, either unlink the feeds they linked to their own workspaces, or at least send an Onyx update that clears private_expensifyCardSettings_<fundID> for that user."*
- **jloa-dev Pre-coded State:** Branch `fix/102730-ecard-feed-selector-admin-check` (`7b78695c39d`) addresses `isPolicyAdmin(policy, currentUserLogin)` to prevent cached admin role display when demoted in `employeeList`.

### 1.4 Issue #103240 — DEV: Duplicate key error on search filter bar
- **Rivals:** `@camesenin`, `@amar-sheikh`
- **Rival Flaw:** Both competitors proposed hardcoding `keyForList: CONST.SEARCH.SYNTAX_FILTER_KEYS.REPORT_FIELD` for all report field chips. When a workspace filters by multiple report fields simultaneously, all report field chips share the exact same key, reproducing the duplicate React key warning.
- **Bot Interception:** On 2026-10-14, C+ `@eVoloshchak` issued `@MelvinBot implement this`. MelvinBot opened Draft PR [#104034](https://github.com/Expensify/App/pull/104034).

### 1.5 Issue #103533 — Concierge: Image appears cut on preview in Concierge RHP
- **Rivals:** `@taieddie`
- **Bot Interception:** On 2026-10-16, C+ `@abzokhattab` stamped 🎀 👀 🎀 C+ reviewed and issued `@MelvinBot implement this`. MelvinBot created Draft PR [#104288](https://github.com/Expensify/App/pull/104288).

### 1.6 Issue #103778 — Sentry APP-M66: ReactModalHostView dialog null check
- **Rivals:** `@haiquywork`, `@tnclaudecode`
- **Rival Flaw:** `@haiquywork` proposed a bare `if (d != null && d.isShowing)` in the posted lambda without cancelling callbacks on modal dismiss. As `@tnclaudecode` detailed, when a dialog is recreated or when Android HybridApp tears down the activity, uncancelled callbacks posted to `window.decorView` execute against null or invalid dialog instances.
- **Current Status:** C+ `@cretadn22` requested expert contributor help for native Android lifecycle. Issue remains open for proposal approval.

### 1.7 Issue #103779 — TriNet: Missing Final Approver on Custom Approval
- **Rivals:** `@haiquywork`, `@David-2002065`
- **Rival Flaw:** `@haiquywork` completely misdiagnosed the subsystem, proposing changes to `WorkflowUtils.ts` and `ApprovalWorkflowSection.tsx` (the report approval chain) instead of `src/pages/workspace/hr/utils.ts` (the HR provider integration card).
- **Design Context:** Commit `6a5a59e` (PR #102750) intentionally hid the row. MelvinBot argued this is expected behavior (NAB). jloa-dev proposed deduplicating the configuration builder while respecting custom workflows.

### 1.8 Issue #103802 — Expense: Edit split when confirming delete per diem expense
- **Rivals:** `@khizzcr7`, `@camesenin`
- **Rival Flaw:** `@khizzcr7` proposed bypassing the Edit Split RHP on *all* split delete flows, destroying the intentional per diem reallocation logic introduced in PR #85293.
- **Timing & Pre-code:** `@camesenin` posted 8 hours *after* `jloa-dev` (2026-10-13 12:08 UTC vs 04:10 UTC). `jloa-dev` holds FCFS priority for the correct surgical fix guarding `shouldRedirectDeleteToSplitExpenseEdit`.

### 1.9 Issue #103824 — Native share: Large video file crash (>125 MB)
- **Status:** **CLOSED / INTERNAL FIX MERGED.** Staff Engineer `@luacmartins` fixed the issue directly in internal repo `Expensify/Mobile-Expensify` (PR #14181). C+ `@huult` confirmed on 2026-10-21: *"The PR fixing this issue was released to production 5 days ago. I think we can close this issue after 2 more days."*

### 1.10 Issue #103876 — Amex: Feed error persists after reconnect until manual scrape
- **Rivals:** `@janiya2`
- **Rival Flaw:** `@janiya2` proposed triggering `updateWorkspaceCompanyCard` sequentially for *all* assigned cards on the feed before closing the RHP. For large corporate card programs with hundreds of cards, this triggers an avalanche of concurrent HTTP requests, causing 429 Rate Limit errors and app freezing. Additionally, `@janiya2` omitted calling `clearCompanyCardFeedErrors`, so feed-level error banners remain stuck in Onyx.
- **jloa-dev Solution:** Selectively syncs only cards with active connection issues (`hasCardConnectionIssue(card)`) and optimistically clears feed errors.

### 1.11 Issue #103961 — Web: Browser back navigates to previous action instead of report
- **Rivals:** `@janiya2`, `@camesenin`, `@khizzcr7`
- **Rival Flaw:** `@camesenin` falsely claimed patch `7.4.1` was an unreleased patch name (verified that `patches/react-navigation/@react-navigation+native+7.4.1+001+initial.patch` is the active patch in `main`). All proposals were posted before the `Help Wanted` label was applied, prompting contributor warnings from `@emkhalid`.

### 1.12 Issue #104138 — Receipts: Receipts not showing fully when sent to receipts@expensify.com
- **Rivals:** `@bconnnnn`, `@Metarenessans`
- **Rival Flaw:** `@bconnnnn` admitted to using unverified AI assistance without reproducing or testing. `@Metarenessans` used invalid typing `ImageProps['resizeMode']` from React Native instead of `ReceiptImageProps['resizeMode']`.
- **jloa-dev Pre-coded State:** Branch `fix/104138-receipt-preview-resize-mode` cleanly forwards `resizeMode={!fillSpace ? 'contain' : undefined}`, verified on tall forwarded receipts without layout shifts.

### 1.13 Issue #104159 — Chat: Short mention with single char followed by dot not recognized
- **Rivals:** `@janiya2`, `@bonnhatnguyen`
- **Rival Flaw:** Both rivals submitted identical copy-pasted proposals suggesting the removal of `isDomainPublic(currentUserDomain)` from `src/hooks/useShortMentionsList.ts`. Doing so causes all public domains (`@gmail.com`, `@yahoo.com`) to resolve short mentions, causing massive cross-tenant user collisions and privacy violations.
- **Classification:** Invalid test prerequisites (NAB) identical to closed Issue #96348.

### 1.14 Issue #104161 — Spend: It's not here page when opening split expense from chat filter
- **Rivals:** `@camesenin`, `@emkhalid`
- **Rival Flaw:** `@camesenin` passed `ROUTES.SEARCH_REPORT.getRoute({reportID})` without `backTo`. When navigating back from the split bill details, the user's Search filters and active query are completely obliterated.
- **jloa-dev Pre-coded State:** Branch `fix/104161-split-bill-details-search-base-route` uses `getReportRouteForCurrentContext({reportID})`, preserving `backTo` query parameters across back navigation.

### 1.15 Issue #104162 — Expense: Report field interactive when all reports are non-reimbursable
- **Rivals:** `@janiya2`, `@sijo0218`
- **Rival Flaw:** `@janiya2` recommended closing as NAB based on outdated assumptions. `@sijo0218` noted that filtering purely by `canAddTransaction` without checking `isPolicyAdmin || isReportManager` breaks admin workflow additions (re-introducing bug #81608).
- **jloa-dev Pre-coded State:** Branch `fix/104162-report-field-non-reimbursable` ready.

### 1.16 Issue #104165 — Bank account: Address line 2 not saved
- **Rivals:** `@janiya2`, `@bonnhatnguyen`
- **C+ Test Finding:** On 2026-10-18, C+ `@nyomanjyotisa` tested the App-only parameter change on staging and verified:
  > *"The App-only change still loses address line 2 on staging. Could a CME investigate the backend support needed by the revised proposal before we select a complete solution? 🎀👀🎀 C+ reviewed"*
- **Status:** Blocked on backend `AddPersonalBankAccount` parameter acceptance.

### 1.17 Issue #104221 — Workspace admin can view card transactions from different workspace
- **Rivals:** `@camesenin`
- **Competitor Flaw:** `@camesenin` posted an identical diff after MelvinBot's analysis. MelvinBot flagged that Current Balance covers the entire program settlement account, raising questions regarding whether scoping by `policyID` is purely client-side or requires backend Search authorization.
- **jloa-dev Pre-coded State:** Branch `fix/104221-workspace-card-view-transactions-scope` ready.

---

## 2. Logic Chain

1. **Bot Intervention Guardrail Triggered:**
   - Issues **#103183**, **#103240**, and **#103533** have active Draft PRs initiated by `@MelvinBot` following maintainer/C+ commands (`@MelvinBot implement this`).
   - Rule 3 of the workspace rules dictates: *"Cero Intervención de Bots: Prohibido trabajar en issues donde un mantenedor haya llamado a @MelvinBot implement this o donde un bot interno ya tenga un PR / Draft PR para resolver el bug (evita que un bot haga merge y nos deje sin cobro)"*.
   - **Deduction:** These 3 issues must be deprioritized from active external bidding to protect against uncompensated bot merges.

2. **Internal Fix / Closed Guardrail Triggered:**
   - Issue **#103824** was resolved directly by Staff Engineer `@luacmartins` in `Mobile-Expensify` PR #14181 and released to production.
   - **Deduction:** Issue #103824 is closed/unpayable for external contributors.

3. **Backend-Blocked / Architectural Gates:**
   - Issue **#104165** was verified by C+ `@nyomanjyotisa` on staging: App-only fixes fail because the backend drops `addressStreet2`.
   - Issue **#102730** was evaluated by C+ `@jayeshmangwani`: frontend filtering in `useDefaultFundID` fails when a user is removed completely from the policy.
   - **Deduction:** Bidding on #104165 and #102730 requires backend deployment coordination or CME intervention.

4. **Identified Competitor Flaws & Competitive Superiority:**
   - **#102683:** Rivals `@bonnhatnguyen` and `@camesenin` broke fallback rendering by declaring `text` before `cardName` is resolved. `jloa-dev`'s branch fixes this ordering and includes unit tests.
   - **#104161:** Rival `@camesenin` omitted `backTo` in `createDynamicRoute`, causing back navigation to wipe out Search filters. `jloa-dev`'s branch uses `getReportRouteForCurrentContext`.
   - **#104138:** Rival `@bconnnnn` submitted unverified AI text; `@Metarenessans` used wrong React Native types. `jloa-dev` has branch `fix/104138-receipt-preview-resize-mode` tested and pushed.
   - **#103802:** Rival `@khizzcr7` broke per diem reallocation by disabling Edit Split entirely. `jloa-dev` holds FCFS on the surgical sibling editability guard.
   - **#103876:** Rival `@janiya2` created an API flood vulnerability by mass-updating all cards instead of targeting broken cards and clearing feed errors.
   - **#104159:** Rivals `@janiya2` and `@bonnhatnguyen` proposed stripping `isDomainPublic`, creating a severe cross-tenant privacy vulnerability.

---

## 3. Caveats

1. **Slack Context Access:** Discussions held in private Slack channels (`#expensify-bugs`, `#expensify-open-source`) were inferred from GitHub comments, quotes, and commit references, as direct Slack API tokens are not accessible.
2. **Backend Codebase Access:** `Web-Expensify` and `Auth` server codebases are private to internal Expensify staff; backend assertions rely on API parameter schemas, staging test results from C+ reviewers, and commit references.
3. **Draft PR Status Changes:** Maintainers may periodically close or reject MelvinBot draft PRs. If a bot PR is rejected, the corresponding issue immediately reopens for contributor proposals.

---

## 4. Conclusion & Actionable Classification

| Issue | Title | Escrow | Rivals | Audit Verdict | Strategic Action |
|---|---|---|---|---|---|
| **#102683** | Spend Card Filter Nicknames | $175 | 2 (@bonnhatnguyen, @camesenin) | **CRITICAL FLAW IN RIVALS** (`text` declaration order bug). jloa-dev branch ready. | **PRIORITY 1 INTERVENTION** (Post proposal highlighting unassigned card flaw). |
| **#104161** | Spend It's Not Here on Split | $175 | 2 (@camesenin, @emkhalid) | **CRITICAL FLAW IN RIVAL** (`backTo` omitted, wipes Search filters). jloa-dev branch ready. | **PRIORITY 1 INTERVENTION** (Post proposal highlighting filter preservation). |
| **#104138** | Receipt Preview Crop Forwarded Email | $175 | 2 (@bconnnnn, @Metarenessans) | **RIVAL FLAW** (Unverified AI / type mismatch). jloa-dev branch ready. | **PRIORITY 1 INTERVENTION** (jloa-dev branch ready for PR). |
| **#103802** | Split Per Diem Delete Guard | $175 | 2 (@camesenin, @khizzcr7) | **CRITICAL FLAW IN RIVAL** (khizzcr7 breaks reallocation; jloa-dev has FCFS over camesenin). | **PRIORITY 1 INTERVENTION** (Bump C+ @situchan on FCFS). |
| **#103876** | Amex Feed Error Persists | $175 | 1 (@janiya2) | **RIVAL FLAW** (API flood / missing feed error clear). | **PRIORITY 2 INTERVENTION** (Highlight batching & rate limit risk). |
| **#104221** | Workspace Card View Transactions Scope | $175 | 1 (@camesenin) | **COMPETITIVE PARITY** (camesenin duplicated fix). jloa-dev branch ready. | **PRIORITY 2 INTERVENTION** (Ready for PR). |
| **#103778** | Sentry APP-M66 Modal Dialog Null | $175 | 2 (@haiquywork, @tnclaudecode) | **NATIVE EXPERT REQUESTED** by C+ @cretadn22. jloa-dev proposal active. | **MONITOR C+ ASSIGNMENT** |
| **#103779** | TriNet Missing Final Approver | $175 | 2 (@haiquywork, @David-2002065) | **RIVAL MISDIAGNOSIS** (haiquywork wrong subsystem; possible NAB). | **HOLD** (Awaiting C+ direction). |
| **#104162** | Non-reimbursable Report Field Interactive | $175 | 2 (@janiya2, @sijo0218) | **DESIGN DISPUTE** (NAB vs Admin/Manager permission check). | **HOLD** (Awaiting C+ @Krishna2323). |
| **#104165** | Bank Account Address Line 2 | $175 | 2 (@janiya2, @bonnhatnguyen) | **BLOCKED ON BACKEND** (C+ verified staging failure). | **BLOCKED** (Do not bid until CME updates backend). |
| **#102730** | Ecard Feed Selector Demoted Admin | $175 | 1 (@yusufdeveloper2903) | **BLOCKED ON BACKEND** (C+ verified policy removal case). | **BLOCKED** (Awaiting CME). |
| **#104159** | Short Mention Single Char Dot | $175 | 2 (@janiya2, @bonnhatnguyen) | **NAB / SEVERE PRIVACY RISK** (Removing domain check leaks public emails). | **DESCARTE / NAB** |
| **#103183** | Transaction Tag Truncated with `\:` | $175 | 2 (@camesenin, @bonnhatnguyen) | **BOT INTERCEPTED** (Draft PR #104305 by MelvinBot). | **DESCARTE** (Rule 3 Anti-Bot Merge). |
| **#103240** | DEV Duplicate Key Search Filter | $50 | 2 (@camesenin, @amar-sheikh) | **BOT INTERCEPTED** (Draft PR #104034 by MelvinBot). | **DESCARTE** (Rule 3 Anti-Bot Merge). |
| **#103533** | Concierge Image Cut in RHP | $175 | 2 (@camesenin, @taieddie) | **BOT INTERCEPTED** (Draft PR #104288 by MelvinBot). | **DESCARTE** (Rule 3 Anti-Bot Merge). |
| **#103824** | Native Share Large Video Crash | $175 | 2 (@j3ffffff, @taieddie) | **INTERNAL FIX MERGED** (Mobile-Expensify PR #14181 in prod). | **CLOSED** (No external bounty). |
| **#103961** | Browser Back Navigates to Action | $175 | 2 (@janiya2, @camesenin) | **NOT HELP WANTED** (Under internal C+ reproduction). | **MONITOR** (Wait for Help Wanted). |

---

## 5. Verification Method

To independently verify the observations and logic chains documented in this report:

1. **Verify Competitor Code Flaws in #102683:**
   - Inspect `src/libs/CardFeedUtils.ts` lines 83–95 in `expensify_app`.
   - Observe that `const text = personalDetails?.displayName ?? cardName;` evaluates before `cardName` is updated from `getCompanyCardCustomName`.
   - Run tests: `npm test tests/unit/Search/buildCardFilterDataTest.ts`.

2. **Verify Bot Interceptions:**
   - Run `gh pr view 104305 --repo Expensify/App` (Issue #103183).
   - Run `gh pr view 104034 --repo Expensify/App` (Issue #103240).
   - Run `gh pr view 104288 --repo Expensify/App` (Issue #103533).
   - Confirm all 3 PRs are authored by `MelvinBot`.

3. **Verify Internal Fix on #103824:**
   - Run `gh issue view 103824 --repo Expensify/App --json comments --jq '.comments[-1]'`.
   - Confirm comment by C+ `@huult`: *"The PR fixing this issue was released to production 5 days ago. I think we can close this issue after 2 more days."*

4. **Verify Backend Block on #104165:**
   - Run `gh issue view 104165 --repo Expensify/App --json comments --jq '.comments[13]'`.
   - Confirm comment by C+ `@nyomanjyotisa`: *"The App-only change still loses address line 2 on staging. Could a CME investigate the backend support..."*
