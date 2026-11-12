// Time: O(k * m) for m flights. Space: O(n) for two distance arrays.
function cheapestRoute(n, flights, src, dst, k) {
    // dist[v] = cheapest price to reach v using the flights allowed so far.
    let dist = new Array(n).fill(Infinity);
    dist[src] = 0;
    // At most k stops means at most k + 1 flights: one round per flight.
    for (let round = 0; round <= k; round++) {
        // Read the previous round and write into a copy, so one round
        // never chains two flights.
        const newDist = dist.slice();
        for (const [u, v, price] of flights) {
            if (dist[u] + price < newDist[v]) {
                newDist[v] = dist[u] + price;
            }
        }
        dist = newDist;
    }
    return dist[dst] === Infinity ? -1 : dist[dst];
}
module.exports = { cheapestRoute };
