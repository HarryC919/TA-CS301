// Time: O(mn). Space: O(mn) table; output O(min(m, n)).
function longestCommonSubsequence(a, b) {
    const m = a.length, n = b.length;
    // L[i][j] = LCS length of a's first i and b's first j characters.
    const L = Array.from({ length: m + 1 }, () => new Array(n + 1).fill(0));
    for (let i = 1; i <= m; i++) {
        for (let j = 1; j <= n; j++) {
            // Key math function: match the last characters, or drop one of them.
            if (a[i - 1] === b[j - 1]) {
                L[i][j] = L[i - 1][j - 1] + 1;
            } else {
                L[i][j] = Math.max(L[i - 1][j], L[i][j - 1]);
            }
        }
    }
    // Trace back from (m, n); prefer moving up on ties.
    const chars = [];
    let i = m, j = n;
    while (i > 0 && j > 0) {
        if (a[i - 1] === b[j - 1]) {
            chars.push(a[i - 1]);
            i--;
            j--;
        } else if (L[i - 1][j] >= L[i][j - 1]) {
            i--;
        } else {
            j--;
        }
    }
    // Characters were collected from the end backwards.
    return chars.reverse().join('');
}
module.exports = { longestCommonSubsequence };
