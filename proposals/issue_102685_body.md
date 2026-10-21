# Issue #102685: [$175] Users are unable to add all AmEx cards through the AmEx Direct Connection when multiple AmEx sign-ins return card lists that share the same main card.

If you haven’t already, check out our [contributing guidelines](https://github.com/Expensify/ReactNativeChat/blob/main/contributingGuides/CONTRIBUTING.md) for onboarding. To join our Slack channel, fill out [this form](https://forms.gle/Q7hnhUJPnQCK7Fe56).
___

**Version Number:**
**Reproducible in staging?:** Needs Reproduction
**Reproducible in production?:** Needs Reproduction
**If this was caught during regression testing, add the test name, ID and link from BrowserStack:**
**Email or phone of affected tester (no customers):**
**Logs:** https://stackoverflow.com/c/expensify/questions/4856
**Expensify/Expensify Issue URL:**
**Issue reported by:**  @@Liz-Canary
**Slack conversation** (hyperlinked to channel name): [#Expensify Bugs](https://expensify.slack.com/archives/C049HHMV9SM/p1790723323267859)

## Action Performed:

1. Navigate to Workspace > Workspace Name > Company Cards.
2. Select AmEx and choose Add Card.
3. Sign in with an AmEx account that returns multiple cards.
4. Repeat the connection using another AmEx login that also has access to the same main card.
5. Observe the AmEx cards and connection/feed information after both connections are processed.
6. Attempt to access cards from the connection that was overwritten.

## Expected Result:
Each AmEx connection should be handled independently, even when the returned card lists contain the same main card or the same last four digits.
All cards accessible through the respective AmEx accounts should remain available without one connection overwriting another.
## Actual Result:
One AmEx login returns 11 cards, while another returns 3 cards.
Both card lists start with the same main card, Delta Reserve Business Card - xxxx.
The feed is named using the last four digits of the first card returned.
Both connections therefore resolve to the same feed identifier (oauth.americanexpressfdx.com 2009).
The later connection overwrites the previously stored cards and credentials.
As a result, cards from the overwritten connection can show a "connection is broken" error.
The latest save on September 29 at 21:54 UTC came from the 3-card login, leaving only those 3 cards in the feed.
## Workaround:
Unknown
## Platforms:
Select the officially supported platforms where the issue was reproduced:
- [ ] Android: App
- [ ] Android: mWeb Chrome
- [ ] iOS: App
- [ ] iOS: mWeb Safari
- [ ] iOS: mWeb Chrome
- [x] Windows: Chrome
- [x] MacOS: Chrome / Safari

## Screenshots/Videos


[View all open jobs on GitHub](https://github.com/Expensify/App/issues?q=is%3Aopen+is%3Aissue+label%3A%22Help+Wanted%22)

<details><summary>Upwork Automation - Do Not Edit</summary>
    <ul>
        <li>Upwork Job URL: <a href="https://www.upwork.com/jobs/~022105375901292668908">https://www.upwork.com/jobs/~022105375901292668908</a></li>
        <li>Upwork Job ID: 2105375901292668908</li>
        <li>Last Price Increase: 2026-09-30</li>
    </ul>
</details>