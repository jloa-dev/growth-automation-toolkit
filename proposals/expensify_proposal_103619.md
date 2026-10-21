## Proposal

### Please re-state the problem that we are trying to solve in this issue.
When sending an image attachment larger than 24 MiB (requiring client-side downscaling) on iOS, Android, or Web, the optimistic thumbnail in the chat message flashes and abruptly jumps its aspect ratio/dimensions moments after being sent.

### What is the root cause of that problem?
When an image exceeds `CONST.API_ATTACHMENT_VALIDATIONS.MAX_SIZE` (24 MiB), `useFilesValidation.tsx` passes the file to `resizeImageIfNeeded(file)` in `src/libs/fileDownload/FileUtils.ts:693-700`:
1. `getImageDimensionsAfterResize(file)` calculates the proportional `{width, height}` for the downscaled image and forwards them to `getImageManipulator`.
2. **Web Discard in `getImageManipulator/index.ts`**:
   On Web (`src/libs/fileDownload/getImageManipulator/index.ts:10-13`), the resized file blob is wrapped in `new File([blob], ...)`. While `result.width` and `result.height` are returned by `manipulateAsync`, they are never assigned to the resulting `File` object.
3. **Cross-Platform Discard in `createFile`**:
   In `src/libs/fileDownload/FileUtils.ts:676-691`:
   - On iOS/Android: `createFile` returns `{uri: file.uri, name: file.name, type: file.type}`, stripping the `width` and `height` produced by `getImageManipulator/index.native.ts`.
   - On Web: `createFile` clones the `File` using `new File([file], ...)`, also omitting `width` and `height`.
4. Because the resized `FileObject` loses its dimensions, `ReportActionItemImage` initially renders the optimistic attachment without known aspect ratio attributes (falling back to square or default layout). When the image finishes loading, the component suddenly resolves the true aspect ratio, causing an abrupt layout jump and visible flash.

### What changes do you think we should make in order to solve the problem?

1. **Preserve Dimensions in Web `getImageManipulator/index.ts`**:
   Assign `width` and `height` to the `File` object returned from `manipulateAsync`:
   ```typescript
   export default function getImageManipulator({fileUri, width, height, fileName}: ImageManipulatorConfig): Promise<FileObject> {
       return manipulateAsync(fileUri ?? '', [{resize: {width, height}}]).then((result) =>
           fetch(result.uri)
               .then((res) => res.blob())
               .then((blob) => {
                   const resizedFile: FileObject = new File([blob], `${fileName}.jpeg`, {type: 'image/jpeg'});
                   resizedFile.uri = URL.createObjectURL(resizedFile as File);
                   resizedFile.width = result.width;
                   resizedFile.height = result.height;
                   return resizedFile;
               }),
       );
   }
   ```

2. **Preserve Dimensions in `FileUtils.ts:createFile`**:
   Update `createFile` to preserve `width` and `height` on both Native and Web:
   ```typescript
   const createFile = (file: FileObject): FileObject => {
       if (getPlatform() === CONST.PLATFORM.ANDROID || getPlatform() === CONST.PLATFORM.IOS) {
           return {
               uri: file.uri,
               name: file.name,
               type: file.type,
               width: file.width,
               height: file.height,
           };
       }
       const clonedFile: FileObject = new File([file as File], file.name ?? '', {
           type: file.type,
           lastModified: file.lastModified,
       });
       clonedFile.uri = file.uri;
       clonedFile.width = file.width;
       clonedFile.height = file.height;
       return clonedFile;
   };
   ```

3. In `FileUtils.ts:resizeImageIfNeeded`, pass the typed `FileObject` through `createFile`:
   ```typescript
   const resizeImageIfNeeded = (file: FileObject) => {
       if (!file || !Str.isImage(file.name ?? '') || (file?.size ?? 0) <= CONST.API_ATTACHMENT_VALIDATIONS.MAX_SIZE) {
           return Promise.resolve(file);
       }
       return getImageDimensionsAfterResize(file)
           .then(({width, height}) => getImageManipulator({fileUri: file.uri ?? '', width, height, fileName: file.name ?? '', type: file.type}))
           .then((result) => createFile(result));
   };
   ```

#### Why this completely fixes the issue:
- Resized images preserve their exact width and height on both Web and Native platforms.
- `ReportActionItemImage` receives valid dimensions immediately upon submission, calculating the correct aspect ratio on frame 1.
- Eliminates layout shifting and flashing when switching between optimistic preview and loaded state.

### What alternative solutions did you explore? (Optional)
Re-measuring the image asynchronously in `ReportUtils` before dispatching the optimistic comment. This was rejected because `getImageDimensionsAfterResize` and `manipulateAsync` already compute the exact scaled dimensions during preprocessing. Preserving them at the source in `getImageManipulator` and `createFile` avoids redundant async overhead.

### Test Plan
#### Automated Unit Tests (`tests/unit/FileUtilsTest.ts`):
- Assert that `createFile` retains `width` and `height` properties on Native platforms.
- Assert that `createFile` retains `width` and `height` properties on Web.
- Assert that `resizeImageIfNeeded` returns a `FileObject` containing matching `width` and `height`.

#### Manual QA Steps:
1. Open any chat on Web, iOS, or Android.
2. Select an image attachment larger than 24 MiB (e.g., 25–40 MiB high-resolution photo).
3. Tap Send.
4. **Verify:** The optimistic attachment thumbnail renders immediately with its true aspect ratio without flashing, jumping, or resizing abruptly.
5. Send a regular image under 24 MiB to verify standard attachments remain unaffected.
