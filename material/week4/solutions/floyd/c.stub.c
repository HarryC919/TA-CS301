#include <stdlib.h>
#define INF 1000000000
int* floydWarshall(int n, const int* edges, int m) {
    // D[i * n + j]; base case D_0: 0 on the diagonal, INF elsewhere.
    int* D = malloc((size_t)n * (size_t)n * sizeof(int));
    if (D == NULL) return NULL;
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++) D[i * n + j] = i == j ? 0 : INF;
    }
    // TODO: load each edge (edges[3 * e], edges[3 * e + 1], edges[3 * e + 2]),
    // keeping the lightest of parallel edges.
    // TODO: for k, then i, then j, apply the key math function in place.
    // Never add to an INF entry.
    (void)edges;
    (void)m;
    free(D);
    return NULL;
}
