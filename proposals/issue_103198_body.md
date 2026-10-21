# Issue #103198: [$175] Make the remove/unassign card warning clearer about which expenses get deleted

## Problem
When someone removes or unassigns a card, the warning says only that "unsubmitted transactions" will be deleted. That doesn't make clear that every imported draft expense is removed, including expenses on open reports. It also doesn't say the deletion can't be undone. One customer removed several personal cards and lost months of draft expenses. They had to rebuild their travel history from their calendar.

## Current copy (`src/languages/en.ts`)
- `workspace.moreFeatures.companyCards.removeCardDescription` (personal card "Remove card", used in [PersonalCardDetailsPage.tsx](https://github.com/Expensify/App/blob/da0cf969340f29c42c1d7b86a2918b0a0e40b37d/src/pages/settings/Wallet/PersonalCardDetailsPage.tsx)): "Removing this card will delete all unsubmitted transactions."
- `unassignCardDescription` / `unassignCardsDescription` (company cards, used in [DynamicWorkspaceCompanyCardDetailsPage.tsx](https://github.com/Expensify/App/blob/da0cf969340f29c42c1d7b86a2918b0a0e40b37d/src/pages/workspace/companyCards/DynamicWorkspaceCompanyCardDetailsPage.tsx) and [WorkspaceCompanyCardsTableControls.tsx](https://github.com/Expensify/App/blob/da0cf969340f29c42c1d7b86a2918b0a0e40b37d/src/components/Tables/WorkspaceCompanyCardsTable/WorkspaceCompanyCardsTableControls.tsx)): "Unassigning this card will delete all unsubmitted transactions." and the plural version.

## Solution
Rewrite these warnings to be more clear about what's being done:

- Removing personal card:
    - Suggested copy: `Removing this card will permanently delete all its unsubmitted transactions, including unreported and transactions on draft reports. This can't be undone.`
- Unassigning single company card:
    - Suggested copy: `Unassigning this card will permanently delete all its unsubmitted transactions, including unreported and transactions on draft reports. This can't be undone.`
-  Bulk unassign company cards:
    - Suggested copy: `Unassigning will permanently delete all unsubmitted transactions from the selected cards, including unreported and transactions on draft reports. This can't be undone.` 

As a first step, change only the copy. If customers still find the warning unclear, we can then consider letting them keep imported expenses when they remove a card.

## Existing unassign personal card 

<img width="1512" height="795" alt="Image" src="https://github.com/user-attachments/assets/05c58e18-e86c-4ec2-98cc-36430129be4f" />

## Existing unassign single company card

<img width="1512" height="800" alt="Image" src="https://github.com/user-attachments/assets/af861f78-adc3-4f6e-96d0-c1441efc844a" />

## Existing bulk unassign card

<img width="1505" height="789" alt="Image" src="https://github.com/user-attachments/assets/5b127d16-5df1-45a0-ba19-657ec2f35815" />

_Reported in [Slack](https://expensify.slack.com/archives/C049HHMV9SM/p1791251203612909)._

<details><summary>Upwork Automation - Do Not Edit</summary>
    <ul>
        <li>Upwork Job URL: <a href="https://www.upwork.com/jobs/~022108266265079512283">https://www.upwork.com/jobs/~022108266265079512283</a></li>
        <li>Upwork Job ID: 2108266265079512283</li>
        <li>Last Price Increase: 2026-10-08</li>
    </ul>
</details>