INF = 1_000_000_000

def floyd_warshall(n: int, edges: list[list[int]]) -> list[list[int]]:
    # Base case D_0: 0 on the diagonal, INF elsewhere.
    D = [[0 if i == j else INF for j in range(n)] for i in range(n)]
    # TODO: load each edge (u, v, w), keeping the lightest of parallel edges.
    # TODO: for k, then i, then j, apply the key math function in place.
    # Never add to an INF entry.
    pass
