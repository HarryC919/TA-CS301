#include <climits>
#include <vector>
int cheapestRoute(int n, const std::vector<std::vector<int>>& flights, int src, int dst, int k) {
    const int INF = INT_MAX;
    // dist[v] = cheapest price to reach v using the flights allowed so far.
    std::vector<int> dist(n, INF);
    dist[src] = 0;
    // At most k stops means at most k + 1 flights: one round per flight.
    for (int round = 0; round <= k; round++) {
        // TODO: relax every flight {u, v, price} for this round.
        // Read this round's starting distances, and do not let one round
        // chain two flights.
    }
    // TODO: return the price of reaching dst, or -1 if it is unreachable.
    (void)flights;
    (void)dst;
    return -1;  // placeholder
}
