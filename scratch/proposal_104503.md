Contributor details
Your Expensify account email: jloa.dev@gmail.com
Upwork Profile Link: https://www.upwork.com/freelancers/~0163955a2ba221e513

## Proposal

### Please re-state the problem that we are trying to solve in this issue.
HybridApp on Android crashes during application startup with a fatal SIGABRT / Tombstone crash:
`com.facebook.react.common.JavascriptException: [runtime not ready]: Error: Cannot find native module 'ExpoAudio'`
thrown while the JS bundle is being evaluated during `ReactInstance::loadScript`.

### What is the root cause of that problem?
1. In `src/libs/Sound/index.native.ts`, line 9 statically imports `createAudioPlayer, setAudioModeAsync` from `expo-audio`:
   ```ts
   import {createAudioPlayer, setAudioModeAsync} from 'expo-audio';
   ```
   And line 25 immediately invokes native module initialization at the module top level:
   ```ts
   const audioModeConfigured = setAudioModeAsync({playsInSilentMode: false, shouldPlayInBackground: false, interruptionMode: 'mixWithOthers'});
   ```
2. Core startup modules, including `src/libs/actions/App.ts` and `src/libs/actions/Session/index.ts`, import `{clearSoundAssetsCache} from '@libs/Sound'`. Therefore, `Sound/index.native.ts` is evaluated immediately when Metro loads and runs the initial JS bundle.
3. During the initial script evaluation on Android HybridApp launches, `requireNativeModule('ExpoAudio')` is invoked synchronously before the native JSI/modules runtime is fully ready and registered.
4. Because the error occurs at module top-level during bundle evaluation (`ReactInstance::loadScript`), it cannot be caught by any React ErrorBoundary, triggering `facebook::react::JsErrorHandler::handleErrorWithCppPipeline` and terminating the process via `std::terminate -> abort() (SIGABRT)`.

### What alternative solutions did you explore? (Optional)
Calling `setAudioModeAsync` inside an `App.ts` lifecycle hook was explored, but static imports of `expo-audio` still trigger module-level initialization code in `expo-audio/src/index.ts`. Lazy dynamic import (`import('expo-audio')`) on demand when sound is actually requested completely isolates startup from audio native module readiness.

### What changes do you think we should make in order to solve the problem?

In `src/libs/Sound/index.native.ts`:
1. Remove the static import of `expo-audio` (`createAudioPlayer`, `setAudioModeAsync`).
2. Remove top-level invocation `const audioModeConfigured = setAudioModeAsync(...)`.
3. Lazily initialize and cache the audio mode and player on demand with graceful fallback:

```diff
--- a/src/libs/Sound/index.native.ts
+++ b/src/libs/Sound/index.native.ts
@@ -6,9 +6,8 @@ import type {AudioSource} from 'expo-audio';
 import type {ValueOf} from 'type-fest';
 
-import {createAudioPlayer, setAudioModeAsync} from 'expo-audio';
-
 import {getIsMuted, SOUNDS, withMinimalExecutionTime} from './BaseSound';
+import Log from '@libs/Log';
 
 // Sound assets are statically imported for bundling.
 const SOUND_ASSETS = {
@@ -21,11 +20,20 @@ const SOUND_ASSETS = {
 // - playsInSilentMode: false — respect the device's silent/mute switch (iOS)
 // - shouldPlayInBackground: false — push notification sounds are played by the system
 // - interruptionMode: 'mixWithOthers' — don't interrupt other audio (e.g. music)
-const audioModeConfigured = setAudioModeAsync({playsInSilentMode: false, shouldPlayInBackground: false, interruptionMode: 'mixWithOthers'});
+let audioModePromise: Promise<void> | null = null;
+const ensureAudioModeConfigured = () => {
+    if (!audioModePromise) {
+        audioModePromise = (async () => {
+            try {
+                const {setAudioModeAsync} = await import('expo-audio');
+                await setAudioModeAsync({playsInSilentMode: false, shouldPlayInBackground: false, interruptionMode: 'mixWithOthers'});
+            } catch (error) {
+                Log.warn('[Sound] Failed to configure audio mode:', error);
+            }
+        })();
+    }
+    return audioModePromise;
+};
 
 const playSound = async (soundFile: ValueOf<typeof SOUNDS>) => {
     if (getIsMuted()) {
         return;
     }
 
     const source = SOUND_ASSETS[soundFile];
     if (!source) {
         return;
     }
 
-    // Wait for audio mode to be configured before playing to ensure the session
-    // uses the .ambient category (which won't interrupt music or other audio)
-    await audioModeConfigured;
-
-    const player = createAudioPlayer(source);
+    try {
+        await ensureAudioModeConfigured();
+        const {createAudioPlayer} = await import('expo-audio');
+        const player = createAudioPlayer(source);
+
+        const subscription = player.addListener('playbackStatusUpdate', (status) => {
+            if (!status.didJustFinish) {
+                return;
+            }
+
+            subscription.remove();
+            player.remove();
+        });
+
+        player.play();
+    } catch (error) {
+        Log.warn('[Sound] Failed to play sound:', error);
+    }
 };
```

### What automated tests can you add to prevent this from re-occurring?
Add a test in `tests/unit/SoundTest.ts` verifying that:
1. Importing `@libs/Sound` does not trigger any native calls or throw even when native audio modules are unavailable.
2. Invoking `playSound` safely handles failure without crashing when native modules reject.
