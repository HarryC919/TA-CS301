# Time: O(n^3 + m). Space: O(n^2) for the distance matrix.
INF = 1_000_000_000

def floyd_warshall(n: int, edges: list[list[int]]) -> list[list[int]]:
    # Base case D_0: direct edges only, 0 on the diagonal, INF elsewhere.
    D = [[0 if i == j else INF for j in range(n)] for i in range(n)]
    for u, v, w in edges:
        if w < D[u][v]:
            D[u][v] = w  # keep the lightest of parallel edges
    # Round k allows vertex k as an intermediate vertex.
    for k in range(n):
        for i in range(n):
            if D[i][k] == INF:
                continue  # never add to INF
            for j in range(n):
                # Key math function: go through k, or do not.
                if D[k][j] != INF and D[i][k] + D[k][j] < D[i][j]:
                    D[i][j] = D[i][k] + D[k][j]
    return D
