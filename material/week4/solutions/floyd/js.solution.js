// Time: O(n^3 + m). Space: O(n^2) for the distance matrix.
const INF = 1_000_000_000;

function floydWarshall(n, edges) {
    // Base case D_0: direct edges only, 0 on the diagonal, INF elsewhere.
    const D = Array.from({ length: n }, (_, i) => Array.from({ length: n }, (_, j) => (i === j ? 0 : INF)));
    for (const [u, v, w] of edges) {
        if (w < D[u][v]) D[u][v] = w;  // keep the lightest parallel edge
    }
    // Round k allows vertex k as an intermediate vertex.
    for (let k = 0; k < n; k++) {
        for (let i = 0; i < n; i++) {
            if (D[i][k] === INF) continue;  // never add to INF
            for (let j = 0; j < n; j++) {
                // Key math function: go through k, or do not.
                if (D[k][j] !== INF && D[i][k] + D[k][j] < D[i][j]) {
                    D[i][j] = D[i][k] + D[k][j];
                }
            }
        }
    }
    return D;
}
module.exports = { floydWarshall, INF };
