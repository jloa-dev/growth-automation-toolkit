# Handoff Report: GitHub Live State Explorer (Survey Explorer 2)

**Agent**: Survey Explorer 2 (`teamwork_preview_explorer_survey_2`)  
**Target Recipient**: Coordinator / Orchestrator (`cc1a87a1-5fc2-4780-b3de-d3ce81c2baad`)  
**Timestamp**: 2026-10-21T01:53:00Z  
**Handoff Type**: Hard (Investigation Complete)  

---

## 1. Observation

### 1.1 Methodology & Scope
- Probed live GitHub state via GitHub CLI (`gh issue view <num> --repo Expensify/App --json ...`) for all **101 unique Expensify/App issues** referenced in `TASK_LEDGER.md` (`c:\Users\Loa\Downloads\GOAL\TASK_LEDGER.md`).
- Auth credential: `gh auth status` active as `jloa-dev` (read:org, repo scope).
- Live dataset recorded in:
  - `scratch/live_pipeline_inspection.json` (Full raw JSON for all 101 issues)
  - `scratch/refined_pipeline_results.json` (Categorized analysis)
  - `scratch/enriched_high_priority.json` (Enriched high priority targets with Upwork URLs and assignees)

### 1.2 Global Issue State Breakdown
```
Total Expensify/App Issues Analyzed: 101
├── 1. Closed Issues (CLOSED): 9
├── 2. Hired or Contributor Assigned (HIRED_OR_ASSIGNED): 11
├── 3. Bot Disqualified (MELVINBOT_ACTIVE): 15
└── 4. Active Unassigned Open Issues: 66
    ├── High-Priority Targets (0 to 2 Human Rivals): 37  ($6,350 USD total)
    │   ├── 0 Human Rivals (Solo / Uncontested): 7       ($1,225 USD)
    │   ├── 1 Human Rival: 9                             ($1,575 USD)
    │   └── 2 Human Rivals: 21                           ($3,550 USD)
    └── Medium-Priority Targets (3+ Human Rivals): 29   ($5,225 USD total)
```

---

### 1.3 High-Priority Targets (0 to 2 Human Rivals, Active, No Bot PR, No Hired Contributor)

#### Tier 1: 0 Human Rivals — Solo / Uncontested (7 Issues / $1,225 USD)
| # | Issue | Title | Bounty | Staff Engineer | C+ Reviewer | Upwork Job Escrow URL | C+ Badge / Review Notes |
|---|---|---|---|---|---|---|---|
| 1 | [#104127](https://github.com/Expensify/App/issues/104127) | Android - Concierge does not change category in report when asked in natural language | $175 USD | `@rojiphil` | — | [Job #022110784962634286346](https://www.upwork.com/jobs/~022110784962634286346) | 0 rivals; Solo proposal from jloa-dev (`#issuecomment-6264422604`) |
| 2 | [#103965](https://github.com/Expensify/App/issues/103965) | Import contacts-Import contacts option is not displayed when tapping Start chat | $175 USD | `@rojiphil` | — | [Job #022110270660163217377](https://www.upwork.com/jobs/~022110270660163217377) | 0 rivals; Solo proposal from jloa-dev (`#issuecomment-6264424011`) |
| 3 | [#103838](https://github.com/Expensify/App/issues/103838) | The tab bar does not visible above the spinner | $175 USD | `@situchan` | — | [Job #022109928824204193624](https://www.upwork.com/jobs/~022109928824204193624) | 0 human rivals (MelvinBot bot comment only); Solo proposal |
| 4 | [#103326](https://github.com/Expensify/App/issues/103326) | When offline Grey text with "Upload Attachment" doesn't appear during uploading attachment | $175 USD | `@TaduJR` | — | [Job #022107813804128160468](https://www.upwork.com/jobs/~022107813804128160468) | 0 rivals; Solo proposal from jloa-dev (`#6138194152`) + bump (`#6155282950`) |
| 5 | [#103307](https://github.com/Expensify/App/issues/103307) | Gusto-Setting defaulted to "Manager approval" instead of "Custom approval" | $175 USD | `@MonilBhavsar` | `@thelullabyy` | [Job #022107779832826515888](https://www.upwork.com/jobs/~022107779832826515888) | 0 rivals; C+ `@thelullabyy` requested internal test account: "It looks like BE issue to me Needs help from bc-team/internal team 🎀 👀 🎀 C+ reviewed" |
| 6 | [#103244](https://github.com/Expensify/App/issues/103244) | Onboarding - Product update / feature announcements still shown to employees invited to a workspace | $175 USD | `@shubham1206agra` | — | [Job #022107586630303041825](https://www.upwork.com/jobs/~022107586630303041825) | 0 human rivals (MelvinBot bot comment only); Solo proposal |
| 7 | [#103156](https://github.com/Expensify/App/issues/103156) | Offline Bank Unlock Doesn’t Open Concierge | $175 USD | `@rojiphil` | — | [Job #022107402976279218900](https://www.upwork.com/jobs/~022107402976279218900) | 0 human rivals (MelvinBot bot comment only); Solo proposal from jloa-dev (`#6138198987`) |

#### Tier 2: 1 Human Rival (9 Issues / $1,575 USD)
| # | Issue | Title | Bounty | Staff Engineer | C+ Reviewer | Human Rival | Upwork Job Escrow URL | Notes |
|---|---|---|---|---|---|---|---|---|
| 8 | [#104505](https://github.com/Expensify/App/issues/104505) | [Sentry: APP-N5H] HybridApp Android: native tab bar crashes with more than 6 items | $175 USD | `@mananjadhav` | `@mountiny` | `@RajGahoi` | [Job #022112637743125227618](https://www.upwork.com/jobs/~022112637743125227618) | Fresh 20 Oct task; 1 competitor |
| 9 | [#104502](https://github.com/Expensify/App/issues/104502) | [Sentry: APP-MHA] HybridApp iOS: FlashList onScroll throws "LayoutManager is not initialized" | $175 USD | `@mountiny` | `@linhvovan29546` | `@haiquywork` | [Job #022112637720568651801](https://www.upwork.com/jobs/~022112637720568651801) | Fresh 20 Oct task; 1 competitor |
| 10 | [#104501](https://github.com/Expensify/App/issues/104501) | [Sentry: APP-DQ2] Web: FlashList commitLayout loops into "Maximum update depth exceeded" | $175 USD | `@mountiny` | `@getusha` | `@magomedta` | [Job #022112683613241355184](https://www.upwork.com/jobs/~022112683613241355184) | Fresh 20 Oct task; 1 competitor |
| 11 | [#104287](https://github.com/Expensify/App/issues/104287) | Search - Error and From filter dropped after entering "group-by: reports" on a saved search | $175 USD | `@truph01` | `@truph01` | `@nabi-ebrahimi` | [Job #022111443332056306411](https://www.upwork.com/jobs/~022111443332056306411) | 1 competitor; `@nabi-ebrahimi` assignee is competitor self-referential |
| 12 | [#104176](https://github.com/Expensify/App/issues/104176) | Filters - Vendor option is missing in filters | $175 USD | `@suneox` | — | `@camesenin` | [Job #022110885193812397155](https://www.upwork.com/jobs/~022110885193812397155) | 1 competitor (`@camesenin`); jloa-dev proposed `FILTER_VIEW_MAP` fix |
| 13 | [#103721](https://github.com/Expensify/App/issues/103721) | 103421 - Per Diem - Not here page after going back online when the destination loads | $175 USD | `@situchan` | — | `@ashusatyarthi-wq` | [Job #022109593475976808400](https://www.upwork.com/jobs/~022109593475976808400) | 1 competitor; offline fallback caching |
| 14 | [#103349](https://github.com/Expensify/App/issues/103349) | Android - Expensify app is not available in the share sheet when sharing an HEVC video file | $175 USD | `@rojiphil` | — | `@camesenin` | [Job #022107849209866715481](https://www.upwork.com/jobs/~022107849209866715481) | 1 competitor (`@camesenin`); intent-filter mimeType fix |
| 15 | [#103245](https://github.com/Expensify/App/issues/103245) | Agent: Agent page stuck in infinity loading after switch to Copilot | $175 USD | `@mananjadhav` | — | `@bonnhatnguyen` | [Job #022107586883241239186](https://www.upwork.com/jobs/~022107586883241239186) | 1 competitor (`@bonnhatnguyen`); copilot loading state |
| 16 | [#103214](https://github.com/Expensify/App/issues/103214) | The new avatar is not reflected after uploading new photo to the profile | $175 USD | `@mkhutornyi` | — | `@camesenin` | [Job #022107501218908067689](https://www.upwork.com/jobs/~022107501218908067689) | 1 competitor (`@camesenin`); Android disk cache invalidation |

#### Tier 3: 2 Human Rivals (21 Issues / $3,550 USD)
| # | Issue | Title | Bounty | Staff Engineer | C+ Reviewer | Human Rivals | Upwork Job Escrow URL | Notes |
|---|---|---|---|---|---|---|---|---|
| 17 | [#104519](https://github.com/Expensify/App/issues/104519) | Search - Contextual suggestion for new Held Report is missing | $175 USD | `@rojiphil` | — | `@taieddie`, `@khizzcr7` | [Job #022112649059231981593](https://www.upwork.com/jobs/~022112649059231981593) | Fresh 20 Oct task; 2 competitors |
| 18 | [#104515](https://github.com/Expensify/App/issues/104515) | All - Empty "Check your info" page appears in RHP after adding BA to Wallet | $175 USD | `@brunovjk` | — | `@camesenin`, `@khizzcr7` | [Job #022112637793222357815](https://www.upwork.com/jobs/~022112637793222357815) | Fresh 20 Oct task; 2 competitors |
| 19 | [#104509](https://github.com/Expensify/App/issues/104509) | Expensify Card - Next button replaced with loading button after enabled then disabled rule | $175 USD | `@eh2077` | — | `@camesenin`, `@khizzcr7` | [Job #022112633586567027913](https://www.upwork.com/jobs/~022112633586567027913) | Fresh 20 Oct task; 2 competitors |
| 20 | [#104503](https://github.com/Expensify/App/issues/104503) | [Sentry: APP-MD4] HybridApp Android: startup abort, "Cannot find native module 'ExpoAudio'" | $175 USD | `@mountiny` | `@ikevin127` | `@taieddie`, `@haiquywork` | [Job #022112637848604843209](https://www.upwork.com/jobs/~022112637848604843209) | Fresh 20 Oct task; 2 competitors |
| 21 | [#104221](https://github.com/Expensify/App/issues/104221) | Workspace admin can view card transactions from a different workspace | $175 USD | `@abdulrahuman5196` | — | `@camesenin`, `@janiya2` | [Job #022111073873591100700](https://www.upwork.com/jobs/~022111073873591100700) | Shared card program boundary leak |
| 22 | [#104165](https://github.com/Expensify/App/issues/104165) | Bank account - Address line is not saved when adding an US bank account | $175 USD | `@puneetlath` | `@nyomanjyotisa` | `@janiya2`, `@bonnhatnguyen` | Internal Applause | C+ `@nyomanjyotisa` flagged BE requirement; proposal open |
| 23 | [#104162](https://github.com/Expensify/App/issues/104162) | Expense - Report files is enable when all report contain non-reimbursable expense | $175 USD | `@Krishna2323` | — | `@janiya2`, `@sijo0218` | [Job #022110833816404111157](https://www.upwork.com/jobs/~022110833816404111157) | 2 competitors |
| 24 | [#104161](https://github.com/Expensify/App/issues/104161) | Spend - It's not here page when opening a split expense from chat filter | $175 USD | `@mkhutornyi` | — | `@camesenin`, `@janiya2` | [Job #022110831219914409226](https://www.upwork.com/jobs/~022110831219914409226) | 2 competitors |
| 25 | [#104159](https://github.com/Expensify/App/issues/104159) | Chat - short mention with a single character followed by dot isn't recognized | $175 USD | `@ahmedGaber93` | — | `@janiya2`, `@bonnhatnguyen` | [Job #022110828231641473065](https://www.upwork.com/jobs/~022110828231641473065) | 2 competitors; mention regex edge case |
| 26 | [#104138](https://github.com/Expensify/App/issues/104138) | Receipts are not showing fully when sent to receipts@expensify.com | $175 USD | `@sobitneupane` | — | `@bconnnnn`, `@Metarenessans` | [Job #022110793935688626891](https://www.upwork.com/jobs/~022110793935688626891) | 2 competitors |
| 27 | [#103961](https://github.com/Expensify/App/issues/103961) | Web - Chat -Browser back navigates to previous action instead of previous report | $175 USD | `@suneox` | — | `@janiya2`, `@camesenin` | [Job #022110241879857618845](https://www.upwork.com/jobs/~022110241879857618845) | 2 competitors |
| 28 | [#103876](https://github.com/Expensify/App/issues/103876) | Amex feed error persists after reconnect until manual scrape | $175 USD | `@TaduJR` | — | `@janiya2`, `@camesenin` | [Job #022109996863454032366](https://www.upwork.com/jobs/~022109996863454032366) | 2 competitors |
| 29 | [#103824](https://github.com/Expensify/App/issues/103824) | Native share - The app crashes after sharing a large video file (>125 MB) | $175 USD | `@huult` | `@luacmartins` | `@j3ffffff`, `@taieddie` | [Job #022109895596413811824](https://www.upwork.com/jobs/~022109895596413811824) | 2 competitors; Android content resolver OOM |
| 30 | [#103802](https://github.com/Expensify/App/issues/103802) | Expense - Edit split when confirming delete expense of a split per diem expense | $175 USD | `@situchan` | — | `@haiquywork`, `@camesenin` | [Job #022109697864167641150](https://www.upwork.com/jobs/~022109697864167641150) | 2 competitors |
| 31 | [#103779](https://github.com/Expensify/App/issues/103779) | TriNet - Missing Final Approver when user select Custom Approval | $175 USD | `@ZhenjaHorbach` | — | `@haiquywork`, `@David-2002065` | [Job #022109655010878713688](https://www.upwork.com/jobs/~022109655010878713688) | 2 competitors |
| 32 | [#103778](https://github.com/Expensify/App/issues/103778) | [Sentry: APP-M66] Android: ReactModalHostView updateSystemAppearance "dialog must exist" | $175 USD | `@mountiny` | `@cretadn22` | `@haiquywork`, `@tnclaudecode` | [Job #022109653602347544408](https://www.upwork.com/jobs/~022109653602347544408) | 2 competitors |
| 33 | [#103533](https://github.com/Expensify/App/issues/103533) | Concierge - Image appears cut on its preview on the Concierge RHP | $175 USD | `@roryabraham` | `@abzokhattab` | `@camesenin`, `@taieddie` | [Job #022108319757049731349](https://www.upwork.com/jobs/~022108319757049731349) | 2 competitors |
| 34 | [#103240](https://github.com/Expensify/App/issues/103240) | DEV - Duplicate key error showing up in the console | $50 USD | `@eVoloshchak` | — | `@camesenin`, `@amar-sheikh` | [Job #022107570335145085652](https://www.upwork.com/jobs/~022107570335145085652) | 2 competitors |
| 35 | [#103183](https://github.com/Expensify/App/issues/103183) | Transaction's tag isn't updated correctly when selecting a tag contain `\:` | $175 USD | `@bernhardoj` | — | `@camesenin`, `@bonnhatnguyen` | [Job #022107464881310224816](https://www.upwork.com/jobs/~022107464881310224816) | 2 competitors; tag escaping regex |
| 36 | [#102730](https://github.com/Expensify/App/issues/102730) | Ecard - The empty illustration is not shown after removing user admin permission | $175 USD | `@jayeshmangwani` | — | `@camesenin`, `@bonnhatnguyen` | [Job #022105573983988233029](https://www.upwork.com/jobs/~022105573983988233029) | 2 competitors |
| 37 | [#102683](https://github.com/Expensify/App/issues/102683) | Company card nicknames don’t show in the Spend page Card filter | $175 USD | `@ChavdaSachin` | — | `@camesenin`, `@bonnhatnguyen` | [Job #022105371204565575660](https://www.upwork.com/jobs/~022105371204565575660) | 2 competitors |

---

### 1.4 Disqualified Issues Due to Bot Activity (15 Issues - Rule 3 Compliance)
Under Rule 3 ("Filtro Anti-Bot y Anti-Estafas: Cero Intervención de Bots — Prohibido trabajar en issues donde un mantenedor haya llamado a `@MelvinBot implement this` o donde un bot interno ya tenga un PR / Draft PR"), the following 15 issues are disqualified:
1. **[#103345]** — MelvinBot automated PR merged/active (`[Due for payment 2026-10-26]`).
2. **[#103488]** — MelvinBot automated PR merged/active (`[Due for payment 2026-10-23]`).
3. **[#103662]** — MelvinBot automated PR merged/active (`[Due for payment 2026-10-27]`).
4. **[#103726]** — MelvinBot automated PR merged/active (`[Due for payment 2026-10-23]`).
5. **[#103775]** — MelvinBot automated PR merged/active (`[Due for payment 2026-10-26]`).
6. **[#103898]** — MelvinBot automated PR merged/active (`[Due for payment 2026-10-23]`).
7. **[#104093]** — MelvinBot automated PR merged/active (`[Due for payment 2026-10-27]`).
8. **[#104147]** — 2 automated PRs and explicit `@MelvinBot implement this` calls by maintainer `@neil-marcellini`.
9. **[#102734]** — `@MelvinBot implement this` called by maintainer `@dubielzyk-expensify`.
10. **[#103058]** — `@MelvinBot implement this` called by C+ reviewer `@marufsharifi`.
11. **[#103759]** — `@MelvinBot implement this` called by maintainer `@rojiphil`.
12. **[#104300]** — `@MelvinBot implement this` called by maintainer `@ChavdaSachin`.
13. **[#103216]** — C+ `@FitseTLT` officially endorsed Melvin: `@MelvinBot implement 🎀 👀 🎀 C+ reviewed`.
14. **[#103492]** — C+ `@cretadn22` officially endorsed Melvin: `@MelvinBot's proposal looks good to me 🎀 👀 🎀 C+ reviewed`.
15. **[#103957]** — C+ `@brunovjk` officially endorsed Melvin analysis: `This appears to be expected behavior, as explained in Melvin's analysis... 🎀 👀 🎀 C+ reviewed`.

---

### 1.5 Issues with Contributor Hired or Already Assigned (11 Issues)
The following issues are OPEN on GitHub, but an external human contributor was already selected and hired via Upwork Escrow:
1. **[#102072]** — Contributor `@yusufdeveloper2903` hired ($250 USD).
2. **[#102792]** — Contributor `@dukenv0307` hired (`[Due for payment 2026-10-27]`, $175 USD).
3. **[#102868]** — Contributor `@dukenv0307` hired ($175 USD).
4. **[#103063]** — Contributor `@gijoe0295` hired ($175 USD).
5. **[#103198]** — Contributor `@thelullabyy` hired ($175 USD).
6. **[#103341]** — Contributor `@dmkt9` hired ($175 USD).
7. **[#103531]** — Contributor `@nabi-ebrahimi` hired ($250 USD).
8. **[#103593]** — Contributor `@nkdengineer` hired (`[Due for payment 2026-10-22]`, $175 USD).
9. **[#103764]** — Contributor `@mountiny` (internal staff) taking over (`[Due for payment 2026-10-26]`, $175 USD).
10. **[#103944]** — Contributor `@Eskalifer1` hired (`[Due for payment 2026-10-23]`, $175 USD).
11. **[#104089]** — Contributor `@rayane-d` hired ($175 USD).

---

### 1.6 Fully Closed Issues (9 Issues)
1. **[#102437]** ($250 USD) — Closed (re-scoped / fixed internally).
2. **[#103324]** ($175 USD) — Closed (test account DNS credential issue).
3. **[#103355]** ($175 USD) — Closed NAB by Expensify design team.
4. **[#103538]** ($175 USD) — Closed / resolved.
5. **[#103663]** ($250 USD) — Closed / merged.
6. **[#103664]** ($250 USD) — Closed / merged.
7. **[#103671]** ($250 USD) — Closed (`[Due for payment 2026-10-21]`).
8. **[#103770]** ($175 USD) — Closed.
9. **[#103863]** ($175 USD) — Closed.

---

### 1.7 Medium-Priority Active Candidates (3+ Human Rivals, 29 Issues)
Issues still open and unassigned, but with 3 or more human competitors:
- **3 Rivals (16 issues)**: #103406, #103493, #103595, #103619, #103776, #103777, #103831, #103875, #103908, #103935, #104113, #104178, #104218, #104231, #104341, #104461.
- **4 Rivals (4 issues)**: #103497, #103931, #104280, #104500.
- **5 Rivals (5 issues)**: #103648, #104247, #104262, #104299, #104302.
- **6+ Rivals (4 issues)**: #104301 (6 rivals), #104307 (10 rivals), #103403 (18 rivals), #102525 (24 rivals).

---

## 2. Logic Chain

1. **Premise 1 (Workspace Pipeline Boundary)**:
   - `TASK_LEDGER.md` contains the authoritative record of all historic and recent Expensify bounties tracked by `jloa-dev`.
   - Parsing all Expensify/App URLs in `TASK_LEDGER.md` identified exactly 101 unique issues.

2. **Premise 2 (Zero-Scam & Zero-Bot Merge Guardrail)**:
   - Rule 3 prohibits working on issues where `@MelvinBot implement this` was called or where MelvinBot already opened an automated PR.
   - Live query of `comments` and `title` tags isolated 15 issues where MelvinBot has active PRs or maintainer endorsements. These were strictly separated into `MELVINBOT_ACTIVE` to protect developer time and escrow payout.

3. **Premise 3 (Hired Contributor Status)**:
   - Issues with 3 assignees (typically Staff + C+ + Contributor) or with explicit Upwork hire announcements ("An application has been approved... Contributor: @...") cannot be awarded to a new proposer unless the current contract is terminated.
   - Exactly 11 open issues have an active hired contributor, leaving 66 truly unassigned open issues.

4. **Premise 4 (Low-Competition Filtering: 0 to 2 Rivals)**:
   - Filtering the 66 active unassigned issues by human competitor count ($\le 2$ human rivals) isolates **exactly 37 High-Priority Targets**.
   - These 37 issues represent **$6,350 USD** in backed Upwork Escrow funds.
   - 7 of these tickets are completely uncontested (0 human rivals), including recent tickets and active C+ reviews (#103307, #103156, #103326, #103838, #103965, #104127, #103244).
   - 9 tickets feature exactly 1 rival, including the latest high-value 20 Oct sentry tickets (#104501, #104502, #104505).
   - 21 tickets feature exactly 2 rivals (#104503, #104509, #104515, #104519, etc.).

---

## 3. Caveats

1. **Dynamic Competition**: Competitor counts reflect the live state on GitHub at `2026-10-21T01:50Z`. New proposals from other contributors may appear at any time.
2. **Upwork Job Ingestion for Internal Issues**: Issue #104165 was filed directly by the Applause Internal team without an embedded Upwork job link in the GitHub description. Its escrow contract is handled via internal Applause/Expensify routing.
3. **No External Comments Posted**: In accordance with the strict read-only scope, zero comments, reactions, or draft submissions were made to GitHub or Upwork.

---

## 4. Conclusion

- The live GitHub pipeline contains **37 active, unassigned Expensify/App issues** meeting the strict criteria:
  - Open GitHub state.
  - Backed by Upwork Escrow.
  - 0 to 2 human competitors.
  - Zero active MelvinBot automated PRs or maintainer implementation calls.
  - No hired contributor.
- Total escrow value across these 37 targets: **$6,350 USD**.
- The highest-probability intervention candidates are:
  1. **Tier 1 (0 Rivals - Uncontested, $1,225 USD)**: #104127, #103965, #103838, #103326, #103307, #103244, #103156.
  2. **Tier 2 (1 Rival - 20 Oct Sentry/HybridApp, $1,575 USD)**: #104505, #104502, #104501, #104287, #104176, #103721, #103349, #103245, #103214.
  3. **Tier 3 (2 Rivals - High Conversion, $3,550 USD)**: #104519, #104515, #104509, #104503, #104165, #103778, etc.

---

## 5. Verification Method

To independently verify these live findings:
1. **Verify Raw Live State**:
   ```powershell
   gh issue view 104505 --repo Expensify/App --json state,assignees,title,comments
   gh issue view 103307 --repo Expensify/App --json state,assignees,title,comments
   ```
2. **Inspect Artifact Files**:
   - `scratch/enriched_high_priority.json`
   - `scratch/refined_pipeline_results.json`
   - `scratch/live_pipeline_inspection.json`
3. **Run Pipeline Summary Script**:
   ```powershell
   python scratch/print_summary.py
   python scratch/inspect_37_high_priority.py
   ```
4. **Invalidation Conditions**:
   - Maintainer posts `@MelvinBot implement this` or hires another contributor on any of the 37 listed issues.
