# Issue #102868: [$175] Export to-do omits reports that Search returns for `action:export`

## Problem
The Export to-do in App can show fewer reports than `Search` returns for `action:export`. On one test account, `Search` returned 4 reports (8 expenses) and the Export to-do showed 0. All 4 reports were approved and paid, belonged to an admin, sat on a workspace with an accounting integration, and had not been exported or hit an export error.

Two rule differences cause the gap:

1. **Exporter check.** The to-do rule requires `policy.exporter === login` ([TodosUtils.ts](https://github.com/Expensify/App/blob/901155d74da8954c96aada81b94f0c1e4415ceac/src/libs/TodosUtils.ts#L167-L170)). On QuickBooks workspaces, `policy.exporter` can be empty while the connection's exporter is the user. `isPreferredExporter` in `PolicyUtils.ts` already reads the connection exporters.
2. **Auto-sync.** With auto-sync on, `isExportAction` decides no manual export is needed, and the report page agrees. The backend still returns these reports for `action:export`.

App also decides "should this user export this report" in four places that don't agree:
- Home to-do count
- Search sidebar item and badge (Awaiting export)
- Search row action and report page primary action
- Report page secondary action (More menu)

## Expected result
Use one export rule in all four places in App, and make it match the backend's `action:export` results.

## Unit tests
The fix must include thorough unit tests for the shared export rule. Cover at least:
- `policy.exporter` set to the user, set to someone else, and empty
- Connection exporter set to the user while `policy.exporter` is empty, for each supported accounting integration
- Auto-sync on and off
- Reports already exported, and reports with an export error
- Admin and non-admin users
- Each of the four places above returning the same result for the same report

## Steps to reproduce
1. Sign in as a workspace admin on a workspace with QuickBooks connected.
2. Set yourself as the exporter in the QuickBooks export settings, and leave `policy.exporter` empty.
3. Approve and pay a report without exporting it. Test once with auto-sync on and once with it off.
4. Open the Export to-do and compare it with the `count` in the `Search` response for `action:export`.

## Related
- #91559

_Reported in [Slack](https://expensify.slack.com/archives/C08CZDJFJ77/p1788794653229289)._

<details><summary>Upwork Automation - Do Not Edit</summary>
    <ul>
        <li>Upwork Job URL: <a href="https://www.upwork.com/jobs/~022105968657944336571">https://www.upwork.com/jobs/~022105968657944336571</a></li>
        <li>Upwork Job ID: 2105968657944336571</li>
        <li>Last Price Increase: 2026-10-02</li>
    </ul>
</details>

<details><summary>Issue Owner</summary>Current Issue Owner: @dukenv0307</details>