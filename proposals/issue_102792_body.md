# Issue #102792: [$175] Inbox shows RBR and Fix for violations on submitted reports that Home and Spend correctly ignore

## Problem

The Inbox shows a red dot (RBR) and a **Fix** to-do for violations on reports the submitter has already submitted. Home and Spend correctly show nothing to do for the same reports. The submitter can't resolve these violations, so the Inbox RBR never clears.

**Example:** An employee submitted a report with two violations: `receiptRequired` on one expense and `itemizedReceiptRequired` on another. `itemizedReceiptRequired` stays even with a receipt attached if SmartScan found no line items. The Inbox shows an RBR. Home and Spend show nothing.

**Expected:** A violation shows as **Fix** only when its transaction is on a draft (open) report. The Inbox, Home and Spend use the same rule.

## Where the rules split

- **Inbox:** [`src/libs/ReportUtils.ts:10103-10137`](https://github.com/Expensify/App/blob/9b74c950a700cf1eac15d59723b8d61a0c022874/src/libs/ReportUtils.ts#L10103-L10137) lets both open and processing reports raise the RBR. After submit, it skips only `companyCardRequired` and the `modifiedAmount` notice. This check drives the workspace chat RBR, its Fix badge, the Inbox tab dot and the Inbox To-do tab.
- **Home:** [`src/pages/home/ForYouSection/useReviewFlaggedExpenses.ts:42-58`](https://github.com/Expensify/App/blob/9b74c950a700cf1eac15d59723b8d61a0c022874/src/pages/home/ForYouSection/useReviewFlaggedExpenses.ts#L42-L58) counts only open reports.
- **Spend:** only has Submit, Approve, Pay and Export lists. None of them look at violations.

Earlier fixes excluded one violation name at a time, for example [After an expense with a “Company card purchases required” violation is submitted, the Fix / To-do action continues to be displayed for the expense](https://github.com/Expensify/App/issues/99793). This issue replaces that approach with one shared rule.

## Solution

1. Move the "does this violation need action from me" check into one function in `TodosUtils.ts`.
2. Make the Inbox (LHN RBR, Fix badge, Inbox tab dot, To-do tab), Home and Spend all call that function.
3. Show violations as **Fix** only for transactions on draft (open) reports.
4. Update the existing `ReportUtilsTest.ts` tests that expect an RBR for violations on submitted reports.

## Tests to add

- A parity test that builds reports in every combination of report state (open, processing, approved), role (submitter, approver, admin) and violation type. It asserts that every Inbox RBR / Fix to-do has a matching Home or Spend to-do, and the reverse.
- Today the only cross-page test, in `tests/unit/useTodoCountsTest.tsx`, checks one direction and uses no violations. Extend it to cover violations.

_Reported in [Slack](https://expensify.slack.com/archives/C05LX9D6E07/p1790475938275859)._


<details><summary>Issue Owner</summary>Current Issue Owner: @dukenv0307</details>
<details><summary>Upwork Automation - Do Not Edit</summary>
    <ul>
        <li>Upwork Job URL: <a href="https://www.upwork.com/jobs/~022105991831465547963">https://www.upwork.com/jobs/~022105991831465547963</a></li>
        <li>Upwork Job ID: 2105991831465547963</li>
        <li>Last Price Increase: 2026-10-02</li>
    </ul>
</details>