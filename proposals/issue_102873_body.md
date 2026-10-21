# Issue #102873: [$175] Workflows - No changelog generated for adding approval workflow with report amount limit

If you haven’t already, check out our [contributing guidelines](https://github.com/Expensify/ReactNativeChat/blob/main/contributingGuides/CONTRIBUTING.md) for onboarding. To join our Slack channel, fill out [this form](https://forms.gle/Q7hnhUJPnQCK7Fe56).
___

**Version Number:** v9.5.1-1
**Reproducible in staging?:** Yes
**Reproducible in production?:** Yes
**If this was caught during regression testing, add the test name, ID and link from BrowserStack:** https://test-management.browserstack.com/projects/2219752/test-runs/76693051/folder/57610056/140237288/1818873053
**Email or phone of affected tester (no customers):** applausetester+bm890334@applause.expensifail.com
**Issue reported by:** Applause Internal Team
**Bug source:** Regression TC Execution
**Device used:** Web, android
**App Component:** Other

## Action Performed:
Preconditions:
Log in with an Expensifail account
Have a workspace with a few members added

1. Go to staging.new.expensify.com
2. Go to Workspace settings > Workflows.
3. Click "Add approval workflow" and select a member.
4. Click "Next" and select an approver.
5. Set a report amount limit and set an additional approver.
6. Click "Next", then click "Add workflow".
7. Go to the #admin room and check for a changelog entry.

## Expected Result:
A changelog entry should be displayed in the #admin room for the added approval workflow.

## Actual Result:
No changelog entry is displayed in the #admin room.

## Workaround:
Unknown

## Platforms:
- [x] Android: App
- [ ] Android: mWeb Chrome
- [ ] iOS: App
- [ ] iOS: mWeb Safari
- [ ] iOS: mWeb Chrome
- [x] Windows: Chrome
- [x] MacOS: Chrome Safari

## Screenshots/Videos

https://github.com/user-attachments/assets/0ae16172-3fe5-47bb-9fba-4d4318901057

[View all open jobs on GitHub](https://github.com/Expensify/App/issues?q=is%3Aopen+is%3Aissue+label%3A%22Help+Wanted%22)


> **Applause Internal Information**
> Exported by: Nathan Lemma
> Bug ID: 7274918
<details><summary>Upwork Automation - Do Not Edit</summary>
    <ul>
        <li>Upwork Job URL: <a href="https://www.upwork.com/jobs/~022105982157197102780">https://www.upwork.com/jobs/~022105982157197102780</a></li>
        <li>Upwork Job ID: 2105982157197102780</li>
        <li>Last Price Increase: 2026-10-02</li>
    </ul>
</details>