import {describe, it, expect} from 'bun:test';

const DEFAULT_NUMBER_ID = 0;

function parseChildAccountIDs(childOldestFourAccountIDs: string | undefined): number[] {
    return (
        childOldestFourAccountIDs
            ?.split(',')
            .filter(Boolean)
            .map((accountID) => Number(accountID))
            .filter((accountID): accountID is number => !Number.isNaN(accountID) && accountID !== DEFAULT_NUMBER_ID) ?? []
    );
}

function resolveAccountIDs(
    childOldestFourAccountIDs: string | undefined,
    processingAgentIDs: number[] | undefined,
): number[] {
    const childAccountIDs = parseChildAccountIDs(childOldestFourAccountIDs);
    return childAccountIDs.length === 0 && processingAgentIDs?.length ? processingAgentIDs : childAccountIDs;
}

describe('Thread avatar account ID resolution', () => {
    it('falls back to processingAgentIDs when childOldestFourAccountIDs is an empty string ""', () => {
        const resolved = resolveAccountIDs('', [999]);
        expect(resolved).toEqual([999]);
    });

    it('falls back to processingAgentIDs when childOldestFourAccountIDs is undefined', () => {
        const resolved = resolveAccountIDs(undefined, [999]);
        expect(resolved).toEqual([999]);
    });

    it('prefers childOldestFourAccountIDs when valid commenters exist', () => {
        const resolved = resolveAccountIDs('111,222', [999]);
        expect(resolved).toEqual([111, 222]);
    });

    it('handles malformed or trailing commas properly', () => {
        const resolved = resolveAccountIDs(',,', [999]);
        expect(resolved).toEqual([999]);
    });

    it('ignores 0 / DEFAULT_NUMBER_ID in childOldestFourAccountIDs', () => {
        const resolved = resolveAccountIDs('0', [999]);
        expect(resolved).toEqual([999]);
    });
});
