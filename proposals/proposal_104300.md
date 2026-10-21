Contributor details
Your Expensify account email: jloa.dev@gmail.com
Upwork Profile Link: https://www.upwork.com/freelancers/~0163955a2ba22190aa

## Proposal
### Please re-state the problem that we are trying to solve in this issue.
In 1:1 and group conversations, typing an emoji colon keyword (e.g., `:star`) displays irrelevant emoji suggestions that do not match the typed keyword or contain the corresponding letters.

### What is the root cause of that problem?
In `src/libs/EmojiUtils.ts` (inside `suggestEmojis` / `searchEmojis`):
The emoji suggestion search was updated to search across extended unicode aliases, keywords, and skin-tone variants. However, the fuzzy matching algorithm matches against secondary phonetic tags and unrelated synonym buckets without enforcing prefix matching or relevance ranking on the primary keyword. As a result, typing `:star` matches emojis where the substring loosely matches obscure localized metadata tags or internal character offsets, causing completely unrelated emojis (such as generic objects or animals) to appear above or alongside actual star emojis.

### What changes do you think we should make in order to solve the problem?
1. In `src/libs/EmojiUtils.ts`, update `suggestEmojis` to prioritize exact prefix matches on the emoji's primary name and standard English keywords:
```typescript
function suggestEmojis(prefix: string, maxResults = CONST.EMOJI_SUGGESTIONS_MAX_RESULTS): Emoji[] {
    const cleanPrefix = prefix.toLowerCase().replace(/^:/, '');
    if (!cleanPrefix) return [];

    return allEmojis.filter(emoji => {
        const nameMatches = emoji.name.toLowerCase().startsWith(cleanPrefix);
        const keywordMatches = emoji.keywords?.some(k => k.toLowerCase().startsWith(cleanPrefix));
        return nameMatches || keywordMatches;
    }).slice(0, maxResults);
}
```
2. Only fall back to broader substring matches if prefix matches yield fewer than the minimum threshold, preventing unrelated emojis from polluting the suggestion list.

### What specific scenarios should we cover in automated tests?
In `tests/unit/EmojiUtilsTest.ts`:
- Verify that typing `:star` returns exclusively star-related emojis (`star`, `star2`, `glowing_star`, `shooting_star`).
- Verify that unrelated emojis without `:star` prefix in name or keywords are excluded from the suggestion list.
