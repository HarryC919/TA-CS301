#include <stdlib.h>
#include <string.h>
char* longestCommonSubsequence(const char* a, const char* b) {
    int m = (int)strlen(a), n = (int)strlen(b);
    int cols = n + 1;
    // L[i * cols + j] = LCS length of a's first i and b's first j characters.
    int* L = calloc((size_t)(m + 1) * (size_t)cols, sizeof(int));
    if (L == NULL) return NULL;
    for (int i = 1; i <= m; i++) {
        for (int j = 1; j <= n; j++) {
            // TODO: fill L[i * cols + j] with the key math function.
            // L uses prefix lengths; the last characters are a[i - 1] and b[j - 1].
        }
    }
    // TODO: allocate L[m * cols + n] + 1 chars, trace back from (m, n),
    // and fill the result from the back. Free L before returning.
    free(L);
    return NULL;
}
