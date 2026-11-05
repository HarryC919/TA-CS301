#include <algorithm>
#include <string>
#include <vector>
std::string longestCommonSubsequence(const std::string& a, const std::string& b) {
    std::size_t m = a.size(), n = b.size();
    // L[i][j] = LCS length of a's first i and b's first j characters.
    std::vector<std::vector<int>> L(m + 1, std::vector<int>(n + 1, 0));
    for (std::size_t i = 1; i <= m; i++) {
        for (std::size_t j = 1; j <= n; j++) {
            // TODO: fill L[i][j] with the key math function.
            // L uses prefix lengths; the last characters are a[i - 1] and b[j - 1].
        }
    }
    // TODO: trace back from (m, n) and return one LCS as a string.
    return "";
}
