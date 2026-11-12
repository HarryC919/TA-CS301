#include <stdlib.h>
// Time: O(n^3 + m). Space: O(n^2) for the distance matrix.
#define INF 1000000000
int* floydWarshall(int n, const int* edges, int m) {
    // D[i * n + j]; base case D_0: direct edges only, 0 on the diagonal, INF elsewhere.
    int* D = malloc((size_t)n * (size_t)n * sizeof(int));
    if (D == NULL) return NULL;
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++) D[i * n + j] = i == j ? 0 : INF;
    }
    for (int e = 0; e < m; e++) {
        int u = edges[3 * e], v = edges[3 * e + 1], w = edges[3 * e + 2];
        if (w < D[u * n + v]) D[u * n + v] = w;  // keep the lightest parallel edge
    }
    // Round k allows vertex k as an intermediate vertex.
    for (int k = 0; k < n; k++) {
        for (int i = 0; i < n; i++) {
            if (D[i * n + k] == INF) continue;  // never add to INF
            for (int j = 0; j < n; j++) {
                // Key math function: go through k, or do not.
                if (D[k * n + j] != INF && D[i * n + k] + D[k * n + j] < D[i * n + j]) {
                    D[i * n + j] = D[i * n + k] + D[k * n + j];
                }
            }
        }
    }
    return D;
}
