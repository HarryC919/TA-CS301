// Time: O(mn). Space: O(mn) table; output O(min(m, n)).
public class Solution {
    public static string LongestCommonSubsequence(string a, string b) {
        int m = a.Length, n = b.Length;
        // L[i, j] = LCS length of a's first i and b's first j characters.
        int[,] L = new int[m + 1, n + 1];
        for (int i = 1; i <= m; i++) {
            for (int j = 1; j <= n; j++) {
                // Key math function: match the last characters, or drop one of them.
                if (a[i - 1] == b[j - 1]) {
                    L[i, j] = L[i - 1, j - 1] + 1;
                } else {
                    L[i, j] = System.Math.Max(L[i - 1, j], L[i, j - 1]);
                }
            }
        }
        // Trace back from (m, n); prefer moving up on ties.
        char[] chars = new char[L[m, n]];
        int k = chars.Length;
        int x = m, y = n;
        while (x > 0 && y > 0) {
            if (a[x - 1] == b[y - 1]) {
                // Fill from the back so no reversal is needed.
                chars[--k] = a[x - 1];
                x--;
                y--;
            } else if (L[x - 1, y] >= L[x, y - 1]) {
                x--;
            } else {
                y--;
            }
        }
        return new string(chars);
    }
}
