public class Solution {
    public static string LongestCommonSubsequence(string a, string b) {
        int m = a.Length, n = b.Length;
        // L[i, j] = LCS length of a's first i and b's first j characters.
        int[,] L = new int[m + 1, n + 1];
        for (int i = 1; i <= m; i++) {
            for (int j = 1; j <= n; j++) {
                // TODO: fill L[i, j] with the key math function.
                // L uses prefix lengths; the last characters are a[i - 1] and b[j - 1].
            }
        }
        // TODO: trace back from (m, n) and return one LCS as a string.
        throw new System.NotImplementedException();
    }
}
