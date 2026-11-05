// Time: O(mn). Space: O(mn) table; output O(min(m, n)).
public class Solution {
    public static String longestCommonSubsequence(String a, String b) {
        int m = a.length(), n = b.length();
        // L[i][j] = LCS length of a's first i and b's first j characters.
        int[][] L = new int[m + 1][n + 1];
        for (int i = 1; i <= m; i++) {
            for (int j = 1; j <= n; j++) {
                // Key math function: match the last characters, or drop one of them.
                if (a.charAt(i - 1) == b.charAt(j - 1)) {
                    L[i][j] = L[i - 1][j - 1] + 1;
                } else {
                    L[i][j] = Math.max(L[i - 1][j], L[i][j - 1]);
                }
            }
        }
        // Trace back from (m, n); prefer moving up on ties.
        StringBuilder chars = new StringBuilder();
        int i = m, j = n;
        while (i > 0 && j > 0) {
            if (a.charAt(i - 1) == b.charAt(j - 1)) {
                chars.append(a.charAt(i - 1));
                i--;
                j--;
            } else if (L[i - 1][j] >= L[i][j - 1]) {
                i--;
            } else {
                j--;
            }
        }
        // Characters were collected from the end backwards.
        return chars.reverse().toString();
    }
}
