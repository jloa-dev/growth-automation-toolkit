# Issue #103326: [$175] When offline Grey text with "Upload Attachment" doesn't appear during uploading attachment

If you haven’t already, check out our [contributing guidelines](https://github.com/Expensify/ReactNativeChat/blob/main/contributingGuides/CONTRIBUTING.md) for onboarding. To join our Slack channel, fill out [this form](https://forms.gle/Q7hnhUJPnQCK7Fe56).
___

**Version Number:** v9.5.4-0
**Reproducible in staging?:** Yes
**Reproducible in production?:** Yes
**If this was caught during regression testing, add the test name, ID and link from BrowserStack:** https://test-management.browserstack.com/projects/2219752/test-runs/76494298/folder/13176710/41236950/1815299163
**Email or phone of affected tester (no customers):** wimbukwa+1021026@applausemail.com
**Issue reported by:** Applause Internal Team
**Bug source:** Regression TC Execution
**Device used:** Samsung A34 / Android 16
**App Component:** Other

## Action Performed:
Precondition: Logged into the Expensify App.

1. Disable the internet connection on your phone.
2. Open the Expensify App.
3. Navigate to a chat and write something in the compose box.
4. Add an attachment to a chat while there is text content in the composer.
5. Verify that a comment appears with grey text "Uploading Attachment" indicating it is "pending".

## Expected Result:
When offline, grey text with "Upload Attachment" should appear during uploading the attachment.

## Actual Result:
When offline, grey text with "Upload Attachment" doesn't appear during uploading the attachment.

## Workaround:
Unknown

## Platforms:
- [x] Android: App
- [ ] Android: mWeb Chrome
- [ ] iOS: App
- [ ] iOS: mWeb Safari
- [ ] iOS: mWeb Chrome
- [ ] Windows: Chrome
- [ ] MacOS: Chrome Safari

## Screenshots/Videos

https://github.com/user-attachments/assets/a04839e5-58d7-4f98-955d-e3a240faf07f

[View all open jobs on GitHub](https://github.com/Expensify/App/issues?q=is%3Aopen+is%3Aissue+label%3A%22Help+Wanted%22)


> **Applause Internal Information**
> Exported by: Julia Ponikarchuk
> Bug ID: 7279617
<details><summary>Upwork Automation - Do Not Edit</summary>
    <ul>
        <li>Upwork Job URL: <a href="https://www.upwork.com/jobs/~022107813804128160468">https://www.upwork.com/jobs/~022107813804128160468</a></li>
        <li>Upwork Job ID: 2107813804128160468</li>
        <li>Last Price Increase: 2026-10-07</li>
    </ul>
</details>