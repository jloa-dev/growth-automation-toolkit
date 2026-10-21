## Proposal

### Please re-state the problem that we are trying to solve in this issue.
On the Spend page, opening the Card filter dropdown and searching for a company card by its assigned nickname (or custom name) yields no matching results. Furthermore, the filter list only displays the default card title rather than the custom nickname assigned by workspace admins.

### What is the root cause of that problem?
In `src/libs/CardFeedUtils.ts`, inside `createCardFilterItem`:
```typescript
const isCSVImportCard = card?.bank === CONST.PERSONAL_CARDS.BANK_NAME.CSV;
const isPersonal = isPersonalCard(card);
if (isPersonal && !isCSVImportCard) {
    cardName = customCardNames?.[card?.cardID] ?? card?.cardName;
}
```
1. `createCardFilterItem` only resolves nicknames for personal cards (`isPersonal && !isCSVImportCard`). For company cards, `isPersonal` is `false`, so `cardName` remains as `card?.nameValuePairs?.cardTitle`.
2. Nicknames for company cards configured by workspace admins are stored in `ONYXKEYS.NVP_EXPENSIFY_COMPANY_CARDS_CUSTOM_NAMES` as well as in shared member NVPs under `ONYXKEYS.COLLECTION.SHARED_NVP_PRIVATE_DOMAIN_MEMBER`. Other views (e.g. `WorkspaceCompanyCardsTable`) resolve names using `CardUtils.getCompanyCardCustomName(cardID, sharedCardCustomNames, customCardNames)`.
3. In `src/components/Search/FilterComponents/CardSelector.tsx`, `sharedCardCustomNames` is not passed to `buildCardsData`, leaving `item.cardName` empty or un-customized for company cards, which prevents `searchFunction` from matching them.

### What changes do you think we should make in order to solve the problem?

1. **Add a selector for shared company card custom names** in `src/selectors/Card.ts`:
   ```typescript
   const allSharedCompanyCardCustomNamesSelector = (sharedNvp: OnyxCollection<CardFeeds>): Record<string, string> => {
       const combined: Record<string, string> = {};
       for (const member of Object.values(sharedNvp ?? {})) {
           if (!member?.settings?.companyCardCustomNames) {
               continue;
           }
           Object.assign(combined, member.settings.companyCardCustomNames);
       }
       return combined;
   };
   ```

2. **In `src/components/Search/FilterComponents/CardSelector.tsx`**:
   - Subscribe to `ONYXKEYS.COLLECTION.SHARED_NVP_PRIVATE_DOMAIN_MEMBER`:
   ```typescript
   const [sharedCardCustomNames] = useOnyx(ONYXKEYS.COLLECTION.SHARED_NVP_PRIVATE_DOMAIN_MEMBER, {selector: allSharedCompanyCardCustomNamesSelector});
   ```
   - Pass `sharedCardCustomNames` to `buildCardsData`.

3. **In `src/libs/CardFeedUtils.ts`**:
   - Accept `sharedCardCustomNames?: Record<string, string>` in `createCardFilterItem` and `buildCardsData`.
   - Use `getCompanyCardCustomName` for non-personal company cards:
   ```diff
   --- a/src/libs/CardFeedUtils.ts
   +++ b/src/libs/CardFeedUtils.ts
   @@ -84,6 +84,8 @@ function createCardFilterItem(
        const isPersonal = isPersonalCard(card);
        if (isPersonal && !isCSVImportCard) {
            cardName = customCardNames?.[card?.cardID] ?? card?.cardName;
   +    } else if (!isExpensifyCard(card)) {
   +        cardName = getCompanyCardCustomName(card?.cardID, sharedCardCustomNames, customCardNames) ?? card?.nameValuePairs?.cardTitle;
        }
   ```

### What alternative solutions did you explore? (Optional)
- Only reading `customCardNames?.[card?.cardID]`: Incomplete because nicknames configured by other workspace domain admins reside in `SHARED_NVP_PRIVATE_DOMAIN_MEMBER`. Using `getCompanyCardCustomName` ensures parity with `WorkspaceCompanyCardsTable`.

### What specific scenarios should we cover in automated tests?
In `tests/unit/Search/buildCardFilterDataTest.ts`:
1. Verify that a company card with a custom nickname in `sharedCardCustomNames` populates `item.cardName`.
2. Verify that typing the custom nickname into the search input matches and filters the card item.
