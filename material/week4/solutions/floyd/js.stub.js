const INF = 1_000_000_000;

function floydWarshall(n, edges) {
    // Base case D_0: 0 on the diagonal, INF elsewhere.
    const D = Array.from({ length: n }, (_, i) => Array.from({ length: n }, (_, j) => (i === j ? 0 : INF)));
    // TODO: load each edge [u, v, w], keeping the lightest of parallel edges.
    // TODO: for k, then i, then j, apply the key math function in place.
    // Never add to an INF entry.
}
module.exports = { floydWarshall, INF };
