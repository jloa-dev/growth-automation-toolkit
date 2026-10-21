Contributor details
Your Expensify account email: jloa.dev@gmail.com
Upwork Profile Link: https://www.upwork.com/freelancers/~01584ea0bc208b0a94

## Proposal

### Please re-state the problem that we are trying to solve in this issue.
The Expensify app crashes when sharing a video larger than 125 MB from the native gallery via the OS share sheet.

### What is the root cause of that problem?
In the native sharing bridge (`src/libs/ShareActionHandlerModule/index.ts` and Android native `ShareActionHandlerModule.kt`), shared media URIs are read and buffered directly into memory or copied synchronously into app cache before validating file dimensions or size. Files exceeding the memory threshold cause an `OutOfMemoryError` on the native Android thread, terminating the process before JavaScript can validate the file against `CONST.API_ATTACHMENT_VALIDATIONS.MAX_SIZE`.

### What changes do you think we should make in order to solve the problem?
1. In `ShareActionHandlerModule.kt` (Android native), inspect the content resolver file descriptor / `OpenableColumns.SIZE` before initiating stream copy.
2. If file size exceeds `MAX_FILE_SIZE` (100MB / 125MB), reject the share promise with a specific error code (`ERROR_FILE_TOO_LARGE`) without copying the file into RAM.
3. In JavaScript, catch this error and present an in-app error alert ("File is too large to upload") rather than crashing.

### What alternative solutions did you explore? (Optional)
Increasing JVM heap size, which does not prevent crashes on lower-end devices with large 4K videos.

### Tests
1. On Android, select a video file >125 MB in the Gallery app.
2. Tap Share and choose Expensify.
3. Verify the app opens smoothly and displays an error toast/modal stating the file is too large, without crashing.
