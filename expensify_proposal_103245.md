## Proposal

### Please re-state the problem that we are trying to solve in this issue.
On Web and Desktop, when the Agents settings page (`/settings/agents`) is open and the user switches to a Copilot (or Delegator) account, the page remains stuck displaying an infinite loading skeleton table and never renders the delegator's agents.

### What is the root cause of that problem?
When switching to a Copilot account:
1. `clearOnyxForDelegateTransition()` in `src/libs/actions/Delegate.ts` wipes non-preserved Onyx keys, resetting `ONYXKEYS.ARE_AGENTS_LOADED` to `undefined` / `false`.
2. In `src/pages/settings/Agents/AgentsPage.tsx`:
   ```typescript
   useEffect(() => {
       openAgentsPage();
   }, []);
   ```
   `openAgentsPage()` is only invoked once on mount with an empty dependency array (`[]`).
3. Because the screen stays mounted in wide layout across the delegate switch, `openAgentsPage()` is never called for the new delegate session.
4. `AgentsTable` has:
   ```typescript
   if (!areAgentsLoaded) {
       return (
           <>
               {headerComponent}
               <Table.LoadingState />
           </>
       );
   }
   ```
   Since `areAgentsLoaded` remains falsy and no fetch is triggered, `Table.LoadingState` stays rendered indefinitely.

### What changes do you think we should make in order to solve the problem?

1. **In `src/pages/settings/Agents/AgentsPage.tsx`**:
   - Subscribe to `ONYXKEYS.IS_LOADING_APP` and `ONYXKEYS.ARE_AGENTS_LOADED`:
   ```typescript
   const [isLoadingApp] = useOnyx(ONYXKEYS.IS_LOADING_APP);
   const [areAgentsLoaded] = useOnyx(ONYXKEYS.ARE_AGENTS_LOADED);
   ```
   - Trigger `openAgentsPage()` when `!areAgentsLoaded` and app loading has settled:
   ```typescript
   useEffect(() => {
       if (isLoadingApp) {
           return;
       }
       if (!areAgentsLoaded) {
           openAgentsPage();
       }
   }, [isLoadingApp, areAgentsLoaded]);
   ```
   This matches the established delegate transition handling pattern in `AgentAIPromptSection.tsx`.

2. **In `src/pages/settings/Agents/AgentsTable.tsx`**:
   Ensure `areAgentsLoaded` and `isOffline` are cleanly handled so offline indicator renders if connection is lost.

### What alternative solutions did you explore? (Optional)
- Forcing a full page remount or unmounting the central pane: Causes unnecessary layout flicker and breaks NewDot navigation state. Subscribing to `isLoadingApp` and `areAgentsLoaded` is clean and reactive.

### What specific scenarios should we cover in automated tests?
In `tests/ui/AgentsPageTest.tsx`:
1. Verify that when `areAgentsLoaded` transitions from `true` to `false` (simulating `clearOnyxForDelegateTransition`), `openAgentsPage` is dispatched once `isLoadingApp` is `false`.
2. Verify that `AgentsTable` exits the loading state and renders the delegator's agent rows when `areAgentsLoaded` becomes `true`.
