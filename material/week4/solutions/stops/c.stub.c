#include <limits.h>
#include <stdlib.h>
#include <string.h>
int cheapestRoute(int n, const int* flights, int m, int src, int dst, int k) {
    const int INF = INT_MAX;
    // dist[v] = cheapest price to reach v using the flights allowed so far.
    int* dist = malloc((size_t)n * sizeof(int));
    int* newDist = malloc((size_t)n * sizeof(int));
    if (dist == NULL || newDist == NULL) {
        free(dist);
        free(newDist);
        return -1;
    }
    for (int v = 0; v < n; v++) dist[v] = INF;
    dist[src] = 0;
    // At most k stops means at most k + 1 flights: one round per flight.
    for (int round = 0; round <= k; round++) {
        // TODO: relax every flight for this round. Flight i is
        // flights[3 * i], flights[3 * i + 1], flights[3 * i + 2] (from, to, price).
        // Read this round's starting distances, and do not let one round
        // chain two flights.
    }
    // TODO: compute the answer for dst (-1 if unreachable), free both arrays,
    // and return it.
    (void)flights;
    (void)m;
    (void)dst;
    free(dist);
    free(newDist);
    return -1;  // placeholder
}
