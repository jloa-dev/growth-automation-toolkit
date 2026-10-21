@cretadn22 Yes, exactly! To reproduce the bug, the workspace must have an existing policy/accounting sync error in Onyx *before* it is archived:

1. An `@expensifail.com` admin account is needed because it has access to the Sage Intacct accounting integration.
2. Go to **Workspace > Accounting > Sage Intacct** and enter invalid credentials so the backend returns an error, setting the RBR error badge on the accounting connection.
3. Then go to **Workspace > Three dots > Archive Workspace > Confirm**.
4. Once archived, the child configuration tabs (like Accounting) are locked/hidden, preventing the user from dismissing or resolving the connection error. However, the workspace navigation row still evaluates `hasPolicyError` on the archived policy in Onyx, leaving the RBR badge permanently visible with no way to remove it.

Without that initial failed connection (via the `@expensifail.com` test account) generating the error state prior to archiving, the workspace remains clean and won't surface an RBR.
