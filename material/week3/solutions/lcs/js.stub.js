function longestCommonSubsequence(a, b) {
    const m = a.length, n = b.length;
    // L[i][j] = LCS length of a's first i and b's first j characters.
    const L = Array.from({ length: m + 1 }, () => new Array(n + 1).fill(0));
    for (let i = 1; i <= m; i++) {
        for (let j = 1; j <= n; j++) {
            // TODO: fill L[i][j] with the key math function.
            // L uses prefix lengths; the last characters are a[i - 1] and b[j - 1].
        }
    }
    // TODO: trace back from (m, n) and return one LCS as a string.
}
module.exports = { longestCommonSubsequence };
