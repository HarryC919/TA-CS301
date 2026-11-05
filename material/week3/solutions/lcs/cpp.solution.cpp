#include <algorithm>
#include <string>
#include <vector>
// Time: O(mn). Space: O(mn) table; output O(min(m, n)).
std::string longestCommonSubsequence(const std::string& a, const std::string& b) {
    std::size_t m = a.size(), n = b.size();
    // L[i][j] = LCS length of a's first i and b's first j characters.
    std::vector<std::vector<int>> L(m + 1, std::vector<int>(n + 1, 0));
    for (std::size_t i = 1; i <= m; i++) {
        for (std::size_t j = 1; j <= n; j++) {
            // Key math function: match the last characters, or drop one of them.
            if (a[i - 1] == b[j - 1]) {
                L[i][j] = L[i - 1][j - 1] + 1;
            } else {
                L[i][j] = std::max(L[i - 1][j], L[i][j - 1]);
            }
        }
    }
    // Trace back from (m, n); prefer moving up on ties.
    std::string chars;
    std::size_t i = m, j = n;
    while (i > 0 && j > 0) {
        if (a[i - 1] == b[j - 1]) {
            chars.push_back(a[i - 1]);
            i--;
            j--;
        } else if (L[i - 1][j] >= L[i][j - 1]) {
            i--;
        } else {
            j--;
        }
    }
    // Characters were collected from the end backwards.
    std::reverse(chars.begin(), chars.end());
    return chars;
}
