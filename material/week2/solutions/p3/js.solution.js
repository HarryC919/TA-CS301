// Time: O(n + m). Output: O(n + m). Extra working space: O(1).
function mergeSorted(left, right) {
    const result = [];
    let i = 0, j = 0;
    // Choose the smaller remaining head; choose left on ties.
    while (i < left.length && j < right.length) {
        if (left[i] <= right[j]) result.push(left[i++]);
        else result.push(right[j++]);
    }
    // Copy either remaining tail.
    while (i < left.length) result.push(left[i++]);
    while (j < right.length) result.push(right[j++]);
    return result;
}
module.exports = { mergeSorted };
