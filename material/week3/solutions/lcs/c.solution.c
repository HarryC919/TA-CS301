#include <stdlib.h>
#include <string.h>
// Time: O(mn). Space: O(mn) table; output O(min(m, n)).
char* longestCommonSubsequence(const char* a, const char* b) {
    int m = (int)strlen(a), n = (int)strlen(b);
    int cols = n + 1;
    // L[i * cols + j] = LCS length of a's first i and b's first j characters.
    int* L = calloc((size_t)(m + 1) * (size_t)cols, sizeof(int));
    if (L == NULL) return NULL;
    for (int i = 1; i <= m; i++) {
        for (int j = 1; j <= n; j++) {
            // Key math function: match the last characters, or drop one of them.
            if (a[i - 1] == b[j - 1]) {
                L[i * cols + j] = L[(i - 1) * cols + (j - 1)] + 1;
            } else {
                int up = L[(i - 1) * cols + j], left = L[i * cols + (j - 1)];
                L[i * cols + j] = up >= left ? up : left;
            }
        }
    }
    int k = L[m * cols + n];
    char* result = malloc((size_t)k + 1);
    if (result == NULL) {
        free(L);
        return NULL;
    }
    result[k] = '\0';
    // Trace back from (m, n), filling the result from the back; prefer up on ties.
    int i = m, j = n;
    while (i > 0 && j > 0) {
        if (a[i - 1] == b[j - 1]) {
            result[--k] = a[i - 1];
            i--;
            j--;
        } else if (L[(i - 1) * cols + j] >= L[i * cols + (j - 1)]) {
            i--;
        } else {
            j--;
        }
    }
    free(L);
    return result;
}
