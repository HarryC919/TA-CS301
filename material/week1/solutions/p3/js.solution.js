// Sort by length, stably, using insertion sort.
// Time: O(n^2) worst, O(n) best (already ordered by length). Space: O(n).
// Returns a NEW array; the input is never modified.
function sortByLength(words) {
    const result = words.slice(); // copy: the caller's array is never modified

    for (let i = 1; i < result.length; i++) {
        const key = result[i];
        let j = i - 1;

        // 1. Shift longer words one slot to the right.
        //    Strict '>' keeps equal-length words in original order.
        while (j >= 0 && result[j].length > key.length) {
            result[j + 1] = result[j];
            j--;
        }

        // 2. Drop the key into the gap.
        result[j + 1] = key;
    }

    return result;
}

module.exports = { sortByLength };
