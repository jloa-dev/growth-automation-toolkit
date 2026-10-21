# Issue #103307: [$175] Gusto-Setting defaulted to "Manager approval" instead of "Custom approval"

If you haven’t already, check out our [contributing guidelines](https://github.com/Expensify/ReactNativeChat/blob/main/contributingGuides/CONTRIBUTING.md) for onboarding. To join our Slack channel, fill out [this form](https://forms.gle/Q7hnhUJPnQCK7Fe56).
___

**Version Number:** 9.5.4-0
**Reproducible in staging?:** Yes
**Reproducible in production?:** Unable to validate in Prod - Provide reasoning.
**If this was caught during regression testing, add the test name, ID and link from BrowserStack:** https://github.com/Expensify/App/pull/102750
**Email or phone of affected tester (no customers):** N/A
**Issue reported by:** Applause Internal Team
**Bug source:** Pull Request QA execution
**Device used:** Windows 11 / Chrome, iPhone 13 / iOS 27 Beta, Samsung Galaxy A52 / Android 14
**App Component:** Workspace Settings

## Action Performed:
Preconditions: 
- logged in to a new gmail account
- create a workspace, invite 2 members to the workspace

Steps:
1. Go to workflow in workspace setting
2. Navigate to approval in workflow, disable and enable the approval
3. Click edit on default workflow, add a second approver
4. Add another approval workflow that will create 2 approvers
5. Go to more features, enable HR
6. Connect Gusto in HR
7. Close the gusto sync complete RHP page
8. Observe the approval mode

## Expected Result:
it should starts with a Custom approval setting as default

## Actual Result:
it starts with a Manager approval setting as default

## Workaround:
Unknown

## Platforms:
- [x] Android: App
- [ ] Android: mWeb Chrome
- [x] iOS: App
- [ ] iOS: mWeb Safari
- [ ] iOS: mWeb Chrome
- [x] Windows: Chrome
- [x] MacOS: Chrome Safari

## Screenshots/Videos

https://github.com/user-attachments/assets/2eb1d064-0748-426f-aeb5-4aa8fe2cc1ab

[View all open jobs on GitHub](https://github.com/Expensify/App/issues?q=is%3Aopen+is%3Aissue+label%3A%22Help+Wanted%22)


> **Applause Internal Information**
> Exported by: Julia Ponikarchuk
> Bug ID: 7279603
<details><summary>Upwork Automation - Do Not Edit</summary>
    <ul>
        <li>Upwork Job URL: <a href="https://www.upwork.com/jobs/~022107779832826515888">https://www.upwork.com/jobs/~022107779832826515888</a></li>
        <li>Upwork Job ID: 2107779832826515888</li>
        <li>Last Price Increase: 2026-10-07</li>
    </ul>
</details>