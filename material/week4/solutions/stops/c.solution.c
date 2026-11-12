#include <limits.h>
#include <stdlib.h>
#include <string.h>
// Time: O(k * m) for m flights. Space: O(n) for two distance arrays.
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
        // Read the previous round and write into a copy, so one round
        // never chains two flights.
        memcpy(newDist, dist, (size_t)n * sizeof(int));
        for (int i = 0; i < m; i++) {
            int u = flights[3 * i], v = flights[3 * i + 1], price = flights[3 * i + 2];
            if (dist[u] != INF && dist[u] + price < newDist[v]) {
                newDist[v] = dist[u] + price;
            }
        }
        int* swap = dist;
        dist = newDist;
        newDist = swap;
    }
    int answer = dist[dst] == INF ? -1 : dist[dst];
    free(dist);
    free(newDist);
    return answer;
}
