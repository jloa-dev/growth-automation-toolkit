## Proposal

### Please re-state the problem that we are trying to solve in this issue.
When a user removes or unassigns a card, the warning modal states only that "unsubmitted transactions" will be deleted. It does not clarify that every imported draft expense will be deleted, including unreported expenses and expenses currently on draft reports, nor does it explicitly warn that the deletion cannot be undone.

### What is the root cause of that problem?
The translation keys in `src/languages/en.ts` and `src/languages/es.ts` use legacy brief copy:
- `workspace.moreFeatures.companyCards.removeCardDescription`: `"Removing this card will delete all unsubmitted transactions."`
- `workspace.moreFeatures.companyCards.unassignCardDescription`: `"Unassigning this card will delete all unsubmitted transactions."`
- `workspace.moreFeatures.companyCards.unassignCardsDescription`: `"Unassigning will delete all unsubmitted transactions from the selected cards."`

These descriptions do not mention unreported transactions, draft reports, or that the action is permanent and irreversible.

### What changes do you think we should make in order to solve the problem?

1. **Update `src/languages/en.ts`** under `workspace.moreFeatures.companyCards`:
   ```typescript
   removeCardDescription: "Removing this card will permanently delete all its unsubmitted transactions, including unreported transactions and those on draft reports. This can't be undone.",
   unassignCardDescription: "Unassigning this card will permanently delete all its unsubmitted transactions, including unreported transactions and those on draft reports. This can't be undone.",
   unassignCardsDescription: "Unassigning will permanently delete all unsubmitted transactions from the selected cards, including unreported transactions and those on draft reports. This can't be undone.",
   ```

2. **Update `src/languages/es.ts`** under `workspace.moreFeatures.companyCards`:
   ```typescript
   removeCardDescription: 'Eliminar esta tarjeta eliminará permanentemente todas sus transacciones no enviadas, incluidas las transacciones no reportadas y aquellas en informes preliminares. Esto no se puede deshacer.',
   unassignCardDescription: 'Desasignar esta tarjeta eliminará permanentemente todas sus transacciones no enviadas, incluidas las transacciones no reportadas y aquellas en informes preliminares. Esto no se puede deshacer.',
   unassignCardsDescription: 'Desasignar eliminará permanentemente todas las transacciones no enviadas de las tarjetas seleccionadas, incluidas las transacciones no reportadas y aquellas en informes preliminares. Esto no se puede deshacer.',
   ```

3. **Verify Modal Component Titles**:
   Keep modal title tokens consistent (`removeCard` / `unassignCard` / `unassignCards`) across:
   - `PersonalCardDetailsPage.tsx`
   - `DynamicWorkspaceCompanyCardDetailsPage.tsx`
   - `WorkspaceCompanyCardsTableControls.tsx`

### What alternative solutions did you explore? (Optional)
- Retaining expenses upon card removal: Requires significant backend data model adjustments; as noted by the maintainers, updating the warning copy is the immediate, non-breaking first step.

### What specific scenarios should we cover in automated tests?
In `tests/ui/PersonalCardDetailsPageTest.tsx` and `tests/ui/WorkspaceCompanyCardsTableTest.tsx`:
1. Verify that clicking "Remove card" on a personal card displays the updated warning text with permanent deletion notes.
2. Verify that clicking "Unassign card" for a single company card displays the single unassign warning copy.
3. Verify that selecting multiple cards and clicking "Unassign cards" renders the plural bulk description.
4. Verify that Spanish locale (`es.ts`) renders the correct translated strings without missing token warnings.
