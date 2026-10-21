Contributor details
Your Expensify account email: jloa.dev@gmail.com
Upwork Profile Link: https://www.upwork.com/freelancers/~0163955a2ba22190aa

## Proposal

### Please re-state the problem that we are trying to solve in this issue.
On Android, when sharing a video file encoded with HEVC or stored in common containers such as `.mov` or `.mkv` from the device gallery or file manager, the Expensify app does not appear in the system share sheet. The expected behavior (matching iOS) is that Expensify appears in the system share sheet, and upon selection, displays an "Invalid file type" alert if the format is unsupported by Expensify.

### What is the root cause of that problem?
1. In `android/app/src/main/AndroidManifest.xml` (lines 156–164), the `android.intent.action.SEND` intent-filter for `MainActivity` uses a narrow, hardcoded list of specific video MIME types:
   ```xml
   <data android:mimeType="video/mp4" />
   <data android:mimeType="video/mpeg" />
   <data android:mimeType="video/mp2t" />
   <data android:mimeType="video/webm" />
   <data android:mimeType="video/avc" />
   <data android:mimeType="video/hevc" />
   <data android:mimeType="video/x-vnd.on2.vp8" />
   <data android:mimeType="video/x-vnd.on2.vp9" />
   <data android:mimeType="video/av01" />
   ```
2. When the Android operating system presents the system share sheet for files, it resolves the MIME type based on the file container (for example, `.mov` maps to `video/quicktime`, `.mkv` maps to `video/x-matroska`, and raw bitstreams may map to `application/octet-stream` or vendor MIME types), rather than inspecting internal codec tracks.
3. Because `AndroidManifest.xml` lacks container types and does not include the standard `<data android:mimeType="video/*" />` wildcard, Android filters out Expensify from the share target list entirely.
4. In contrast, the iOS Share Extension (`ios/ShareViewController/Info.plist`) uses `<key>NSExtensionActivationSupportsMovieWithMaxCount</key><integer>1</integer>`, which universally matches all movie files and allows the app's JS logic to handle file validation.

### What changes do you think we should make in order to solve the problem?
1. **Add `video/*` Wildcard to Android Intent Filter:**
   In `android/app/src/main/AndroidManifest.xml`, add `<data android:mimeType="video/*" />` to the `android.intent.action.SEND` intent filter (and ensure it is mirrored in `Mobile-Expensify/Android/AndroidManifest.xml` for HybridApp):
   ```diff
   diff --git a/android/app/src/main/AndroidManifest.xml b/android/app/src/main/AndroidManifest.xml
   --- a/android/app/src/main/AndroidManifest.xml
   +++ b/android/app/src/main/AndroidManifest.xml
   @@ -163,6 +163,7 @@
                    <data android:mimeType="video/x-vnd.on2.vp9" />
                    <data android:mimeType="video/av01" />
   +                <data android:mimeType="video/*" />
                </intent-filter>
            </activity>
   ```
2. **Preserve JS App-Level Validation:**
   In `src/pages/Share/ShareRootPage.tsx` (lines 107–112):
   ```typescript
   if (!tempFile?.mimeType || !shareFileMimeTypes.includes(tempFile?.mimeType)) {
       setErrorTitle(translate('attachmentPicker.wrongFileType'));
       setErrorMessage(translate('attachmentPicker.notAllowedExtension'));
       return;
   }
   ```
   When the user selects Expensify from the share sheet with an unsupported container format (such as `.mov` or `.mkv`), `ShareActionHandler` delivers the file to `ShareRootPage`, where it is safely halted and presents the expected "Invalid file type" alert (`attachmentPicker.wrongFileType`).

### What alternative solutions did you explore? (Optional)
- **Adding individual container types (`video/quicktime`, `video/x-matroska`, `video/3gpp`, etc.)**:
  Rejected as fragile and non-future-proof, as vendor-specific video containers would still be omitted. Using `<data android:mimeType="video/*" />` aligns Android with the iOS architecture (`NSExtensionActivationSupportsMovieWithMaxCount`), delegating file-type validation to the JavaScript application layer in `ShareRootPage.tsx`.

### What specific scenarios should we cover in automated tests?
Manual verification on Android device / emulator:
1. Transfer an HEVC video with a `.mov` or `.mkv` extension to the Android device.
2. Select the video in the Files app and tap **Share**.
3. Verify that **Expensify** appears in the system share sheet.
4. Tap Expensify and verify that the app opens and displays the "Invalid file type" error alert.
5. Share a standard supported `.mp4` video and verify it opens the normal attachment sharing workflow without errors.
