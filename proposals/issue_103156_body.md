# Issue #103156: [$175] Offline Bank Unlock Doesn’t Open Concierge

If you haven’t already, check out our [contributing guidelines](https://github.com/Expensify/ReactNativeChat/blob/main/contributingGuides/CONTRIBUTING.md) for onboarding. To join our Slack channel, fill out [this form](https://forms.gle/Q7hnhUJPnQCK7Fe56).
___

**Version Number:** v9.5.3-0
**Reproducible in staging?:** Yes
**Reproducible in production?:** Yes
**If this was caught during regression testing, add the test name, ID and link from BrowserStack:** https://github.com/Expensify/App/pull/102367
**Email or phone of affected tester (no customers):** sintayewhaylu01@gmail.com
**Issue reported by:** Applause Internal Team
**Bug source:** Pull Request QA execution
**Device used:** Windows 10 /Chrome
**App Component:** Other

## Action Performed:
Precondition:
Use account: applausetester+lockedba@applause.expensifail.com

1. Open https://staging.new.expensify.com/
2. Navigate to Workspace settings → Workflows → Payment.
3. Go offline.
4. Click Unlock.

## Expected Result:
Concierge opens with one new bank-account unlock acknowledgement.

## Actual Result:
Concierge does not open. Instead, a “Request already submitted” message ppears.

## Workaround:
Unknown

## Platforms:
- [x] Android: App
- [ ] Android: mWeb Chrome
- [ ] iOS: App
- [ ] iOS: mWeb Safari
- [ ] iOS: mWeb Chrome
- [x] Windows: Chrome
- [ ] MacOS: Chrome Safari

## Screenshots/Videos

https://github.com/user-attachments/assets/c15db594-700b-49e6-ac02-27667c6dd968

[View all open jobs on GitHub](https://github.com/Expensify/App/issues?q=is%3Aopen+is%3Aissue+label%3A%22Help+Wanted%22)


> **Applause Internal Information**
> Exported by: Julia Ponikarchuk
> Bug ID: 7278362
<details><summary>Upwork Automation - Do Not Edit</summary>
    <ul>
        <li>Upwork Job URL: <a href="https://www.upwork.com/jobs/~022107402976279218900">https://www.upwork.com/jobs/~022107402976279218900</a></li>
        <li>Upwork Job ID: 2107402976279218900</li>
        <li>Last Price Increase: 2026-10-06</li>
    </ul>
</details>