# Time: O(k * m) for m flights. Space: O(n) for two distance arrays.
def cheapest_route(n: int, flights: list[list[int]], src: int, dst: int, k: int) -> int:
    INF = float("inf")
    # dist[v] = cheapest price to reach v using the flights allowed so far.
    dist = [INF] * n
    dist[src] = 0
    # At most k stops means at most k + 1 flights: one round per flight.
    for _ in range(k + 1):
        # Read the previous round and write into a copy, so one round
        # never chains two flights.
        new_dist = dist[:]
        for u, v, price in flights:
            if dist[u] != INF and dist[u] + price < new_dist[v]:
                new_dist[v] = dist[u] + price
        dist = new_dist
    return -1 if dist[dst] == INF else dist[dst]
