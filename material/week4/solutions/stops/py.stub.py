def cheapest_route(n: int, flights: list[list[int]], src: int, dst: int, k: int) -> int:
    INF = float("inf")
    # dist[v] = cheapest price to reach v using the flights allowed so far.
    dist = [INF] * n
    dist[src] = 0
    # At most k stops means at most k + 1 flights: one round per flight.
    for _ in range(k + 1):
        # TODO: relax every flight (u, v, price) for this round.
        # Read this round's starting distances, and do not let one round
        # chain two flights.
        pass
    # TODO: return the price of reaching dst, or -1 if it is unreachable.
    pass
