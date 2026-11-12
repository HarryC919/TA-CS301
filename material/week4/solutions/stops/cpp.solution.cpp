#include <climits>
#include <vector>
// Time: O(k * m) for m flights. Space: O(n) for two distance arrays.
int cheapestRoute(int n, const std::vector<std::vector<int>>& flights, int src, int dst, int k) {
    const int INF = INT_MAX;
    // dist[v] = cheapest price to reach v using the flights allowed so far.
    std::vector<int> dist(n, INF);
    dist[src] = 0;
    // At most k stops means at most k + 1 flights: one round per flight.
    for (int round = 0; round <= k; round++) {
        // Read the previous round and write into a copy, so one round
        // never chains two flights.
        std::vector<int> newDist = dist;
        for (const std::vector<int>& flight : flights) {
            int u = flight[0], v = flight[1], price = flight[2];
            if (dist[u] != INF && dist[u] + price < newDist[v]) {
                newDist[v] = dist[u] + price;
            }
        }
        dist = newDist;
    }
    return dist[dst] == INF ? -1 : dist[dst];
}
