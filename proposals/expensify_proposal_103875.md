## Proposal

### Please re-state the problem that we are trying to solve in this issue.
On Web and Desktop platforms, selecting text inside the message composer and pressing the `Delete` key (forward delete) duplicates the content in the input field instead of deleting the selected text range.

### What is the root cause of that problem?
In `src/pages/inbox/report/ReportActionCompose/ComposerWithSuggestions.tsx` (around lines 594–655), `handleKeyPress` intercepts keyboard shortcuts and specific navigation keys (`Enter`, `ArrowUp`, `Backspace`), but does not intercept the `Delete` key (`webEvent.key === 'Delete'`).

1. **Native ContentEditable Reconciler Flaw**:
   When text is selected (`selection.start !== selection.end`) and the user presses `Delete`, the event is not captured and falls through to the native `contenteditable` container managed by `@expensify/react-native-live-markdown` (`MarkdownTextInput.web.tsx`).
2. Because live markdown parses formatting into styled DOM elements (`<span class="syntax">...</span>`), dispatching a native forward deletion (`deleteContentForward`) across styled nodes causes Chromium and WebKit DOM selection reconcilers to duplicate text nodes rather than collapsing and slicing them before `beforeinput`/`input` fires.
3. `MarkdownTextInput.web.tsx` executes `handleOnChangeText`, reads the duplicated inner DOM tree via `parseInnerHTMLToText`, and passes the duplicated string to `updateComment`, overwriting the React state with duplicate text.
4. Additionally, if the caret is positioned immediately before a composite emoji (e.g., flag emojis or ZWJ sequences) with no text selected, native forward `Delete` slices a single UTF-16 code unit rather than the full grapheme cluster, leaving dangling surrogates.

### What changes do you think we should make in order to solve the problem?
In `src/pages/inbox/report/ReportActionCompose/ComposerWithSuggestions.tsx`:
Inside `handleKeyPress`, add an explicit branch for `webEvent.key === 'Delete'`:

```typescript
if (webEvent.key === 'Delete') {
    if (webEvent.isComposing || webEvent.shiftKey) {
        return;
    }
    const start = selection.start ?? 0;
    const end = selection.end ?? start;

    // 1. Handle selected range deletion deterministically
    if (start !== end) {
        webEvent.preventDefault();
        const textLength = lastTextRef.current.length;
        const minIndex = Math.min(textLength, Math.max(0, Math.min(start, end)));
        const maxIndex = Math.min(textLength, Math.max(0, Math.max(start, end)));
        const newText = lastTextRef.current.slice(0, minIndex) + lastTextRef.current.slice(maxIndex);

        setSelection({start: minIndex, end: minIndex});
        setCurrentEditMessageSelection((prevSelection) => ({
            ...prevSelection,
            start: minIndex,
            end: minIndex,
        }));
        updateComment(newText, true);
        return;
    }

    // 2. Handle forward grapheme cluster deletion (multi-codepoint emojis)
    const splitter = new Intl.Segmenter(CONST.LOCALES.EN, {granularity: 'grapheme'});
    const graphemes = Array.from(splitter.segment(lastTextRef.current.substring(start, start + 14)));
    const firstGrapheme = graphemes.at(0);
    const firstGraphemeLength = firstGrapheme?.segment.length ?? 0;
    if (firstGraphemeLength > 1) {
        webEvent.preventDefault();
        const newText = lastTextRef.current.slice(0, start) + lastTextRef.current.slice(start + firstGraphemeLength);

        setSelection({start, end: start});
        setCurrentEditMessageSelection((prevSelection) => ({
            ...prevSelection,
            start,
            end: start,
        }));
        updateComment(newText, true);
    }
}
```

#### Why this completely fixes the issue:
- Intercepting `Delete` when a selection exists calls `webEvent.preventDefault()`, stopping the faulty DOM contenteditable replication in its tracks.
- Controlled state and cursor selection are updated synchronously and cleanly via `updateComment(newText, true)` and `setSelection`.
- Provides full symmetry with the existing `Backspace` handler at lines 620–654, protecting both selected text deletion and multi-codepoint forward grapheme deletion.

### What alternative solutions did you explore? (Optional)
Patching upstream `@expensify/react-native-live-markdown`. Handling this within `ComposerWithSuggestions.tsx` is superior because it mirrors our established `Backspace` emoji handling, prevents DOM reconciliation defects directly at the composer boundary, and avoids waiting for upstream release cycles.

### Test Plan
#### Manual QA Steps:
1. Navigate to any chat on Web or Desktop (Chrome, Safari, Edge, Desktop App).
2. Type a test message into the composer (e.g. `hello world`).
3. Select a portion of the text (e.g. `world`) via mouse or Shift+Arrow.
4. Press `Delete`.
5. **Verify:** The selected text is cleanly removed (e.g. leaving `hello `) without duplicating any text.
6. Select the entire remaining string (`Ctrl+A` / `Cmd+A`) and press `Delete`.
7. **Verify:** The composer input clears completely.
8. Type text with markdown formatting (e.g. `*bold* text`) and select part of it across boundaries.
9. Press `Delete`.
10. **Verify:** The selection is cleanly deleted and remaining markdown parses normally.
11. Insert a composite emoji (e.g. 🏴󠁧󠁢󠁷󠁬󠁳󠁿 Wales flag), place the caret right before it, and press `Delete`.
12. **Verify:** The entire composite emoji is deleted forward without leaving orphaned code units.

#### Regression Verification:
1. Verify pressing `Backspace` with and without selection continues to work normally.
2. Verify typing while IME composition is active is not interrupted.
3. Verify `Enter` to send message and `ArrowUp` to edit previous message continue to function as expected.
