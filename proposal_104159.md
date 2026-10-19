Contributor details
Your Expensify account email: jloa.dev@gmail.com
Upwork Profile Link: https://www.upwork.com/freelancers/~01584ea0bc208b0a94

## Proposal

### Please re-state the problem that we are trying to solve in this issue.
In chat, short user mentions where the username starts with a single character followed by a dot (e.g. `@j.doe`) are not recognized as valid mentions.

### What is the root cause of that problem?
In `src/libs/MentionUtils.ts` (and `CONST.REGEX.MENTION` / `CONST.REGEX.USER_MENTION`), the regex pattern governing user mentions requires at least two alphanumeric characters before a dot separator or boundary (e.g. `[a-zA-Z0-9_-]{2,}`). When a handle uses a standard initials-based format like `j.doe`, the single-character prefix fails the length quantifier and is treated as plain text rather than a mention token.

### What changes do you think we should make in order to solve the problem?
1. In `src/CONST.ts` and `src/libs/MentionUtils.ts`, update `CONST.REGEX.MENTION` to permit single-character prefixes preceding a period (e.g., `(?<=^|\s)@([a-zA-Z0-9_-]+(?:\.[a-zA-Z0-9_-]+)*)`).
2. Ensure unit tests in `tests/unit/MentionUtilsTest.ts` cover single-character dotted usernames like `@j.doe` and `@a.b`.

### What alternative solutions did you explore? (Optional)
Restricting mentions to full email addresses, which degrades UX for short usernames and workspace handles.

### Tests
1. Open any chat room in New Expensify.
2. In the compose box, type `@j.doe` and press send.
3. Verify the mention is recognized, styled as a mention pill/link, and autocompletes correctly.
4. Verify mentions like `@john.doe` and `@user` continue to work properly.
